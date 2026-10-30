# Changelog

User-visible changes to the core. Versions follow [Semantic Versioning](https://semver.org/). The
first release, `v0.1.0`, is tagged once a workbench passes base acceptance in
[docs/VALIDATION.md](docs/VALIDATION.md); until then, changes stay under Unreleased. Workbenches
pin a release tag together with its commit.

## Unreleased

- The core no longer assumes one host or operating system. `docs/HOSTS.md` records where Claude
  Code, Codex, and other hosts differ in instruction loading, delegation, and model evidence.
- A Claude Code workbench excludes `repos/` and `tools/` in `.claude/settings.json`, so that the
  instructions of reference repositories do not reach the Director. The subfolder probe now targets
  those folders, and it no longer accepts a clean reply as proof: an agent may ignore a file the
  host loaded.
- Assignments name the instruction files of each repository, and model evidence comes from the
  turn that did the work.
- The agent updates the core on request: it validates the candidate commit apart from the active
  core, activates exactly that commit after approval, and records the new and previous revisions
  in `workspace.json`.
- Reference clones and tool checkouts can live inside the workbench, in `repos/<project>/<repo>`
  and `tools/`, once a preflight probe shows that the host does not load instruction files from
  subfolders; until then they stay outside the opened root.
- Changes reach `main` only through reviewed pull requests that pass a documentation check of
  line width and relative links.
- First Markdown core: the operating contract, the validation procedure, templates for the
  entrypoint and private files, an agent-guided setup, and the MIT license.
