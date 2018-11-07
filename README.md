# arXivToJSON
This repository contains code written for a project that required obtaining a substantial portion of the arXiv corpus in a format amenable to textual analysis. 

PDFs lack the structure typical of most document formats and often use strange encodings for collections, which makes extracting high quality text difficult and extracting math essentially impossible. Fortunately, the vast majority of papers hosted on arXiv also have LaTeX source code available which simplifies the matter considerably.

One script, `parser.hs`, uses Pandoc to create a syntax tree from the LaTeX sources and returns a JSON file containing plain text and math extract from the document. This script reads from `stdin` and returns to `stdin` and is meant to be used in a pipeline, e.g.,

```
$ input.tex | runghc parser.hs > out.json
```

or, if `parser.hs` was compiled

```
$ input.tex | ./parser > out.json
```

The other script, `fetch.py`, takes an arXiv category code as an argument and returns a JSON file containing information for `parser.hs` and metadata associated with the article based on the OAI Simple Dublin Core format.

