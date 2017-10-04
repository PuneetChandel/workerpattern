from celery import Celery,task

def makecelery(app):

    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL']
                    )

    celery.conf.update(app.config)

    celery.conf.update(CELERY_ROUTES = [{"usagefeed": {"queue" : "usage_queue"}},
                                        {"customerfeed": {"queue": "customer_queue"}}])

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery
