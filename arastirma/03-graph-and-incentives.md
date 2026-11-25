# 03 — Graph storage, tie strength, ranking and incentives

Scope: a free university referral network of about 1k–50k people. Sources are cited inline and listed at the end.

## 1. Data modeling

| Option | Fit at 1k–50k nodes | Maintenance for a student team |
|---|---|---|
| **Postgres + adjacency tables + recursive CTE** | 2–3 hop queries with an index on `(src, dst)` run in milliseconds at this size [7]. | One database for users, CVs, logs and the graph. Every host supports it. Plain SQL, easy backups. |
| **Apache AGE** (openCypher in Postgres) | Good. Cypher is nicer for paths. | Not on most managed hosts. Azure Flexible Server supports it [9]; DigitalOcean and Render users still request it [9]. Partial openCypher, no APOC/GDS [8]. |
| **Neo4j AuraDB Free** | Free tier allows 200k nodes / 400k relationships [5]. | Pauses after 3 days idle; deleted after a long pause (docs say 30 or 90 days) [5]. That is a bad fit for a production tool. Two databases to keep in sync. |
| **Memgraph** | Fast, in-memory, Cypher. | Self-host only. The Community edition uses the BSL licence (source-available, not open source) [6]. Adds ops work. |

**Recommendation: Postgres with adjacency tables.** The graph is small and queries are shallow (max 2–3 hops). The real data (users, consent, CVs, request logs, credits) is relational and needs transactions. Write the traversal in one SQL view or function, so you can swap to AGE later without changing the app.

### Schema

```sql
CREATE TABLE person   (id bigserial PRIMARY KEY, name text, email citext UNIQUE,
                       joined_at timestamptz DEFAULT now(), status text DEFAULT 'active'); -- active|frozen
CREATE TABLE sector   (id serial PRIMARY KEY, name text UNIQUE);
CREATE TABLE position (id serial PRIMARY KEY, name text, sector_id int REFERENCES sector);
CREATE TABLE company  (id serial PRIMARY KEY, name text, sector_id int REFERENCES sector);

-- KNOWS: store both directions so traversal is simple
CREATE TABLE knows (src bigint REFERENCES person, dst bigint REFERENCES person,
                    rel_type text,            -- family|friend|classmate|colleague|acquaintance
                    strength real CHECK (strength BETWEEN 0 AND 1),
                    since date, confirmed bool DEFAULT false,   -- both sides agreed
                    PRIMARY KEY (src, dst));
CREATE INDEX ON knows (dst);

CREATE TABLE works_at (person_id bigint REFERENCES person, company_id int REFERENCES company,
                       position_id int REFERENCES position, verified bool DEFAULT false, -- e.g. work-email check
                       PRIMARY KEY (person_id, company_id));

CREATE TABLE referral_request (id bigserial PRIMARY KEY, seeker_id bigint, referrer_id bigint,
                       position_id int, path bigint[],          -- chain of person ids
                       status text,  -- sent|seen|accepted|declined|expired|introduced|hired
                       created_at timestamptz DEFAULT now(), responded_at timestamptz,
                       seeker_rating smallint, referrer_rating smallint);
```

### Query: referrers within 2 hops at a sector-X company in position Y, ranked by path strength

Path strength = product of edge strengths (a 2-hop path is weaker than either edge).

```sql
WITH RECURSIVE walk(node, depth, strength, path) AS (
  SELECT k.dst, 1, k.strength, ARRAY[k.src, k.dst]
  FROM knows k WHERE k.src = :seeker AND k.confirmed
  UNION ALL
  SELECT k.dst, w.depth + 1, w.strength * k.strength, w.path || k.dst
  FROM walk w JOIN knows k ON k.src = w.node
  WHERE w.depth < 2 AND k.confirmed AND NOT k.dst = ANY(w.path)
)
SELECT DISTINCT ON (p.id) p.id, p.name, c.name AS company, w.depth, w.strength, w.path
FROM walk w
JOIN person p   ON p.id = w.node AND p.status = 'active'
JOIN works_at wa ON wa.person_id = p.id
JOIN company c  ON c.id = wa.company_id AND c.sector_id = :sector
WHERE wa.position_id = :position
ORDER BY p.id, w.strength DESC;   -- best path per person; re-sort by strength in the app
```

AGE/Neo4j equivalent:
`MATCH path=(s:Person {id:$seeker})-[:KNOWS*1..2]-(r:Person)-[w:WORKS_AT]->(:Company)-[:IN]->(:Sector {id:$sector}) WHERE w.position=$pos RETURN r, reduce(x=1.0, e IN relationships(path)[..-1] | x*e.strength) AS s ORDER BY s DESC`.

## 2. Tie strength

- **Granovetter (1973)**: weak ties bridge to new information; close friends know the same openings you already know [1].
- **Rajkumar et al. (2022, *Science*)**: randomized LinkedIn "People You May Know" experiments on 20M+ people over 5 years. The link between tie strength and job transmission is an **inverted U**. *Moderately* weak ties help most. Weak ties helped more in digital industries; strong ties helped more in less digital industries [2]. Implication: do not rank strong ties first by default. Ranking only by strength over-selects family, who often cannot help in the target sector.
- **Estimating strength from simple inputs**: Gilbert & Karahalios (CHI 2009) predicted strong vs weak ties with >85% accuracy from interaction data. The dimensions were intensity, intimacy, duration, reciprocal services, structural overlap, emotional support and social distance [3]. A cheap form for the MVP:

```
strength = 0.4*type + 0.3*frequency + 0.2*duration + 0.1*mutual_contacts
type:      family 1.0, close friend 0.9, colleague 0.7, classmate 0.6, acquaintance 0.3
frequency: weekly 1.0, monthly 0.7, yearly 0.4, rarely 0.1
duration:  min(years/5, 1)
mutual:    min(common_contacts/10, 1)
```
Ask both people and take the minimum, so one side cannot inflate it. Treat the weights as guesses to tune from outcome data.

## 3. Ranking

**Start explainable:**

```
score = hop_factor(1 hop 1.0, 2 hops 0.6) × tie_term × responsiveness × position_match × verified_bonus
tie_term       = 1 - |path_strength - 0.5|      -- peaks at moderate strength, per [2]
responsiveness = (accepted + 1) / (requests + 2)  -- Laplace smoothing; new users get 0.5
position_match = 1.0 exact, 0.6 same sector, 0.3 other
```
Show the reason on screen ("2 hops, via Ayşe; replies to 80% of requests"). Users trust it and the team can debug it. Cap requests per referrer per week, so the most responsive people do not burn out.

**Later "AI ranking", only once you have data:**
1. Embeddings (e.g. multilingual sentence embeddings) of CV text vs referrer's role text for `position_match`; store in `pgvector` in the same Postgres.
2. LLM re-ranking of the top 20 with a written rationale.
3. A learned model, only after a few hundred `accepted`/`hired` labels exist.

**Over-engineering warning:** with < 1,000 requests you have no labels. An ML ranker would learn noise. The bottleneck is referrer supply and willingness, not ranking quality.

## 4. Incentives and the reluctant referrer

**Evidence:**
- Burks et al. (QJE 2015), 9 firms: referred applicants are more likely to be hired. They perform similarly, quit 10–30% less, and yield more profit per worker. The mechanism is better job fit [4].
- Pallais & Sands (Upwork field experiments): referrals carry information employers cannot see. Referred workers had about 20 pp higher retention [10].
- Beaman & Magruder (AER 2012): with a fixed fee, people refer friends regardless of skill. Only performance-linked pay made able referrers send able candidates [11]. **Social networks push referrers toward favors, not quality.** This is the team member's warning, in experimental form.
- Time banks: equal-time credits create tension between instrumental and altruistic members [12]. Credits need a sink, or balances pile up.
- Marketplaces: Blind runs free stranger referrals among verified employees. Referrers accept many requests, but recruiters discount the flood [13]. The paid spin-off (Rooftop Slushie) drew employer pushback; Amazon said selling referrals can breach contracts [13]. Teamable (employee referral software) was acquired, not scaled alone [14]; RolePoint was also acquired [14]. I could not verify Refer.me, Jobcase or RippleMatch outcomes. The pattern: referral tools survive when **employers** pay or need them. Seeker-only cold referrals lose value fast.

**Professor's rules, judged:**

| Rule | Likely effect | Abuse | Mitigation |
|---|---|---|---|
| 3-month wait before search | Cuts drive-by users. It also blocks the urgent seekers you want, and early growth. | Pre-register dormant accounts. | Replace with "earn-in": search unlocks after contributing (confirm 5 ties, review 1 CV) or 3 months, whichever comes first. |
| Add ≥ 5 referrers | Seeds the graph. | Fake or unwilling names. | Count only ties the other side **confirms**. |
| x2 transferable search credits for a hire | Rewards helpers. | **Credit farming and sybil rings**: friends "hire" each other with fake claims, then pass credits along. | Verify hires (offer letter or HR email, two-sided confirm). Make credits non-transferable at first, or transferable only to confirmed 1-hop ties. Add expiry and a cap. |
| Freeze unresponsive / negatively rated | Keeps the list fresh. | Revenge ratings. | Use soft decay (rank drop) before freeze. Count "politely declined" as a response, not a failure. |
| Activity score via own referrers | Encourages recruiting helpers. | Ring inflation. | Graph sybil defenses rely on few real links between fake and honest regions [15]. Weight scores by confirmed, verified (work-email) nodes only. |

**For the reluctant referrer:** make "no" free and fast (one tap, no reason). Use opt-in per request, a blind preview (role and short pitch, no name until accept), and weekly caps. Use non-monetary recognition (thank-you, visible "helped 3 people"). Make it easy to give an honest signal. Referrers fear reputation damage more than they value credits [13].

## 5. HR perspective

Generally, referred candidates get faster screening and a higher hire rate [4][10]. Many firms pay internal referral bonuses, so check whether the platform's introduction counts as a company referral. In Turkey, "referans" competes with the stigma of "torpil" (favoritism). One cited survey says 74.7% of young people see favoritism as decisive, but the original source is unverified [16]. Referrers normally carry no legal liability. They carry reputational risk. Under KVKK, the platform must get consent before storing contacts' data and before sharing CVs [17].

**Interview script (Turkish):**
1. Şirketinizde çalışan referansıyla gelen adaylar süreçte farklı bir muamele görüyor mu (örneğin ön elemeyi atlama, daha hızlı dönüş)?
2. Referans veren çalışanın adayı ne kadar iyi tanıdığı sizin için önemli mi? Uzak bir tanıdığın referansı ile yakın bir arkadaşın referansını nasıl değerlendirirsiniz?
3. Referans verdiği aday kötü performans gösterirse, referans veren çalışan için resmi ya da gayriresmi bir sonuç oluyor mu?
4. Dışarıdan bir platform aracılığıyla gelen, çalışanınızın şahsen tanımadığı bir adayın referansını ciddiye alır mısınız? Hangi bilgi olursa alırsınız?
5. Referans sistemini "torpil"den ayırmak için sizce bir platformda neler olmalı (doğrulama, şeffaflık, değerlendirme)?

## Recommendations for the MVP

1. Use **one Postgres** (adjacency tables, recursive CTE, later `pgvector`). Skip graph databases until hop depth or size forces it.
2. Count only **two-side-confirmed** `KNOWS` edges and **work-email-verified** `WORKS_AT` edges.
3. Use the transparent score above. Favor moderate ties [2]. Show the reason. Hold off on AI until you have hundreds of labeled outcomes.
4. Log every request state change (`referral_request` status + timestamps). This is your future training data and your audit trail.
5. Replace the 3-month wait with contribution-based unlock. Start with non-transferable, expiring credits that need a verified hire.
6. Make declining free, cap weekly requests per referrer, and use soft decay before freezing.
7. Recruit **referrers first** (alumni, faculty, parents' employers). Supply is the bottleneck. Run the HR interviews before building incentive mechanics.
8. Write the KVKK consent flow on day one.

## Sources

1. Granovetter, M. (1973). The Strength of Weak Ties. *American Journal of Sociology* 78(6). https://www.jstor.org/stable/2776392
2. Rajkumar, K., Saint-Jacques, G., Bojinov, I., Brynjolfsson, E., Aral, S. (2022). A causal test of the strength of weak ties. *Science* 377. https://pubmed.ncbi.nlm.nih.gov/36107999/ ; summary: https://ide.mit.edu/insights/new-study-proves-that-weak-ties-have-strong-employment-value
3. Gilbert, E., Karahalios, K. (2009). Predicting Tie Strength With Social Media. CHI '09. https://doi.org/10.1145/1518701.1518736
4. Burks, S., Cowgill, B., Hoffman, M., Housman, M. (2015). The Value of Hiring through Employee Referrals. *QJE* 130(2). https://www.iza.org/publications/dp/7382
5. Neo4j AuraDB quotas and limits. https://neo4j.com/docs/aura/quotas-and-limits/ ; pause policy: https://neo4j.com/blog/auradb/pause-neo4j-aura-instance-save-80-percent/
6. Memgraph licensing. https://memgraph.com/legal ; https://github.com/memgraph/memgraph
7. "Your PostgreSQL already has a graph engine" (CTE timings). https://dev.to/ineron/your-postgresql-already-has-a-graph-engine-you-just-have-to-build-it-2ng7 ; Capital One, graph DB evaluation: https://www.capitalone.com/software/blog/graph-database-evaluation/
8. Apache AGE vs Neo4j. https://www.puppygraph.com/learn/apache-age-vs-neo4j ; https://age.apache.org/overview/
9. Azure PostgreSQL AGE support. https://learn.microsoft.com/en-gb/azure/postgresql/flexible-server/generative-ai-age-overview ; DigitalOcean request: https://ideas.digitalocean.com/managed-database/p/support-apache-age-postgresql-extension
10. Pallais, A., Sands, E. G. (2015). Why the Referential Treatment? NBER WP 21357. https://scholar.harvard.edu/sites/scholar.harvard.edu/files/pallais/files/referrals.pdf
11. Beaman, L., Magruder, J. (2012). Who Gets the Job Referral? *AER*. https://are.berkeley.edu/~jmagruder/kolkatanetworks.pdf
12. Timebanking motivation tension, CHI 2015 / Revista Galega de Economía 2024. https://doaj.org/article/c855aef0b8a9492a8ddfe349e5418523
13. Bloomberg (2025), referrals for strangers as a side hustle. https://www.bloomberg.com/news/articles/2025-01-09/how-employee-referrals-for-tech-jobs-became-a-side-hustle ; The Next Web (2020) on paid referrals: https://thenextweb.com/news/google-facebook-job-paid-referral
14. CB Insights: Teamable https://www.cbinsights.com/company/teamable ; RolePoint https://www.cbinsights.com/company/rolepoint
15. Yu, H. et al. (2006/2008). SybilGuard. https://www.comp.nus.edu.sg/~yuhf/sybilguard-ton08.pdf
16. Taşçı, F. "Çok katmanlı bir referans sistemine ihtiyacımız var." Haber7. https://www.haber7.com/yazarlar/prof-dr-faruk-tasci/3635192-cok-katmanli-bir-referans-sistemine-ihtiyacimiz-var ; Indigo Dergisi on torpil: https://indigodergisi.com/2019/06/torpil-liyakat-turkiye-torpilsiz-is-bulmak/
17. KVKK (Law No. 6698 on the Protection of Personal Data). https://www.kvkk.gov.tr/
