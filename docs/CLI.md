## Pylp CLI docs

### Flags

Pylp has very few flags to know about.

- `-v` or `--version` will display Pylp versions
- `--pylpfile <pylpfile path>` will manually set path of pylpfile. Useful if you have multiple pylpfiles. This will set the CWD to the pylpfile directory as well
- `--cwd <dir path>` will manually set the CWD. The search for the pylpfile will be from here


### Tasks

Tasks can be executed by running `pylp <task> <task>...`.

If more than one task is listed, Pylp will execute all of them
concurrently, that is, as if they had all been listed as dependencies of
a single task.

Just running `pylp` will execute the task `default`. If there is no
`default` task, an error will be returned.
