import type { Course, Lecture, Mentor, Subject, Tutor } from "./types";

// Base URL of the backend API. Set VITE_API_URL in a .env file to change it.
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

// Sends a GET request and returns the parsed JSON, or throws if the server answers with an error.
async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
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

export function getSubjects(): Promise<Subject[]> {
  return getJson<Subject[]>("/subjects/");
}

export function getTutors(): Promise<Tutor[]> {
  return getJson<Tutor[]>("/tutors/");
}

export function getMentors(): Promise<Mentor[]> {
  return getJson<Mentor[]>("/mentors/");
}

export function getLectures(): Promise<Lecture[]> {
  return getJson<Lecture[]>("/lectures/");
}
