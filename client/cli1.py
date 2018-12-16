import requests
from random import shuffle
q = requests.get('http://localhost:6000/srv/quizz')
print (q.text)
q1=eval(q.text)
shuffle(q1['kubernetes'])
questions={}
for i,k in enumerate(q1):
    questions[str(i)]=k
print (questions)