## Pylp API docs

Jump to
  [pylp.src](#pylpsrcglobs-options) |
  [pylp.dest](#pylpdestpath-options) |
  [pylp.task](#pylptaskname--deps--fn) |
  [pylp.pipes](#pylppipesstream-plugins)



### pylp.src(globs, **options)

Create a new stream and add some files found from a glob or a list of globs.  
The function returns this `pylp.Stream` that can be piped to plugins.

```python
pylp.src('templates/*.jade')
  .pipe(jade())
  .pipe(pylp.dest('build'))
```


#### globs
Type: `str` or `list` of `str`

Glob or list of globs to read.

A glob that begins with `!` excludes matching files from the glob results up to that point.
For example, consider this directory structure:

    client/
      a.js
      bob.js
      bad.js

The following expression matches `a.js` and `bad.js`:

    pylp.src(['client/*.js', '!client/b*.js', 'client/bad.js'])


#### options

##### options.read
Type: `bool`  
Default: `True`

Setting this to `False` will return `file.contents` as an empty string and not read the file
at all.

##### options.base
Type: `str`  
Default: everything before a glob starts.

E.g., consider `somefile.js` in `client/js/somedir`:

```python
pylp.src('client/js/**/*.js') # Matches 'client/js/somedir/somefile.js'
  .pipe(pylp.dest('build'))   # Writes 'build/somefile.js'

pylp.src('client/js/**/*.js', base='client')
  .pipe(pylp.dest('build'))   # Writes 'build/js/somedir/somefile.js'
```



### pylp.dest(path, **options)

Can be piped to and it will write files. Re-emits all data passed to it so you can pipe to multiple folders.  Folders that don't exist will be created.

```python
pylp.src('templates/*.jade')
  .pipe(jade())
  .pipe(pylp.dest('build'))
```

The write path is calculated by appending the file relative path to the given
destination directory. In turn, relative paths are calculated against the file base.
See `pylp.src` above for more info.


#### path
Type: `str` or `callable`

The path (output folder) to write files to. Or a function that returns it, the function will be provided a `pylp.File`.

#### options

##### options.cwd
Type: `str`  
Default: `os.getcwd()`

`cwd` for the output folder, only has an effect if provided output folder is relative.



### pylp.task(name [, deps] [, fn])

Define a task in a pylpfile.  
You can also use this function as decorator with `pylp.fn.task(name [, deps])`.

```python
pylp.task('default', lambda:
    pylp.src('folder/file.py')
      .pipe(plugin1())
      .pipe(pylp.dest('build'))
)
```


#### name
Type: `str`

The name of the task. Tasks that you want to run from the command line should not have spaces in them.


#### deps
Type: `list`

A list of tasks to be executed and completed before your task will run.

```python
pylp.task('mytask', ['list', 'of', 'task', 'names'], lambda: ...)
```

You can also omit the function if you only want to run a bundle of dependency tasks:

```python
pylp.task('build', ['list', 'of', 'task', 'names'])
```

**Note:** The tasks will run in parallel (all at once), so don't assume that the tasks will start/finish in order.


#### fn
Type: `callable`

The function performs the task's main operations. This function **must** return a `pylp.Stream`.  
Generally it's a lambda that takes the form of:

```python
pylp.task('buildStuff', lambda:
    pylp.src('<some source path>')
      .pipe(plugin1())
      .pipe(plugin2())
      .pipe(pylp.dest('<some destination>'))
)
```

You can also use a decorator from the module `pylp.fn` for creating a task.

```python
@pylp.fn.task('buildStuff')
def build_stuff:
    stream = pylp.src('<some source path>') \
      .pipe(plugin1()) \
      .pipe(plugin2()) \
      .pipe(pylp.dest('<some destination>'))
    return stream
```



### pylp.pipes(stream, *plugins)

Pipes plugins end-to-end, starting with a stream.

The following tasks give the same result.

```python
pylp.task('buildStuff', lambda: pylp.pipes(
    pylp.src('<some source path>'),
    plugin1(),
    plugin2(),
    pylp.dest('<some destination>')
))
```

```python
pylp.task('buildStuff', lambda:
    pylp.src('<some source path>')
      .pipe(plugin1())
      .pipe(plugin2())
      .pipe(pylp.dest('<some destination>'))
)
```


#### name
Type: `pylp.Stream`

The stream where the piping will start.


#### plugins
Type: `list` of `pylp.Transformer`

The list of plugins to pipe.
