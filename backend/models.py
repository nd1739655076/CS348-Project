from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index

db = SQLAlchemy()

class Students(db.Model):
    student_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)

class Instructor(db.Model):
    instructor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(50))
    number = db.Column(db.String(10))
    maxCapacity = db.Column(db.Integer)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref='courses')

class CourseSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.instructor_id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    duration = db.Column(db.Integer)
    description = db.Column(db.Text)
    enrolledCount = db.Column(db.Integer)
    attendedCount = db.Column(db.Integer)
    course = db.relationship('Course', backref='sessions')
    instructor = db.relationship('Instructor', backref='sessions') 
    room = db.relationship('Room', backref='sessions')


Index("ix_cs_course",      CourseSession.course_id)
Index("ix_cs_instructor",  CourseSession.instructor_id)
Index("ix_cs_room",        CourseSession.room_id)
Index("ix_cs_course_date", CourseSession.course_id, CourseSession.date)





    

