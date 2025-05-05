import { useState, useEffect } from "react";
import "./CourseReport.css";

export default function CourseReport() {
  const [courses, setCourses] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/report/courses")
      .then(res => res.json())
      .then(data => setCourses(data))
      .catch(err => console.error("Failed to load courses", err));
  }, []);

  const fetchReport = async () => {
    const res = await fetch(`http://localhost:5000/report/course?course_id=${selectedId}`);
    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="course-report-container">
      <h2>📘 Course Report</h2>
      <select value={selectedId} onChange={e => setSelectedId(e.target.value)}>
        <option value="">Select a course</option>
        {courses.map(course => (
          <option key={course.id} value={course.id}>
            {course.title}
          </option>
        ))}
      </select>

      <button onClick={fetchReport} disabled={!selectedId}>
        Fetch Report
      </button>

      {result && (
        <div className="course-report-results">
          <p><strong>Total Sessions:</strong> {result.total_sessions}</p>
          <p><strong>Total Enrollment:</strong> {result.total_enrollment}</p>
          <p><strong>Average Attendance Rate:</strong> {result.avg_attendance_rate}</p>
          <p><strong>Instructors:</strong></p>
          <ul>
            {result.instructors.map((name, idx) => (
              <li key={idx}>{name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
