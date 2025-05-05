import React, { useEffect, useState } from "react";
import { getCourses, getInstructors, getRooms, getReport } from "../api";
import "./ReportForm.css";

export default function ReportForm() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [roomId, setRoomId] = useState("");
  const [courseId, setCourseId] = useState("");
  const [instructorId, setInstructorId] = useState("");

  const [rooms, setRooms] = useState([]);
  const [courses, setCourses] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [report, setReport] = useState(null);

  useEffect(() => {
    async function loadOptions() {
      setRooms(await getRooms());
      setCourses(await getCourses());
      setInstructors(await getInstructors());
    }
    loadOptions();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    const params = {
      start_date: startDate,
      end_date: endDate,
      room_id: roomId || null,
      course_id: courseId || null,
      instructor_id: instructorId || null,
    };

    try {
      const result = await getReport(params);
      setReport(result);
    } catch (err) {
      alert("Error fetching report. Please try again.");
      console.error(err);
    }
  }

  return (
    <div className="report-form-container">
      <h2>🔍Generate Report</h2>
      <form onSubmit={handleSubmit} className="report-form">
        <div className="form-group">
          <label>Start Date</label>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
        </div>

        <div className="form-group">
          <label>End Date</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
        </div>

        <div className="form-group">
          <label>Room</label>
          <select value={roomId} onChange={(e) => setRoomId(e.target.value)}>
            <option value="">All Rooms</option>
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                {room.building} {room.number}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Course</label>
          <select value={courseId} onChange={(e) => setCourseId(e.target.value)}>
            <option value="">All Courses</option>
            {courses.map((c) => (
              <option key={c.id} value={c.id}>{c.title}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Instructor</label>
          <select value={instructorId} onChange={(e) => setInstructorId(e.target.value)}>
            <option value="">All Instructors</option>
            {instructors.map((i) => (
              <option key={i.instructor_id} value={i.instructor_id}>{i.name}</option>
            ))}
          </select>
        </div>

        <button type="submit">Generate</button>
      </form>

      {report && (
        <div className="report-results">
          <h3>Report Summary</h3>
          <p><strong>Average Duration:</strong> {report.avg_duration} minutes</p>
          <p><strong>Average Enrolled:</strong> {report.avg_enrolled}</p>
          <p><strong>Average Attended:</strong> {report.avg_attended}</p>
          <p><strong>Average Attendance Rate:</strong> {(report.avg_attendance_rate * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  );
}
