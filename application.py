## HOW TO USE THIS APP:
# Start server by setting variables
# export FLASK_APP=application.py
# export FLASK_ENV=development
# flask run

# TODO : Read doc on huggingface summarization pipeline, e.g. what to do
# if the text is very short, maybe don't summarize it if its not longer
# than X words
# TODO : Escape characters


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline

app = Flask(__name__)
# # Create SQL like database in the same directory to store texts
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Text(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(1200))
    summary = db.Column(db.String(120))

    def __repr__(self):
        return f'{self.id} - {self.content}'


@app.route('/')
def index():
    return 'Visit /texts or /texts/&ltid&gt to browse texts and summaries.'


@app.route('/texts')
def get_texts():
    texts = Text.query.all()
    output = [{"ID": text.id,
              "content": text.content,
              "summary": text.summary} for text in texts]
    return jsonify({"texts": output})


@app.route('/texts/<id>', methods=['GET'])
def get_text(id):
    text = Text.query.get_or_404(id)
    print(text)
    data = {"ID": text.id,
            "content": text.content}
    if text.summary != "":
        data["summary"] = text.summary
    return jsonify(data)


@app.route('/texts', methods=['POST'])
def add_text():
    text = Text(content=request.json['text'],
                summary="")
    db.session.add(text)
    db.session.commit()
    return jsonify({'id': text.id})


@app.route('/texts/<id>', methods=['DELETE'])
def delete_text(id):
    text = Text.query.get(id)
    if text is None:
        return {"error": "Text not found"}
    db.session.delete(text)
    db.session.commit()
    return {"message": f"{id} deleted"}

@app.route('/summary/<id>', methods=['GET'])
def summarize_text(id):
    text = Text.query.get_or_404(id)
    if text.summary == "":
        summarizer = pipeline("summarization")
        max_length = len(text.content)
        summary = summarizer(text.content,
                             max_length=max_length,
                             min_length=1)
        text.summary = summary[0]['summary_text']
        db.session.commit()
        return {"summary": text.summary}
    return {"summary": text.summary}
