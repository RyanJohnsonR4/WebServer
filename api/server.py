#!/usr/bin/python
#from flask import Flask
from flask import Flask, jsonify, request, redirect, current_app, json, abort
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
def add_notes():
    if not request.json or not 'title' in request.json:
        abort(400)
    reminder = {
        'id': uuid.uuid4(),
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'completed': False,
        'date_due': request.json.get('date_due', "")
    }
    reminders.append(reminder)
    #for i in range(len(attributes)):
        #if(reminders[len(reminders)-1][attributes[i]]):
            #reminders[len(reminders)-1].update({attributes[i]:None})      #Assign a None value to all required attributes (except title)
    updateIDs()
    return jsonify({'reminder': reminder}), 201

@app.route('/api/v2/edit-note/<int:uid>', methods=['PUT'])
def edit_notes(uid):
    reminder= [reminder for reminder in reminders if reminder['id']==uid]
    if len(reminder) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    reminder[0]['title'] = request.json.get('title', reminder[0]['title'])
    reminder[0]['description'] = request.json.get('description', reminder[0]['description'])
    reminder[0]['done'] = request.json.get('done', reminder[0]['done'])
    return jsonify({'reminder': reminder[0]})

@app.route('/api/v2/delete-note/<int:uid>', methods=['DELETE'])
def delete_note(uid):
    reminder= [reminder for reminder in reminders if reminder['id']==uid]
    if len(reminder)==0:
        abort(404)
    reminders.remove(reminder[0])
    return jsonify({'result':True})

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
