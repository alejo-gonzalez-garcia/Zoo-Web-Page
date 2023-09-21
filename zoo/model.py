import flask_login
from datetime import datetime
import enum
from . import db

DEFAULT_STRING_SIZE = 128

DEFAULT_PASSWORD_HASH_SIZE = 100
DEFAULT_CODE_SIZE = 100


class UserRole(enum.Enum):
    customer = 1
    manager = 2


class User(flask_login.UserMixin, db.Model):
    __tablename__ = "user"

    email = db.Column(db.String(DEFAULT_STRING_SIZE),
                      primary_key=True, nullable=False)
    name = db.Column(db.String(DEFAULT_STRING_SIZE), nullable=False)
    last_name = db.Column(db.String(DEFAULT_STRING_SIZE), nullable=False)
    password_hash = db.Column(
        db.String(DEFAULT_PASSWORD_HASH_SIZE), nullable=False)
    role = db.Column(db.Enum(UserRole),
                     default=UserRole.customer, nullable=False)
    code = db.Column(db.String(DEFAULT_CODE_SIZE), default=None)

    bookings = db.relationship("ActivityBooking", back_populates="user", cascade="delete")

    def get_id(self):
        return self.email

class AnimalType(enum.Enum):
    Mamal = 1
    Bird = 2
class AnimalDiet(enum.Enum):
    Herbivorous = 1
    Carnivorous = 2
    Omnivorous = 3
class AnimalContinent(enum.Enum):
     Asia = 1
     Africa = 2
     America = 3
     Antarctica = 4
     Europe = 5
     Australia = 6
class AnimalHabitat(enum.Enum):
    Sabana = 1
    Jungle = 2
    Tropical = 3
    Desert = 4
    Glaciar = 5
    Steppe = 6
    Forest = 7
class Animal(db.Model):
    __tablename__ = "animal"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(DEFAULT_STRING_SIZE), nullable=False)
    scientific_name = db.Column(db.String(DEFAULT_STRING_SIZE), nullable=False)
    type =  db.Column(db.Enum(AnimalType), nullable=False)
    diet =  db.Column(db.Enum(AnimalDiet), nullable=False)
    weight =  db.Column(db.Float, nullable=False)
    size =  db.Column(db.Float, nullable=False)
    is_danger_extinction = db.Column(db.Boolean, nullable=True)
    birthdate = db.Column(db.DateTime(), nullable=False)
    image = db.Column(db.String(DEFAULT_STRING_SIZE*5), default=None)
    continent = db.Column(db.Enum(AnimalContinent), nullable=False)
    description = db.Column(db.Text(), default=None)
    habitat = db.Column(db.Enum(AnimalHabitat), nullable=False)
class Activity(db.Model):
    __tablename__ = "activity"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(DEFAULT_STRING_SIZE), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(DEFAULT_STRING_SIZE), default=None)
    minimum_age = db.Column(db.Integer, nullable=False)
    is_parent_required = db.Column(db.Boolean, nullable=False)
    is_featured = db.Column(db.Boolean, nullable=False)

    type_name = db.Column(db.ForeignKey("activity_type.name"), nullable=False)

    type = db.relationship("ActivityType", back_populates="activities")
    schedules = db.relationship("ActivitySchedule", back_populates="activity", order_by="ActivitySchedule.timestamp", cascade="delete")


    def get_future_schedules(self):
        future_schedules = db.session.query(
                ActivitySchedule
        ).filter(
            ActivitySchedule.activity_id == self.id,
            ActivitySchedule.timestamp >= datetime.now()
        ).all()

        print(future_schedules)

        return future_schedules

class ActivityType(db.Model):
    __tablename__ = "activity_type"

    name = db.Column(db.String(DEFAULT_STRING_SIZE),
                     primary_key=True, nullable=False)

    activities = db.relationship("Activity", back_populates="type", cascade="delete")


class ActivitySchedule(db.Model):
    __tablename__ = "activity_schedule"

    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)
    price = db.Column(db.Float, nullable=False)

    activity_id = db.Column(db.ForeignKey("activity.id"), nullable=False)

    activity = db.relationship("Activity", back_populates="schedules")
    bookings = db.relationship(
        "ActivityBooking", back_populates="activity_schedule", cascade="delete")

    def get_total_booked_seats(self):
        total_booked_seats = db.session.query(
            db.func.sum(ActivityBooking.seats_booked).label('booked')
        ).filter(
            ActivityBooking.activity_schedule == self
        ).one()

        booked = total_booked_seats.booked
        try:
            booked = int(booked)
        except:
            booked = 0

        return booked

    def get_available(self):
        total_booked_seats = self.get_total_booked_seats()
        return self.total - total_booked_seats


class ActivityBooking(db.Model):
    __tablename__ = "activity_booking"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False)

    user_email = db.Column(db.ForeignKey("user.email"), nullable=False)
    activity_schedule_id = db.Column(db.ForeignKey(
        "activity_schedule.id"), nullable=False)

    user = db.relationship("User", back_populates="bookings")
    activity_schedule = db.relationship(
        "ActivitySchedule", back_populates="bookings")
