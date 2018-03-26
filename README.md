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
I played around with a couple of different ideas for how to delineate code blocks. 
I've settled on a syntax hat combines the _magics_ syntax from IPython/Jupyter and 
the Matlab cell syntax. To start a cell you begin a line with `%%` followed by a
_processor_ name. This is the name of the kernel or other method to parse, execute,
and/or render what is in the block. Including a `tilde` "~" directly after the processor
name tells the parser that a section of metadata will follow (not married to the tilde,
was just my first hit). The metadata is in YAML format and sepcifies such things as
variables imported from other kernels, stylesheets, whether or not to display code
and/or output, etc. A code cell is closed with `/%%`.

Example:

```
This is is ignored because it is not in a cell

%%kerneldefs
r1 = kernel(language="R", kernel_name="ir")
p1 = kernel(languag="Python", kernel="IPython")
m1 = kernel(language="Markedown", renderer="markdown.js")
/%%

%%r1
a <- 10
/%%

%%m1~
------
imports:
  - r1:
      data: a
stylesheet: sleek
------
This is some markdown. In the kernel _r1_ the variable
`a` has the value {{a}}.
/%%

%%python~
------
imports:
  - r1:
      maximum: a
------
for i in range(maximum):
  print(i)
/%%
```

## Importing Data
You will be able to import data from one kernel into another for a limited number of
data types. For starters, these will be an extended set of the usual primitive types:

> int, float, string, array, dict, table

### Import equivalencies can be defined:

data.table <==> DataFrame (Python), Object (JS), TSV (bash)
string <==> string
int <==> int
Array <==> List, Array, etc.
Dict <==> JS object (JS), nested named lists (R), YAML, XML
etc.

## Status
I currently have a working parser class `polylparser.py` which successfully parses the
file `sample.poly`.

I also have a working wrapper for the the `jupyter_client` in `simple_kernel.py` that 
allows me to create kernels in multiple languages. A separate test of running code in 
diferent kernels (currently have tested Python, R, bash, javascript, typescript, and 
nodejs) is `multi_kernel_test.py`.

## Short-Term ToDo
- [x] Choose a format and write a parser
- [x] Create a parser class
- [ ] Combine `simple_kernel.py`, `polyparser.py`, and `multi_kernel_client.py` into a 
      prototype of parsing an actual `.poly` file.
- [x] Learn how to create kernels in languages other than Python.
- [ ] Learn to use more of the `jupyter_client` API such as the JSON payloads
described in the documentation.
- [ ] 
