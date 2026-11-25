# 04 — Stack, Hosting and Team Process (research, 2026-11-25)

Prices exclude VAT. *verify* = conflicting or third-party-only sources.

## 1. Stack options

| | (a) Next.js 16 + Postgres + Drizzle + Better Auth | (b) TanStack Start 1.x | (c) SvelteKit 2/3 | (d) Separate API (NestJS/FastAPI/.NET/Go) + React SPA |
|---|---|---|---|---|
| Current state | 16.x line since Oct 2025; 16.4 shipped Oct 2026; security release 2026-11-03 ([blog](https://nextjs.org/blog)) | 1.0 stable only on 2026-10-13; first stable npm tag is 1.169; needs Vite 8 ([TanStack](https://tanstack.com/blog/tanstack-start-1-0)) | SvelteKit 3 RC since Aug 2026; remote functions still tied to 3.0 final ([devclass](https://devclass.com/devops/2026/08/20/sveltekit-3-puts-heat-on-nextjs-with-radical-approach-to-rpcs/5290688), [svelte.dev](https://svelte.dev/blog/whats-new-in-svelte-june-2026)) | Mature, stable |
| Learning curve | Medium. One language; Server Components/caching are the hard part | Medium. Explicit, few tutorials | Lowest syntax burden, new to most | High. Two languages, CORS, split auth, contract drift |
| AI friendliness | Best. Largest corpus; 16.2 added agent tooling ([heise](https://heise.de/-11219357)) | Weak. Assistants still emit RC APIs (`.inputValidator()` → `.validator()`) | Medium. Runes/remote functions post-date much training data | Good per side; breaks at the seam |
| End-to-end types | Server Actions/route handlers + Drizzle + Zod: one TS type chain | Excellent (typed routes + server functions) | Good (remote functions) | Only with OpenAPI codegen; easy to break |
| Testing / i18n | Vitest + Playwright; `next-intl` mature | Vitest + Playwright; Paraglide | Vitest + Playwright; Paraglide add-on | Two test stacks, two CI pipelines, i18n on both sides |

**Recommendation: (a) Next.js 16 + PostgreSQL + Drizzle ORM + Better Auth + next-intl + Zod, tested with Vitest and Playwright.**

- One language and one deploy unit for beginners. Backend and DB students still own clear layers (`db/`, `server/`).
- AI help (pstack/poteto, Claude, Copilot) is most reliable on the stack with the most prior art. Next 16, Better Auth and Drizzle are current enough for "bleeding edge" without betting the term on a six-week-old framework.
- Better Auth: Auth.js moved under its team in Sept 2025 ([blog](https://better-auth.com/blog/authjs-joins-better-auth)). It stores users in *your* Postgres, so identity data stays on your server. Pin stable 1.x; v1.8 is beta ([docs](https://better-auth.com/docs/beta/guides/next-auth-migration-guide)).
- Drizzle over Prisma: SQL-shaped schema the DB students can review, plain SQL migrations in Git.
- Turkish casing: `"i".toUpperCase()` gives `"I"`, not `"İ"`. Use `toLocaleUpperCase("tr-TR")`, `Intl.Collator("tr")` and an ICU collation (`tr-TR-x-icu`) on name columns.
- Guard rails against the previous failure: ESLint `max-lines` (300); one action file per feature; Playwright smoke tests required in CI.

## 2. Hosting and KVKK

**Legal frame.** Law 7499 (12.03.2024) rewrote KVKK Art. 9: transfer abroad needs an adequacy decision (none exists for EU/US), a Board standard contract, or BCRs. Each standard contract must be notified within 5 business days ([KVKK](https://www.kvkk.gov.tr/Icerik/2053/Yurtdisina-Aktarim), [module](https://www.kvkk.gov.tr/Icerik/8043/Standart-Sozlesme-Bildirim-Modulu-Hakkinda-Kamuoyu-Duyurusu)). The 2026 fine for no notification is about 90k–1.8M TL ([Cottgroup](https://cottgroup.com/tr/blog/kvkk-gdpr/item/standart-sozlesme-bildirim-yukumlulugu-ve-yaptirimlari), *verify*). **An EU region is still a transfer abroad.**

| Option | Data location | Est. monthly cost (small app) | Notes |
|---|---|---|---|
| Vercel + Neon/Supabase (EU) | EU (Frankfurt), US companies | Hobby $0 is **non-commercial/personal only** ([Vercel](https://vercel.com/docs/plans/hobby)). Pro ≈ $20/seat (*verify*). Neon Free $0: 0.5–1 GB, scale-to-zero after 5 min ([Neon](https://neon.com/faqs/free-plan-limits-and-quotas)). Supabase Free pauses after a week idle ([Supabase](https://supabase.com/docs/guides/platform/free-project-pausing)); Pro ≈ $25 | Least ops. Needs SCC with each processor plus KVKK notification. Weakest KVKK story |
| Hetzner + Coolify | EU (DE/FI), EU company | CX23 €5.49 + €0.50 IPv4 since June 2026; often out of stock ([Hetzner](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/), [bitdoze](https://www.bitdoze.com/hetzner-cloud-cost-optimized-plans/)). Coolify v4 is free ([guide](https://noqta.tn/en/tutorials/coolify-v4-self-hosted-deployment-nextjs-2026)) | Cheap, Vercel-like Git deploys. Still a transfer abroad (one SCC) |
| Turhost / Natro VDS | **Türkiye** (Turhost: Istanbul Gayrettepe Tier 3) | ≈ 240–490 TL for 1–4 GB plans; campaign prices vary ([karekod comparison](https://www.karekod.org/blog/en-ucuz-vds-fiyatlari/), *verify on vendor site*) | Same Coolify setup, no transfer paperwork. Smaller ecosystem, check backups/snapshots |
| Radore cloud (RCD) | Türkiye (Istanbul) | Not published; a listing shows ~92 TL entry plan ([whtop](https://www.whtop.com/plans/radore.com/54048), *verify*) | Enterprise-oriented, quote-based |
| Turkcell Dijital İş Servisleri | Türkiye | Quote only ([Turkcell](https://www.turkcell.com.tr/kurumsal/dijital-is-servisleri/veri-merkezi-data-center/sunucu-barindirma)) | Overkill for a student project |

**Is keeping data in Türkiye worth it? Yes, here.** It costs about the same as Hetzner (≈ €10–15/month for 4 GB). It removes the standard-contract and notification duty for the main database of CVs and referral requests, whose controller is a professor without a legal team. Name the small remaining transfers (e-mail, error tracking, CDN) in the aydınlatma metni. Next.js builds need 1.5–3 GB RAM: take **4 GB minimum**, or build the Docker image in GitHub Actions.

## 3. GitHub organization

**Plan facts** ([github.com/pricing](https://github.com/pricing), [rulesets docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)):

| Feature | Free org, **public** repo | Free org, **private** repo | Team ($4/user/mo) |
|---|---|---|---|
| Rulesets / branch protection, required reviews | Yes | **No** | Yes |
| CODEOWNERS enforcement, draft PRs, wiki | Yes | **No** | Yes |
| Secret scanning + push protection | Yes | **No** | Yes (Secret Protection add-on for full GHAS) |
| Dependabot alerts + version updates | Yes | Yes | Yes |
| Projects, issue forms, labels, Discussions | Yes | Yes | Yes |
| Actions minutes | Unlimited | 2,000/mo | 3,000/mo |

Two $0 routes: (1) **public repos (recommended)** — every protection plus unlimited CI, secrets live only in Coolify/Actions; (2) for private code, a professor gets **free GitHub Team via GitHub Education for Teachers**, applied to the org ([teachers](https://education.github.com/teachers), [docs](https://docs.github.com/en/education/about-github-education/github-education-for-teachers/about-github-education-for-teachers)).

**Structure**
- Repos: `.github` (`profile/README.md`, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, default issue forms and PR template), `docs` (SRS, UML, wireframes, ADRs), `web` (the app).
- Teams: `maintainers` (2 leads, Admin), `backend`, `frontend`, `db`, `docs` (Write), `professors` (Maintain). Base permission **Read**; 2 owners maximum.
- Ruleset on the default branch: block deletion and force push; linear history; PR with **1 approval**; dismiss stale approvals; Code Owner review; resolve conversations; required checks `lint`, `typecheck`, `test`, `e2e`, `build` (up to date); squash-merge only; empty bypass list.
- `CODEOWNERS`: `/src/db/ @org/db`, `/src/app/ @org/frontend`, `/src/server/ @org/backend`, `/e2e/ @org/maintainers`.
- Issue forms: `feature.yml` (requires an FR ID), `bug.yml`, `task.yml`; `config.yml` disables blank issues. PR template: "Closes #", screenshots, test checklist.
- Labels: `type:*`, `area:*`, `prio:p0–p2`, `good first issue`, `out-of-scope`. Any request without an FR ID gets `out-of-scope`.
- Projects board: Backlog → Ready → In progress → In review → Done, with Iteration (2 weeks), Area and FR ID fields.
- Conventional Commits on the PR title (`amannn/action-semantic-pull-request`). Dependabot weekly, grouped, for npm and github-actions.
- `.gitignore` covers `.next/`, `coverage/`, `playwright-report/`, `test-results/`. A CI step fails on any file over 1 MB.

## 4. Analysis-phase tools

- **Use cases:** Mermaid supports them only as **`usecase-beta`** (v12+), syntax still unstable, and GitHub's renderer can lag ([Mermaid](https://mermaid.js.org/syntax/usecase.html)). Use **PlantUML** for the graded diagram: stable actors, `<<include>>`/`<<extend>>`, generalization, boundaries ([PlantUML](https://plantuml.com/use-case-diagram)). Keep Mermaid for flow, sequence and ER diagrams in Markdown.
- **draw.io:** commit `*.drawio.svg`; it edits in VS Code and renders on GitHub ([draw.io](https://www.drawio.com/docs/diagram-types/uml/use-case-diagrams/)).
- **Wireframes:** Excalidraw files in the repo for low fidelity. **Figma Education** (free Professional features, verification, about 2 years; some 2026 verification delays) for clickable screens ([Figma](https://www.figma.com/education/higher-education/)).
- **SRS:** a light **ISO/IEC/IEEE 29148** (successor to IEEE 830) Markdown file: 1 Introduction with an *explicit out-of-scope list*; 2 Stakeholders; 3 `FR-xx` with MoSCoW and Given/When/Then criteria; 4 `NFR-xx` (KVKK, WCAG 2.2 AA, TR/EN, latency, backups); 5 Use cases mapped to FRs; 6 Traceability FR → issue → test. Cap v1 at about 15 Must FRs and run grill-me on the scope before sign-off.

## 5. Prior art and the gap

| Platform | What it does | Gap |
|---|---|---|
| Kariyer.net, Yenibiriş | Turkish job boards: CV bank, employer search, reference checks *for employers* ([Kariyer.net](https://www.kariyer.net/veri-politikamiz/ucuncu-sahis-aydinlatma-metni), [Yenibiriş](https://www.yenibiris.com/bireysel-kullanim-sartlari)) | Employer-paid; no peer referrals |
| LinkedIn "Ask for a referral" | Button on postings where you have a connection (2018) ([LinkedIn](https://news.linkedin.com/2018/3/introducing-ask-for-a-referral)) | Needs an existing network |
| Blind | Anonymous tech-worker forum with a jobs/referrals board, about 12M users ([Inquirer](https://inquirer.com/business/referral-jobs-strangers-bonus-employees-20250118.html)) | Big-tech, US-centric, unstructured |
| Refer Me | Referral marketplace. 1 request/week free, $12/mo for unlimited | Paywalled. Incentives are bonus-driven |
| Jobcase | Free "people helping people" community for hourly workers, for-profit, 100M+ members ([Jobcase](https://www.jobcase.com/faqs/)) | US only. No Turkish context |
| Alumni networks (e.g. ODTÜM) | Alumni directory, career postings ([ODTÜM](https://mezun.metu.edu.tr/odtum.network)) | Siloed per university; no referral tracking |
| Dayanışma ağları, İŞKUR | Basic-needs solidarity; public job matching | No referral-solidarity platform found |

**Gap:** no free, Turkish, KVKK-compliant, cross-university platform where juniors request referrals from volunteer employees and track them (requested → accepted → referred → outcome), with no paywall.

## Recommendation

- **Stack:** Next.js 16 (App Router, TypeScript strict), PostgreSQL 17/18, Drizzle ORM, Better Auth (stable 1.x), Zod, next-intl (tr default, en), Tailwind + shadcn/ui, Vitest, Playwright, pnpm.
- **Hosting:** a Türkiye-located 4 GB VDS (Turhost or Natro, Istanbul) running Coolify v4, with Postgres in Docker. Take nightly `pg_dump` backups to a second Turkish location. Fallback: Hetzner CX/CPX + Coolify with a KVKK standard contract and notification.
- **Monthly cost:** about **400–600 TL (≈ €10–15)** for the VDS, plus a `.com.tr`/`.org` domain at about 300–600 TL/year. GitHub (public repos), Coolify, Figma Education and GitHub Actions cost $0.

**Starter layout**
```
org/
├─ .github/   profile/README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md,
│             ISSUE_TEMPLATE/{feature,bug,task}.yml, pull_request_template.md
├─ docs/      srs.md, use-cases/*.puml, wireframes/*.excalidraw, diagrams/*.drawio.svg,
│             adr/0001-stack.md, kvkk/{aydinlatma-metni.md, veri-envanteri.md}
└─ web/
   ├─ .github/{workflows/ci.yml, dependabot.yml, CODEOWNERS}
   ├─ src/app/[locale]/...        # routes, one folder per feature
   ├─ src/features/<feature>/     # actions.ts, queries.ts, components/ (each file under 300 lines)
   ├─ src/server/{auth.ts, db.ts}
   ├─ src/db/{schema/*.ts, migrations/}
   ├─ messages/{tr.json, en.json}
   ├─ tests/ (Vitest)   e2e/ (Playwright)
   ├─ Dockerfile  drizzle.config.ts  eslint.config.mjs  .env.example
   └─ .gitignore  (.next, coverage, playwright-report, test-results)
```
