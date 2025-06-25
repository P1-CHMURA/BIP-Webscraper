from celery import Celery
from redbeat import RedBeatScheduler


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])


    # RedBeat setup
    celery.conf.update(
        redbeat_redis_url="redis://webscraping_redis:6379/0",
    )
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery