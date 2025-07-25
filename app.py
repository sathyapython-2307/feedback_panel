from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    new_feedback = Feedback(name=data['name'], message=data['message'])
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'Thank you for your feedback!'})

@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    data = [{'name': fb.name, 'message': fb.message, 'time': fb.created_at.strftime("%Y-%m-%d %H:%M:%S")} for fb in feedbacks]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
