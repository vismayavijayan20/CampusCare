import os
import uuid

from flask import (
    Flask, render_template, redirect,
    url_for, request, flash
)

from flask_login import (
    LoginManager, login_user,
    logout_user, login_required, current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from config import Config
from models import db, User, Complaint, Notification


app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

CATEGORIES = [
    "Classroom",
    "Laboratory",
    "Library",
    "Hostel",
    "Electricity",
    "Water Supply",
    "Sanitation",
    "Infrastructure",
    "Other"
]

STATUSES = ["Pending", "In Progress", "Resolved"]
PRIORITIES = ["Low", "Medium", "High"]


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# HOME

@app.route("/")
def home():

    if current_user.is_authenticated:

        if current_user.role == "Admin":
            return redirect(url_for("admin_dashboard"))

        return redirect(url_for("student_dashboard"))

    return redirect(url_for("login"))


# STUDENT REGISTRATION

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "danger")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for("register"))

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role="Student"
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful.", "success")

        return redirect(url_for("login"))

    return render_template("register.html")


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            if user.role == "Admin":
                return redirect(url_for("admin_dashboard"))

            return redirect(url_for("student_dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


# STUDENT DASHBOARD

@app.route("/student/dashboard")
@login_required
def student_dashboard():

    if current_user.role != "Student":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    complaints = Complaint.query.filter_by(
        user_id=current_user.user_id
    ).order_by(
        Complaint.created_at.desc()
    ).all()

    total = len(complaints)

    pending = sum(c.status == "Pending" for c in complaints)

    in_progress = sum(
        c.status == "In Progress" for c in complaints
    )

    resolved = sum(c.status == "Resolved" for c in complaints)
    notifications = Notification.query.filter_by(
    user_id=current_user.user_id
).order_by(
    Notification.created_at.desc()
).all()

    return render_template(
        "student_dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,
        notifications=notifications
    )


# SUBMIT COMPLAINT

@app.route("/submit-complaint", methods=["GET", "POST"])
@login_required
def submit_complaint():

    if current_user.role != "Student":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "")

        if not title or not description or category not in CATEGORIES:
            flash("Please complete all required fields.", "danger")
            return redirect(url_for("submit_complaint"))

        image = request.files.get("image")
        filename = None

        if image and image.filename:

            if not allowed_file(image.filename):
                flash("Only PNG, JPG, JPEG and WEBP images are allowed.", "danger")
                return redirect(url_for("submit_complaint"))

            original_name = secure_filename(image.filename)
            extension = original_name.rsplit(".", 1)[1].lower()

            filename = f"{uuid.uuid4().hex}.{extension}"

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

        complaint = Complaint(
            user_id=current_user.user_id,
            title=title,
            description=description,
            category=category,
            image=filename,
            status="Pending",
            priority="Medium"
        )

        db.session.add(complaint)
        db.session.commit()

        flash("Complaint submitted successfully!", "success")

        return redirect(url_for("student_dashboard"))

    return render_template(
        "submit_complaint.html",
        categories=CATEGORIES
    )


# ADMIN DASHBOARD

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "Admin":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    total = len(complaints)

    pending = sum(c.status == "Pending" for c in complaints)

    in_progress = sum(
        c.status == "In Progress" for c in complaints
    )

    resolved = sum(c.status == "Resolved" for c in complaints)

    return render_template(
        "admin_dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,
        statuses=STATUSES,
        priorities=PRIORITIES
    )


# UPDATE COMPLAINT

@app.route(
    "/admin/update-complaint/<int:complaint_id>",
    methods=["POST"]
)
@login_required
def update_complaint(complaint_id):

    if current_user.role != "Admin":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    complaint = db.session.get(Complaint, complaint_id)

    if complaint is None:
        flash("Complaint not found.", "danger")
        return redirect(url_for("admin_dashboard"))

    status = request.form.get("status")
    priority = request.form.get("priority")

    if status not in STATUSES or priority not in PRIORITIES:
        flash("Invalid status or priority.", "danger")
        return redirect(url_for("admin_dashboard"))

    old_status = complaint.status

    complaint.status = status
    complaint.priority = priority

    # Generate notification only when status changes
    if old_status != status:

        notification = Notification(
            user_id=complaint.user_id,
            message=(
                f"Your complaint '{complaint.title}' "
                f"has been updated to {status}."
            )
        )

        db.session.add(notification)

    db.session.commit()

    flash("Complaint updated successfully.", "success")

    return redirect(url_for("admin_dashboard"))

# LOGOUT

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "info")

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)