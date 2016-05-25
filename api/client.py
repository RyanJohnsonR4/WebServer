from flask import Flask, jsonify, request, redirect, current_app, render_template, json
import urllib, os, ast, uuid, urllib2
template_dir=os.getcwd()+"/templates/"
app = Flask(__name__,template_folder=template_dir)
serverURL = "http://terrible-dugong-9690.vagrantshare.com"
months = {
    "January":{
        "name":"January",
        "number":1,
        "days":31,
        "startday":6
    },
    "February":{
        "name":"February",
        "number":2,
        "days":29,
        "startday":2
    },
    "March":{
        "name":"March",
        "number":3,
        "days":31,
        "startday":3
    },
    "April":{
        "name":"April",
        "number":4,
        "days":30,
        "startday":6
    },
    "May":{
        "name":"May",
        "number":5,
        "days":31,
        "startday":1
    },
    "June":{
        "name":"June",
        "number":6,
        "days":30,
        "startday":4
    },
    "July":{
        "name":"July",
        "number":7,
        "days":31,
        "startday":6
    },
    "August":{
        "name":"August",
        "number":8,
        "days":31,
        "startday":2
    },
    "September":{
        "name":"September",
        "number":9,
        "days":30,
        "startday":5
    },
    "October":{
        "name":"October",
        "number":10,
        "days":31,
        "startday":7
    },
    "November":{
        "name":"November",
        "number":11,
        "days":30,
        "startday":3
    },
    "December":{
        "name":"December",
        "number":12,
        "days":31,
        "startday":5
    }
}

@app.route('/api/v2/test', methods=['GET','POST'])
def test():
    temp = {
        "title":"Hello?",
        "description":"Is this working?",
        "date_due":"05052016"
    }

    url = "%s/api/v2/add-note" % (serverURL)
    data = json.dumps(temp)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return response

@app.route('/api/v2/calendar', methods=['GET','POST'])
def get_html():
    weekL = []
    month = "May"
    numDays = getMonthInfo(month,"days")
    startDay = getMonthInfo(month,"startday")
    count = 0
    tempList = []
    while count < numDays + startDay:
        if (count % 7 == 0 and count !=0) or count == numDays+startDay-1:
            weekL.append(tempList[:])
            del tempList[:]
        if count+1 >= startDay:
            tempList.append(count-startDay+2)
        else:
            tempList.append(0)
        count+=1
    return(render_template('calendar.html',weekL=weekL,month=month))

def getMonth(i):
        for x in months:
            if months[x]["number"] == i:
                return months[x]["name"]
        return "January"

def getMonthInfo(month, attribute):
        try:
            return months[month][attribute]
        except:
            return None

@app.route('/api/v2/calendar/<date>', methods=['GET','POST'])
def get_new(date):
    if len(date) != 8:
        if date[2:6] == "&gt;":
            monthN = int(date[:2])+1
            if monthN > 12:
                month = getMonth(1)
            else:
                month = getMonth(monthN)
        else:
            if date[2:6] == "&lt;":
                monthN = int(date[:2])-1
                if monthN < 1:
                    month = getMonth(12)
                else:
                    month = getMonth(monthN)
            else:
                month = getMonth(int(date[:2]))
        weekL = []
        numDays = getMonthInfo(month,"days")
        startDay = getMonthInfo(month,"startday")
        count = 0
        tempList = []
        while count < numDays + startDay:
            if (count % 7 == 0 and count !=0) or count == numDays+startDay-1:
                weekL.append(tempList[:])
                del tempList[:]
            if count+1 >= startDay:
                tempList.append(count-startDay+2)
            else:
                tempList.append(0)
            count+=1
        return(render_template('calendar.html',weekL=weekL,month=month))
    else:
        var1 = '%s/api/v2/attribute-filter/date_due/' % (serverURL) +str(date)+'?'
        var2 = (urllib.urlopen(var1).read())
        print(str(var2))
        response = json.loads(var2)
        return render_template("reminders.html",reminderL=response)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8888, debug=True)
