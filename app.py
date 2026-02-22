from flask import Flask, render_template, jsonify, request, session
from decision_tree import build_decision_tree, find_node_by_id
import uuid

app = Flask(__name__)
app.secret_key = 'gen_z_secret_key_skibidi_toilet' # Keep it fun based on prompt style, though "gen-z" implies modern slang :P

# Store the tree in memory (it's static)
TREE_ROOT = build_decision_tree()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/simulate')
def simulate_page():
    return render_template('simulate.html')

# API ENDPOINTS

@app.route('/api/start', methods=['POST'])
def start_game():
    session['current_node_id'] = TREE_ROOT.id
    session['path'] = [] # List of questions asked
    session['step_count'] = 1
    
    return jsonify({
        "status": "success",
        "node": TREE_ROOT.to_dict(),
        "step": 1,
        "path": []
    })

@app.route('/api/answer', methods=['POST'])
def answer_question():
    data = request.json
    answer = data.get('answer') # "yes" or "no"
    
    current_node_id = session.get('current_node_id')
    current_node = find_node_by_id(TREE_ROOT, current_node_id)
    
    if not current_node:
        return jsonify({"error": "Game session error. restart."}), 400

    # Record the step
    path = session.get('path', [])
    path.append({
        "question": current_node.text,
        "answer": answer.upper(),
        "step": session.get('step_count')
    })
    session['path'] = path

    # Move to next node
    next_node = None
    if answer == 'yes':
        next_node = current_node.yes
    elif answer == 'no':
        next_node = current_node.no
    else:
        return jsonify({"error": "Invalid answer"}), 400

    if not next_node:
        # Should not happen in a complete tree unless we are at a leaf (guess) and client tried to answer again
        return jsonify({"error": "End of tree reached unexpectedly"}), 500

    session['current_node_id'] = next_node.id
    session['step_count'] = session.get('step_count') + 1

    return jsonify({
        "status": "success",
        "finished": not next_node.is_question,
        "node": next_node.to_dict(),
        "step": session['step_count'],
        "path": path # Return full path for sidebar
    })

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    data = request.json
    target_number = int(data.get('number'))
    
    # We need to traverse the tree automatically based on the target number
    # Since the tree is logic-based, we can just run the questions against the number
    
    path_log = []
    current_node = TREE_ROOT
    step = 1
    
    while current_node.is_question:
        answer = "no"
        
        # Simulate logic matching the tree structure queries
        if current_node.text == "Is the number prime?":
            if target_number in [2, 3, 5, 7]: answer = "yes"
            else: answer = "no"
            
        elif current_node.text == "Is it less than 5?":
            if target_number < 5: answer = "yes"
            else: answer = "no"
            
        elif current_node.text == "Is it divisible by 2?":
            if target_number % 2 == 0: answer = "yes"
            else: answer = "no"
            
        elif current_node.text == "Is it divisible by 5?":
            if target_number % 5 == 0: answer = "yes"
            else: answer = "no"
            
        elif current_node.text == "Is it even?":
            if target_number % 2 == 0: answer = "yes"
            else: answer = "no"
            
        elif current_node.text == "Is it less than 3?":
            if target_number < 3: answer = "yes"
            else: answer = "no"
            
        elif current_node.text == "Is it divisible by 3?":
            if target_number % 3 == 0: answer = "yes"
            else: answer = "no"
            
        elif current_node.text == "Is it less than 7?":
            if target_number < 7: answer = "yes"
            else: answer = "no"
        
        # Log the visit
        path_log.append({
            "step": step,
            "text": current_node.text,
            "answer": answer.upper(),
            "id": current_node.id
        })
        
        # Move
        if answer == "yes":
            current_node = current_node.yes
        else:
            current_node = current_node.no
        step += 1
        
    # Append the final guess node
    path_log.append({
        "step": step,
        "text": current_node.text, # "Is it [X]?" or just guess text
        "answer": "GUESS",
        "guess_value": current_node.guess,
        "id": current_node.id,
        "success": (current_node.guess == target_number)
    })
    
    return jsonify({
        "target": target_number,
        "path": path_log
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
