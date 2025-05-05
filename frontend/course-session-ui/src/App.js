import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopNavBar from "./components/TopNavBar";
import SessionForm from "./components/SessionForm";
import SessionList from "./components/SessionList";
import ReportForm from "./components/ReportForm";
import InstructorReport from "./components/InstructorReport";
import RoomReport from "./components/RoomReport";
import CourseReport from "./components/CourseReport";
import "./App.css";

function App() {
  const [refresh, setRefresh] = useState(false);
  const [editing, setEditing] = useState(null);

  return (
    <Router>
      <div className="App">
        <TopNavBar />
        <Routes>
          <Route path="/" element={
            <>
              <h1>Course Session Manager</h1>
              <SessionForm
                onAdd={() => {
                  setRefresh(!refresh);
                  setEditing(null);
                }}
                editingSession={editing}
              />
              <SessionList reload={refresh} onEdit={setEditing} />
              <hr />
              <ReportForm />
            </>
          } />
          <Route path="/report/instructor" element={<InstructorReport />} />
          <Route path="/report/room" element={<RoomReport />} />
          <Route path="/report/course" element={<CourseReport />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
