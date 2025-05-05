import React, { useEffect, useState } from "react";
import "./SessionForm.css";
import {
  getCourses,
  getInstructors,
  getRooms,
  addSession,
  updateSession
} from "../api";

export default function SessionForm({ onAdd, editingSession }) {
  const [courses, setCourses] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [form, setForm] = useState({
    course_id: "",
    instructor_id: "",
    room_id: "",
    date: "",
    time: "",
    duration: "",
    enrolledCount: 0,
    attendedCount: 0,
    description: ""
  });


  useEffect(() => {
    async function load() {
      setCourses(await getCourses());
      setInstructors(await getInstructors());
      setRooms(await getRooms());
    }
    load();
  }, []);

  useEffect(() => {
    if (editingSession) {
      setForm({
        id: editingSession.id,
        course_id: editingSession.course_id,
        instructor_id: editingSession.instructor_id,
        room_id: editingSession.room_id,
        date: editingSession.date,
        time: editingSession.time,
        duration: editingSession.duration,
        enrolledCount: editingSession.enrolledCount,
        attendedCount: editingSession.attendedCount,
        description: editingSession.description
      });
    } else {
      // Reset form if not editing
      setForm({
        course_id: "",
        instructor_id: "",
        room_id: "",
        date: "",
        time: "",
        duration: "",
        enrolledCount: 0,
        attendedCount: 0,
        description: ""
      });
    }
  }, [editingSession]);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (form.id) {
      const response = await updateSession(form.id, form);
      if (response) {
        alert("Update successfully!");
      }
      else {
        alert("Failed to update, please try again");
      }
    } else {
      const response = await addSession(form);
      if (response) {
        alert ("Add successfully!");
      }
      else {
        alert("Failed to add. Please try again!");
      }
    }
    onAdd();
  }

  return (
    <form onSubmit={handleSubmit} className="session-form">
      <h2 className="form-title">
        {form.id ? "Edit Course Session" : "💻Create a New Course Session"}
      </h2>

      <div className="form-group">
        <label>Course</label>
        <select
          name="course_id"
          value={form.course_id}
          onChange={handleChange}
          required
        >
          <option value="">Select Course</option>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>
              {c.title}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Instructor</label>
        <select
          name="instructor_id"
          value={form.instructor_id}
          onChange={handleChange}
          required
        >
          <option value="">Select Instructor</option>
          {instructors.map((i) => (
            <option key={i.instructor_id} value={i.instructor_id}>
              {i.name}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Room</label>
        <select
          name="room_id"
          value={form.room_id}
          onChange={handleChange}
          required
        >
          <option value="">Select Room</option>
          {rooms.map((r) => (
            <option key={r.id} value={r.id}>
              {r.building} {r.number}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Date</label>
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Time</label>
        <input
          type="time"
          name="time"
          value={form.time}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Duration (minutes)</label>
        <input
          type="number"
          name="duration"
          value={form.duration}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Enrolled Count</label>
        <input
          type="number"
          name="enrolledCount"
          value={form.enrolledCount}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>Attended Count</label>
        <input
          type="number"
          name="attendedCount"
          value={form.attendedCount}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>Description</label>
        <textarea
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Session description (optional)"
        />
      </div>

      <button type="submit" className="submit-btn">
        {form.id ? "Update Session" : "Add Session"}
      </button>
    </form>
  );
}
