# Writing style — canonical policy

This is Kalam's single source of truth for reader-facing manuscript prose. `skills/Manuscript_writing_instuctions.md` operationalizes this policy and must not contradict it. Explicit instructions from the user or coauthors and recorded manuscript-specific decisions take precedence; the target-journal profile then sets the audience and format.

## Editorial contract before drafting

Before a skeleton or manuscript draft is written, record:

- target journal and article type;
- primary reader and adjacent-field reader;
- what those readers can and cannot be assumed to know;
- the research question and its one-sentence answer;
- the intended narrative arc;
- descriptive versus assertion-led title and caption style; and
- a manuscript-specific evidence-placement policy.

For broad Nature- or Science-level audiences, use an explicit scientific narrative: established context, unresolved question, decisive test, finding, and consequence. Do not recount the chronology of analysis unless that chronology affects interpretation.

Before the skeleton, create or refresh `research/style_refs/style_profile.md` from three to five recent papers in the target journal. When approved passages from the lead author and principal coauthor are available, use them as equal voice anchors; use the journal exemplars to calibrate register rather than erase the authors' voice. This author-voice calibration is a preference, not a reason to delay work when suitable passages are unavailable.

## Central contribution and paragraph roles

Prefer one central contribution or one unifying claim that can organize the title, figures, and main sections. A genuinely multifaceted paper may retain more than one contribution when the science requires it.

Assign each paragraph one primary role before drafting: context, gap, question, test, result, interpretation, limitation, or implication. The opening should serve that role and connect to the previous paragraph.

- Results paragraphs normally lead with the comparison, measurement, or finding.
- Introduction paragraphs may lead with context, a problem, or a knowledge gap.
- Discussion paragraphs may lead with interpretation, synthesis, a limitation, or an implication.
- Use old information to provide continuity and place the new point where the sentence or paragraph gives it natural emphasis.

Do not force every paragraph into an experiment-to-metric-to-result template. Do not open with guided-tour language when the scientific content can carry the transition.

## Field-native language

Name the scientific operation, process, or quantity directly. In Earth and climate manuscripts, do not default to machine-learning or computer-science language when a field-native term is more accurate.

Examples, when they preserve the intended meaning:

- `pipeline` → analysis workflow;
- `benchmark` → reference comparison;
- `ablation` → sensitivity test or control;
- `performance` → the measured quantity, such as agreement, error, bias, or predictive skill;
- `feature` → predictor, variable, tracer, or observable;
- `ground truth` → reference field or observation, only when justified;
- `generalization` → transfer across years, regions, sites, or models;
- `architecture` → model formulation, unless the computational architecture is scientifically relevant.

Keep genuine terms of art. Remove jargon that signals sophistication without adding meaning, and define unavoidable cross-disciplinary terms where the intended reader first needs them.

## Evidence placement and trust

Set the main-text evidence budget separately for every manuscript; there is no universal quota for robustness paragraphs.

At skeleton stage, assign every result, control, and sensitivity test to **Main**, **Methods**, **Extended Data**, **Supplementary Information**, or **Omit**, with a one-line rationale. The main text should retain the evidence needed to understand and trust the central claim: the primary estimate, uncertainty, comparison, essential validity test, and any limitation that changes interpretation.

Build and approve the scientific story before running adversarial factual, statistical, citation, and sensitivity audits. An audit changes the main narrative only when it changes the claim or its interpretation; otherwise its detail remains in the assigned Methods, Extended Data, Supplementary Information, or review record.

A robustness result is load-bearing and stays in the main text when it changes the effect size, sign, mechanism, scope, or credibility of the central claim. Supporting checks that leave the interpretation unchanged can be summarized briefly and placed in Methods, Extended Data, or Supplementary Information. Audit agents must not automatically promote every check into the narrative.

State a material limitation where it affects interpretation, explain its consequence precisely, and normally state it once. Do not organize prose as objection, rebuttal, and reassurance, rehearse an imagined peer review, or add caveats that do not alter the claim.

## Clarity and rhythm

- State the scientific point instead of announcing it. Remove metadiscourse such as “the key point is,” “it is worth noting,” “the next question is,” or descriptions of what the agent considered.
- Prefer concrete verbs and visible actors when agency matters. Passive voice is appropriate when the procedure or scientific object is the natural topic; never rewrite mechanically to satisfy an active-voice count.
- Avoid long runs of identically structured sentences or paragraph openings. Vary length and syntax only when it improves emphasis and flow. Do not introduce fragments, errors, personal asides, or arbitrary synonyms to make text seem human.
- Remove promotional, slogan-like, overly symmetrical, or defensive phrasing. Keep claims direct where the evidence is strong and hedge only the uncertain part.
- Do not use lists of supposedly AI-associated words, AI-detector scores, or an “AI-risk” label as editing criteria. Edit a word or construction only when it is vague, repetitive, promotional, inaccurate, or disruptive in context.

## Scoped rather than categorical claims

Prefer a bounded, evidence-linked statement to an interpretation phrased as universally true. If a claim depends on a model, dataset, population, region, period, experimental design, or assumption, state that scope in the sentence or make it unambiguous in the immediately preceding context. A compact slogan must not turn a local result into a general scientific principle.

Do not solve overstatement by adding vague modal verbs throughout the manuscript. Qualify the domain, evidence, or uncertainty that actually limits the inference. For example, replace “Climate extremes create a persistent carbon debt” with “Across the four DALEC site experiments, repeated hot–dry extremes left less ecosystem carbon after 20 years than the matched counterfactual.”

Categorical wording is appropriate for a definition, a verified experimental setting, an established relationship, or a direct result within an explicit domain. “Combustion was disabled in both runs” should remain direct. Judge scope from the sentence and its paragraph context rather than mechanically flagging words such as *is*, *all*, or *never*.

## Em dashes

Use em dashes sparingly, only when a parenthetical interruption is the clearest construction. As a diagnostic rather than a quota, inspect the prose when there is more than about one em dash per 150 words or more than one in a sentence. Prefer commas, parentheses, a colon, or a new sentence when they read more naturally.

## Titles and figure captions

Record whether the manuscript uses descriptive or assertion-led titles and captions, following the journal and coauthor decision. Apply that stance consistently. Do not turn every title or caption lead into a punchline by default.

Captions should remain concrete and self-contained: identify what is shown, the data or model, the metric where needed, the result relevant to the figure, and any caveat needed to interpret the display. Supporting detail belongs in Methods or Supplementary Information when it is not needed to read the figure.

## Numbers and claims

Preserve scientific meaning, citations, figure references, and numerical values. Do not invent results, mechanisms, citations, sample sizes, or interpretations. Mark missing information as `[VERIFY: ...]`.

Every quantitative claim in the abstract must match the body and figures. Define every acronym on first use in the body, separately from the abstract.

Use the appropriate number of significant digits: no more than necessary, but enough to resolve any difference the text asserts. Precision is set by the comparison a number takes part in, not by a uniform house rule.

Two failure modes matter:

- **Too many digits.** A correlation reported as `R² = 0.728` when nothing hinges on the third decimal is false precision. Round it (`0.73`).
- **Too few digits.** Rounding away a real difference is worse. If the text says one configuration outperforms another and the values are 0.140 versus 0.124 ppm yr⁻¹, keep the precision needed to resolve that comparison for both values. Never state a difference while printing identical numbers.

**Numerical clutter.** Keep the abstract, main text and Results free of numerical clutter: quote only the numbers the argument turns on and move supporting values to Methods, tables or the SI. A paragraph dense with figures stops being read; a reader should be able to follow the argument without decoding a table embedded in prose.

Rounding must not manufacture a difference that the underlying values do not support. Quantities whose small absolute size is itself the result, such as a near-zero bias of −0.002 ppm yr⁻¹, keep the digits needed to make that result visible.

## Empirical estimates versus algebraic constraints

Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly.

A quantity that follows from the definitions is not evidence about the world, and a quantity estimated from data is not a property of the algebra. Say which one a number is, and under what conditions it holds.

- **Identities presented as findings.** Regressing ΔX(t+1) on X(t) gives a slope of φ − 1 by construction, so "the slope is −0.98, showing strong reversion" reports an identity as a result. Name the identity and give the condition that makes it one.
- **Nominal parameters presented as equilibria.** Calling stocks "equilibrium contents" when they do not satisfy the model's own steady state invites a reader to check and find that they do not. State what the values are — reference stocks, assumed parameters, observed quantities — and what the equations imply instead.
- **One symbol, several meanings.** A threshold used once as a measurement uncertainty, once as an assigned benchmark and once as a statement about statistical power is three different quantities sharing a name. Define it once, derive it once, name it consistently.
- **Unstated conditions.** Every constraint carries assumptions: which variables are held fixed, which sample it was evaluated on, which convention fixes its sign, whether it is exact or asymptotic. If the condition changes the meaning, it belongs in the sentence.

Applies to Methods and figure captions as much as to the main text.

## Terminology consistency

Use one canonical term per concept across text and figures. Harmonize variants with `/km-polish-terms` and audit them with `/km-polish-audit`.
