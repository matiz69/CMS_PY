from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False)
    addit_info = db.Column(db.String, nullable=True)



@app.route('/')
def home():
    return 'hello world'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

