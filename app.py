from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)

app.debug = True
app.secret_key="anystringhere"

#toolbar = DebugToolbarExtension(app)

high_score = 0

#Declare the array
#for some reason this breaks things if I don't
#assign a board to it.  Can't use an empty array.
#boggle_game.board = boggle_game.make_board()
#board_logical = boggle_game.make_board()

# #for debugging
# print ("Original board initialization")
# for i in  range(5):
#     print(boggle_game.board[i])


@app.route("/boggle")
def serve_boggle():
    """this is the view that the user goes to start a new game"""
    if session.get('games') is None:
        session['games'] = 0

    boggle_game.board = boggle_game.make_board()
    #board_logical = boggle_game.make_board()

    #for debugging
    print("resetting board")                     #for debugging
    for i in  range(5):
        print(boggle_game.board[i])

    session["board_logical"] = boggle_game.board
    session["points"] = 0

    return render_template("board.html")


@app.route("/boggle/play", methods = ["POST"])
def check_word():
    """This view checks submitted words and sends back json resonses"""

    found_words = []

    #for debugging
    print("cofirming board:")
    for i in  range(5):
        print(boggle_game.board[i])

    word = request.json["word"]

    # import pdb
    # pdb.set_trace()

    if word in found_words:
        return jsonify(result="already-found")

    elif word:
        reply = boggle_game.check_valid_word(boggle_game.board, word)
        print(reply)
        found_words.append(word)
        if reply == "ok":
            print("session points: " + str(session["points"]))
            print("adding points")
            session["points"] = session["points"] + len(word)
            print("session points: " + str(session["points"]))
        return jsonify(result=reply, points=session["points"])
        
    else:
         return jsonify(result="not-word")


@app.route("/boggle/done", methods = ["POST"])
def update_stats():
    """This view records game statistics"""

    if request.json['stats'] == 'game complete':
        print("points: ")
        print(session.get('points'))
        session['games'] += 1
        
        #This was a huge problem without the
        #global keyword
        #what in the actual F?
        global high_score
        if session.get('points') > high_score:
            print("The highscore: " + str(high_score))
            high_score = session.get('points')
            session["hscore"] = high_score
            return jsonify(new_hscore='true',hscore=high_score,games=session['games'])
        else:
            print("must not be any points") 
            return jsonify(new_hscore='false',hscore=high_score,games=session['games'])



