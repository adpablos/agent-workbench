# Changelog

User-visible changes to the core. Versions follow [Semantic Versioning](https://semver.org/). The
first release, `v0.1.0`, is tagged once a workbench passes base acceptance in
[docs/VALIDATION.md](docs/VALIDATION.md); until then, changes stay under Unreleased. Workbenches
pin a release tag together with its commit.

## Unreleased

- `docs/PULL-REQUESTS.md` defines what a pull request contains, the review request, what counts as
  a material finding and a verdict, how to answer findings, what later rounds cover, and what
  happens when the base moves.
- `docs/DEFAULTS.md` lists what the core does by default, with one-line settings in
  `private/POLICY.md` or a project's agent instructions, and a five-rule safety floor that takes a
  recorded waiver to change. Project practices such as the changelog and versioning apply according
  to what a project is, or is meant to be.
- Independent review is the floor; a different model family is the default way to get it. Rounds
  after the first review cover the earlier findings and the new diff, unless a project sets
  `re-review: full`. The report labels follow the conversation's language and can be turned off.
- Updating the core takes a project's `core-version`, then the latest tag, then the tip of `main`.
- The README explains how anyone can contribute, how to work with others, and that `main` stays
  usable.
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
