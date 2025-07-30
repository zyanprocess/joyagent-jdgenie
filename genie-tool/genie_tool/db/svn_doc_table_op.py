from typing import List, Optional
from sqlmodel import select

from genie_tool.db.db_engine import async_session_local
from genie_tool.db.svn_doc_table import SvnDocSummary
from genie_tool.util.log_util import timer


class SvnDocOp:
    @staticmethod
    @timer()
    async def upsert(path: str, revision: str, summary: str, tags: Optional[str] = None) -> SvnDocSummary:
        async with async_session_local() as session:
            state = select(SvnDocSummary).where(SvnDocSummary.path == path)
            result = await session.execute(state)
            doc = result.scalars().one_or_none()
            if doc:
                doc.revision = revision
                doc.summary = summary
                doc.tags = tags
                session.add(doc)
            else:
                doc = SvnDocSummary(path=path, revision=revision, summary=summary, tags=tags)
                session.add(doc)
            await session.commit()
            return doc

    @staticmethod
    @timer()
    async def search_by_keyword(keyword: str) -> List[SvnDocSummary]:
        async with async_session_local() as session:
            state = select(SvnDocSummary).where(SvnDocSummary.summary.contains(keyword))
            result = await session.execute(state)
            return result.scalars().all()
