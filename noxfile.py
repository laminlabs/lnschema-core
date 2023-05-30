import sys
from pathlib import Path

import nox
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_artifact
from laminci.nox import build_docs, login_testuser1, run_pytest  # noqa

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    session.run(*"pip install pre-commit".split())
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def install(session: nox.Session) -> None:
    session.run(*"pip install --no-deps .[django]".split())
    session.run(*"git clone https://github.com/laminlabs/lamindb --depth 1".split())
    if sys.platform.startswith("linux"):  # remove version pin when running on CI
        session.run(*"sed -i /lnschema_core/d ./lamindb/pyproject.toml".split())
    session.run(*"pip install ./lamindb[aws,test]".split())


@nox.session()
def build(session: nox.Session) -> None:
    login_testuser1(session)
    run_pytest(session)
    prefix = "." if Path("./lndocs").exists() else ".."
    session.run(*f"pip install {prefix}/lndocs".split())
    session.run(*"lamin init --storage ./docsbuild".split())
    session.run("lndocs")
    upload_docs_artifact()
    move_built_docs_to_docs_slash_project_slug()
