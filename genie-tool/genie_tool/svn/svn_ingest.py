import os
import subprocess
from pathlib import Path

from genie_tool.db.svn_doc_table_op import SvnDocOp
from genie_tool.util.log_util import logger


def list_changed_files(repo_path: str) -> list[str]:
    """Return a list of new or modified files under repo_path."""
    try:
        output = subprocess.check_output(["svn", "status", repo_path], text=True)
    except Exception as exc:
        logger.error(f"svn status failed: {exc}")
        return []
    changed = []
    for line in output.splitlines():
        if line and line[0] in {"A", "M"}:
            changed.append(line[8:].strip())
    return changed


def get_file_revision(path: str) -> str:
    try:
        output = subprocess.check_output(["svn", "info", path], text=True)
        for ln in output.splitlines():
            if ln.startswith("Revision:"):
                return ln.split(":", 1)[1].strip()
    except Exception:
        return ""
    return ""


def summarize(content: str) -> str:
    """Simple summarization placeholder."""
    if len(content) > 200:
        return content[:200] + "..."
    return content


def ingest(repo_path: str):
    changed_files = list_changed_files(repo_path)
    for rel_path in changed_files:
        abs_path = os.path.join(repo_path, rel_path)
        if not os.path.isfile(abs_path):
            continue
        try:
            with open(abs_path, "r", errors="ignore") as f:
                content = f.read()
        except Exception as exc:
            logger.error(f"read file failed {abs_path}: {exc}")
            continue
        revision = get_file_revision(abs_path)
        summary = summarize(content)
        tags = Path(rel_path).suffix.lstrip(".")
        logger.info(f"ingest {rel_path} rev {revision}")
        try:
            import asyncio
            asyncio.run(SvnDocOp.upsert(rel_path, revision, summary, tags))
        except Exception as exc:
            logger.error(f"db update failed for {rel_path}: {exc}")


if __name__ == "__main__":
    repo = os.getenv("SVN_REPO_PATH", ".")
    ingest(repo)
