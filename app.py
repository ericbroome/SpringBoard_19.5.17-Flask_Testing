from flask import Flask, redirect, render_template, request, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
debug = DebugToolbarExtension(app)
game = Boggle()

def reset():
    session.clear()
    session['board'] = [[]]
    session['highscore'] = {"score": 0, "plays": 0}
    session['score'] = 0
    session['plays'] = 0
    session['words'] = []

@app.route('/', methods=["GET"])
@app.route('/<action>', methods=["POST"])
def home(action=''):
    """
        Show a home page where a game can be configured then launched.
        If <action> == 'play' then launch game
        If <action> == 'reset' then reset session data
        If <action> == 'end' then end the game and return to start screen
    """
    if action == 'play':
        # Create the board given a width from the start page
        board = game.make_board(width = int(request.form['config']))
        session['board'] = board

        # Ensure that the highscore session variable exists
        highscore = session.get("highscore", {"score": 0, "plays": 0})
        session['highscore'] = highscore

        # Set score and plays to 0 for a new game
        session['score'] = 0
        session['plays'] = 0

        # Words are stored in the session as key->value where the word is the key and the value is the score
        session['words'] = []

        return render_template("game.html", session=session)
    elif action =='end':
        if session['score'] > session['highscore']['score']:
            session['highscore']['score'] = session['score']
            session['highscore']['plays'] = session['plays']
            session.modified = True
            return jsonify({"highscore":{"score":session['highscore']['score'], "plays":session['highscore']['plays']}, "message":"You have made a new high score"})
        else:
            return redirect("/")
    elif action == 'reset':
        reset()
          
    # Default action in case action was not valid. Just reload the start page.
    return render_template('index.html')
    



@app.route('/add-word', methods=["POST"])
def add_word():
    """If word is in dictionary, score it and add it. Reject duplicate words."""
    try:
        werd = request.json['word']
        werd = str(werd).upper()
    except:
        return jsonify({"word":'', "score":-1, "plays": -1, "message":"Server error - no data or invalid data passed in request"})
    result = game.check_valid_word(session['board'], werd)
    if result == "ok":
        if werd in session['words']:
             return jsonify({"word":werd, "score": 0, "message":"Already played"})
        session['score'] = session['score'] + len(werd)
        session['plays'] = session['plays'] + 1
        words = list(session['words'])
        words.append(werd)
        session['words'] = words
        return jsonify({"word":werd, "score":len(werd), "message":"ok"})
    return jsonify({"word":werd, "score": 0, "message":result})
