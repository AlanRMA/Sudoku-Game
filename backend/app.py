from flask import Flask, request, jsonify
from flask_cors import CORS
from sudoku import SudokuBoard

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Permitindo todas as origens para rotas iniciadas com /api/

@app.route('/api/game/', methods=['GET'])
def generate_sudoku():
    n = int(request.args.get('n'))
    if n not in [4, 9]:
        return jsonify({"error": "Invalid value for n. Must be 4 or 9."}), 400

    sudoku_board = SudokuBoard(n)
    sudoku_board.generate_board()

    sudoku_to_play = sudoku_board.get_sudoku_to_play()
    solution = sudoku_board.get_solution()

    return jsonify({
        "sudoku_game": sudoku_to_play,
        "sudoku_solution": solution
    })

if __name__ == '__main__':
    app.run(debug=False)
