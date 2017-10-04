from flask import Flask
from celerytask.makeCelery import makecelery
import time
from celery import states,result


flask_app = Flask(__name__)

flask_app.config.update(
    CELERY_BROKER_URL='amqp://puneet:Welcome1@localhost:5672/myvhost',
    CELERY_RESULT_BACKEND='mongodb://localhost:27017'

)

celery = makecelery(flask_app)

def monitor_worker():
    i = celery.control.inspect()
    print("Active : ", i.active() , "registered : ", i.registered() , "  scheduled : ", i.scheduled())


def recordusage(customerId,deviceId):
    time.sleep(2)
    print("processed feed for customer {0} and device {1} ".format(customerId,deviceId))

@celery.task(bind=True, name='usagefeed')
def processusagefeed(self,data):
    percent=1
    count = len(data)

    for x in data:
        progress=(percent/count)*100
        self.update_state(state=states.RECEIVED, meta={'progress': progress, 'customerId':x["custid"] , "deviceId":x["deviceid"] })
        print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r} delivery : {0.delivery_info!r}'.format(self.request))
        time.sleep(2)
        self.update_state(state=states.STARTED,meta={'progress': progress, 'customerId': x["custid"], "deviceId": x["deviceid"]})
        recordusage(x["custid"],x["deviceid"])

    self.update_state(state=states.SUCCESS,meta={'progress': "100%"})
    return {
        "message":"usage data processing complete"
    }


@celery.task
def error_handler(uuid):
    taskresult = result.AsyncResult(uuid)
    print('**** TASK *********** {0} raised exception: {1!r} ********************'.format(
          uuid, taskresult.traceback))
