from flask import Flask, render_template, jsonify, request
from apps.Asian210CreativeProject.tools.timeline_json import get_timeline_json, update_timeline_json
from apps.Asian210CreativeProject.tools.quiz_questions import generate_quiz_questions

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/timelineAdder")
def timeline_adder():
    return render_template("timelineContentAdder.html")

@app.route("/timelineQuiz")
def timeline_quiz():
    return render_template("timelineQuiz.html")

@app.route("/getTimelineJson", methods=["GET"])
def get_timeline_json_req():
    print(get_timeline_json())
    return jsonify(get_timeline_json())

@app.route("/updateTimelineJson", methods=["POST"])
def update_timeline_json_req():
    update_timeline_json(request.form)
    
    return {"status": "success"}

@app.route("/getQuizQuestions", methods=['GET'])
def get_quiz_questions_req():
    return generate_quiz_questions(10)

if __name__ == '__main__':
    app.run(debug=True)