# Vibers Wiki

Internal knowledge base. For the public README see [../README.md](../README.md).

---

## Product

| Doc | Description |
|-----|-------------|
| [../SKILL.md](../SKILL.md) | AI Agent skill — client-facing quickstart (English) |
| [../REVIEW-RUNBOOK.md](../REVIEW-RUNBOOK.md) | Step-by-step review workflow for reviewers |
| [../CLAUDE.md](../CLAUDE.md) | Claude Code project instructions |

## Marketing & SEO

| Doc | Description |
|-----|-------------|
| [COMPETITORS.md](COMPETITORS.md) | 11 competitors — pricing, features, SEO strategies, keywords |
| [competitive-research/](competitive-research/) | Ad copy analysis (SonarSource, Google Ads) |
| [keywords/](keywords/) | SEMrush keyword exports (6 CSV files, 2026-04-14) |
| [reddit-alpha-beta-users.md](reddit-alpha-beta-users.md) | Reddit strategy for finding alpha/beta users |
| [backlink-opportunities.md](backlink-opportunities.md) | 13 directories + 6 dev blogs + media pitch targets |
| [COMPETITORS.md#markerio-markerio](COMPETITORS.md) | Marker.io — adjacent competitor ($39/mo, tooling only — не чинит). Топ-5 статей + контент-паттерн (template hubs, platform × format matrix, utility tripwire, living docs) разобраны в секции Marker.io |
| [advertising-channels.md](advertising-channels.md) | Полная карта рекламы: каталоги, ad networks, newsletters, стратегия по бюджету |
| [backlinks/](backlinks/) | Raw SEMrush backlink exports (CodeRabbit 4.6K, Qodo 6K domains) |
| [topic-research-20260414.xlsx](topic-research-20260414.xlsx) | SEMrush Topic Research — 108 content ideas with volumes, questions, backlinks |
| [WIKI.md#seo-intelligence](WIKI.md#seo-intelligence-april-2026) | Google March 2026 Core Update итоги + Claude SEO Prompts methodology |

### Content Plan (from keyword research)

**Priority 1 — Landing pages (KD < 5):**
- [x] `/blog/code-review-as-a-service/` — "code review as a service" (110 vol, KD=1)

**Priority 2 — Blog listicles (KD < 30):**
- [x] `/blog/best-ai-code-review-tools/` — "best ai code review tools" (170 vol, KD=26)
- [x] `/blog/claude-code-review/` — "claude code review" (320 vol, KD=25)
- [ ] "code review checklist" (390 vol, KD=24) — lead magnet, human+AI checklist
- [ ] "secure code review" (480 vol, KD=25) — security angle
- [ ] "automated code review tools" (260 vol, KD=27) — comparison
- [ ] "best code review tools" (110 vol, KD=16) — listicle

**Priority 3 — High-volume from Topic Research (2026-04-14):**
- [ ] "how to review pull requests" (2900 vol, KD=38) — guide for AI-generated PRs
- [ ] "code review best practices" (590 vol, KD=47) — with AI+human angle
- [ ] "improve code quality" (70 vol, KD=15) — contrarian: "Why code reviews don't improve quality anymore"
- [ ] "why ai code review is not enough" — hot take / link bait (top backlinked format)

**Priority 4 — Platform-specific:**
- [ ] "gitlab ai code review" (170 vol, KD=24)
- [ ] "bitbucket ai code review" (110 vol, KD=16)

**Priority 5 — Comparison pages:**
- [x] `/blog/coderabbit-alternative-human-review/`
- [x] `/blog/coderabbit-vs-human-review/`
- [ ] "Vibers vs Qodo"
- [ ] "Human vs AI Code Review: 50 Real Bugs Benchmark"

**Priority 6 — Programmatic SEO (шаблонные страницы):**
- [ ] `/review/cursor-code`, `/review/claude-code`, `/review/copilot-code`
- [ ] `/review/bolt-code`, `/review/v0-code`, `/review/lovable-code`, `/review/replit-code`

**Priority 7 — Template hubs & utility content (вдохновлено Marker.io паттерном):**
- [ ] "AI Code Review Checklist Templates" — long-form (4-5K слов) с шаблонами под GitHub PR / GitLab MR / Jira / Notion / Confluence / Google Docs (аналог `/blog/user-acceptance-testing-template` — 1.6K uniques/mo у них)
- [ ] "Code Review Bug Report Templates" — шаблоны под { GitHub, Jira, Linear, Asana, Notion } × { critical bug, security, perf, logic } (аналог `/blog/bug-report-template`)
- [x] "Best Chrome Extensions for AI Code Review" — utility tripwire (смежная аудитория, аналог `/blog/google-chrome-screenshot-extensions` — 774 uniques/mo)
- [ ] "AI Code Review Tools" — перестроить `best-ai-code-review-tools` как resource hub: каждый tool → внутренняя ссылка на "vs" comparison
- [ ] Добавить visible "Last updated" даты на топ-статьи + квартальный апдейт-цикл (freshness signal)

**People Also Ask (для FAQ-секций):**
- "What is the best free website for code reviews?"
- "How to review pull requests as a software engineer?"
- "How often should I be reviewing pull requests?"
- "How Can You Streamline the Code Review Process?"
- "What does a detailed code review look like?"

### SEO Intelligence (April 2026)

**Google March 2026 Core Update — итоги (Alex Groberman, @alexgroberman, 2026-04-14)**
Источник: https://x.com/i/status/2044080004842303818

Ключевые данные:
- Обновление длилось 12 дней (27 марта — 8 апреля 2026), одно из самых волатильных в истории Google
- 55%+ отслеживаемых доменов получили измеримые изменения в ранжировании
- 71% affiliate-сайтов пострадали (тонкие сравнения, шаблонные обзоры, рерайт)
- Сайты с оригинальными данными/исследованиями получили +22% видимости (анализ 600K+ страниц, JetDigitalPro)
- Типичное падение проигравших: 20-35%, у сильнейших страниц — более 50%
- Information Gain теперь прямой ранжирующий фактор: страницы, не добавляющие ничего нового к существующим результатам, проигрывают
- Topical Authority: сайт на 10 несвязанных тем оценивается хуже, чем сайт на 2 темы с глубиной
- Пример: HubSpot потерял ~80% органического блог-трафика (14.8M → 2.8M) после расширения в нерелевантные темы
- Победители: gov/institutional домены, сайты с экспертной атрибуцией, first-hand experience, third-party citations

Что это значит для Vibers:
- Наш контент уже на правильном пути (узкая ниша code review, экспертный опыт)
- Нужно усилить: оригинальные данные в статьях (benchmarks из реальных ревью, статистика багов)
- Прунинг: не расширяться за пределы code review / vibe coding / AI quality
- Экспертная атрибуция: добавлять авторов, их опыт, ссылки на профили

**10 SEO-промптов для Claude Cowork (Charles Floate, @Charles_SEO, 2026-04-14)**
Источник: https://x.com/i/status/2044010207458853314

Методология SEO через Claude Projects + Skills:
1. Prompt Zero — Business Context (загрузить в Project instructions, 30-45 мин на заполнение)
2. SERP Consensus Analyzer — анализ формата, DR, ссылочных профилей, entity-сигналов топа
3. Competitor Content Consensus Mapper — структурный анализ контента конкурентов (нужен Firecrawl MCP)
4. OnPage NLP & Entity Audit — entity relationships, topical completeness, information gain
5. Money Page Writer — CRO-оптимизация посадочных с учётом SEO-сигналов
6. Supporting Content Researcher — кластеры поддерживающего контента + internal linking
7. Supporting Content Writer — драфты на 80-90% готовности (нужен human editor!)
8. Brand Entity Stack — аудит brand entity signals (Wikipedia, Wikidata, Knowledge Graph)
9. Link Profile Analyzer — сегментация ссылок по tier/quality/anchor (лучше с Ahrefs MCP)
10. Link Bait Researcher — реверс-инжиниринг контента с 50+ referring domains в нише
11. SEO Dashboard Builder — кастомный дашборд как Claude Artifact
12. Self-Audit QA Gate — финальный QA перед публикацией

Ключевые инсайты для нас:
- Подход "Claude Project per business" — мы уже так работаем
- Skills для повторяющихся задач — у нас есть seo-content-writer, можно усилить по его схеме
- SERP Consensus перед написанием контента — внедрить в наш workflow
- Entity Audit — проверить наши статьи на entity coverage
- QA Gate как финальный шаг — добавить в наш seo-content-writer skill

**TODO (из инсайтов выше):**
- [ ] Добавить оригинальные данные в существующие статьи: реальная статистика багов из наших ревью, benchmarks time-to-fix, примеры найденных уязвимостей
- [ ] Внедрить SERP Consensus Analysis перед написанием новых статей (анализ топ-10 перед созданием контента)
- [ ] Добавить экспертную атрибуцию: авторы статей с именами, должностями, ссылками на профили
- [x] Entity Audit существующих статей — проверить entity coverage vs конкуренты (done 2026-04-15, see docs/entity-audit-2026-04-15.md)
- [ ] Добавить QA Gate в seo-content-writer skill (финальная проверка перед публикацией)
- [ ] Создать proprietary research piece: "50 Real Bugs AI Missed" на основе данных из реальных ревью
- [ ] Проверить topical focus: не расширяемся ли за пределы code review / vibe coding / AI quality

### Existing Blog Articles

| Slug | Target Keyword | Status |
|------|---------------|--------|
| `code-review-as-a-service` | code review as a service | NEW |
| `best-ai-code-review-tools` | best ai code review tools | NEW |
| `claude-code-review` | claude code review | NEW |
| `best-chrome-extensions-ai-code-review` | best chrome extensions for ai code review | Published |
| `markerio-vs-vibers` | marker.io vs vibers | Published |
| `coderabbit-alternative-human-review` | coderabbit alternative | Published |
| `coderabbit-vs-human-review` | coderabbit vs human review | Published |
| `ai-code-review-bots-miss-bugs` | ai code review bots miss bugs | Published |
| `human-in-the-loop-code-review-teams` | human in the loop code review | Published |
| `ai-generated-code-security-vulnerabilities` | ai generated code security vulnerabilities | Published |
| `review-cursor-generated-code` | review cursor generated code | Published |
| `how-to-test-ai-generated-code` | how to test ai generated code | Published |
| `ai-writes-code-who-verifies` | ai writes code who verifies | Published |
| `review-vibe-coded-app-before-launch` | review vibe coded app before launch | Published |
| `vibe-coded-app-production-ready` | vibe coded app production ready | Published |
| `vibe-coding-mistakes-production` | vibe coding mistakes production | Published |
| `vibe-coding-security-risks` | vibe coding security risks | Published |
| `claude-ai-performance-issues` | claude ai performance issues | Published |

## Product Evaluation

| Doc | Description |
|-----|-------------|
| [prototyping-criteria.md](prototyping-criteria.md) | Criteria for evaluating the product prototype |
| [evaluation-round-1.md](evaluation-round-1.md) | First evaluation round results |
| [evaluation-round-2.md](evaluation-round-2.md) | Second evaluation round results |
| [improvement-log.md](improvement-log.md) | Log of improvements made |

## Community

| Doc | Description |
|-----|-------------|
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guidelines (public) |
| [../SECURITY.md](../SECURITY.md) | Security policy (public) |
| [../.github/ISSUE_TEMPLATE/](../.github/ISSUE_TEMPLATE/) | Issue templates (bug, feature, review request) |

## Key Numbers

| Metric | Value | Source |
|--------|-------|--------|
| Target keyword (best) | "code review as a service" | KD=1, Vol=110 |
| Highest CPC keyword | "hire remote code review devs" | $73.97 |
| Main competitor | CodeRabbit | $24/user/mo, 15K+ customers |
| Our price | $15/hr | Free promo available |
| First client | MethasMP/Paycif (Thailand) | 2026-03-23 |
