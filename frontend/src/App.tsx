import { Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import CourseDetail from "./pages/CourseDetail";
import Courses from "./pages/Courses";
import Home from "./pages/Home";
import LectureDetail from "./pages/LectureDetail";
import Lectures from "./pages/Lectures";
import Login from "./pages/Login";
import MentorDetail from "./pages/MentorDetail";
import Mentors from "./pages/Mentors";
import NotFound from "./pages/NotFound";
import Register from "./pages/Register";
import TutorDetail from "./pages/TutorDetail";
import Tutors from "./pages/Tutors";

// Every page is shown inside <Layout> (navigation bar on top, footer at the bottom).
// ":id" is read by the detail page with useParams().
export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/courses/:id" element={<CourseDetail />} />
        <Route path="/tutors" element={<Tutors />} />
        <Route path="/tutors/:id" element={<TutorDetail />} />
        <Route path="/mentors" element={<Mentors />} />
        <Route path="/mentors/:id" element={<MentorDetail />} />
        <Route path="/lectures" element={<Lectures />} />
        <Route path="/lectures/:id" element={<LectureDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
