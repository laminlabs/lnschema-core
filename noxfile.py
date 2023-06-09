import nox
from laminci.nox import run_pre_commit  # noqa

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)
