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


@app.route("/secret-invite")
def show_secret_invite():
    if session.get("entered-pin", False):
        return render_template("invite.html")
    else:
        return redirect("/login-form")


@app.route("/login-form")
def show_login_form():
    return render_template("login-form.html")


@app.route("/login")
def verify_secret_code():
    SECRET = "chickenz_are_gre8"
    entered_code = request.args["secret_code"]
    if entered_code == SECRET:
        session["entered-pin"] = True
        return redirect("/secret-invite")
    else:
        return redirect("/login-form")
