from flask import Flask, render_template, request, jsonify
from ai import get_random_move, get_medium_move, get_best_move

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "This is our Tic Tac Toe game!"

@app.route("/computer-move", methods=["POST"])
def computer_move():
    data = request.get_json()
    board = data.get("board")

    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"error": "Invalid board"}), 400

    if any(cell not in ["", "X", "O"] for cell in board):
        return jsonify({"error": "Invalid board values"}), 400

    difficulty = data.get("difficulty", "easy")

    if difficulty == "impossible":
        move = get_best_move(board)

    elif difficulty == "medium":
        move = get_medium_move(board)

    else:
        move = get_random_move(board)

    return jsonify({"move": move})

if __name__ == "__main__":
    app.run(debug=True, port=5001)