import requests
import json


def check_ok(resp):
    count=0
    quizzok = {'1':'1', '2':'2', '3':'1', '4':'2', '5':'4', '6':'1', '7':'4', '8':'2', '9':'2', '10':'3', '11':'2', '12':'3', '13':'3'}
    for k,v in resp.items():
        if quizzok[k] == v:
            count+=1
    return count

def evaluate_responses(uri):
    r = requests.get('{}/srv/data'.format(uri))
    resp=eval(json.dumps(r.json()))
    #print (resp)
    #print (type(resp))
    # backup data
    ###open('c:\\temp\\resp.json','w').write(str(resp))
    for k,v in resp.items(): 
        r = eval(v)
        if isinstance(r,dict):
            print ( 'user: {}, quizz eval={}'.format(k,check_ok(r['result'])))
            #print ( r['result'])
        #print (type(eval(v)))

if __name__ == '__main__':
    evaluate_responses('http://quizz.cossme.pw')