from tasktree import TaskTree
from fractalcli.fractaltaskengine import FractalTaskEngine
from fractalcli.database import DEFAULT_DB_FILE_PATH

tasktree = TaskTree()
taskengine = FractalTaskEngine(DEFAULT_DB_FILE_PATH)