# texToJSON

This is a tiny little haskell script I wrote for an old computational text analysis project several years ago. It uses Pandoc to create a syntax tree from the LaTeX sources and returns a JSON file containing plain text and math extracted from the document. This script reads from `stdin` and returns to `stdout`. It is meant to be used in a pipeline, e.g.,

```
$ input.tex | runghc parser.hs > out.json
```

or, if `parser.hs` was compiled

```
$ input.tex | ./parser > out.json
```


