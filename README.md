# Polyglottus
_Code blocks and markup interacting in a single script in a consistent format
for literate programming_.

## Overview
Polyglottus will be a format for writing a script that contains blocks in different
languages, including markup languages, that will run in multiple kernels which
can import data from each other. A script of this type should be able to be
imported into a notebook (or run as a notebook given the proper infrastructure),
or simply run at the command line to output a notebook-like document.

## Reason
I love using Jupyter notebooks and use them quite a lot. I have taught workshops
with them. But I would also like to have something similar that is a little more
programmatic. A notebook is less a program or a document than a serialized client
"session." I also very much like R-Markdown for it's programmatic and textual simplicity.
Then there is R-Spin, and more recently Nteract.

All of these are attempts at literate programming that emphasize code and
documentation in different ways. Some are more flexible than others, and some are
more rational than others. For instance, although `hydrogen` (nteract for the Atom
editor) seems close to what I want to do, it is still "markup first", and does not
have a robust syntax to define cells.

This is my own attempt. My idea is that only things in cells (blocks, chunks, ...)
are executed, processed, or rendered. specified block. Anything outside of a block
is a comment, and not rendered. Thus code and documentation are on completely equal
footing, and all blocks (or cells) are delineated in the same way. Importing and
exporting variables between cells, even with different kernels, is also done in a
consistent manner (this is a feature that Jupyter lacks).

## Formats
The `.poly` files are my attempts at a syntax. Right now the one that I like the
best combines the _magics_ syntax from IPython/Jupyter and the Matlab cell syntax.
To start a cell you begin a line with `%%` followed by a _processor_ and optional
keyword arguments. My second favorite has the arguments in a YAML header similar
to the meta section of an RMarkdown document.

## Status
I currently have a working parser prototype for the #1 choice, `parse_poly.py` and
a short test called `small_parse_test.txt`. Right now the parser can isolate code
blocks, the processor, the keyword arguments (if present) and the code.

I also have a working wrapper for the the `jupyter_client` that allows me to
create Jupyter python kernels, execute code in them, and collect the responses.

## Short-Term ToDo
- [ ] Test creating multiple kernels and importing data from them into other kernels
as well as Markup such as markdown and HTML.
- [ ] Learn how to create kernels in languages other than Python.
- [ ] Learn to use more of the `jupyter_client` API such as the JSON payloads
described in the documentation.
