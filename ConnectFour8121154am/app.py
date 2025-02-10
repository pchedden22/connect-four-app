from flask import Flask, render_template, request, jsonify
from connectFour import ConnectFour

app = Flask(__name__)

games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET'])
def game():
    rows = int(request.args.get('rows', 6))
    columns = int(request.args.get('columns', 7))
    win_length = int(request.args.get('win_length', 4))
    difficulty = request.args.get('difficulty')
    game_id = f"{rows}x{columns}x{win_length}x{difficulty}"
    games[game_id] = {'game': ConnectFour(rows, columns, win_length), 'difficulty': difficulty}
    return render_template('game.html', rows=rows, columns=columns, win_length=win_length, game_id=game_id, difficulty=difficulty)

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    game_id = data['game_id']
    column = data['column']
    game_data = games[game_id]
    game = game_data['game']
    difficulty = game_data['difficulty']
    success = game.drop_piece(column)
    board = game.board
    winner = game.winner
    tie = game.tie

    ai_move = None
    if success and not winner and not tie:
        ai_move = game.apply_ai_move(difficulty)
        board = game.board
        winner = game.winner
        tie = game.tie

    return jsonify({'success': success, 'board': board, 'winner': winner, 'tie': tie, 'ai_move': ai_move})

if __name__ == '__main__':
    app.run(debug=True)
