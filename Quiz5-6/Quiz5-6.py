from flask import Flask,render_template, url_for, session, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'avko'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Alta.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Product_Name = db.Column(db.String(60), nullable=False)
    Price = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return "მოდელი: {},   ფასი: {}".format(self.Product_Name, self.Price)



@app.route('/')
def home():
    all_Phones = Data.query.all()
    return render_template('homepage.html', allphones=all_Phones)



@app.route('/AddPhone', methods=['POST', 'GET'])
def addphone():

    if request.method == 'POST':
        phone_name = request.form['Pname']
        phone_price = request.form['Pprice']
        if phone_name == "" or  phone_price == "":
            flash("გთხოვთ შეავსოთ ყველა ველი", "error")
        elif not phone_price.isnumeric():
            flash("გთხოვთ ფასი შეიყვანოთ მხოლოდ რიცხვებით", "error")
        else:
            session['pname'] = phone_name
            session['pprice'] = phone_price
            phone = Data(Product_Name=phone_name, Price=phone_price)
            db.session.add(phone)
            db.session.commit()
            flash("მოდელი დამატებულია", "info")

    return render_template('Addphone.html')


@app.route('/about')
def about():
    return render_template("aboutus.html")


@app.route('/Login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username_name = request.form['uname']
        username_pass = request.form['psw']
        if username_name == "" or username_pass == "":
            flash("Please Fill All Fields", "error")
        else:
            session['name'] = username_name
            session['pass'] = username_pass
            return redirect(url_for("home"))

    return render_template("Login.html")


@app.route('/Logout')
def logout():
    session.pop('name', None)
    session.pop('pass', None)
    return render_template("Logout.html")



app.run(debug=True)
