# Database schema visualiser for documentation.  # noqa: INP001
# need to install erdantic: https://github.com/drivendataorg/erdantic

import erdantic as erd

from hardpy.pytest_hardpy.db.schema import ResultRunStore, ResultStateStore

erd.draw(ResultRunStore, out="runstore.png")
erd.draw(ResultStateStore, out="statestore.png")
