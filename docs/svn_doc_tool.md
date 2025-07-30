# SVN Document Integration

This document describes how to enable searching SVN documents with JDGenie.

The new `svn_ingest.py` script scans a local SVN working copy, extracts summaries
for changed files and stores them in the SQLite database used by Genie Tool.

Run it periodically (for example via cron):

```bash
SVN_REPO_PATH=/path/to/working/copy python -m genie_tool.svn.svn_ingest
```

Use `svn_search.py` to query the stored summaries:

```bash
python -m genie_tool.svn.svn_search "payment design"
```

Results will include the file path and stored summary.
