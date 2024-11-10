from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app =  Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable tracking modifications

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(120), unique=True, nullable=False)
    
@app.route('/', methods=['GET'])
def home():
    return jsonify({"Message":"hello world"})




if __name__ == '__main__':
    app.run(debug=True)