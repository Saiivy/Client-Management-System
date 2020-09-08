from pyrebase import pyrebase
from flask import Flask, render_template, request, redirect,url_for


app = Flask(__name__)
firebaseConfig = {
   "apiKey": "AIzaSyAcIpjd8obUhGrvpsGDDSFFrkquv-5WpiU",
    "authDomain": "officedatabase-86859.firebaseapp.com",
    "databaseURL": "https://officedatabase-86859.firebaseio.com",
    "projectId": "officedatabase-86859",
    "storageBucket": "officedatabase-86859.appspot.com",
    "messagingSenderId": "593707442957",
    "appId": "1:593707442957:web:eebe088a96a5c377a60644"
  }

client={}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

#global variables
totalClients=0
inCompleteDeals=0
completeDeals=0
inProgressDeals=0
count = 0

keyValueDatabase=""
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/checkExisting")
def checkExisting():
  return render_template("Dashboard.html")

@app.route("/form")
def form():
  return render_template("ClientDetailsForm.html")
    
@app.route("/formProcessor",methods=['GET', 'POST'])
def processForm():
    #get from form
    name = request.form.get('firstname')
    email = request.form.get('email')
    rmai = request.form.get('rmai')
    phone = request.form.get('phone')
    notes = request.form.get('notes')
    reference = request.form.get('reference')
    purpose = request.form.get('purpose')
    status = request.form.get('status')
    
    client={
        "a":name,
        "b":phone,
        "c":rmai,
        "d":reference,
        "e":purpose,
        "f":email,
        "g":status,
        "h":notes
        
        
    }
    
    
    
    #push to database
    db.child("client").push(client)

    
    #read from database
    global dataDb
    dataDb=db.child("client").get().val()
    
    #count number of complete deals
    for k,v in dataDb.items():
       for key,value in v.items():
           if value=="complete":
             global completeDeals
             global count
             completeDeals+1
    
   #count number of Incomplete deals
    for k,v in dataDb.items():
       for key,value in v.items():
           if value=="Incomplete":
             global inCompleteDeals
             
    #count number of inProgress deals
    for k,v in dataDb.items():
       for key,value in v.items():
           if value=="Inprogress":
             global inProgressDeals
              
    #counting number of rows
    countClients=len(dataDb)
    
    #render next page
    return render_template("Dashboard.html",dataDb=dataDb,countClients=countClients,completeDeals=completeDeals,inProgressDeals=inProgressDeals,inCompleteDeals=inCompleteDeals)
    
    #using this method, we will update database data..
@app.route('/deleteData/<string:keyValue>', methods=['GET', 'POST'])
def deleteData(keyValue):
    db.child("client").child(keyValue).remove()
    global dataDb
    return redirect(url_for("processForm"))
  
@app.route('/getdata/<string:keyValue>', methods=['GET', 'POST'])
def getdata(keyValue):    
   updateDataDb= db.child("client").child(keyValue).get().val()
   global keyValueDatabase
   keyValueDatabase=keyValue
   return render_template("ClientDetailsUpdate.html",updateDataDb=updateDataDb)
        
#this method will let us edit the client data
@app.route("/updateData",methods=['GET', 'POST'])
def updateData():
   #get from form
    name = request.form.get('name')
    email = request.form.get('email')
    rmai = request.form.get('rmai')
    phone = request.form.get('phone')
    notes = request.form.get('notes')
    reference = request.form.get('reference')
    purpose = request.form.get('purpose')
    status = request.form.get('status')
    
    client={
        "a":name,
        "b":phone,
        "c":rmai,
        "d":reference,
        "e":purpose,
        "f":email,
        "g":status,
        "h":notes
        
        
    }
    db.child("client").child(keyValueDatabase).update(client)
    return redirect(url_for("processForm"))
  