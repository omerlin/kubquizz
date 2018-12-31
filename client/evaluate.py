import requests
import json

class Student:
    def __init__(self, email):
        self.ident=email
        self.eval_note=0
        self.techno=None
        self.quizz_value=0
    def __repr__(self):
        return 'student: {},techno: {}, quizz: {}, note: {}'.format(self.ident,self.techno,self.quizz_value,self.eval_note)
    def to_csv(self):
        return '{},{},{},{}'.format(self.ident,self.techno,self.quizz_value,self.eval_note)

def check_ok(resp):
    count=0
    quizzok = {'1':'1', '2':'2', '3':'1', '4':'2', '5':'4', '6':'1', '7':'4', '8':'2', '9':'2', '10':'3', '11':'2', '12':'3', '13':'3'}
    for k,v in resp.items():
        if quizzok[k] == v:
            count+=1
    return count

def check_techno( environment ):
    if 'WINDIR' in environment:
        # print ('Python on windows')
        return 'python'
    # There are probably better criteria ...
    if 'HOSTNAME' in environment:
        try:
            if environment['HOSTNAME'].startswith('quizz-deployment'):
                return 'gcp'
            if environment['HOSTNAME'].startswith('cliquizz'):
                return 'minikube'
            if len(environment['HOSTNAME'])==12 and int(environment['HOSTNAME'],16):
                return 'docker'
        except:
            pass
    # probably some trials
    return 'notfound'

def evaluate_responses(uri):
    # The minimum note per technology used
    base_note={'python':7,'docker':9,'minikube':12,'gcp':12}
    # Count technology usage
    techno_used={'python':0,'docker':0,'minikube':0,'gcp':0, 'notfound':0}
    # Get the examination data stored on Redis
    r = requests.get('{}/srv/data'.format(uri))
    # Store the data to file system (just in case of)
    open('/tmp/isen_kubernetes_data.json','w').write(str(r.json))

    # Evaluate to a Python dictionary
    resp=eval(json.dumps(r.json()))
    
    # analyze the response
    students=[]
    for k,v in resp.items(): 
        curr_student = Student(k)
        r = eval(v)
        if isinstance(r,dict):
            curr_student.quizz_value = check_ok(r['result'])
            curr_student.techno = check_techno(eval(r['env']))
            techno_used[curr_student.techno]+=1
            if curr_student.techno != 'notfound':
                curr_student.eval_note =  base_note[curr_student.techno] + round(int(curr_student.quizz_value)/13*7)
                students.append( curr_student)
    print('Nb students: {}'.format(len(students)))
    print(techno_used)
    fp=open('/tmp/m2_virtualization_notes.txt','w')
    for student in students:
        print( student ) 
        fp.write(student.to_csv()+'\n')
    fp.close()


if __name__ == '__main__':
    evaluate_responses('http://quizz.cossme.pw')