import type {
  Course,
  CourseDetail,
  Lecture,
  Mentor,
  MentorDetail,
  Subject,
  Tutor,
  TutorDetail,
} from "./types";

// Base URL of the backend API. Set VITE_API_URL in a .env file to change it.
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

// Thrown when the server answers with an error. Keeps the HTTP status,
// so a page can tell "not found" (404) apart from other problems.
export class ApiError extends Error {
  status: number;

  constructor(status: number) {
    super(`API error: ${status}`);
    this.status = status;
  }
}

// Sends a GET request and returns the parsed JSON.
async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`);
  if (!response.ok) {
    throw new ApiError(response.status);
  }
  return response.json() as Promise<T>;
}

export type CourseFilters = {
  subject: string; // subject slug, "" means all subjects
  level: string; // level value, "" means all levels
};

export function getCourses(filters: CourseFilters): Promise<Course[]> {
  // Only send the filters the user actually picked.
  const params = new URLSearchParams();
  if (filters.subject) params.set("subject", filters.subject);
  if (filters.level) params.set("level", filters.level);
  const query = params.toString();
  return getJson<Course[]>(query ? `/courses/?${query}` : "/courses/");
}

// The id comes from the page address (/courses/:id), so it is a string.
// encodeURIComponent stops odd addresses like /courses/a%2Fb from changing the API path.
export function getCourse(id: string): Promise<CourseDetail> {
  return getJson<CourseDetail>(`/courses/${encodeURIComponent(id)}/`);
}

export function getSubjects(): Promise<Subject[]> {
  return getJson<Subject[]>("/subjects/");
}

export function getTutors(): Promise<Tutor[]> {
  return getJson<Tutor[]>("/tutors/");
}

export function getTutor(id: string): Promise<TutorDetail> {
  return getJson<TutorDetail>(`/tutors/${encodeURIComponent(id)}/`);
}

export function getMentors(): Promise<Mentor[]> {
  return getJson<Mentor[]>("/mentors/");
}

export function getMentor(id: string): Promise<MentorDetail> {
  return getJson<MentorDetail>(`/mentors/${encodeURIComponent(id)}/`);
}

export function getLectures(): Promise<Lecture[]> {
  return getJson<Lecture[]>("/lectures/");
}

export function getLecture(id: string): Promise<Lecture> {
  return getJson<Lecture>(`/lectures/${encodeURIComponent(id)}/`);
}
