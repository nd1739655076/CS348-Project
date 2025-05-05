import { Link } from "react-router-dom";

export default function TopNavBar() {
  return (
    <nav style={{ padding: "1rem", background: "#f0f0f0" }}>
      <Link to ="/"> Home Page </Link> | {" "}
      <Link to="/report/instructor">Instructor Report</Link> |{" "}
      <Link to="/report/room">Room Report</Link> |{" "}
      <Link to="/report/course">Course Report</Link> |{" "}
    </nav>
  );
}