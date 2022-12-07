import os
from pathlib import Path
from time import sleep

import nox
from lndb_setup._clone import setup_local_test_postgres

# from lndb_setup._nox_tools import setup_test_instances_from_main_branch
# from lndb_setup._test_migrate import model_definitions_match_ddl

nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.default_venv_backend = None


def setup_test_instances_from_main_branch(session):
    login_user_1 = "lndb login testuser1@lamin.ai --password cEvcwMJFX4OwbsYVaMt2Os6GxxGgDUlBGILs2RyS"  # noqa
    session.run(*(login_user_1.split(" ")), external=True)
    # init a test instance from the main branch
    if "GITHUB_BASE_REF" in os.environ and os.environ["GITHUB_BASE_REF"] != "":
        session.run("git", "checkout", os.environ["GITHUB_BASE_REF"], external=True)
    # install the current package from main
    # currently not needed
    # session.install(".")
    # session.run(*"lndb init --storage testdb".split(" "), external=True)
    # postgres test instance
    url = setup_local_test_postgres()
    sleep(2)
    session.run(*f"lndb init --storage pgtest --db {url}".split(" "), external=True)
    # go back to the PR branch
    if "GITHUB_HEAD_REF" in os.environ and os.environ["GITHUB_HEAD_REF"] != "":
        session.run("git", "checkout", os.environ["GITHUB_HEAD_REF"], external=True)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    setup_test_instances_from_main_branch(session)
    session.install(".[dev,test]")
    # do not test sqlite
    # try:
    #     # cannot run from within pytest right now
    #     model_definitions_match_ddl("lnschema_core", dialect_name="sqlite")
    # except Exception as e:
    #     print(e)
    # url = "postgresql://postgres:pwd@0.0.0.0:5432/pgtest"
    # session.run(*f"lndb init --storage pgtest --db {url}".split(" "))
    session.run(
        "pytest",
        "-s",
        "--cov=lnschema_core",
        "--cov-append",
        "--cov-report=term-missing",
    )
    session.run("coverage", "xml")
    prefix = "." if Path("./lndocs").exists() else ".."
    session.install(f"{prefix}/lndocs")
    session.run("lndocs")
