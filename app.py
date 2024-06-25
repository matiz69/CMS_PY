from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False)
    addit_info = db.Column(db.String, nullable=True)


class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    target_status = db.Column(db.Integer, nullable=True)
    phone_num = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __init__(self, date, time):
        self.date = date
        self.time = time



@app.route('/')
def home():
    company_list = Company.query.all()
    meeting_list = Meeting.query.all()
    return render_template('base.html', company_list=company_list, meeting_list=meeting_list)

@app.route('/add_company', methods=["POST"])
def add_company():
    company_name = request.form.get("company_name")
    company_phone = request.form.get("company_phone")
    company_addinfo = request.form.get("company_addinfo")
    new_company = Company(name=company_name, phone_num=company_phone, status=0, addit_info=company_addinfo)
    db.session.add(new_company)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update_status/<int:company_id>")
def update_status(company_id):
    company = Company.query.filter_by(id=company_id).first()
    company.status += 1
    db.session.commit()
    return redirect(url_for("home"))





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

