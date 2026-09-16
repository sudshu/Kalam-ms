# Nature Machine Intelligence

> Sourced 2026-06-12 via Gemini web search of nature.com/natmachintell author
> guidelines. Verify word/figure limits against the live guidelines at submission
> time; items marked (unverified) were not confirmed against the official page.

## Overview
- **Full name**: Nature Machine Intelligence
- **Publisher**: Springer Nature (launched 2019, monthly)
- **Scope**: Machine learning, AI, and robotics research, including applications of ML in other scientific domains when the ML insight itself is the contribution. Cross-disciplinary work must carry a clear ML-legible message, not just a domain result obtained with ML.
- **Audience**: ML/AI researchers first, domain scientists second — the inverse of a geoscience journal
- **Open Access**: Hybrid — subscription (no fee) or Gold OA (APC ~$12k; confirm current rate)

## Article Types
| Type | Word Limit | Figures | Abstract | References |
|------|-----------|---------|----------|------------|
| Article | ~3,000–5,000 words (excl. abstract, Methods, legends) | up to 10 display items | 150 words, unreferenced | ~50 |
| Analysis | ~3,000–5,000 words | up to 10 | 150 words | ~50 |
| Perspective | ~3,000–4,000 words | up to 6 | 150 words | 50 (up to 100 if broad) |
| Review | ~5,000 words | up to 10 | 150 words | up to 100 |

## Formatting
- **Sections**: Unheaded introduction → Results → Discussion → Methods (at end). Nature-family layout.
- **Abstract**: 150 words, single paragraph: background → problem → main results → implications.
- **Citation style**: Numbered, superscript (Nature family); `naturemag.bst`.
- **Data Availability**: REQUIRED.
- **Code Availability**: REQUIRED, and enforced harder than at most journals — see below.
- **Author Contributions / Competing Interests**: REQUIRED.

## Code & Reproducibility (distinctive policy)
- Code must be available to referees during review; NMI runs **dedicated code peer review** (often via Code Ocean capsules).
- For acceptance, code deposited in a DOI-issuing permanent repository (Zenodo / Code Ocean / Figshare); a bare GitHub link is not sufficient for the final version.
- Plan for this early: a reproducibility capsule covering training + the headline evaluation is effectively part of the submission.

## LaTeX
- **Document class**: No official class; `article` + Nature template conventions.
- **Bibliography style**: `naturemag.bst`.

## Writing Style
- The ML contribution must be stated in ML terms: what does the learning result say beyond the application domain?
- Quantitative, accessible to a broad technical audience; methods rigor expected at NeurIPS/ICML level but written in journal prose.
- Strong preference for honest baselines, ablations, and bias controls in the main text.

## What Reviewers Look For
- A genuine ML insight or framework, not "we applied a U-Net to X" (the most common desk-reject pattern for domain submissions — unverified but widely reported)
- Rigorous baselines and ablations; controls against leakage/shortcut learning
- Reproducibility: code review is part of the process
- Generality: does the finding transfer beyond the single dataset/system?

## Tips for Acceptance
- Lead with the learning-theoretic/framework contribution; let the domain result be the demonstration.
- Cross-system and real-data generalization is the strongest currency.
- Pre-empt the "just an application" objection in the cover letter: name the ML-legible principle the paper establishes.
