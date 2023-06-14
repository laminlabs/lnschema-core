import nox
from laminci.nox import run_pre_commit, run_pytest  # noqa

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def test(session: nox.Session) -> None:
    run_pytest(session)
