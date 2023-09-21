from flask import Blueprint, render_template, request, url_for, redirect, current_app
from flask_mail import Message
import flask_login
from . import model, db, mail

from datetime import datetime

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    featured_activities = model.Activity.query.filter(model.Activity.is_featured == True).all()
    return render_template("pages/index.html", featured=featured_activities)

@bp.route("/animals")
def animals():
    animals = model.Animal.query.all()

    return render_template("pages/animals.html", animals=animals, animal_types=model.AnimalType, animal_diets=model.AnimalDiet, animal_continents=model.AnimalContinent)

@bp.route("/animal/<int:animal_id>")
def animal(animal_id):
    animal = model.Animal.query.filter_by(id=animal_id).first()

    return render_template("fragments/modal_animal.html", animal=animal)

@bp.route("/activities")
def activities():
    activities = model.Activity.query.all()

    return render_template("pages/activities.html", activities=activities)

@bp.route("/activity_edit/<int:activity_id>", methods=["GET", "POST"])
def activity_edit(activity_id):
    if not flask_login.current_user.is_authenticated or flask_login.current_user.role != model.UserRole.manager:
        return redirect(url_for("main.index"))

    activity = model.Activity.query.filter_by(id = activity_id).first()

    if request.method == "GET":
        activity_types = model.ActivityType.query.all()

        return render_template("pages/activity_edit.html", activity=activity, activity_types=activity_types)


    activity_id_form = request.form.get("activity_id", type=int)

    if (activity.id != activity_id_form):
        return "error", 400

    name = request.form.get("name")
    type = request.form.get("type")
    description = request.form.get("description")
    image = request.form.get("image")
    minimum_age = request.form.get("minimum_age", type=int)
    is_parent_required = request.form.get("is_parent_required") != None
    is_featured = request.form.get("is_featured") != None

    activity.name = name
    activity.type = model.ActivityType.query.filter_by(name=type).first()
    activity.description = description
    activity.image = image
    activity.minimum_age = minimum_age
    activity.is_parent_required = is_parent_required
    activity.is_featured = is_featured

    db.session.commit()
    return "success", 200

@bp.route("/activity_new", methods=["GET", "POST"])
def activity_new():
    if not flask_login.current_user.is_authenticated or flask_login.current_user.role != model.UserRole.manager:
        return redirect(url_for("main.index"))

    if request.method == "GET":
        activity_types = model.ActivityType.query.all()

        return render_template("pages/activity_new.html", activity_types=activity_types)


    name = request.form.get("name")
    type = request.form.get("type")
    description = request.form.get("description")
    image = request.form.get("image")
    minimum_age = request.form.get("minimum_age", type=int)
    is_parent_required = request.form.get("is_parent_required") != None
    is_featured = request.form.get("is_featured") != None

    activity = model.Activity(name=name, type=model.ActivityType.query.filter_by(name=type).first(), description=description, image=image, minimum_age=minimum_age, is_parent_required=is_parent_required, is_featured=is_featured)
    
    db.session.add(activity)
    db.session.commit()

    return redirect(url_for('main.activities'))


@bp.route("/activity_schedule_edit/<int:activity_schedule_id>", methods=["GET", "POST"])
def activity_schedule_edit(activity_schedule_id):
    if not flask_login.current_user.is_authenticated or flask_login.current_user.role != model.UserRole.manager:
        return redirect(url_for("main.index"))

    schedule = model.ActivitySchedule.query.filter_by(id=activity_schedule_id).first()

    if request.method == "GET":
        return render_template("fragments/modal_activity_schedule_edit.html", schedule=schedule)

    activity_schedule_id_form = request.form.get("schedule_id", type=int)

    if (schedule.id != activity_schedule_id_form):
        return "error", 400

    total = request.form.get("total", type=int)
    if (total < schedule.get_total_booked_seats()):
        return "error", 40

    timestamp = request.form.get("timestamp")
    format = "%Y-%m-%d %H:%M:%S" #2022-09-05 06:05:06
    price = request.form.get("price", type=float)
    
    try:
        timestamp = datetime.strptime(timestamp, format)

        schedule.total = total
        schedule.timestamp = timestamp
        schedule.price = price
        db.session.commit()

        return "success", 200
    except Exception as _:
        return "error", 406

@bp.route("/activity_schedule_remove/<int:activity_schedule_id>", methods=["POST"])
def activity_schedule_remove(activity_schedule_id):
    if flask_login.current_user.role != model.UserRole.manager:
        return redirect(url_for("main.index"))

    schedule = model.ActivitySchedule.query.filter_by(id=activity_schedule_id).first()

    if (not schedule):
        return "error", 406

    db.session.delete(schedule)
    db.session.commit()

    return "success", 200

@bp.route("/activity_schedule_new/<int:activity_id>", methods=["GET", "POST"])
def activity_schedule_new(activity_id):
    if not flask_login.current_user.is_authenticated or flask_login.current_user.role != model.UserRole.manager:
        return redirect(url_for("main.index"))

    activity = model.Activity.query.filter_by(id = activity_id).first()

    if request.method == "GET":
        return render_template("fragments/modal_activity_schedule_new.html", activity=activity)

    activity_id_form = request.form.get("activity_id", type=int)
    if (activity.id != activity_id_form):
        return "error", 400

    total = request.form.get("total", type=int)
    timestamp = request.form.get("timestamp")
    format = "%Y-%m-%d %H:%M:%S" #2022-09-05 06:05:06
    timestamp = datetime.strptime(timestamp, format)
    price = request.form.get("price", type=float)


    schedule = model.ActivitySchedule(total=total, timestamp=timestamp, activity=activity, price=price)
    db.session.add(schedule)
    db.session.commit()

    return "success", 200

@bp.route("/activity/<int:activity_id>")
def activity(activity_id):
    activity = model.Activity.query.filter_by(id = activity_id).first()
    print(request.base_url)

    return render_template("fragments/modal_activity.html", activity=activity)

@bp.route("/profile")
def profile():
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for("main.index"))

    return render_template("pages/profile.html", user=flask_login.current_user, datetime=datetime)

@bp.route("/book/<int:activity_schedule_id>", methods=["GET"])
def book(activity_schedule_id):
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for("main.index"))

    activity_schedule = model.ActivitySchedule.query.filter_by(id=activity_schedule_id).first()

    return render_template("fragments/modal_book.html", activity_schedule=activity_schedule)

@bp.route("/book", methods=["POST"])
def book_post():
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for("main.index"))

    activity_schedule_id = request.form.get("activity_schedule_id")
    seats = request.form.get("seats")

    if (not activity_schedule_id or not seats):
        return "error", 400

    activity_schedule_id = int(activity_schedule_id)
    seats = int(seats) 

    activity_schedule = model.ActivitySchedule.query.filter_by(id=activity_schedule_id).first()
    total_booked_seats = activity_schedule.get_total_booked_seats()

    if ((activity_schedule.total - total_booked_seats) < seats) or (seats < 1):
        return "a lot of seats", 406

    booking = model.ActivityBooking(timestamp=datetime.now(), seats_booked=seats, user=flask_login.current_user, activity_schedule=activity_schedule)

    db.session.add(booking)
    db.session.commit()
    
    return "success", 200

@bp.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    if request.method == "GET":
        return render_template("pages/contact_us.html")

    try:
        email = request.form.get("email")
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        info = request.form.get("info")

        message = Message(f"{name} contacted you", recipients=[current_app.config.get("MAIL_DEFAULT_SENDER")]);
        message.body = f"Email: {email}\nName: {name} {last_name}\nInfo: {info}"
        mail.send(message)
    except Exception as _:
        return "error", 400

    return "success", 200

