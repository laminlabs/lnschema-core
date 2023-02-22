import shutil

import lamindb as ln
import lamindb.schema as lns
import lndb
import nox
from lndb.test._env import get_package_name
from lndb.test.nox import (
    build_docs,
    login_testuser1,
    run_pre_commit,
    run_pytest,
    setup_test_instances_from_main_branch,
)

nox.options.reuse_existing_virtualenvs = True


def upload_run(session):
    package_name = get_package_name()
    filename = f"{package_name}_docs.zip"
    shutil.make_archive(filename, "zip", "./docs")
    lndb.load("testuser1/lamin-site-assets", migrate=True)
    with ln.Session() as ss:
        dobject = ss.select(ln.DObject, name=filename).one_or_none()
        dobject_id = None if dobject is None else dobject.id
        pipeline = ln.add(lns.Pipeline, name=f"CI {package_name}")
        run = lns.Run(pipeline=pipeline)
        dobject = ln.DObject(filename, id=dobject_id, run=run)
        ss.add(dobject)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    login_testuser1(session)
    setup_test_instances_from_main_branch(session)
    session.install(".[dev,test]")
    run_pytest(session)
    build_docs(session)
