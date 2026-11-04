# Workbench

This folder coordinates agent work across repositories and information sources. It is not a Git
repository.

Before acting, read these files in full:

1. `core/OPERATING.md`: the operating contract.
2. `private/POLICY.md`: approved local rules and preferences.

A read counts only when the tool returned the whole file. A refused, truncated, or partial read, or
one issued together with the first operation, does not: finish reading before you act.

A complete read stays valid while it is visible in your current context and the file has not
changed since. Read again at the start of a session or worker; after compaction, summarization, or
any other context reset; whenever the earlier read is no longer visible; before taking over
ownership; and after the file changed. When unsure, read again. A new request in the same context
does not by itself require reading unchanged files again. The whole current text of a file that the
host places in your context counts as a read, also right after a reset; a summary of a file or a
reference to it does not. This file needs no separate read while its text is in your context, for
example because the host loaded it.

Read `private/workspace.json` before accessing any source or path, and `private/INDEX.md` when you
resume work in a new or reset context; both reads stay valid in the same way. If `core/OPERATING.md`
cannot be read, report that and do nothing else. If `private/POLICY.md` or `private/workspace.json`
is missing or still shows a placeholder approval date, the workbench is being set up: only continue
the setup in `core/README.md`.

Organizational requirements and the instructions of each repository you work in remain binding.
Report conflicts instead of choosing between them.
