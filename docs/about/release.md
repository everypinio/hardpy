# Release

Jig is published to [PyPI](https://pypi.org/project/pytest-jig/) as `pytest-jig`.
The distribution name differs from the import name because `jig` was already
taken on PyPI; `import jig` and the `jig` command are unaffected.

Releases are driven entirely by git tags. Pushing a version tag runs
`.github/workflows/release.yml`, which checks the tag against the package
version, runs the test suite and the Python/pytest matrix, builds the
distributions, signs them, creates the GitHub release, then publishes to
TestPyPI followed by PyPI.

## One-time setup

The pipeline authenticates to PyPI with
[trusted publishing](https://docs.pypi.org/trusted-publishers/), an OIDC
exchange between GitHub Actions and PyPI. There is no API token to create,
store, or rotate, and nothing to add to the repository secrets.

### 1. Enable two-factor authentication

PyPI requires 2FA to upload. Enable it on both
[PyPI](https://pypi.org/manage/account/) and
[TestPyPI](https://test.pypi.org/manage/account/) (the two are separate
accounts and need separate registration).

### 2. Register the trusted publisher on PyPI

Because `pytest-jig` does not exist on PyPI yet, register it as a *pending*
publisher, which both reserves the name and authorizes the workflow. Go to
[PyPI publishing settings](https://pypi.org/manage/account/publishing/), choose
**GitHub** under "Add a new pending publisher", and fill in:

| Field | Value |
| --- | --- |
| PyPI Project Name | `pytest-jig` |
| Owner | `samuelint` |
| Repository name | `jig` |
| Workflow name | `release.yml` |
| Environment name | `pypi` |

The values must match exactly — trusted publishing only accepts a token minted
by that workflow, in that repository, running in that environment.

### 3. Repeat on TestPyPI

Do the same at
[TestPyPI publishing settings](https://test.pypi.org/manage/account/publishing/),
with **Environment name** set to `testpypi` instead of `pypi`.

### 4. Create the GitHub environments

In the repository, open **Settings → Environments** and create two
environments named exactly `pypi` and `testpypi`. They can be empty; the names
are what the trusted publishers are bound to.

Adding a **required reviewer** to the `pypi` environment is worthwhile: the
release then pauses for an explicit approval after TestPyPI succeeds and before
anything is published to PyPI, which is the last point where a bad build can
still be stopped.

After the first successful publish, PyPI converts the pending publisher into a
regular one. No further setup is needed for later releases.

## Cutting a release

1. Set the new version in `pyproject.toml`. It is the single source of truth:
   `jig.__version__` reads it from the installed metadata, and the pipeline
   refuses to release when the git tag disagrees with it.
2. Move the `Unreleased` entries in `docs/changelog.md` under the new version.
3. Reinstall the package so the local metadata matches
   (`pip install -e .`, or `poetry install`), then run `pytest tests -m "not manual"`.
   `tests/test_packaging.py` fails if the installed version has drifted.
4. Merge to `main`.
5. Tag the merge commit with the bare version — no `v` prefix — and push it:

```bash
git tag 1.0.0
git push origin 1.0.0
```

Only tags shaped like `1.0.0` or `1.0.0rc1` trigger the release workflow.

## Verifying a release

Watch the **Release** workflow in the Actions tab. Once it is green:

```bash
pip install pytest-jig
jig --version
```

The version printed must match the tag. The build also asserts that the
operator panel frontend is bundled in both the sdist and the wheel
(`scripts/check_dist.py`), so a package that installs but serves an empty panel
fails the pipeline instead of reaching PyPI.

## If a release fails

Nothing is published unless every earlier job passed, so a failure before the
publish step is safe to fix and retry by deleting and re-pushing the tag.

A version already uploaded to PyPI cannot be replaced or reused, even after
deletion — that is a PyPI rule, not a pipeline limitation. Recover by releasing
the next patch version. TestPyPI is exempt: the workflow skips an existing
version there so a rehearsal upload never blocks the real release.
