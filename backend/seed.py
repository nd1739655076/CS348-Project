from app import app
from models import db, Students, Instructor, Department, Room, Course, CourseSession
from datetime import date, time

with app.app_context():
    db.drop_all()
    db.create_all()

    # 插入 Department
    cs_dept = Department(name="Computer Science", address="305 N University St, West Lafayette, IN")
    math_dept = Department(name="Mathematics", address="150 N University St, West Lafayette, IN")
    db.session.add_all([cs_dept, math_dept])
    db.session.commit()

    # 插入 Courses
    cs348 = Course(title="CS348", description="Database Systems", department_id=cs_dept.id)
    cs180 = Course(title="CS180", description="Intro to Programming", department_id=cs_dept.id)
    ma261 = Course(title="MA261", description="Multivariate Calculus", department_id=math_dept.id)
    db.session.add_all([cs348, cs180, ma261])
    db.session.commit()

    # 插入 Instructors
    instructor1 = Instructor(name="Dr. Smith", email="smith@purdue.edu")
    instructor2 = Instructor(name="Prof. Johnson", email="johnson@purdue.edu")
    db.session.add_all([instructor1, instructor2])
    db.session.commit()

    # 插入 Rooms
    room1 = Room(building="Lawson", number="B134", maxCapacity=100)
    room2 = Room(building="HAMP", number="2201", maxCapacity=80)
    db.session.add_all([room1, room2])
    db.session.commit()

    # 插入 Students（非必要字段但可以测试）
    student1 = Students(name="Alice Wang", email="alice@purdue.edu")
    student2 = Students(name="Bob Lee", email="bob@purdue.edu")
    db.session.add_all([student1, student2])
    db.session.commit()

    # 插入 CourseSession
    session1 = CourseSession(
        course_id=cs348.id,
        instructor_id=instructor1.instructor_id,
        room_id=room1.id,
        date=date(2025, 4, 1),
        time=time(10, 30),
        duration=90,
        description="First CS348 session",
        enrolledCount=50,
        attendedCount=48
    )

    session2 = CourseSession(
        course_id=cs180.id,
        instructor_id=instructor2.instructor_id,
        room_id=room2.id,
        date=date(2025, 4, 3),
        time=time(14, 0),
        duration=60,
        description="CS180 Intro session",
        enrolledCount=80,
        attendedCount=70
    )

    db.session.add_all([session1, session2])
    db.session.commit()

    print("✅ Sample data seeded successfully!")
