from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from folder2.models import db, User, Trek, Booking

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Create Database
with app.app_context():
    db.create_all()

# Home Page
@app.route("/")
def home():
    return """
    <h1>Trekking Management Application</h1>

    <br>

    <a href="/login">Login</a>

    <br><br>

    <a href="/register">Register</a>

    """

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]

        if role == "user":
            approved = True
        else:
            approved = False

        user = User(
            name=name,
            email=email,
            password=password,
            role=role,
            approved=approved
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.role == "staff" and not user.approved:
                return "Your account is waiting for admin approval."
            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "admin":
                return redirect("/admin")

            elif user.role == "staff":
                return redirect("/staff")

            else:
                return redirect("/user")

        return "Invalid Login"

    return render_template("login.html")


@app.route("/admin")
def admin():

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return redirect("/login")

    treks = Trek.query.all()
    print("Treks:", treks)

    pending_staff = User.query.filter_by(
        role="staff",
        approved=False
    ).all()
    print("Pending Staff:", pending_staff)

    return render_template(
        "admin_dashboard.html",
        treks=treks,
        pending_staff=pending_staff
    )

@app.route("/delete_trek/<int:trek_id>")
def delete_trek(trek_id):

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return redirect("/login")

    trek = Trek.query.get(trek_id)

    if trek:
        db.session.delete(trek)
        db.session.commit()

    return redirect("/admin")
@app.route("/add_trek", methods=["GET", "POST"])
def add_trek():

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return redirect("/login")

    if request.method == "POST":

        trek = Trek(
            trek_name=request.form["trek_name"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=int(request.form["duration"]),
            slots=int(request.form["slots"]),
            status="Open",
            start_date=request.form["start_date"],
            end_date=request.form["end_date"]
        )

        db.session.add(trek)
        db.session.commit()

        return redirect("/admin")

    return render_template("add_trek.html")

@app.route("/staff")
def staff():

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "staff":
        return redirect("/login")

    treks = Trek.query.filter_by(
        staff_id=session["user_id"]
    ).all()

    for trek in treks:
        trek.booking_count = Booking.query.filter_by(
            trek_id=trek.id
        ).count()

    return render_template(
        "staff_dashboard.html",
        treks=treks
    )
@app.route("/update_trek/<int:id>", methods=["POST"])
def update_trek(id):

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "staff":
        return redirect("/login")

    trek = Trek.query.get(id)

    if trek:

        trek.status = request.form["status"]
        trek.slots = int(request.form["slots"])

        db.session.commit()

    return redirect("/staff")


@app.route("/user")
def user():

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "user":
        return redirect("/login")

    treks = Trek.query.all()

    print("TREKS:", treks)
    print("NUMBER OF TREKS:", len(treks))

    return render_template(
        "user_dashboard.html",
        treks=treks
    )
@app.route("/book_trek/<int:trek_id>")
def book_trek(trek_id):

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "user":
        return redirect("/login")

    trek = Trek.query.get(trek_id)

    if not trek:
        return "Trek not found"

    if trek.slots <= 0:
        return "No slots available for this trek."


    booking = Booking(
    user_id=session["user_id"],
    trek_id=trek.id,
    booking_date="Today",
    status="Booked"
    )

    trek.slots -= 1

    db.session.add(booking)
    db.session.commit()

    return redirect("/user")

@app.route("/my_bookings")
def my_bookings():

    if "role" not in session:
        return redirect("/login")

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "bookings.html",
        bookings=bookings
    )



with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@gmail.com").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin123"),
            role="admin",
            approved=True,
            blacklisted=False
        )

        db.session.add(admin)
        db.session.commit()

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/approve_staff/<int:id>")
def approve_staff(id):

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return redirect("/login")

    staff = User.query.get(id)

    if staff:
        staff.approved = True
        db.session.commit()

    return redirect("/admin")

@app.route("/assign_staff/<int:trek_id>", methods=["POST"])
def assign_staff(trek_id):

    if "role" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return redirect("/login")

    trek = Trek.query.get(trek_id)

    if trek:

        trek.staff_id = request.form["staff_id"]

        db.session.commit()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(debug=True)



