import os
from flask import Flask, session, render_template, url_for, redirect, request, flash
from random import randint, shuffle
import requests
import yaml,json
from copy import deepcopy
from datetime import datetime, date, time

#------------- Server side ---------------------
def get_questions(uri, category='kubernetes'):
    q = requests.get(uri)
    # a trick to transcode JSON "null" to python None
    null=None
    q1=eval(q.text)
    shuffle(q1[category])
    questions={}
    for i,k in enumerate(q1[category]):
        questions[str(i+1)]=k    
    return questions

def load_config():
    with open('/etc/quizz/config.yml') as fp:
        return yaml.load(fp)

def filter_env():
    d = dict(os.environ)
    for k in ['LS_COLORS','PS1']:
        d.pop(k,None)
    return str(d)


#-------------- Client side ----------------------------------
# Create a flask app and set its secret key
app = Flask(__name__)
app.secret_key = os.urandom(24)

config = load_config()

questions = get_questions('{}/srv/quizz'.format(config['uri']))
resp_uri='{}/srv/answer'.format(config['uri'])
app.nquestions=len(questions)
start_date = datetime.now()
msg = { 'user': config['user'], 'quizz': config['category'], 'env': filter_env(),
        'start_date': str(start_date), 'end_date': None, 'duration': None, 'result':None }
respids = {}

@app.route('/quizz', methods=['GET', 'POST'])
def quizz():
  if request.method == "POST":
    entered_answer = request.form.get('answer_python', '')
    print (entered_answer)
    if not entered_answer:
        # Show error if no answer entered    		
        flash("Please choose an answer", "error")
    respids[questions[session["current_question"]]["id"]] = entered_answer

    # set the current question to the next number when checked
    session["current_question"] = str(int(session["current_question"])+1)
    if session["current_question"] in questions:
    # If the question exists in the dictionary, redirect to the question
        redirect(url_for('quizz'))
    else:
        end_date=datetime.now()
        msg['duration']=str(end_date-start_date)
        msg['end_date']=str(end_date)
        msg['result']=respids
        requests.post( resp_uri, headers={'Content-type': 'application/json', 'Accept': 'text/plain'},
                       data=json.dumps(msg))
        return render_template("end_pyquizz.html")

#  
# The first time the page is loaded, the current question is not set.
# This means that the user has not started to quiz yet. So set the 
# current question to question 1 and save it in the session.
  if "current_question" not in session:
    session["current_question"] = "1"
  
  # If the request is a GET request 
  currentN=int(session["current_question"])   
  currentQ =  questions[session["current_question"]]["question"]
  options = questions[session["current_question"]]["options"] 
  # 
  return render_template('pyquizz.html',num=currentN,ntot=app.nquestions,question=currentQ,opts=options,optrand=randint(1,len(options)))   

	
# Runs the app using the web server on port 80, the standard HTTP port
if __name__ == '__main__':
	app.run( host='0.0.0.0')
    # host="0.0.0.0",
    # port=33507

