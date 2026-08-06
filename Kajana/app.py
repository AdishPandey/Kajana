import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def create_database():

    connection = sqlite3.connect("Kajana.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            service TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            booking_time TEXT NOT NULL,
            details TEXT,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()



# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":

            return render_template("dashboard.html")

        else:
            error = "Invalid username or password."

    return render_template("Login.html", error=error)



# DASHBOARD
@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")



# BOOK SERVICES PAGE
@app.route("/book_services")
def book_services():

    return render_template("book_services.html")



# SERVICE BOOKING FORM
@app.route("/book_services/<service>")
def booking_form(service):

    service_names = {

        "lawn_mowing": "Lawn Mowing",

        "garden_cleanup": "Garden Cleanup",

        "irrigation_check": "Irrigation Check",

        "tree_trimming": "Tree Trimming"
    }


    service_name = service_names.get(service)


    if service_name is None:

        return "Service not found", 404


    return render_template(
        "booking_form.html",
        service=service_name
    )



# SAVE BOOKING
@app.route("/submit_booking", methods=["POST"])
def submit_booking():

    service = request.form.get("service")
    booking_date = request.form.get("booking_date")
    booking_time = request.form.get("booking_time")
    details = request.form.get("details")


    connection = sqlite3.connect("Kajana.db")

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO bookings
        (username, service, booking_date, booking_time, details, status)

        VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        "admin",
        service,
        booking_date,
        booking_time,
        details,
        "Pending"
    ))


    connection.commit()
    connection.close()


    return redirect("/booking_status")



# BOOKING STATUS
# BOOKING STATUS
@app.route("/booking_status")
def booking_status():

    # Connect to the Kajana database
    connection = sqlite3.connect("Kajana.db")

    # Create a cursor to run SQL commands
    cursor = connection.cursor()

    # Get every booking from the bookings table
    cursor.execute("""
        SELECT booking_id,
               service,
               booking_date,
               booking_time,
               details,
               status
        FROM bookings
        ORDER BY booking_id DESC
    """)

    # Store all bookings in a variable
    bookings = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Send the bookings to the HTML page
    return render_template(
        "booking_status.html",
        bookings=bookings
    )

# UPDATE BOOKING STATUS
@app.route("/update_status/<int:booking_id>", methods=["POST"])
def update_status(booking_id):

    # Get the new status selected by the admin
    new_status = request.form.get("status")


    # Connect to database
    connection = sqlite3.connect("Kajana.db")

    cursor = connection.cursor()


    # Update the booking status
    cursor.execute("""
        UPDATE bookings
        SET status = ?
        WHERE booking_id = ?
    """,
    (
        new_status,
        booking_id
    ))


    # Save changes
    connection.commit()

    # Close database
    connection.close()


    # Return to booking status page
    return redirect("/booking_status")
    



# OTHER PAGES
@app.route("/suggested_quote")
def suggested_quote():

    return render_template("suggested_quote.html")



@app.route("/enquiry")
def enquiry():

    return render_template("enquiry.html")



# LOGOUT
@app.route("/logout")
def logout():

    return render_template("Login.html")



if __name__ == "__main__":

    create_database()

    app.run(debug=True)
