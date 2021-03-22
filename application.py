import datetime
from random import randint
from flask import *
from flask_mail import Mail, Message
from flask import Flask, request, render_template
import mysql.connector
from filter import Filter
from Stats import Stat
from price import price
import crops
from xbgt_test import XgbtTest
from Rf_test import RFTest
from flask import jsonify, make_response
import math

application = app = Flask(__name__, template_folder='template')
app.secret_key = 'the random string'
mail = Mail(app)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'ronshawn29@gmail.com'
app.config['MAIL_PASSWORD'] = 'ViS29@@@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)

mydb = mysql.connector.connect(
    host="agri.cj9kv3v4akuv.us-east-2.rds.amazonaws.com",
    user="inferno",
    password="vishal2942",
    database="useragri"
)
vars = []

otps = {

    "otp2": otp,
}


@app.route('/')
def root():
    return render_template('login.html')


@app.route('/suggestedcrops', methods=["POST"])
def suggestedcrops():
    state = request.form['state']
    crops = Filter()
    crops = crops.findCrops(state)
    return render_template("filtered.html", crops=crops)


@app.route('/register')
def register():
    return render_template('register.html', otps=otps)


@app.route('/cropsuggest')
def cropsuggestt():
    return render_template('cropsuggest.html', otps=otps)


@app.route('/success', methods=["POST"])
def success():
    email1 = request.form["email"]
    pass1 = request.form["password"]
    print(email1, pass1)

    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM login WHERE email = %s AND password = %s', (email1, pass1,))
    checkUsername = mycursor.fetchone()
    print(checkUsername)
    if checkUsername != None:
        return render_template('cropsuggest.html')
    else:
        return "<h1>No Matching User Found</h1>"


@app.route('/success1', methods=["POST"])
def success1():
    email2 = request.get_data().decode("utf-8")

    print(email2)
    msg = Message('OTP', sender='username@gmail.com', recipients=[email2])
    msg.body = str(otp)
    mail.send(msg)


@app.route('/validate', methods=["POST"])
def validate():
    if request.method == 'POST':

        data = request.get_data().decode("utf-8")
        str = ""
        i = 0
        for i in range(len(data)):
            if data[i] == '|':
                vars.append(str)
                str = ""
                continue
            str += data[i]


@app.route('/verified', methods=["POST"])
def verfied():
    global vars
    mycursor = mydb.cursor()
    mycursor.execute("""INSERT INTO login values(%s,%s,%s)""", (vars[0], vars[2], vars[1]))
    mydb.commit()
    vars = []
    return render_template("login.html")


@app.route('/resetpass', methods=['POST'])
def resetpass():
    cemail = request.get_data().decode("utf-8")
    print(cemail)

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM login WHERE email = %s', (cemail,))
    checkusername = mycursor.fetchone()
    print(checkusername)

    if (checkusername != None):
        # mycursor.execute('UPDATE login SET password = %s,WHERE email=%s',(cpass,cemail,))
        mycursor.execute('SELECT password FROM login WHERE email = %s', (cemail,))
        check1 = mycursor.fetchone()

        msg = Message('OTP', sender='username@gmail.com', recipients=[cemail])
        msg.body = str(check1[0])
        mail.send(msg)

        a = 1;


    else:
        return "<h1>Email not found</h1>"


@app.route('/index')
def index():
    states = Filter()
    states = states.findStates()
    seasons = Filter()
    seasons = seasons.findSeason()
    # districts = Filter()
    # districts = districts.findDistrict()
    return render_template('input.html', states=states, seasons=seasons)


@app.route('/predict', methods=["POST"])
def predict():
    rainfall = float(request.form['rainfall'])
    temperature = float(request.form['temperature'])
    ph = float(request.form['ph'])
    area = float(request.form['area'])
    area = area * 0.000404686
    state = request.form['state']
    season = request.form['season']
    district = request.form['district']
    season = season.strip()
    print(state)
    print(season,"Hii")
    print(temperature, rainfall, ph, area, season)
    model = XgbtTest()
    crop = model.xgbt_Predict(rainfall, temperature, ph)
    #
    model = RFTest()
    yeild = model.RF_Predict(state, crop, season, district, area)

    return render_template("result.html", result=crop, yeild=yeild)


# @app.context_processor
@app.route('/index1', methods=['POST', 'GET'])
def index1():
    global text


@app.route('/send')
def add_numbers():
    dis3 = Filter()
    dis3 = dis3.findDistrict()
    # dis1 = {
    #     "Andaman and Nicobar Islands": ['NICOBARS', 'NORTH AND MIDDLE ANDAMAN', 'SOUTH ANDAMANS'],
    #     "Andhra Pradesh": ['ANANTAPUR', 'CHITTOOR', 'EAST GODAVARI', 'GUNTUR', 'KADAPA', 'KRISHNA',
    #                        'KURNOOL', 'PRAKASAM', 'SPSR NELLORE', 'SRIKAKULAM', 'VISAKHAPATANAM'
    #         , 'VIZIANAGARAM', 'WEST GODAVARI'],
    #     "Arunachal Pradesh": ['ANJAW', 'CHANGLANG', 'DIBANG VALLEY', 'EAST KAMENG', 'EAST SIANG',
    #                           'KURUNG KUMEY', 'LOHIT', 'LONGDING', 'LOWER DIBANG VALLEY', 'LOWER SUBANSIRI'
    #         , 'NAMSAI', 'PAPUM PARE', 'TAWANG', 'TIRAP', 'UPPER SIANG', 'UPPER SUBANSIRI',
    #                           'WEST KAMENG', 'WEST SIANG'],
    #     "Assam": ['BAKSA', 'BARPETA', 'BONGAIGAON', 'CACHAR', 'CHIRANG', 'DARRANG', 'DHEMAJI',
    #               'DHUBRI', 'DIBRUGARH', 'DIMA HASAO', 'GOALPARA', 'GOLAGHAT', 'HAILAKANDI',
    #               'JORHAT', 'KAMRUP', 'KAMRUP METRO', 'KARBI ANGLONG', 'KARIMGANJ', 'KOKRAJHAR',
    #               'LAKHIMPUR', 'MARIGAON', 'NAGAON', 'NALBARI', 'SIVASAGAR', 'SONITPUR',
    #               'TINSUKIA', 'UDALGURI']
    # }

    return jsonify(result=dis3)


@app.route('/stats')
def stats():
    crops = ['Wheat', 'Paddy', 'Barley', 'Groundnut', 'Cotton', 'Coconut',
             'Maize', 'Soyabean', 'Moong', 'Bajra', 'Chillies', 'Gram', 'Jowar', 'Potato'
        , 'Peas', 'Sugarcane', 'Turmeric', 'Onion']
    n = len(crops)
    num = n // 6 + math.ceil(n // 6 - n / 6)
    a = n // 6
    b = [[]]
    for i in range(num):
        if i == num - 1:
            b.append(range(n % 6))
        else:
            b.append(range(6))
    if num == 1:
        pass
    else:
        num = num + 1
    param = {
        'size': 6,
        'range1': range(num),
        'range': range(6),
        'names': crops,
        'range2': range(1),
        'cnt': n

    }
    return render_template("stats.html", param=param)


pr = price()


@app.route('/stats/<name>')
def statview(name):
    param = {
        'name': name,
        'range1': range(2),
        'range': range(6)

    }

    cur_price = pr.cur_price(name)
    max_price, min_price, full_year = pr.priceyear(name)
    prev_year = pr.prevyear(name)
    crop_d = crops.cropss(name)
    x_cord = [i[0] for i in full_year]
    y_cord = [i[1] for i in full_year]
    p_x_cord = [i[0] for i in prev_year]
    p_y_cord = [i[1] for i in prev_year]

    crops_dat = {
        "name": name,
        "cur_price": cur_price,
        "exports": crop_d[2],
        "Majorl": crop_d[0],
        "season": crop_d[1],
        "max_p": max_price,
        "min_p": min_price,
        "full_year": full_year,
        "x_cord": x_cord,
        "y_cord": y_cord,
        "p_x_cord": p_x_cord,
        "p_y_cord": p_y_cord
    }
    return render_template("statview.html", param=param, crops_dat=crops_dat)


@app.route('/trend')
def trend():
    top = pr.firstfive()
    bot = pr.bottomfive()
    topyear = pr.yeartopfive()

    data1 = {

        "top": top,
        "bot": bot,
        "topyear":topyear

    }
    return render_template("/trend.html", data1=data1)

app.run(host='127.0.0.1', port=4000, debug=True)
