// api.js

const BASE = "http://localhost:5000";

export async function getCourses() {
  const res = await fetch(`${BASE}/courses`);
  return res.json();
}

export async function getInstructors() {
  const res = await fetch(`${BASE}/instructors`);
  return res.json();
}

export async function getRooms() {
  const res = await fetch(`${BASE}/rooms`);
  return res.json();
}

export async function getSessions() {
  const res = await fetch(`${BASE}/sessions`);
  return res.json();
}

export async function addSession(data) {
  const res = await fetch(`${BASE}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

// try:
//     with db.session.begin():
//         db.session.add(new_session)
// except Exception as e:
//     db.session.rollback()
//     print("Transaction failed:", e)

export async function deleteSession(id) {
  const res = await fetch(`${BASE}/sessions/${id}`, {
    method: "DELETE",
  });
  return res.json();
}

export async function updateSession(id, data) {
  const res = await fetch(`${BASE}/sessions/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function getReport({ start_date, end_date, room_id, instructor_id, course_id }) {
  const params = new URLSearchParams();

  if (start_date) params.append("start_date", start_date);
  if (end_date) params.append("end_date", end_date);
  if (room_id) params.append("room_id", room_id);
  if (instructor_id) params.append("instructor_id", instructor_id);
  if (course_id) params.append("course_id", course_id);

  const response = await fetch(`${BASE}/report/summary?${params.toString()}`);
  if (!response.ok) {
    throw new Error("Failed to fetch report");
  }
  return await response.json();
}
