from flask import Flask, request, jsonify
from flask_cors import CORS
from clients_hub import build_full_report

app = Flask(__name__)
CORS(app)

@app.route('/analyze',  methods=["GET", "POST"])
def analyze():
    owner = "veiston"
    repo = "Ufotutkija-Pekka"
    board_id = 'Ozbf2TiG'
    
    result = build_full_report(board_id, owner, repo)

    return jsonify(result)
    
# @app.route("/github", methods=["GET"])
# def github():
#     owner = "veiston"
#     repo = "Ufotutkija-Pekka"
    
#     commits = get_github_commits(owner, repo)
#     stats = build_github_stats(commits)
    
#     return jsonify(stats)

# @app.route("/trello", methods=["GET"])
# def trello():
#     board_id = 'Ozbf2TiG'
    
#     stats = build_trello_stats(board_id)
    
#     return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
