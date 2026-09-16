# Journal families — limits quick reference

**The per-journal profile in `resources/journal_profiles/` is authoritative.** Always read it (path in each manuscript's `metadata.yaml → journal_profile`) and take word/abstract/figure/reference limits from there. This table is an indicative quick reference only; if it disagrees with a profile, the profile wins. **Skills must not hardcode these numbers — read the profile.**

| Journal | Main text | Abstract | Display items | References | SI |
|---|---|---|---|---|---|
| Nature (Article) | ~3,000 | ~150 (unstructured, no refs) | 6 | ~50 | extensive; up to ~10 Extended Data |
| Nature Communications | ~5,000 | ~150 | flexible | unlimited | extensive |
| Nature Geoscience / Climate Change | ~3,000 | ~150 | ~6 | ~50 | extensive |
| AGU (GRL) | short (≈12 publication units) | ~150 | ~4 | unlimited | yes |
| AGU (JGR / AGU Advances) | longer-form | ~250 | flexible | unlimited | yes |
| PNAS | ~6 pages | ~250 + 120-word significance statement | flexible | unlimited | yes |
| Copernicus (ACP) | no hard limit | concise | flexible | unlimited | yes |
| Elsevier (RSE) | journal-specific | structured ~250 | flexible | unlimited | yes |

Abstract reference policy and section structure also vary by journal — see the profile and `resources/conventions/writing_style.md`.

## Supplementary / Supporting Information prefix conventions

How SI display items are referred to **in the main text** varies by family. The per-journal profile wins; this is the indicative quick reference. Skills must not hardcode a single convention — read the family from `metadata.yaml → target_journal`.

| Family | Figures | Tables | Other | SI called |
|---|---|---|---|---|
| Nature (Nature, NGeo, NCC, NComms) | "Supplementary Fig. S1" / "Supplementary Figure 1" | "Supplementary Table 1" | "Supplementary Note 1" | Supplementary Information (separate PDF) |
| AGU (AGU Advances, GRL, JGR, GBC) | "Figure S1" (no "Supplementary" prefix) | "Table S1" | "Text S1" | Supporting Information |
| Copernicus (ACP, BG, GMD) | "Fig. S1" / "Figure S1" | "Table S1" | — | Supplement |
| PNAS | "SI Appendix, Fig. S1" | "SI Appendix, Table S1" | — | SI Appendix |

Every main-text reference must use the correct prefix for the target family; flag mixed conventions (e.g. "Supplementary Fig." and "Figure S" in the same manuscript).
