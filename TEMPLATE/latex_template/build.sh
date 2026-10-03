#!/bin/sh
# Builds main.pdf with XeLaTeX (run twice for page totals and header marks).
latexmk -xelatex -interaction=nonstopmode main.tex
