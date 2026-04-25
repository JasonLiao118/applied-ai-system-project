import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, reset_game, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_new_game_resets_all_state():
    # Bug: clicking New Game only reset attempts and secret, leaving score and history dirty.
    state = reset_game(new_secret=42)
    assert state["attempts"] == 0
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert state["secret"] == 42

def test_win_score_uses_correct_attempt_number():
    # Bug: update_score used (attempt_number + 1) but attempts is already 1-indexed
    # (incremented before being passed in), so the win bonus was always 10 points too low.
    # Guessing correctly on attempt 1 should award 100 - 10*1 = 90 points.
    assert update_score(0, "Win", 1) == 90
    # Attempt 2 should award 100 - 10*2 = 80 points.
    assert update_score(0, "Win", 2) == 80

def test_hint_numeric_not_string_comparison():
    # Regression: secret was cast to str on even attempts, making "9" > "50" lexicographically
    # (True, because "9" > "5"), so guess 9 against secret 50 wrongly returned "Too High".
    # With correct integer comparison, 9 < 50 must return "Too Low".
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"
