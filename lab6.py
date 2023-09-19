from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    test = db.relationship('Test', backref='questions')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', backref='answers')

@app.route('/tests', methods=['POST', 'GET'])
def tests():
    if request.method == 'POST':
        data = request.json
        new_test = Test(name=data['name'])
        db.session.add(new_test)
        db.session.commit()
        return jsonify({'message': 'Test created successfully'})

    elif request.method == 'GET':
        tests = Test.query.all()
        test_list = [{'id': test.id, 'name': test.name} for test in tests]
        return jsonify(test_list)

@app.route('/questions', methods=['POST', 'GET'])
def questions():
    if request.method == 'POST':
        data = request.json
        new_question = Question(text=data['text'], test_id=data['test_id'])
        db.session.add(new_question)
        db.session.commit()
        return jsonify({'message': 'Question created successfully'})

    elif request.method == 'GET':
        questions = Question.query.all()
        question_list = [{'id': question.id, 'text': question.text, 'test_id': question.test_id} for question in questions]
        return jsonify(question_list)

@app.route('/answers', methods=['POST', 'GET'])
def answers():
    if request.method == 'POST':
        data = request.json
        new_answer = Answer(text=data['text'], is_correct=data['is_correct'], question_id=data['question_id'])
        db.session.add(new_answer)
        db.session.commit()
        return jsonify({'message': 'Answer created successfully'})

    elif request.method == 'GET':
        answers = Answer.query.all()
        answer_list = [{'id': answer.id, 'text': answer.text, 'is_correct': answer.is_correct, 'question_id': answer.question_id} for answer in answers]
        return jsonify(answer_list)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
