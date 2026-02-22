class Node:
    def __init__(self, id, text, is_question=True, guess=None, yes=None, no=None):
        self.id = id
        self.text = text  # Information shown to user (Question or Guess)
        self.is_question = is_question
        self.guess = guess  # Only for leaf nodes
        self.yes = yes      # Left child
        self.no = no        # Right child

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_question": self.is_question,
            "guess": self.guess
        }

def build_decision_tree():
    # Leaf Nodes (The Guesses)
    # Using IDs 20-29 for guesses to keep them distinct
    g0 = Node("g0", "Is it 0?", is_question=False, guess=0)
    g1 = Node("g1", "Is it 1?", is_question=False, guess=1)
    g2 = Node("g2", "Is it 2?", is_question=False, guess=2)
    g3 = Node("g3", "Is it 3?", is_question=False, guess=3)
    g4 = Node("g4", "Is it 4?", is_question=False, guess=4)
    g5 = Node("g5", "Is it 5?", is_question=False, guess=5)
    g6 = Node("g6", "Is it 6?", is_question=False, guess=6)
    g7 = Node("g7", "Is it 7?", is_question=False, guess=7)
    g8 = Node("g8", "Is it 8?", is_question=False, guess=8)
    g9 = Node("g9", "Is it 9?", is_question=False, guess=9)

    # Sub-branches construction based on "MY DECISION APPROACH"
    
    # --- IF PRIME BRANCH ---
    # Q3: Is it divisible by 2? (Yes->2, No->3)
    q3 = Node("q3", "Is it divisible by 2?", yes=g2, no=g3)
    
    # Q4: Is it divisible by 5? (Yes->5, No->7)
    q4 = Node("q4", "Is it divisible by 5?", yes=g5, no=g7)

    # Q2: Is it less than 5? (Yes->Q3, No->Q4)
    q2 = Node("q2", "Is it less than 5?", yes=q3, no=q4)


    # --- IF NOT PRIME BRANCH ---
    # Q7: Is it less than 3? (Yes->0, No->4)
    q7 = Node("q7", "Is it less than 3?", yes=g0, no=g4)
    
    # Q6: Is it even? (Yes->Q7, No->1)
    q6 = Node("q6", "Is it even?", yes=q7, no=g1)

    # Q9: Is it less than 7? (Yes->6, No->9)
    q9 = Node("q9", "Is it less than 7?", yes=g6, no=g9)

    # Q8: Is it divisible by 3? (Yes->Q9, No->8)
    q8 = Node("q8", "Is it divisible by 3?", yes=q9, no=g8)
    
    # Q5: Is it less than 5? (Yes->Q6, No->Q8)
    q5 = Node("q5", "Is it less than 5?", yes=q6, no=q8)


    # --- ROOT ---
    # Q1: Is the number prime? (Yes->Q2, No->Q5)
    # Primes 0-9: 2, 3, 5, 7. 
    # (Note: 0 and 1 are not prime. 2,3,5,7 are prime. 4,6,8,9 are not prime.)
    root = Node("q1", "Is the number prime?", yes=q2, no=q5)

    return root

def find_node_by_id(current_node, target_id):
    if not current_node:
        return None
    if current_node.id == target_id:
        return current_node
    
    # DFS search
    res = find_node_by_id(current_node.yes, target_id)
    if res: return res
    return find_node_by_id(current_node.no, target_id)
