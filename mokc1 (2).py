import sqlite3
from difflib import SequenceMatcher


def find_best_match(user_comment, comments):
    # Calculate similarity scores for each comment
    scores = [(comment, SequenceMatcher(None, user_comment, comment).ratio()) for comment in comments]

    # Sort the comments based on similarity scores in descending order
    sorted_comments = sorted(scores, key=lambda x: x[1], reverse=True)

    # Return the best match
    return sorted_comments[0][0]


def get_game_recommendation(user_comment):
    # Connect to the database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Retrieve comments from the database
    cursor.execute("SELECT comment FROM game_comments")
    comments = [row[0] for row in cursor.fetchall()]

    # Find the best-matching comment
    best_match = find_best_match(user_comment, comments)

    # Retrieve the game corresponding to the best-matching comment
    cursor.execute("SELECT game_name FROM game_comments WHERE comment = ?", (best_match,))
    game_recommendation = cursor.fetchone()

    # Close the database connection
    conn.close()

    return game_recommendation[0] if game_recommendation else "No matching game found"


# Example of usage
user_input = "I love games with great graphics!"
recommended_game = get_game_recommendation(user_input)
print("Recommended Game:", recommended_game)
