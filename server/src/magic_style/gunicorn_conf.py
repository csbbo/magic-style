import multiprocessing

bind = "0.0.0.0:8000"
workers = (2 * multiprocessing.cpu_count()) + 1
errorlog = '/web/log/error.log'
accesslog = '/web/log/access.log'
loglevel = 'warning'
proc_name = 'gunicorn_project'
timeout = 300
