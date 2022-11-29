import pylp
from pylpconcat import concat

# Concat all py files from 'src' folder
pylp.task('py', lambda:
    pylp.src('../unit/**/*.py')
      .pipe(concat('all.py'))
      .pipe(pylp.dest('.build'))
)

# The default task (called when you run 'pylp' from cli)
pylp.task('default', ['py'])

