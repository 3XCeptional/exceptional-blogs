# Prompt-Injection / LLM Red-Teaming Niche — Competition, Differentiation, Earnings, Trajectory

Date: 2026-08-23
Context: research grounded in `Plans/roadmap_ai_security.md` (Career-Goals vault) — specialty target is
prompt-injection & LLM red-teaming / eval engineering, flagship artifact "PromptInject-Bench" (benchmark +
severity-classification methodology), adjacent work on MCP/vector-DB attack surface, scopepilot, and an
Alignerr-style eval-contract income floor. Researched via a delegated general-purpose agent (WebSearch/WebFetch
+ opencode CLI cross-checks), per the standing `career/strategy research questions` rule in project `CLAUDE.md`.

---

## 1. Competition landscape

**Existing benchmarks/tools (confirmed, current):**
- **PINT (Prompt Injection Test)** — Lakera's benchmark, 4,314 inputs (3,016 English + 1,298 non-English), pulls
  from Gandalf game data, public jailbreak sets (DAN), hard negatives, chat/document corpora.
  [github.com/lakeraai/pint-benchmark](https://github.com/lakeraai/pint-benchmark). The `lakeraai` GitHub org was
  archived Aug 6, 2026 — but this is because **Lakera was acquired by Check Point Software for ~$300M in Sept
  2025** (deal closed Q4 2025), becoming the foundation of Check Point's "Global Center of Excellence for AI
  Security." Not abandonment — a full commercial exit for the category's most visible startup. Strongest
  market-validation signal in this research.
- **Gandalf the Red / D-SEC** (arXiv:2501.07927, Pfister/Volhejn/Knott et al., Lakera team) — crowd-sourced
  gamified red-teaming platform, released a **279k-prompt attack dataset**, proposes "Dynamic Security Utility
  Threat Model" (D-SEC), an adaptive severity/utility framework. Close prior art on the severity-methodology angle.
- **garak** (NVIDIA-backed, ~8.1k GitHub stars, 120+ probe modules) — LLM vulnerability scanner covering
  injection/extraction/hallucination.
- **promptfoo** — dominant open-source tool: 10.4k stars, 350k+ developers, ~130k MAU, used at ~25% of Fortune
  500s. **Acquired by OpenAI in March 2026**, core kept MIT-licensed. Second major consolidation exit in ~6 months.
- **PyRIT** (Microsoft, 3.4k stars, multimodal), **DeepTeam**, **CyberArk FuzzyAI**, **Giskard** — round out the
  "consolidated" open-source stack per multiple 2026 comparison posts.
- **HarmBench** (Mazeika et al. 2024, NeurIPS) and **JailbreakBench** (NeurIPS 2024 Datasets/Benchmarks track) —
  academic jailbreak-robustness benchmarks, adjacent but broader-scope than pure injection.
- **PromptBench** — adversarial-prompt-robustness library, not jailbreak-specific.
- **⚠️ CRITICAL NAME COLLISION**: `agencyenterprise/PromptInject` on GitHub — won **Best Paper Award at the
  NeurIPS ML Safety Workshop 2022** (Perez & Ribeiro, "Ignore Previous Prompt: Attack Techniques For Language
  Models," arXiv:2211.09527). Still cited in 2025-26 defense papers (PromptArmor 2025). "PromptInject-Bench" is
  close enough to cause confusion and dilute discoverability/SEO. **Recommend renaming before publishing.**
- **Recent taxonomy/severity papers (2025-2026, verify overlap before claiming novelty)**: SoK "Taxonomy and
  evaluation of prompt security in large language models" (arXiv:2510.15476); a 3-D taxonomy paper meta-analyzing
  78 studies (2021-2026) finding attack success rates >85% against SOTA defenses under adaptive attacks (exact
  arXiv ID unverified); OWASP GenAI Security Project's LLM01:2025 (Prompt Injection, ranked #1 severity) and the
  "OWASP Top 10 for Agentic Applications (2026)."
- **Indirect/RAG-injection specific**: "Hidden-in-Plain-Text: A Benchmark for Social-Web Indirect Prompt
  Injection in RAG" (OpenRAG-Soc benchmark), U Wisconsin-Madison, ACM Web Conference 2026 (WWW '26, Dubai, April
  2026), arXiv:2601.10923.
- **MCP/tool-poisoning research (already active, not empty white space)**: Invariant Labs published the first
  public MCP tool-poisoning PoC (April 2025, >60% ASR across 45+ real MCP servers). MCPGuard (arXiv:2510.23673),
  "MCP-38: A Comprehensive Threat Taxonomy for MCP Systems v1.0" (arXiv:2603.18063), "Parasites in the Toolchain"
  (arXiv:2509.06572), MDPI threat-modeling paper (arXiv:2603.22489). **CVE-2025-6514** (mcp-remote RCE, CVSS 9.6,
  JFrog, 437k affected downloads) is real, well-documented, high-severity — good citable anchor but widely covered.

**Individual/solo researchers**: pattern confirmed (solo bug-bounty hunters pivoting into AI red-teaming) but no
specific named individuals found publishing benchmark-grade prompt-injection work at solo scale — visible names
skew toward small teams inside funded startups (Lakera/Check Point, Gray Swan AI, HiddenLayer) or academic labs.
Gandalf bypass writeups (Medium, Hashnode, ByteBreach) are a saturated low-value genre.

**Oversaturated**: generic jailbreak writeups/DAN-style content, "prompt injection 101" explainers, Gandalf
walkthroughs, basic red-team tool comparison posts. arXiv is producing multiple new prompt-injection papers *per
week* in 2025-2026 (7-10 distinct new papers found from just Jan-June 2026: coding-agent injection, RAG injection,
reverse-engineering-agent injection, resume-screening injection, etc.).

**Thinner**: rigorous, reusable severity/impact×likelihood classification methodology as a standalone practitioner
contribution (D-SEC is closest prior art but is a utility-tradeoff model, not a CVSS-analog severity rubric);
cross-benchmark data-poisoning eval cases specifically (most benchmarks are inference-time injection, not
poisoning); non-English/multilingual injection corpora; MCP *server-implementation* auditing tooling (vs.
conceptual taxonomy papers) is still young.

## 2. Differentiation angle

- **Rename the benchmark** — "PromptInject" is taken and awarded; a near-identical name actively hurts
  discoverability, citation, and portfolio credibility.
- **Severity methodology** is not virgin territory (D-SEC exists) but is less saturated than raw
  benchmark-building. Pitch a CVSS-analog specifically for prompt-injection findings, mapping to bug-bounty
  program severity tiers, as "the rubric triagers actually use" — a practitioner tool, not another taxonomy paper.
- **MCP/vector-DB angle**: earlier-stage and less benchmarked than prompt-injection proper. Most 2025-2026 MCP
  output is taxonomy/PoC papers, not large reusable eval suites. A concrete MCP-server eval harness is more
  differentiated than another MCP taxonomy paper.
- **Data poisoning** eval cases: genuinely thin in the reviewed corpora (PINT, HarmBench, JailbreakBench,
  OpenRAG-Soc are all inference-time-injection-heavy). A real, well-labeled poisoning subset in the 500-1000 cases
  is a distinguishing chunk few benchmarks have.
- **Guardrail-bypass-as-research** is oversaturated as a writeup genre but under-exploited as *systematic,
  generalizable pattern documentation* — a paper on bypass-technique transferability across guardrail products
  (not just Gandalf) would stand out more than another single-target walkthrough.
- **Consolidation angle**: with Lakera→Check Point and promptfoo→OpenAI both 2025/2026 acquisitions, the two
  dominant open brands in this exact niche are now owned by bigger players — arguably *opens* space for an
  independent, vendor-neutral voice rather than crowding it further.

## 3. Earnings potential (sourced figures)

- **Prompt injection specialist**: $100K–$160K full-time; contractors $100–$150/hr (infosec.qa AI Red Teamer
  Salary 2026 / AICareerFinder).
- **AI Safety & Red Teaming Specialist (general)**: ~$160K–$230K one source; $130K–$220K per AICareerFinder.
- **Senior AI Red Teamer**: $120K–$220K+ base at elite orgs, some >$300K cited (vs $90K–$140K for traditional
  pentesters at equivalent seniority) — TheMoneyZoo/techjacksolutions 2026 career-guide pieces (aggregator-sourced,
  moderate reliability).
- **Contractor/day-rate**: avg ~$67.60/hr across contract AI red-team engagements in 2026; typical annualized
  contract band $80K–$150K; senior specialists with frontier-lab experience or published AI safety research
  command $120–$200+/hr (infosec.qa).
- **Named employer with a verified real posting**: **Gray Swan AI** — Red Team Engineer, explicitly covering
  prompt injection, tool use, agent exploitation, both public Arena-challenge design and private client red-team
  engagements. Referenced in 11 recent frontier-model system cards (Anthropic, OpenAI, Meta) as a safety-eval
  vendor.
- **Eval/gig income floor (Alignerr, verified)**: advertised range $15–$150/hr; realistic community-reported range
  $15–$60/hr for general work; AI Red Team Analyst posting specifically found at **$45/hr**; STEM/domain-expert
  tasks $30–50/hr. Reports of empty project boards for weeks — treat as supplemental/volatile, not a reliable floor.
- **Bug bounty, prompt-injection specific (verified, current)**:
  - Anthropic HackerOne program: opened to the public May 2026; ~$550,835 total paid across 429 reports since
    opening.
  - HackerOne reports 210% growth in valid AI vulnerability reports, led by prompt injection — strong demand-side
    growth signal.
  - Reality check: researcher Aonan Guan hijacked Anthropic/Google/Microsoft AI agents via prompt injection on
    GitHub Actions integrations (real, documented) — payouts were small: **$100 from Anthropic, $500 from GitHub**,
    undisclosed from Google, no CVEs assigned, no public advisories. Individual prompt-injection bounty payouts
    can be trivial even for legitimate cross-vendor findings.
  - Anthropic x HackerOne guide cites a max reward of $15,000 for a top-tier submission.
  - **Google's AI VRP explicitly excludes prompt injection and jailbreaks from scope.**
  - OpenAI runs its AI bounty program via Bugcrowd, not HackerOne.

## 4. Growth trajectory / timing

- Not cooling — accelerating, but crowding fast too, both true at once. arXiv producing multiple new
  prompt-injection papers per week as of H1 2026.
- **Two major acquisitions in ~12 months** (Lakera→Check Point $300M Sept 2025; promptfoo→OpenAI March 2026) —
  strong signal the category is commercially validated and consolidating around a few winners.
- **DEF CON AI Village (DC 34, 2026)**: red-teaming track expanded significantly, explicit prompt-injection
  workshops, a new pentesting-agent-building competition, deliberate outreach bringing "hundreds of students from
  overlooked institutions" into hands-on LLM red-teaming — the entrant funnel is being deliberately widened, i.e.
  more competition is coming.
- **Regulatory tailwind**: EU AI Act requires automated red-teaming tools for high-risk AI systems, enforcement
  deadline **August 2, 2026**, penalties up to 7% of global revenue — a real compliance-driven demand driver
  landing right in the roadmap's ship window.
- Could not verify precise arXiv cs.CR paper-count-by-year aggregate stats; directionally confirmed via manual
  sampling that volume is high and rising, exact YoY % growth unconfirmed.

## 5. Other findings / risks not explicitly asked about

- **Benchmark obsolescence risk is real and specific**: 2025-2026 papers track how fast defenses patch known
  injection classes (Meta SecAlign arXiv:2507.02735, Meta Llama Prompt Guard 2, Google Spotlighting-style
  delimiter defenses) — a static 500-1000 case benchmark risks being "solved" or stale within months unless
  versioned (PINT itself iterates via CHANGELOG). Budget for a v2/v3 cadence, not a one-shot arXiv drop.
- **In-house absorption risk is real but not existential**: model vendors do extensive in-house red-teaming, but
  the evidence shows a complementary rather than substitutive relationship — smaller orgs without in-house AI
  security teams sustain demand for red-teaming as a service. Target mid-market/smaller AI-product companies as
  clients/employers, not just frontier labs.
- **Concrete firms to study/target**: Trail of Bits has an active, well-regarded practice specifically on
  prompt-injection-to-RCE in agents ("Prompt injection to RCE in AI agents," Oct 2025); Bishop Fox and NCC Group
  treat AI/prompt-injection testing as embedded within broader red-team engagements rather than standalone —
  meaning firms treating it as a standalone discipline (Trail of Bits, Gray Swan, boutique AI-security shops like
  HiddenLayer/Robust Intelligence — latter two not independently confirmed via job postings) are more precise
  employer targets than generalist pentest shops.
- **Naming/branding fix is urgent and free** — rename "PromptInject-Bench" before any public arXiv/GitHub push.
- **Adjacent higher-value niche worth considering**: MCP server security auditing tooling (not just taxonomy
  papers) is measurably thinner than prompt-injection benchmarking proper and sits directly on the existing
  bug-bounty/scopepilot skillset — leaning harder into a practical MCP-server scanning/eval tool may be less
  crowded than adding another injection benchmark to an already dense field.
- **Venues worth targeting beyond arXiv-only**: DEF CON AI Village (confirmed active, growing); USENIX Security
  (standard academic venue, not directly confirmed this pass); ACM Web Conference (WWW) — confirmed 2026
  publication venue for RAG-injection benchmark work, a model for placing the benchmark paper somewhere with more
  weight than a bare arXiv drop.

---

**Unverified/flagged items** — do not cite as settled fact: exact YoY arXiv paper-count trend numbers; the
"78 studies, >85% ASR" meta-analysis's precise arXiv ID; whether HiddenLayer/Robust Intelligence have open reqs
matching this exact niche; precise named solo/individual researchers publishing benchmark-grade work in this
niche (pattern confirmed, specific names not).

**Immediate action item**: rename PromptInject-Bench before shipping anything public — the collision is real,
damaging, and free to fix now.
