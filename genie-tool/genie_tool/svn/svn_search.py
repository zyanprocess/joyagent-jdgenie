import asyncio
from typing import List

from genie_tool.db.svn_doc_table_op import SvnDocOp


def search(keyword: str) -> List[str]:
    docs = asyncio.run(SvnDocOp.search_by_keyword(keyword))
    return [f"{d.path}: {d.summary}" for d in docs]


if __name__ == "__main__":
    import sys
    kw = sys.argv[1] if len(sys.argv) > 1 else ""
    for line in search(kw):
        print(line)
