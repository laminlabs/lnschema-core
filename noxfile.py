import nox
from laminci.nox import login_testuser1, run, run_pre_commit, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def test(session: nox.Session) -> None:
    run(session, "pip install -e .[dev]")
    run(
        session,
        "pip install lamindb_setup@git+https://github.com/laminlabs/lamindb-setup",
    )
    run_pytest(session, coverage=False)
