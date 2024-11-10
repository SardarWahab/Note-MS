from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app =  Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable tracking modifications

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(120), nullable=False)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"Message":"Server is running"})

@app.route('/api/note', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    print(title,content)
    if not title:
        return jsonify({"error": "Title is required"})
    if not content:
        return jsonify({"error": "Content is required"})
    
    new_note = Note(title=title,content=content)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({"Message":"Note created successfully"})



if __name__ == '__main__':
    app.run(debug=True)