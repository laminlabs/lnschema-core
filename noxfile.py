import sys

import nox
import requests  # type: ignore  # noqa
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_artifact
from laminci.nox import build_docs, login_testuser1, run_pre_commit, run_pytest  # noqa

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def install(session: nox.Session) -> None:
    session.run(*"pip install --no-deps .[django]".split())
    session.run(*"git clone --no-single-branch --depth 1 https://github.com/laminlabs/lamindb".split())
    # response = requests.get("https://github.com/laminlabs/lamindb/tree/cleanup")
    # if response.status_code < 400:
    #     with session.chdir("./lamindb"):
    #         session.run(*"git switch cleanup".split())
    if sys.platform.startswith("linux"):  # remove version pin when running on CI
        session.run(*"sed -i /lnschema_core/d ./lamindb/pyproject.toml".split())
    session.run(*"pip install ./lamindb[aws,test]".split())


@nox.session()
def build(session: nox.Session) -> None:
    login_testuser1(session)
    run_pytest(session)
    session.run(*"lamin init --storage ./docsbuild".split())
    build_docs(session)
    upload_docs_artifact()
    move_built_docs_to_docs_slash_project_slug()
