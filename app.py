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

@app.route('/api/get_notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    all_notes = []
    for note in notes:
        single_note={
            "id":note.id,
            "title":note.title,
            "content":note.content
            }
        all_notes.append(single_note)
        print(all_notes)
        return jsonify({"notes":all_notes})
    print(notes)
    return "api to get all data"
    

@app.route('/api/note/<int:id>', methods=['GET'])
def get_note(id):  # sourcery skip: use-named-expression
    note = Note.query.get(id)
    if note:
        single_note = {
            "id": note.id,
            "title": note.title,
            "content": note.content
            }
        return jsonify(single_note)
    else:
        return jsonify({"error": "Note not found"})


@app.route('/api/note/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"Message":"Note deleted successfully"})
    else:
        return jsonify({"error": "Note not found"})
    


@app.route('/api/note/<int:id>', methods=['GET', 'POST'])
def update_note(id):
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches, switch
    note = Note.query.get(id)
    if note:
        if request.method == 'POST':
            note.title = request.json.get('title', note.title)  
            note.content = request.json.get('content', note.content)  
            db.session.commit()
            return jsonify({"message": "Note updated successfully"})
        
        elif request.method == 'GET':
            single_note = {
                "id": note.id,
                "title": note.title,
                "content": note.content
            }
            return jsonify(single_note), 
    else:
        return jsonify({"error": "Note not found"})


if __name__ == '__main__':
    app.run(debug=True)