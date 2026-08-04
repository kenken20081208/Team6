import random
# """クイズで使用する問題データ。"""

futoccho_questions = [
    {
        "question": "問題文1",
        "answer": "ふとっちょ",
        "comment": "解説1"
    },
    {
        "question": "問題文2",
        "answer": "ふとっちょ",
        "comment": "解説2"
    },
    {
        "question": "問題文3",
        "answer": "ふとっちょ",
        "comment": "解説3"
    }
]

macho_questions = [
    {
        "question": "問題文1",
        "answer": "マッチョ",
        "comment": "解説1"
    },
    {
        "question": "問題文2",
        "answer": "マッチョ",
        "comment": "解説2"
    },
    {
        "question": "問題文3",
        "answer": "マッチョ",
        "comment": "解説3"
    }
]

def create_quiz():
    futoccho = random.sample(futoccho_questions, 3)

    macho = random.sample(macho_questions, 3)

    quiz_list = futoccho + macho

    random.shuffle(quiz_list)

    return quiz_list

def check_answer(question, user_answer):

    if user_answer == question["answer"]:
        return True

    return False