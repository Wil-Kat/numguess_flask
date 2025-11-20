# import required add ons
from flask import Flask, render_template, request, session
import random

# prepare flask
app = Flask(__name__)
app.secret_key = "guessgame"  

# create constant for number of attempts allowed
MAX_ATTEMPTS = 5

# function to reset game
def reset_game():
    """Start a new game."""
    session["target"] = random.randint(1, 100)
    session["attempts"] = 0

# run the function when the page is loaded
@app.route("/", methods=["GET", "POST"])
def index():
    # First visit: create a game
    if request.method == "GET":
        reset_game()

    message = ""
    game_over = False
    attempts = session.get("attempts", 0)
    target = session["target"]

    if request.method == "POST":
        # If user clicked "Play again"
        if request.form.get("play_again") == "yes":
            reset_game()
            attempts = 0
            message = "New game started! Guess a number between 1 and 100."
            game_over = False

        # If user submitted a guess
        elif "guess" in request.form:
            try:
                guess = int(request.form["guess"])
            except ValueError:
                message = "❌ Invalid input. Please enter a number."
            else:
                # Only process a guess if the game is not already over
                if attempts < MAX_ATTEMPTS:
                    attempts += 1
                    session["attempts"] = attempts

                    if guess == target:
                        message = f"Yay! You guessed correctly in {attempts} attempts! 🎉"
                        game_over = True
                    elif attempts >= MAX_ATTEMPTS:
                        # This was the last allowed attempt and still wrong
                        message = f"Sorry! You ran out of attempts. The number was {target}. 😵"
                        game_over = True
                    elif guess < target:
                        message = "Your number is too low. 👎"
                    else:  # guess > target
                        message = "Your number is too high. 👎"
                else:
                    # Safety: already out of attempts but somehow got another POST
                    message = f"Game over! The number was {target}. Click 'Play again' to start a new game."
                    game_over = True

    return render_template(
        "numguess.html",
        message=message,
        attempts=attempts,
        max_attempts=MAX_ATTEMPTS,
        game_over=game_over,
    )

if __name__ == "__main__":
    app.run(debug=True)