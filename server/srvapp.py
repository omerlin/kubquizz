from flask import Flask, jsonify, request
import yaml
from redis import Redis

redis=Redis()
app = Flask(__name__)
with open('quizz.yml') as fp:
    quizz = yaml.load(fp)

@app.route('/srv/quizz', methods=['GET'])
def get_quizz():
    return jsonify({'kubernetes': quizz['kubernetes']})

@app.route('/srv/answer', methods=['POST'])
def answer():
    redis.set(request.json['user'], str(request.json))
    return jsonify({'doneFor': request.json['user']}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0')