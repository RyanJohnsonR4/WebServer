#!/usr/bin/python
#from flask import Flask
from flask import Flask, jsonify, request, redirect, current_app, json
import urllib, os, uuid
app = Flask(__name__)

attributes=('id','title','description','completed','date_due') #List of all required attributes a reminder needs
reminders=[
    {
        'id': uuid.uuid4(),
        'title':'Reminder',
        'description': 'You are stupid',
        'completed': False,
        'date_due': '05192016' #mm/dd/yyyy
    },
    {
        'id':uuid.uuid4(),
        'title':'Test 2',
        'description': 'This is a reminder',
        'completed': False,
        'date_due': '05192016' #mm/dd/yyyy
    }
]
unique_ids=[]

def updateIDs():
    for i in unique_ids:
        unique_ids.remove(i)
    for i in reminders:
        unique_ids.append(i['id'])
updateIDs()

@app.route('/api/v2/get-id/<index>', methods=['GET'])
def get_id(index):
    updateIDs()
    return str(unique_ids[int(index)])

#FOR DEBUG ONLY Usually Handled by client
@app.route('/api/v2', methods=['GET'])
def get_notes():
    temp=""
    for i in reminders:
        temp+=i['title']
        temp+="\n"
    return temp

@app.route('/api/v2/add-note', methods=['POST'])
def add_notes(title):
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': uuid.uuid4(),
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'completed': False,
        'date_due': request.json.get('date_due', "")
    }
    reminders.append(task)
    #for i in range(len(attributes)):
        #if(reminders[len(reminders)-1][attributes[i]]):
            #reminders[len(reminders)-1].update({attributes[i]:None})      #Assign a None value to all required attributes (except title)
    updateIDs()
    return jsonify({'task': task}), 201

@app.route('/api/v2/edit-note/<uid>/<attribute>/<value>', methods=['PUT'])
def edit_notes(uid, attribute, value):
    for i in reminders:
        if str(i['id'])==uid:
            try:
                i[attribute]=value
                return "success"
            except:
                return "No such attribute to edit"
    return "No such note"

@app.route('/api/v2/inspect-note/<uid>/<attribute>', methods=['GET'])
def inspect_note(uid, attribute):
    for i in reminders:
        if str(i['id'])==uid:
            try:
                return str(i[attribute])
            except:
                return "No such attribute"
    return "No such note"

@app.route('/api/v2/attribute-filter/<attribute>/<value>', methods=['GET'])
def find_attribute(attribute, value):
    matches=[]
    match=False
    for i in range(len(reminders)):
        if str(reminders[i][attribute])==value:
             matches.append(reminders[i])
             match=True
    if match is True:
        return json.dumps(matches)
    return "No "+str(attribute)+" found with the value "+str(value)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080, debug=True)
