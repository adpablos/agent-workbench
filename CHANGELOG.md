# Changelog

User-visible changes to the core. Versions follow [Semantic Versioning](https://semver.org/). The
first release, `v0.1.0`, is tagged once a workbench passes base acceptance in
[docs/VALIDATION.md](docs/VALIDATION.md); until then, changes stay under Unreleased. Workbenches
pin a release tag together with its commit.

## Unreleased

- The agent updates the core on request: it shows the changes since the pinned revision, pulls
  after approval, and records the new and previous revisions in `workspace.json`.
- Reference clones and tool checkouts can live inside the workbench, in `repos/<project>/<repo>`
  and `tools/`, once a preflight probe shows that the host does not load instruction files from
  subfolders; until then they stay outside the opened root.
- Changes reach `main` only through reviewed pull requests that pass a documentation check of
  line width and relative links.
- First Markdown core: the operating contract, the validation procedure, templates for the
  entrypoint and private files, an agent-guided setup, and the MIT license.
