from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")


        # Hard-coded login details
        correct_username = "admin"
        correct_password = "Password123!"


        if username == correct_username and password == correct_password:

            return render_template("dashboard.html")


        else:
            error = "Invalid username or password. Please try again."


    return render_template("Login.html", error=error)



@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")



if __name__ == "__main__":
    app.run(debug=True)
    