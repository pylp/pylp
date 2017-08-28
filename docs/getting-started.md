# Getting Started


#### Check for Python 3

Make sure that you've installed Python **3.5** or higher to install Pylp.

```sh
python --version
```

In certain cases Python 3 is named `python3` so you have to run:

```sh
python3 --version
```


#### Install Pylp

```sh
pip install pylp
```

If you don't have Python `Scripts` folder in your PATH you can run also:

```sh
python -m pip install pylp
```


#### Create a `pylpfile`

Create a file named `pylpfile.py` in your project root with these contents:

```python
import pylp

pylp.task('default', lambda:
    pylp.src("pylpfile.py")
    # .pipe(a_plugin())  <-- Here you can pipe plugins you want
    # .pipe(another_plugin())
      .pipe(pylp.dest("copy"))
)
```


#### Test it out

Run the `pylp` command in your project directory:

```sh
pylp
```

If you don't have Python `Scripts` folder in your PATH you can run also:

```sh
python -m pylp
```

To run multiple tasks, you can use `pylp <task> <othertask>`.


#### Result

Voila! This default task will run and copy your `pylpfile` in the `copy` folder.

```sh
[12:48:56] Using pylpfile ~/my-project/pylpfile.py
[12:48:56] Starting 'default'...
[12:48:56] Finished 'default' after 5 ms
```


## Where do I go now?

- [API Documentation](API.md) - The programming interface
- [CLI documentation](CLI.md) - Learn how to call tasks
