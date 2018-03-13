# polyglottus
A format for writing a script that contains blocks in different languages that will run in multiple kernels and potentially intercommunicate. A script of this type should be able to be imported into a notebook, or just run at the command line.

I love using Jupyter notebooks and use them quite a lot. I have taught workshops with them. But I would also like to have something similar that is a little more programmatic. A notebook is less a program or a document than a serialized client "session." I also very much like R-Markdown for it's programmatic and textual simplicity. Then there is R-Spin, and more recently Nteract.

All of these are attempts at literal programming that emphasize code and documentation in different ways. Some are more flexible than others, and some are more rational than others. For instance, although Nteract seems close to what I want to do, I think it is still a bit confused and inconsistent about how to define cells.

I'd like to make my own attempt. My idea is that everything rendered or computed is in a specified block. Anything outside of a block is a comment, and not rendered. Thus code and documentation are on completely equal footing, and all blocks (or cells) are delineated in the same way. Importing and exporting variables between cells, even with different kernels, is also done in a consistent manner (this is a feature that Jupyter lacks).
