import os, platform
from flask import Flask, jsonify, request
import yaml
import redis

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))

rediscli=redis.StrictRedis(host=redis_host, port=redis_port)
app = Flask(__name__)
with open(os.environ.get('SRVAPPENV','/etc/config/quizz.yml')) as fp:
    quizz = yaml.load(fp)

@app.route('/srv/quizz/<category>', methods=['GET'])
def get_quizz(category):
    try:
        return jsonify({category: quizz[category]}), 200
    except KeyError:
        return jsonify('Unknown quizz category: {}'.format(category), 500)

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
    for key in rediscli.scan_iter("*"):
        results[key.decode('utf-8')] = rediscli.get(key).decode('utf-8')
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=os.environ.get('SRVAPPDEBUG','FALSE').upper()=='TRUE',
            port=int(os.environ.get('SRVAPPPORT', 60000 if platform.system() else 6000)))
