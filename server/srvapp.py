import os
from flask import Flask, jsonify, request
import yaml
import redis

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))

rediscli=redis.StrictRedis(host=redis_host, port=redis_port)
app = Flask(__name__)
with open('/etc/config/quizz.yml') as fp:
    quizz = yaml.load(fp)

@app.route('/srv/quizz', methods=['GET'])
def get_quizz():
    return jsonify({'kubernetes': quizz['kubernetes']}), 200

@app.route('/srv/answer', methods=['POST'])
def answer():
    """
      Store user quizz results 
    """
    # try increment
    rediscli.incr('{}_counter'.format(request.json['user']))
    # quizz result
    rediscli.set(request.json['user'], str(request.json))
    return jsonify({'doneFor': request.json['user']}), 201

@app.route('/srv/data', methods=['GET'])
def get_data():
    """
       Get all the datas stored in redis
    """
    results={}
    for key in rediscli.scan_iter("user:*"):
        results[key] = rediscli.get(key)
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
