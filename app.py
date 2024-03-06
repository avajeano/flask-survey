from flask import Flask, render_template, request, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

# # the toolbar is only enabled in debug mode:
# app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'your_secret_key'

# debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def home_page():
    return render_template('home.html', survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():
    """start with no responses"""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def save_answer():
    """save answer and go to next question"""
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    #redirects the user based on where they are in the survey
    if (len(responses) == len(survey.questions)):
        return redirect('/thank_you')
    else:
        return redirect (f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect('/thank_you')
    
    if (len(responses) != qid):
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route('/thank_you')
def thank_you():
    return render_template("thank_you.html")