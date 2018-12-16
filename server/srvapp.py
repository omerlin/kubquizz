import os
from flask import Flask, jsonify, request
import yaml
import redis

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))

rediscli=redis.StrictRedis(host=redis_host, port=redis_port)
app = Flask(__name__)
with open('quizz.yml') as fp:
    quizz = yaml.load(fp)

@app.route('/srv/quizz', methods=['GET'])
def get_quizz():
    return jsonify({'kubernetes': quizz['kubernetes']})

@app.route('/srv/answer', methods=['POST'])
def answer():
    # try increment
    rediscli.incr('{}_counter'.format(request.json['user']))
    # quizz result
    rediscli.set(request.json['user'], str(request.json))
    return jsonify({'doneFor': request.json['user']}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)