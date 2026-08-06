from flask import Flask, render_template, session, redirect, request
from questions import create_quiz, check_answer

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

    if "quiz_list" not in session:
        return redirect("/")

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

    question = quiz_list[current_index]

    result = check_answer(question, user_answer)

    if result:

        if question["answer"] == "ふとっちょ":
            session["futoccho_point"] += 1

        else:
            session["macho_point"] += 1

    else:
        session["miss_count"] += 1

    session["is_correct"] = result

    return redirect("/comment")

@app.route("/comment")
def comment():

    quiz_list = session["quiz_list"]

    current_index = session["current_index"]

    question = quiz_list[current_index]

    return render_template(
        "comment.html",
        question=question
    )

@app.route("/next", methods=["POST"])
def next():

    session["current_index"] += 1

    if session["current_index"] >= 6:
        return redirect("/result")

    return redirect("/quiz")

@app.route("/result")
def result():
    futoccho = session["futoccho_point"]
    macho = session["macho_point"]
    miss = session["miss_count"]

    # 全問不正解
    if miss == 6:
        return render_template("result_karappo.html")

    # ふとっちょマインド
    elif futoccho > macho:
        return render_template("result_futoccho.html")

    # マッチョマインド
    elif macho > futoccho:
        return render_template("result_macho.html")

    # 同点
    else:
        return render_template("result_balance.html")


if __name__ == "__main__":
    app.run(debug=True)