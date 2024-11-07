from flask import Flask, jsonify, request, render_template
from collections import deque

app = Flask(__name__)

highest_scores = deque(maxlen=10)
lowest_scores = deque(maxlen=10)
usernames = {}

@app.route('/')
def index():
    sorted_highest = sorted(highest_scores, key=lambda x: x['score'], reverse=True)
    sorted_lowest = sorted(lowest_scores, key=lambda x: x['score'])
    return render_template('leaderboard.html', highest_scores=sorted_highest, lowest_scores=sorted_lowest)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    global highest_scores, lowest_scores

    data = request.json
    score = data.get('score')
    username = data.get('username')
    
    if score is not None and username:
        score_entry = {"username": username, "score": score}

        if len(highest_scores) < 10 or score > min(highest_scores, key=lambda x: x['score'])['score']:
            if len(highest_scores) == 10:
                highest_scores.remove(min(highest_scores, key=lambda x: x['score']))
            highest_scores.append(score_entry)
            highest_scores = deque(sorted(highest_scores, key=lambda x: x['score'], reverse=True), maxlen=10)

        if len(lowest_scores) < 10 or score < max(lowest_scores, key=lambda x: x['score'])['score']:
            if len(lowest_scores) == 10:
                lowest_scores.remove(max(lowest_scores, key=lambda x: x['score']))
            lowest_scores.append(score_entry)
            lowest_scores = deque(sorted(lowest_scores, key=lambda x: x['score']), maxlen=10)

        return jsonify(success=True, highest=list(highest_scores), lowest=list(lowest_scores)), 200
    return jsonify(success=False), 400

@app.route('/submit_username', methods=['POST'])
def submit_username():
    global usernames
    username = request.json.get('username')

    if username in usernames:
        return jsonify(success=False, message="Username taken. Try another."), 400
    else:
        usernames[username] = True
        return jsonify(success=True), 200

@app.route('/scores', methods=['GET'])
def get_scores():
    return jsonify(highest=list(highest_scores), lowest=list(lowest_scores)), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
