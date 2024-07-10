import time

from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False, default=0)
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

#Archive of closed companies- that reached status nr 5.
class Archived_Company(db.Model):
    __tablename__ = 'archived_company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False)
    addit_info = db.Column(db.String, nullable=True)
    close_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def home():
    company_list = Company.query.all()
    meeting_list = Meeting.query.all()

    # Sprawdź czy istnieją jakiekolwiek firmy w bazie danych
    if not company_list:
        show_status_message = False
    else:
        show_status_message = request.args.get('show_status_message', '').lower() in ['true', '1', 't', 'y', 'yes']
        invalid_data = request.args.get('invalid_data', '').lower() in ['true', '1', 't', 'y', 'yes']
    return render_template('base.html',
                           company_list=company_list,
                           meeting_list=meeting_list,
                           show_status_message=show_status_message,
                           invalid_data=invalid_data)


@app.route('/add_company', methods=["POST"])
def add_company():
    invalid_data = False
    company_name = request.form.get("company_name")
    company_phone = request.form.get("company_phone")
    company_addinfo = request.form.get("company_addinfo")
    if company_name != "" and company_phone != "" and len(company_phone) > 8 \
            and company_phone.isdigit() == True:
        new_company = Company(name=company_name, phone_num=company_phone, status=0, addit_info=company_addinfo)
        db.session.add(new_company)
        db.session.commit()
    else:
        invalid_data = True
    return redirect(url_for("home", invalid_data=invalid_data))

@app.route("/update_status/<int:company_id>")
def update_status(company_id):
    company = Company.query.filter_by(id=company_id).first()
    show_status_message = False
    if company.status < 5:
        company.status += 1
    else:
        show_status_message = True
    db.session.commit()
    return redirect(url_for("home", show_status_message=show_status_message))

@app.route("/archive this company/<int:company_id>")
def archive_company(company_id):
    to_archive = Company.query.filter_by(id=company_id).first()
    new_archived_comp = Archived_Company(name=to_archive.name,
                                        phone_num=to_archive.phone_num,
                                        status=to_archive.status,
                                        addit_info=to_archive.addit_info,
                                        close_date=datetime.utcnow())
    db.session.delete(to_archive)
    db.session.add(new_archived_comp)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

