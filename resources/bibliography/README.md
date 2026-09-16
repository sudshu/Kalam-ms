# Shared bibliography (optional)

Kalam ships this folder empty on purpose: a reference library is personal, and
yours should not be replaced by someone else's.

If you keep one consolidated BibTeX file — a Zotero, Mendeley, JabRef or Paperpile
export, say — drop it here as `master.bib`. `/km-new-manuscript` will then seed each
new manuscript's `references.bib` from it instead of starting empty, and
`/km-ref-check` will have more to validate against.

```
resources/bibliography/
├── master.bib    # your consolidated pool (you add this)
└── INDEX.md      # optional: a topic → citation-key index you maintain
```

Nothing breaks without it. With no `master.bib`, every manuscript simply starts
from an empty `references.bib` and grows as you cite.

`master.bib` and `INDEX.md` are git-ignored by default, so your library stays out
of any fork you publish. Remove those lines from `.gitignore` if you *want* to
version your own pool in your own private repo.
