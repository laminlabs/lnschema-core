import os

import nox
import requests  # type: ignore  # noqa
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_artifact
from laminci.nox import build_docs, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    session.run(*"pip install pre-commit".split())
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def build(session):
    session.run(*"pip install .[dev,test]".split())
    session.run(*"git clone https://github.com/laminlabs/lamindb --depth 1".split())
    if os.system().startswith("linux"):  # remove version pin when running on CI
        session.run(*"sed -i '/lnschema_core/d' ./lamindb/pyproject.toml".split())
    session.run(*"pip install ./lamindb".split())
    run_pytest(session)
    build_docs(session)
    upload_docs_artifact()
    move_built_docs_to_docs_slash_project_slug()
