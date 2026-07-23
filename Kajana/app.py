from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]

        # Example valid username
        if username != "admin":
            error = "Invalid username. Please try again."

    return render_template("Login.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)