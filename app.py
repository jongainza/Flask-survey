from flask import Flask, request, render_template, redirect, flash, jsonify, session
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
print("hi")

app.config["SECRET_KEY"] = "chickenzarecool"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.route("/")
def survey_intructions():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("welcome.html", title=title, instructions=instructions)


@app.route("/questions", methods=["POST"])
def beggan():
    session[RESPONSES_KEY] = []
    return redirect("questions/0")


@app.route("/questions/<int:n>")
def questions(n):
    responses = session.get(RESPONSES_KEY)

    if responses == None:
        return redirect("/")
    if len(responses) != n:
        flash(f"Invalid question number: {n}")
        return redirect(f"/questions/{len(responses)}")
    if len(responses) == len(satisfaction_survey.questions):
        flash("Survey Completed")
        return redirect("/thankyou")

    question = satisfaction_survey.questions[n]
    return render_template("questions.html", question_num=n, question=question)


@app.route("/answer", methods=["POST"])
def answer():
    choice = request.form["answer"]
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(satisfaction_survey.questions):
        flash("Survey Completed")
        return redirect("/thankyou")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")
