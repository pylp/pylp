# Getting Started


#### Check for Python 3

Make sure that you've installed Python **3.5** or higher to install Pylp.

```sh
python3 --version
```
In some cases Python 3 is just named `python` so you have to run:
```sh
python --version
```


#### Install the `pylp` command

```sh
pip install pylp
```


#### Create a `pylpfile`

Create a file named `pylpfile.py` in your project root with these contents:

```python
import pylp

pylp.task('default', function() {
    pylp.src("pylpfile.py")
      .pipe(pylp.dest("copy"))
)
```


#### Test it out

Run the pylp command in your project directory:

```sh
pylp
```

To run multiple tasks, you can use `pylp <task> <othertask>`.


#### Result

Voila! This default task will run and copy your `pympfile` in the `copy` folder.

```sh
[12:48:56] Using pylpfile ~/my-project/pympfile.py
[12:48:56] Starting 'default'...
[12:48:56] Finished 'default' after 5 ms
```


## Where do I go now?

- [API Documentation](API.md) - The programming interface
- [CLI documentation](CLI.md) - Learn how to call tasks
