from flask import Flask
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
    status = db.Column(db.Integer(10), nullable=False)
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
    return 'hello world'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

