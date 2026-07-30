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
        correct_password = "admin123"


        if username == correct_username and password == correct_password:

            return render_template("dashboard.html")


        else:
            error = "Invalid username or password. Please try again."


    return render_template("Login.html", error=error)



@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")

@app.route("/book-services")
def book_services():
    return render_template("book_services.html")


@app.route("/suggested-quote")
def suggested_quote():
    return render_template("suggested_quote.html")


@app.route("/enquiry")
def enquiry():
    return render_template("enquiry.html")


@app.route("/booking-status")
def booking_status():
    return render_template("booking_status.html")
    

if __name__ == "__main__":
    app.run(debug=True)


    