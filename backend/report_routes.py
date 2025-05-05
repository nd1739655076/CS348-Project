from flask import Blueprint, request, jsonify
from models import db, Course, Instructor, Room
from sqlalchemy import text

report_bp = Blueprint("report_bp", __name__, url_prefix="/report")


@report_bp.route("/instructor", methods=["GET"])
def instructor_report():
    instructor_id = request.args.get("instructor_id")

    stats_sql = text("""
        SELECT COUNT(*) as total_sessions,
               AVG(attendedCount) as avg_attended,
               AVG(enrolledCount) as avg_enrolled
        FROM course_session
        WHERE instructor_id = :instructor_id
    """)

    stats_row = db.session.execute(stats_sql, {"instructor_id": instructor_id}).fetchone()
    stats = stats_row._mapping

    courses_sql = text("""
        SELECT DISTINCT c.title
        FROM course_session cs
        JOIN course c ON cs.course_id = c.id
        WHERE cs.instructor_id = :instructor_id
    """)
    courses = db.session.execute(courses_sql, {"instructor_id": instructor_id}).fetchall()
    course_titles = [row[0] for row in courses]

    return jsonify({
        "total_sessions": stats["total_sessions"] or 0,
        "avg_attended": round(stats["avg_attended"] or 0, 2),
        "avg_enrolled": round(stats["avg_enrolled"] or 0, 2),
        "avg_attendance_rate": round(
            (stats["avg_attended"] or 0) / (stats["avg_enrolled"] or 1), 2
        ),
        "courses": course_titles
    })

@report_bp.route("/room", methods=["GET"])
def room_report():
    room_id = request.args.get("room_id")

    stats_sql = text("""
        SELECT COUNT(*) as total_sessions,
               AVG(enrolledCount) as avg_enrolled
        FROM course_session
        WHERE room_id = :room_id
    """)
    stats_row = db.session.execute(stats_sql, {"room_id": room_id}).fetchone()
    stats = stats_row._mapping

    courses_sql = text("""
        SELECT DISTINCT c.title
        FROM course_session cs
        JOIN course c ON cs.course_id = c.id
        WHERE cs.room_id = :room_id
    """)
    courses = db.session.execute(courses_sql, {"room_id": room_id}).fetchall()
    course_titles = [row[0] for row in courses]

    room = Room.query.get(room_id)

    return jsonify({
        "room_label": f"{room.building} {room.number}",
        "max_capacity": room.maxCapacity,
        "total_sessions": stats["total_sessions"] or 0,
        "avg_enrolled": round(stats["avg_enrolled"] or 0, 2),
        "courses": course_titles
    })




@report_bp.route("/course", methods=["GET"])
def course_report():
    course_id = request.args.get("course_id")

    stats_sql = text("""
        SELECT COUNT(*) as total_sessions,
               SUM(enrolledCount) as total_enrollment,
               AVG(CASE WHEN enrolledCount > 0 THEN attendedCount * 1.0 / enrolledCount ELSE 0 END) as avg_attendance_rate
        FROM course_session
        WHERE course_id = :course_id
    """)
    stats_row = db.session.execute(stats_sql, {"course_id": course_id}).fetchone()
    stats = stats_row._mapping

    instructors_sql = text("""
        SELECT DISTINCT i.name
        FROM course_session cs
        JOIN instructor i ON cs.instructor_id = i.instructor_id
        WHERE cs.course_id = :course_id
    """)
    instructors = db.session.execute(instructors_sql, {"course_id": course_id}).fetchall()
    instructor_names = [row[0] for row in instructors]

    return jsonify({
        "total_sessions": stats["total_sessions"] or 0,
        "total_enrollment": stats["total_enrollment"] or 0,
        "avg_attendance_rate": round(stats["avg_attendance_rate"] or 0, 2),
        "instructors": instructor_names
    })

@report_bp.route("/summary", methods=["GET"])
def summary_report():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    room_id = request.args.get("room_id")
    course_id = request.args.get("course_id")
    instructor_id = request.args.get("instructor_id")

    conditions = []
    params = {}

    if start_date:
        conditions.append("cs.date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        conditions.append("cs.date <= :end_date")
        params["end_date"] = end_date
    if room_id:
        conditions.append("cs.room_id = :room_id")
        params["room_id"] = room_id
    if course_id:
        conditions.append("cs.course_id = :course_id")
        params["course_id"] = course_id
    if instructor_id:
        conditions.append("cs.instructor_id = :instructor_id")
        params["instructor_id"] = instructor_id

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    summary_sql = text(f"""
        SELECT AVG(cs.duration) as avg_duration,
               AVG(cs.enrolledCount) as avg_enrolled,
               AVG(cs.attendedCount) as avg_attended,
               AVG(CASE WHEN cs.enrolledCount > 0 THEN cs.attendedCount * 1.0 / cs.enrolledCount ELSE 0 END) as avg_attendance_rate
        FROM course_session cs
        WHERE {where_clause}
    """)

    summary = db.session.execute(summary_sql, params).fetchone()
    data = summary._mapping

    return jsonify({
        "avg_duration": round(data["avg_duration"] or 0, 2),
        "avg_enrolled": round(data["avg_enrolled"] or 0, 2),
        "avg_attended": round(data["avg_attended"] or 0, 2),
        "avg_attendance_rate": round(data["avg_attendance_rate"] or 0, 2)
    })

@report_bp.route("/search", methods=["GET"])
def search_sessions():
    keyword = request.args.get("keyword", "")
    sql = text("""
        SELECT cs.id, cs.date, cs.time, c.title AS course_title, i.name AS instructor_name
        FROM course_session cs
        JOIN course c ON cs.course_id = c.id
        JOIN instructor i ON cs.instructor_id = i.instructor_id
        WHERE c.title LIKE :kw
    """)
    result = db.session.execute(sql, {"kw": f"%{keyword}%"}).fetchall()
    return jsonify([dict(row) for row in result])



@report_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([
        {"id": course.id, "title": course.title}
        for course in courses
    ])

@report_bp.route("/instructors", methods=["GET"])
def get_instructors():
    instructors = Instructor.query.all()
    return jsonify([
        {"id": inst.instructor_id, "name": inst.name}
        for inst in instructors
    ])

@report_bp.route("/rooms", methods=["GET"])
def get_rooms():
    print(">>> Serving /rooms from report_bp")
    rooms = Room.query.all()
    return jsonify([
        {
            "id": room.id,
            "building": room.building,
            "number": room.number,
            "maxCapacity": room.maxCapacity,
            "label": f"{room.building} {room.number}"
        }
        for room in rooms
    ])
