from flask import Flask, render_template, session, redirect, request
from questions import create_quiz, check_answer

app = Flask(__name__)

app.secret_key = "team6"


QUIZ_SESSION_KEYS = (
    "quiz_list",
    "current_index",
    "futoccho_point",
    "macho_point",
    "miss_count",
    "answered_indices",
)


def has_quiz_session():
    return all(key in session for key in QUIZ_SESSION_KEYS)


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
    session["answered_indices"] = []
    session.pop("is_correct", None)

    return redirect("/quiz")

@app.route("/quiz")
def quiz():

    if not has_quiz_session():
        return redirect("/")

    quiz_list = session["quiz_list"]
    current_index = session["current_index"]

    if current_index >= len(quiz_list):
        return redirect("/result")

    question = quiz_list[current_index]

    return render_template(
        "quiz.html",
        question=question,
        question_number=current_index + 1,
        total_questions=len(quiz_list)
    )

@app.route("/answer", methods=["GET", "POST"])
def answer():

    if not has_quiz_session():
        return redirect("/")

    quiz_list = session["quiz_list"]
    current_index = session["current_index"]

    if current_index >= len(quiz_list):
        return redirect("/result")

    if request.method != "POST":
        return redirect("/quiz")

    user_answer = request.form.get("answer")

    if user_answer not in ("ふとっちょ", "マッチョ"):
        return redirect("/quiz")

    if request.form.get("question_number") != str(current_index + 1):
        return redirect("/quiz")

    question = quiz_list[current_index]

    answered_indices = session["answered_indices"]

    if current_index in answered_indices:
        return redirect("/comment")

    result = check_answer(question, user_answer)

    if result:

        if question["answer"] == "ふとっちょ":
            session["futoccho_point"] += 1

        else:
            session["macho_point"] += 1

    else:
        session["miss_count"] += 1

    answered_indices.append(current_index)
    session["answered_indices"] = answered_indices
    session["is_correct"] = result

    return redirect("/comment")

@app.route("/comment")
def comment():

    if not has_quiz_session():
        return redirect("/")

    quiz_list = session["quiz_list"]
    current_index = session["current_index"]

    if current_index >= len(quiz_list):
        return redirect("/result")

    if current_index not in session["answered_indices"]:
        return redirect("/quiz")

    question = quiz_list[current_index]

    return render_template(
        "comment.html",
        question=question,
        is_correct=session.get("is_correct", False)
    )

@app.route("/next", methods=["GET", "POST"])
def next():

    if not has_quiz_session():
        return redirect("/")

    quiz_list = session["quiz_list"]
    current_index = session["current_index"]

    if current_index >= len(quiz_list):
        return redirect("/result")

    if current_index not in session["answered_indices"]:
        return redirect("/quiz")

    if request.method != "POST":
        return redirect("/comment")

    session["current_index"] = current_index + 1

    if session["current_index"] >= len(quiz_list):
        return redirect("/result")

    return redirect("/quiz")

@app.route("/result")
def result():
    if not has_quiz_session():
        return redirect("/")

    quiz_list = session["quiz_list"]
    current_index = session["current_index"]

    if current_index < len(quiz_list):
        if current_index in session["answered_indices"]:
            return redirect("/comment")

        return redirect("/quiz")

    futoccho = session["futoccho_point"]
    macho = session["macho_point"]
    miss = session["miss_count"]
    result_data = {
        "futoccho_point": futoccho,
        "macho_point": macho,
        "total_correct": futoccho + macho,
        "total_questions": len(quiz_list),
    }

    # 全問不正解
    if miss == len(quiz_list):
        return render_template("result_karappo.html", **result_data)

    # ふとっちょマインド
    elif futoccho > macho:
        return render_template("result_futoccho.html", **result_data)

    # マッチョマインド
    elif macho > futoccho:
        return render_template("result_macho.html", **result_data)

    # 同点
    else:
        return render_template("result_balance.html", **result_data)


if __name__ == "__main__":
    app.run(debug=True)
