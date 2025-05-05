from flask import Blueprint, request, jsonify
from models import db, CourseSession, Course, Instructor, Room
from datetime import datetime


sessions_bp = Blueprint("sessions_bp", __name__)
courses_bp = Blueprint("courses_bp", __name__)
instructors_bp = Blueprint("instructors_bp", __name__)
rooms_bp = Blueprint("rooms_bp", __name__)


##############################
#         SESSIONS           #
##############################

@sessions_bp.route("/sessions", methods=["GET"])
def list_sessions():
    sessions = CourseSession.query.all()
    result = []
    for s in sessions:
        result.append({
            "id": s.id,
            "course_id": s.course_id,
            "course": s.course.title if s.course else None,
            "instructor_id": s.instructor_id,
            "instructor": s.instructor.name if s.instructor else None,
            "room_id": s.room_id,
            "room": f"{s.room.building} {s.room.number}" if s.room else None,
            "date": s.date.isoformat() if s.date else None,
            "time": s.time.strftime("%H:%M") if s.time else None,
            "duration": s.duration,
            "description": s.description,
            "enrolledCount": s.enrolledCount,
            "attendedCount": s.attendedCount
        })
    return jsonify(result), 200



@sessions_bp.route("/sessions", methods=["POST"])
def create_session():
    """Create a new CourseSession."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    try:
        date_str = data.get("date")
        time_str = data.get("time")
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        parsed_time = datetime.strptime(time_str, "%H:%M").time() if time_str else None
    except ValueError:
        return jsonify({"error": "Invalid date or time format"}), 400

    new_session = CourseSession(
        course_id=int(data.get("course_id")),
        instructor_id=int(data.get("instructor_id")),
        room_id=int(data.get("room_id")),
        date=parsed_date,
        time=parsed_time,
        duration=int(data.get("duration")),
        description=data.get("description"),
        enrolledCount=int(data.get("enrolledCount", 0)),
        attendedCount=int(data.get("attendedCount", 0))
    )

    db.session.add(new_session)
    db.session.commit()

    return jsonify({"message": "Session created", "id": new_session.id}), 201


@sessions_bp.route("/sessions/<int:session_id>", methods=["GET"])
def get_session(session_id):
    """Return a single CourseSession by ID."""
    session_obj = CourseSession.query.get_or_404(session_id)
    return jsonify({
        "id": session_obj.id,
        "course_id": session_obj.course_id,
        "instructor_id": session_obj.instructor_id,
        "room_id": session_obj.room_id,
        "date": session_obj.date.isoformat() if session_obj.date else None,
        "time": session_obj.time.strftime("%H:%M") if session_obj.time else None,
        "duration": session_obj.duration,
        "description": session_obj.description,
        "enrolledCount": session_obj.enrolledCount,
        "attendedCount": session_obj.attendedCount
    }), 200


@sessions_bp.route("/sessions/<int:session_id>", methods=["PUT"])
def update_session(session_id):
    """Update an existing CourseSession."""
    session_obj = CourseSession.query.get_or_404(session_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    session_obj.course_id = data.get("course_id", session_obj.course_id)
    session_obj.instructor_id = data.get("instructor_id", session_obj.instructor_id)
    session_obj.room_id = data.get("room_id", session_obj.room_id)
    session_obj.duration = data.get("duration", session_obj.duration)
    session_obj.description = data.get("description", session_obj.description)
    session_obj.enrolledCount = data.get("enrolledCount", session_obj.enrolledCount)
    session_obj.attendedCount = data.get("attendedCount", session_obj.attendedCount)
    date_str = data.get("date")
    time_str = data.get("time")
    if date_str:
        try:
            session_obj.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if time_str:
        try:
            session_obj.time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return jsonify({"error": "Invalid time format. Use HH:MM."}), 400

    db.session.commit()
    return jsonify({"message": f"Session {session_id} updated"}), 200


@sessions_bp.route("/sessions/<int:session_id>", methods=["DELETE"])
def delete_session(session_id):
    """Delete a CourseSession by ID."""
    session_obj = CourseSession.query.get_or_404(session_id)
    db.session.delete(session_obj)
    db.session.commit()
    return jsonify({"message": f"Session {session_id} deleted"}), 200




@courses_bp.route("/courses", methods=["GET"])
def list_courses():
    """Return a list of all Courses."""
    courses = Course.query.all()
    result = []
    for c in courses:
        result.append({
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "department_id": c.department_id
        })
    return jsonify(result), 200


@courses_bp.route("/courses", methods=["POST"])
def create_course():
    """Create a new Course."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    new_course = Course(
        title=data.get("title"),
        description=data.get("description"),
        department_id=data.get("department_id")
    )
    db.session.add(new_course)
    db.session.commit()

    return jsonify({"message": "Course created", "id": new_course.id}), 201


@courses_bp.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """Get a single Course by ID."""
    course = Course.query.get_or_404(course_id)
    return jsonify({
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "department_id": course.department_id
    }), 200


@courses_bp.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """Update an existing Course."""
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    course.title = data.get("title", course.title)
    course.description = data.get("description", course.description)
    course.department_id = data.get("department_id", course.department_id)

    db.session.commit()
    return jsonify({"message": f"Course {course_id} updated"}), 200


@courses_bp.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """Delete a Course by ID."""
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": f"Course {course_id} deleted"}), 200



@instructors_bp.route("/instructors", methods=["GET"])
def list_instructors():
    """Return a list of all Instructors."""
    instructors = Instructor.query.all()
    result = []
    for i in instructors:
        result.append({
            "instructor_id": i.instructor_id,
            "name": i.name,
            "email": i.email
        })
    return jsonify(result), 200


@instructors_bp.route("/instructors", methods=["POST"])
def create_instructor():
    """Create a new Instructor."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    new_instructor = Instructor(
        name=data.get("name"),
        email=data.get("email"),
    )
    db.session.add(new_instructor)
    db.session.commit()

    return jsonify({"message": "Instructor created", "id": new_instructor.instructor_id}), 201


@instructors_bp.route("/instructors/<int:instructor_id>", methods=["GET"])
def get_instructor(instructor_id):
    """Get a single Instructor by ID."""
    instructor = Instructor.query.get_or_404(instructor_id)
    return jsonify({
        "instructor_id": instructor.instructor_id,
        "name": instructor.name,
        "email": instructor.email
    }), 200


@instructors_bp.route("/instructors/<int:instructor_id>", methods=["PUT"])
def update_instructor(instructor_id):
    """Update an existing Instructor."""
    instructor = Instructor.query.get_or_404(instructor_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    instructor.name = data.get("name", instructor.name)
    instructor.email = data.get("email", instructor.email)

    db.session.commit()
    return jsonify({"message": f"Instructor {instructor_id} updated"}), 200


@instructors_bp.route("/instructors/<int:instructor_id>", methods=["DELETE"])
def delete_instructor(instructor_id):
    """Delete an Instructor by ID."""
    instructor = Instructor.query.get_or_404(instructor_id)
    db.session.delete(instructor)
    db.session.commit()
    return jsonify({"message": f"Instructor {instructor_id} deleted"}), 200




@rooms_bp.route("/rooms", methods=["GET"])
def list_rooms():
    """Return a list of all Rooms."""
    rooms = Room.query.all()
    result = []
    for r in rooms:
        result.append({
            "id": r.id,
            "building": r.building,
            "number": r.number,
            "maxCapacity": r.maxCapacity
        })
    return jsonify(result), 200


@rooms_bp.route("/rooms", methods=["POST"])
def create_room():
    """Create a new Room."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    new_room = Room(
        building=data.get("building"),
        number=data.get("number"),
        maxCapacity=data.get("maxCapacity")
    )
    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Room created", "id": new_room.id}), 201


@rooms_bp.route("/rooms/<int:room_id>", methods=["GET"])
def get_room(room_id):
    """Get a single Room by ID."""
    room = Room.query.get_or_404(room_id)
    return jsonify({
        "id": room.id,
        "building": room.building,
        "number": room.number,
        "maxCapacity": room.maxCapacity
    }), 200


@rooms_bp.route("/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    """Update an existing Room."""
    room = Room.query.get_or_404(room_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    room.building = data.get("building", room.building)
    room.number = data.get("number", room.number)
    room.maxCapacity = data.get("maxCapacity", room.maxCapacity)

    db.session.commit()
    return jsonify({"message": f"Room {room_id} updated"}), 200


@rooms_bp.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    """Delete a Room by ID."""
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": f"Room {room_id} deleted"}), 200
