import json
from flask import Flask, request, render_template, redirect, session
import login
import requests
import get_data

app = Flask(__name__)
app.secret_key = 'DelhiisDelhi'
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'userid' not in session:
        return redirect('/login')
    query = "SELECT * FROM Users WHERE userid ='{0}';".format(session["userid"]) 
    data = login.get_info(query)[0]
    Resident_format = get_data.get_Resident_App_format(data[1]).replace("[","").replace("]","")
    Resident_format = Resident_format.split(",")
    App_data = []
    for Appl in Resident_format:
        if 'Motor' in Appl:
            App_data.append(get_data.get_appliance_data(data[1], 'Motors', Appl))
        if 'LED' in Appl:
            App_data.append(get_data.get_appliance_data(data[1], 'LEDs', Appl))
        if 'Buzzer' in Appl:
            App_data.append(get_data.get_appliance_data(data[1], 'Buzzer', Appl))
    Resident_status = get_data.get_Resident_status(data[1]).replace("[","").replace("]","")
    return render_template('index.html', user = data, App_data = App_data, Resident_status = Resident_status, Resident_format = Resident_format)


@app.route('/change_stat/<user_name>/<str>', methods=['GET', 'POST'])
def change_stat(user_name, str):
    headers = {'X-M2M-Origin': 'admin:admin', "Content-Type": "application/json;ty=4"}
    body = {
    "m2m:cin":{
        "lbl":[
            "status"
        ],
        "con": str
    }
}
    link = "http://127.0.0.1:5089/~/in-cse/in-name/Smart-Grid/Users/"+user_name+"/All_status"
    print(link)
    response = requests.post(link,json=body, headers=headers)
    print(response)
    return redirect('/')


@app.route('/health', methods=['GET', 'POST'])
def health():
    query = "SELECT * FROM Users WHERE userid ='{0}';".format(session["userid"]) 
    data = login.get_info(query)[0]
    Resident_format = get_data.get_Resident_App_format(data[1]).replace("[","").replace("]","")
    Resident_format = Resident_format.split(",")
    return render_template("health.html", user = data, Resident_format = Resident_format)


@app.route('/circuits', methods=['GET', 'POST'])
def circuit():
    query = "SELECT * FROM Users WHERE userid ='{0}';".format(session["userid"]) 
    data = login.get_info(query)[0]
    return render_template("circuits.html", user = data)


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    query = "SELECT * FROM Users WHERE userid ='{0}';".format(session["userid"]) 
    data = login.get_info(query)[0]
    return render_template("statistics.html", user = data)


@app.route('/extra', methods=['GET', 'POST'])
def extra():
    query = "SELECT * FROM Users WHERE userid ='{0}';".format(session["userid"]) 
    data = login.get_info(query)[0]
    return render_template("extra.html", user = data)

@app.route('/login', methods=['GET', 'POST'])
def login_fun():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        query = "SELECT * FROM Users WHERE email ='{0}';".format(username) 
        data = login.get_info(query)
        if(data and data[0][3] == password):
            session['userid'] = data[0][0]  
            return redirect("/")
        else:
            return render_template("login.html",error=True)
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)