# Database schema visualiser for documentation.  # noqa: INP001
# need to install erdantic: https://github.com/drivendataorg/erdantic
# Installation:
# conda install erdantic -c conda-forge

import erdantic as erd

from jig.pytest_jig.db.schema import ResultRunStore, ResultStateStore

erd.draw(ResultRunStore, out="runstore.png")
erd.draw(ResultStateStore, out="statestore.png")
