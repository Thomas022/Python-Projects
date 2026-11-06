# Lesson configuration

When creating or updating Python lessons, load the project-root `.env` with `python-dotenv` before initializing LangGraph or LangSmith. Resolve the path from `__file__` so scripts work from any directory; preserve existing environment variables (`override=False`, the default). Include `python-dotenv` in fresh-environment setup instructions.

Teach learners to save LangSmith credentials once in `.env` and reuse them across lessons and terminal sessions. Configure tracing, project, optional endpoint, and workspace there. Explain that existing terminal exports take precedence. Keep `.env` ignored by Git; never read, print, or copy its secret values into lessons, chat, or committed files. Use placeholders in documentation.
