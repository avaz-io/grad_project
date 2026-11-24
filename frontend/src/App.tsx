import { Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import Courses from "./pages/Courses";
import Home from "./pages/Home";
import Lectures from "./pages/Lectures";
import Login from "./pages/Login";
import Mentors from "./pages/Mentors";
import NotFound from "./pages/NotFound";
import Register from "./pages/Register";
import Tutors from "./pages/Tutors";

// Every page is shown inside <Layout> (navigation bar on top, footer at the bottom).
export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/tutors" element={<Tutors />} />
        <Route path="/mentors" element={<Mentors />} />
        <Route path="/lectures" element={<Lectures />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
