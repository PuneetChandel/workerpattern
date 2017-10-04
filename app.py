from flask import Flask,request,jsonify
from celery import result
from tasks.feedtask import processusagefeed,error_handler
app = Flask(__name__)

@app.route('/Usagefeed', methods=['POST'])
def processFeeds():

    if not 'application/json' in request.headers.get('Content-Type'):

        resp = jsonify({
            "status": 400,
            "success": False
        })
        resp.headers['Content-Type'] = 'application/json'
        resp.status_code = 400
        return resp

    data = request.json
    result = processusagefeed.apply_async(kwargs={"data": data}, serializer='json', link_error=error_handler.s())

    resp = jsonify({
        "taskId": result.task_id
    })
    resp.headers['Content-Type'] = 'application/json'
    resp.status_code = 200
    return resp

@app.route('/Usagefeed/<uuid>', methods=['GET'])
def getStatus(uuid):
    taskresult = result.AsyncResult(uuid)
    return taskresult.state


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4001)
