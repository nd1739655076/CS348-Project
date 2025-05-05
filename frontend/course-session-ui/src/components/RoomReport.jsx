import { useState, useEffect } from "react";
import "./RoomReport.css";

export default function RoomReport() {
  const [rooms, setRooms] = useState([]);
  const [selectedId, setSelectedId] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/report/rooms")
      .then(res => res.json())
      .then(data => setRooms(data))
      .catch(err => console.error("Failed to load rooms", err));
  }, []);

  const fetchReport = async () => {
    const res = await fetch(`http://localhost:5000/report/room?room_id=${selectedId}`);
    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="room-report-container">
      <h2>🏢 Room Report</h2>
      <select value={selectedId} onChange={e => setSelectedId(e.target.value)}>
        <option value="">Select a room</option>
        {rooms.map(room => (
          <option key={room.id} value={room.id}>
            {room.label}
          </option>
        ))}
      </select>

      <button onClick={fetchReport} disabled={!selectedId}>
        Fetch Report
      </button>

      {result && (
        <div className="room-report-results">
          <h3>Room: {result.room_label}</h3>
          <p><strong>Max Capacity:</strong> {result.max_capacity}</p>
          <p><strong>Total Sessions:</strong> {result.total_sessions}</p>
          <p><strong>Average Enrolled:</strong> {result.avg_enrolled}</p>
          <p><strong>Courses Held:</strong></p>
          <ul>
            {result.courses.map((course, idx) => (
              <li key={idx}>{course}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
