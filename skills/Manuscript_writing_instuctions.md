# Manuscript Writing Instructions

These instructions operationalize the canonical prose policy in `resources/conventions/writing_style.md` for atmospheric science, Earth system science, remote sensing, carbon-cycle science, and machine learning used in geophysical research. They must not override that policy.

## Instruction order

Apply instructions in this order:

1. explicit user and coauthor instructions, plus recorded manuscript decisions;
2. the selected journal's requirements and the manuscript's reader contract;
3. `resources/conventions/writing_style.md`;
4. this operational guide and the individual `/km-*` skill.

If two instructions conflict, follow the higher one and record the decision in the manuscript notes. Preserve scientific meaning, numbers, citations, figure references, model and dataset names, experiment definitions, and uncertainty ranges. Never invent a result, mechanism, citation, sample size, or interpretation. Mark missing information as `[VERIFY: ...]`.

## Calibrate before drafting

Before writing a skeleton or prose, read or create `research/style_refs/style_profile.md`. It must record:

- target journal and article type;
- primary disciplinary reader and adjacent-field reader;
- what each reader can be assumed to know;
- research question and one-sentence answer;
- central or unifying contribution;
- intended narrative arc;
- descriptive or assertion-led title and caption stance; and
- the manuscript-specific evidence-placement policy.

Calibrate register with three to five recent papers from the target journal. When approved prose from the lead author and principal coauthor is available, treat the two as equal voice anchors. Journal examples set reader expectations; they do not erase the authors' voice. Missing author samples are not a reason to delay work.

For broad Nature- or Science-level readers, prefer an explicit argument:

**established context → unresolved question → decisive test → finding → consequence**

Write the scientific argument, not the chronology of analyses, unless chronology itself affects interpretation.

## Paragraph roles and reader flow

Assign one main role to each paragraph before drafting: context, gap, question, test, result, interpretation, limitation, or implication. Its opening sentence should perform that role and connect to what the reader already knows.

- A Results paragraph normally begins with the comparison, measurement, or finding.
- An Introduction paragraph may begin with context, the scientific problem, or the unresolved question.
- A Discussion paragraph may begin with interpretation, synthesis, a limitation, or a consequence.
- A Methods paragraph normally begins with the scientific operation or object being defined.

Do not impose one experiment-to-metric template on every paragraph. Remove guided-tour openings such as “We next...” when the scientific relationship supplies the transition. Remove metadiscourse such as “the key point is,” “it is worth noting,” and descriptions of what the writer or agent considered.

Keep each paragraph to one reasoning unit. Use old information to provide continuity and place the new point where it receives natural emphasis. Vary sentence length and syntax when it improves flow, but never add fragments, errors, arbitrary synonyms, or personal asides merely to manufacture variation.

## Scientific language

Write in the language of the field and name the process or quantity directly. In Earth and climate manuscripts, replace generic computational language when a more precise scientific term exists. Depending on meaning:

- pipeline → analysis workflow;
- benchmark → reference comparison;
- ablation → sensitivity test or control;
- performance → agreement, error, bias, predictive skill, or the measured quantity;
- feature → predictor, variable, tracer, or observable;
- ground truth → reference field or observation, only when justified;
- generalization → transfer across years, regions, sites, or models;
- architecture → model formulation, unless computational architecture is relevant.

Retain genuine terms of art. Define an unavoidable cross-disciplinary term at the first point where the intended reader needs it.

Prefer concrete verbs and visible actors when agency matters. Passive voice is appropriate when the procedure or scientific object is the natural topic; do not rewrite mechanically to meet an active-voice count.

Avoid promotional, slogan-like, overly symmetrical, or vague language. Keep a strong supported claim strong, and hedge only the uncertain part. Edit words because they are inaccurate, repetitive, promotional, or disruptive in context—not because they appear on a detector-oriented word list.

## Claims and evidence

Calibrate the verb to the evidence:

- use “shows” for a directly demonstrated result;
- use “indicates,” “suggests,” “is consistent with,” “supports,” or “argues against” for interpretation;
- avoid “proves,” “definitively shows,” and “rules out” unless the evidence genuinely warrants an exhaustive claim.

Prefer scoped claims to categorical interpretations. When an inference depends on a particular model, dataset, population, region, period, experimental design, or assumption, name that domain in the sentence or make it unambiguous in the immediate context. Do not turn a local finding into a short universal slogan. Qualify the actual scope instead of adding vague “may,” “might,” or “could” to an otherwise overgeneral statement.

Keep categorical wording for definitions, verified settings, established relationships, and direct results within their stated domain. Do not weaken a factual sentence such as “Combustion was disabled in both runs.”

Distinguish explicitly among controlled simulation results, within-model information content, cross-model transfer, real-observation tests, controls, and reference comparisons. Never present within-model skill as demonstrated real-world skill.

Use quantitative evidence where it informs the claim. Report baselines, uncertainties, sample sizes, periods, and metrics when necessary for interpretation, not as a reflexive display of every available diagnostic.

## Evidence placement

At skeleton stage, create `drafts/evidence_placement.md`. Assign every result, control, and sensitivity test to **Main**, **Methods**, **Extended Data**, **Supplementary Information**, or **Omit**, and give a one-line rationale.

Set the evidence budget separately for each manuscript. There is no fixed global quota. The main narrative normally contains:

- the primary estimate or comparison;
- uncertainty needed to interpret it;
- the essential validity test; and
- any limitation or robustness result that changes the sign, magnitude, mechanism, scope, or credibility of the central claim.

Supporting checks that leave the interpretation unchanged belong in Methods, Extended Data, or Supplementary Information and can be summarized briefly in the main text. Do not promote every audit result into the narrative. Do not hide load-bearing evidence outside the main text.

Complete and approve the scientific story before running adversarial factual, statistical, citation, and sensitivity audits. Audit findings change the main prose only when they alter the claim or its interpretation; otherwise retain them in their assigned supporting destination or review record.

State a material limitation where it affects interpretation, explain its consequence precisely, and normally state it once. Do not arrange the paper as an imagined sequence of reviewer objections, rebuttals, and reassurances.

## Results

For each Results paragraph:

1. identify the scientific comparison or question;
2. give the relevant result and metric early;
3. state the supported interpretation without overstating mechanism;
4. cite the figure where it naturally supports the sentence; and
5. follow the evidence-placement ledger for supporting tests.

The paragraph need not literally begin “Fig. X shows.” Lead with the finding when that is clearer, then point to the figure. Use code-style configuration names only when scientifically necessary; otherwise provide a stable plain-language descriptor.

## Discussion

Organize the Discussion around interpretation and consequence, not a full replay of Results. Relate the finding to prior work, distinguish supported mechanism from speculation, state material limitations once, and end with a precise scientific conclusion rather than a slogan.

The order should follow the argument of the particular paper. Do not enforce a universal sequence of simulation, replication, observation, controls, and limitations.

## Methods

Give the main reader enough information to understand what was done and why. Put the detail required for reproduction in the appropriate Methods or Supplementary section without importing the entire audit trail into the main narrative.

For each experiment, record where relevant:

- inputs and targets;
- data and model versions;
- model formulation;
- training, calibration, and evaluation periods;
- spatial domain and temporal sampling;
- normalization and initialization;
- reference comparison or counterfactual;
- metric and uncertainty estimate; and
- number of seeds, samples, or ensemble members.

## Titles and figure captions

Use the descriptive or assertion-led stance recorded for the manuscript; neither is a universal default. Apply the choice consistently across main figures while following the journal and coauthor preference.

Captions should be concrete and self-contained. Include the data or model, what is shown, the metric where needed, the result relevant to reading the figure, and any caveat required to interpret it. Move implementation detail elsewhere when it is not needed to read the display.

## Numbers and terminology

Use no more significant digits than necessary, but enough to resolve every stated comparison. Apply consistent precision to values being compared. Never print identical rounded values while asserting a difference, and never let rounding manufacture a difference. Preserve additional precision when a small magnitude is itself the result.

Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. State whether a quantity is estimated from data or implied by the definitions, and give the conditions under which it holds. Do not report an algebraic identity as a finding, do not call a nominal parameter an equilibrium unless it satisfies the model's steady state, and do not reuse one threshold under different meanings in different sections.

Use one canonical term per concept across the abstract, main text, Methods, figures, and Supplementary Information. Define acronyms on first use in the body, separately from the abstract.

## Editing existing text

When revising an existing manuscript:

1. preserve scientific content unless the user asks to revise the science;
2. preserve citations and figure references;
3. retain caveats that alter interpretation;
4. resolve or flag `[CHECK: ...]`, `[PENDING: ...]`, `[TBD: ...]`, and incomplete cross-references;
5. reduce repetition across the Abstract, Introduction, Results, and Discussion;
6. replace guided-tour and internal-process prose with the scientific relationship;
7. check terminology and metric names across text and figures; and
8. keep simulations, observations, and counterfactuals clearly distinguished.

Before returning edited text, verify that every claim has support, all numerical values and references remain correct, the intended reader can follow the argument, evidence remains in its assigned destination, no repeated caveat or defensive aside interrupts the narrative, and interpretations do not exceed their stated model, dataset, population, spatial, temporal, or assumption domain.

## Human checkpoints

Pause for human approval at three points:

1. after the reader contract, central contribution, narrative arc, caption stance, and evidence policy are recorded;
2. after the skeleton and evidence-placement ledger are complete; and
3. after the full narrative is assembled, before a global polish or submission audit.

The domain author must verify factual claims, numerical statements, causal interpretations, and citations. A reader outside the immediate specialty should assess whether the title, abstract, figures, and central argument can be understood without insider knowledge.
