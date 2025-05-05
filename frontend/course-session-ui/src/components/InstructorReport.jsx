import { useState, useEffect } from "react";

export default function InstructorReport() {
  const [instructors, setInstructors] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/instructors")
      .then(res => res.json())
      .then(data => {
        console.log("Loaded instructors:", data);
        setInstructors(data);
      })
      .catch(err => console.error("Failed to load instructors", err));
  }, []);

  const fetchReport = async () => {
    const res = await fetch(`http://localhost:5000/report/instructor?instructor_id=${selectedId}`);
    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="report-form-container">
      <h2>Instructor Report</h2>

      <select
        value={selectedId}
        onChange={e => setSelectedId(e.target.value)}
      >
        <option value="">Select an instructor</option>
        {instructors.map((inst) => (
          <option key={inst.instructor_id} value={inst.instructor_id}>
            {inst.name}
          </option>
        ))}
      </select>

      <button onClick={fetchReport} disabled={!selectedId}>
        Fetch
      </button>

      {result && (
        <div style={{ marginTop: "1rem", textAlign: "left" }}>
          <h4>Total Sessions: {result.total_sessions}</h4>
          <h4>Average Attendance Rate: {result.avg_attendance_rate}</h4>
          <h4>Courses Taught:</h4>
          <ul>
            {result.courses.map((title, idx) => (
              <li key={idx}>{title}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
