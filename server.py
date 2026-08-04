from flask import Flask, render_template
from questions import create_quiz, check_answer, session, redirect, request

app = Flask(__name__)

app.secret_key = "team6"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():

    quiz_list = create_quiz()

    session["quiz_list"] = quiz_list

    session["current_index"] = 0

    session["futoccho_point"] = 0
    session["macho_point"] = 0
    session["miss_count"] = 0

    return redirect("/quiz")

@app.route("/quiz")
def quiz():
    quiz_list = session["quiz_list"]

    question = quiz_list[session["current_index"]]

    return render_template(
        "quiz.html",
        question=question
    )

@app.route("/answer", methods=["POST"])
def answer():

    user_answer = request.form["answer"]

    quiz_list = session["quiz_list"]

    current_index = session["current_index"]

    result = check_answer(question, user_answer)

    

    session["current_index"] += 1

    if session["current_index"] >= 6:
        return redirect("/result")

    return redirect("/quiz")

@app.route("/result")
def result():
    
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)