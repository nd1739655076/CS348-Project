import React, { useEffect, useState } from "react";
import { getSessions, deleteSession } from "../api";
import "./SessionList.css";

export default function SessionList({ reload, onEdit }) {
  const [sessions, setSessions] = useState([]);
  const [expandedSessionId, setExpandedSessionId] = useState(null);

  useEffect(() => {
    getSessions().then(setSessions);
  }, [reload]);

  async function handleDelete(id) {
    if (window.confirm("Are you sure you want to delete this session?")) {
      await deleteSession(id);
      setSessions(await getSessions());
    }
  }

  function toggleDetails(id) {
    setExpandedSessionId(expandedSessionId === id ? null : id);
  }

  return (
    <div className="session-list-container">
      <h2 className="list-title">📅 Scheduled Course Sessions</h2>
      <ul className="session-list">
        {sessions.map((s) => (
          <li
            key={s.id}
            className={`session-item ${expandedSessionId === s.id ? "expanded" : ""}`}
            onClick={() => toggleDetails(s.id)}
          >
            <div className="session-summary">
              <span className="course-title">{s.course}</span>
              <span className="session-time">{s.date} at {s.time}</span>
            </div>

            {expandedSessionId === s.id && (
              <div className="session-details">
                <p><strong>Instructor:</strong> {s.instructor}</p>
                <p><strong>Room:</strong> {s.room}</p>
                <p><strong>Duration:</strong> {s.duration} min</p>
                <p><strong>Enrolled:</strong> {s.enrolledCount}</p>
                <p><strong>Attended:</strong> {s.attendedCount}</p>
                <p><strong>Description:</strong> {s.description || "N/A"}</p>

                <div className="button-group">
                  <button className="edit-btn" onClick={(e) => { e.stopPropagation(); onEdit(s); }}>Edit</button>
                  <button className="delete-btn" onClick={(e) => { e.stopPropagation(); handleDelete(s.id); }}>Delete</button>
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
