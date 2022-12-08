import nox
from lndb_setup.test.nox import (
    build_docs,
    login_testuser1,
    setup_test_instances_from_main_branch,
)

nox.options.reuse_existing_virtualenvs = True


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    login_testuser1(session)
    setup_test_instances_from_main_branch(session)
    session.install(".[dev,test]")
    session.run(
        "pytest",
        "-s",
        "--cov=lnschema_core",
        "--cov-append",
        "--cov-report=term-missing",
    )
    session.run("coverage", "xml")
    build_docs(session)
