def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


#Refactored logic with Claude to be imported into app.py and tested in test_game_logic.py
def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📈 Go LOWER!"
    return "Too Low", "📉 Go HIGHER!"


#Refactored logic with Claude that found the incorrect calculation of score
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

#Refactored logic with Claude that reimplemented a fresh game state that makes sure everything is reset correctly
def reset_game(new_secret: int):
    """
    Return a fresh game state dict for a new game.

    Returns a dict with keys: secret, attempts, score, status, history
    """
    return {
        "secret": new_secret,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }
