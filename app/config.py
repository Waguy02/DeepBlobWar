import os
DEBUG = 10
INFO = 20
WARN = 30
ERROR = 40
DISABLED = 50


ROOT_DIR=os.path.abspath(os.curdir)
LOGDIR = os.path.join(ROOT_DIR,"logs")
RESULTSPATH = os.path.join(ROOT_DIR,'viz/results.csv')
TMPMODELDIR = os.path.join(ROOT_DIR,"zoo/tmp")
MODELDIR = os.path.join(ROOT_DIR,"zoo")
