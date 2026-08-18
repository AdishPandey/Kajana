import sqlite3
import os

from flask import Flask, render_template, request, redirect
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


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




@app.route("/booking_status")
def booking_status():

    # Connect to database
    connection = sqlite3.connect("Kajana.db")

    cursor = connection.cursor()


    # Get bookings
    cursor.execute("""
        SELECT *
        FROM bookings
        ORDER BY booking_id DESC
    """)


    bookings = cursor.fetchall()


    connection.close()



    # Summary counters

    total_bookings = len(bookings)

    pending_bookings = 0

    completed_bookings = 0



    for booking in bookings:

        status = booking[6].strip().lower()


        if status == "pending" or status == "confirmed":
            pending_bookings += 1


        if status == "completed":
            completed_bookings += 1



    return render_template(
        "booking_status.html",
        bookings=bookings,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        completed_bookings=completed_bookings
    )


    # Connect to database
    connection = sqlite3.connect("Kajana.db")

    cursor = connection.cursor()


    # Get all bookings
    cursor.execute("""
        SELECT *
        FROM bookings
        ORDER BY booking_id DESC
    """)


    bookings = cursor.fetchall()


    connection.close()



    # Summary numbers

    total_bookings = len(bookings)

    pending_bookings = 0

    completed_bookings = 0



    for booking in bookings:

        status = booking[5].strip().lower()


        if status == "pending" or status == "confirmed":
            pending_bookings += 1


        if status == "completed":
            completed_bookings += 1



    latest_booking = "None"


    if bookings:

        latest_booking = bookings[0][1]



    return render_template(
        "booking_status.html",
        bookings=bookings,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        completed_bookings=completed_bookings,
        latest_booking=latest_booking
    )


    connection = sqlite3.connect("Kajana.db")

    cursor = connection.cursor()


    cursor.execute("""
        SELECT *
        FROM bookings
        ORDER BY booking_id DESC
    """)


    bookings = cursor.fetchall()


    connection.close()


    total_bookings = len(bookings)

    pending_bookings = 0

    completed_bookings = 0


    for booking in bookings:

        if booking[5] == "Pending" or booking[5] == "Confirmed":
            pending_bookings += 1


        if booking[5] == "Completed":
            completed_bookings += 1



    latest_booking = "None"


    if bookings:
        latest_booking = bookings[0][2]


    return render_template(
        "booking_status.html",
        bookings=bookings,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
        completed_bookings=completed_bookings,
        latest_booking=latest_booking
    )


    # Connect to database
    connection = sqlite3.connect("Kajana.db")

    cursor = connection.cursor()


    # Get all bookings
    cursor.execute("""
        SELECT *
        FROM bookings
        ORDER BY booking_id DESC
    """)


    bookings = cursor.fetchall()


    connection.close()


    # Calculate summary information

    total_bookings = len(bookings)


    upcoming_bookings = 0
    completed_bookings = 0
    next_appointment = "None"


    for booking in bookings:

        status = booking[5]


        if status == "Pending" or status == "Confirmed":
            upcoming_bookings += 1


        if status == "Completed":
            completed_bookings += 1


    # Send data to HTML
    return render_template(
        "booking_status.html",
        bookings=bookings,
        total_bookings=total_bookings,
        upcoming_bookings=upcoming_bookings,
        completed_bookings=completed_bookings,
        next_appointment=next_appointment
    )

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

# DELETE BOOKING
@app.route("/delete_booking/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):

    # Connect to database
    connection = sqlite3.connect("Kajana.db")

    # Create cursor
    cursor = connection.cursor()


    # Delete selected booking
    cursor.execute("""
        DELETE FROM bookings
        WHERE booking_id = ?
    """,
    (booking_id,))


    # Save changes
    connection.commit()

    # Close database connection
    connection.close()


    # Return to booking status page
    return redirect("/booking_status")



# SUGGESTED QUOTE
@app.route("/suggested_quote", methods=["GET", "POST"])
def suggested_quote():

    quote = None
    error = None

    if request.method == "POST":

        # Get information entered by the customer
        service = request.form.get("service")
        area = request.form.get("area")
        details = request.form.get("details")

        try:

            # Send the job information to OpenAI
            response = client.responses.create(

                model="gpt-5-mini",

                input=f"""
You are an AI quote assistant for Kajana,
an Australian landscaping.
Estimate a reasonable price range in AUD for this job.

Service:
{service}

Approximate area:
{area} square metres

Customer description:
{details}

Consider:
- Type of service
- Size of the job
- Amount of labour required
- Difficulty
- Materials or equipment that may be required

Return:
1. Estimated price range in AUD
2. A short explanation of the estimate (1-2 sentences)


Make it clear that this is only an estimate
and the final price may change after inspection.
"""
            )

            # Get the text generated by OpenAI
            quote = response.output_text

        except Exception as e:

            # Display an error if something goes wrong
            error = "Unable to generate a quote. Please try again."

            print("OpenAI error:", e)

    return render_template(
        "suggested_quote.html",
        quote=quote,
        error=error
    )


    return render_template("suggested_quote.html")



@app.route("/enquiry", methods=["GET", "POST"])
def enquiry():

    response = None
    error = None

    if request.method == "POST":

        user_enquiry = request.form.get("enquiry")

        try:

            ai_response = client.responses.create(

                model="gpt-5.6",

                input=f"""
You are Kajana's customer enquiry assistant.

Kajana is an Australian landscaping and civil engineering business.

A customer has submitted the following enquiry:

{user_enquiry}

Answer the customer's question clearly and professionally.

Rules:
- Keep the response concise.
- Use Australian English.
- Only discuss Kajana's landscaping and civil engineering services.
- If you do not know something, say that the customer should contact Kajana directly.
- Do not invent specific prices.
- Do not make promises about bookings or availability.
- Keep the response under 100 words.
"""

            )

            response = ai_response.output_text

        except Exception as e:

            error = "Unable to respond to your enquiry. Please try again."

            print("OpenAI error:", e)


    return render_template(
        "enquiry.html",
        response=response,
        error=error
    )

    



# LOGOUT
@app.route("/logout")
def logout():

    return render_template("Login.html")




if __name__ == "__main__":

    create_database()

    app.run(debug=True)
