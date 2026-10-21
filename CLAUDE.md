## Project
AutoPilot ML X: Self-healing MLOps platform. Current version: v2.
This batch: test-database fix only (docs/specs/fix-test-db.md).

## Commands
- Run app: streamlit run app.py
- Check: pytest -q and pre-commit run --all-files

## Rules
- IMPORTANT: ask before adding any dependency.
- Every number on a page comes from a function, a file or the database.
- No HTML in the app: no unsafe_allow_html, no st.html.
- Do not commit. Do not edit README.md, docs/design.md, docs/build_log.md
  or docs/specs/.
- Ask before installing a package, deleting a file or touching anything
  outside this folder.
- Code layout: comments 4-6 words, verb first; max 76 characters a line.