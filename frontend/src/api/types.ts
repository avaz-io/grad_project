// Shapes of the JSON returned by the public API (see the backend serializers).
// Decimal fields (prices, ratings) arrive as strings, for example "150000.00".
// All prices are in Uzbek so'm.

export type SubjectShort = {
  slug: string;
  name_en: string;
  name_uz: string;
};

export type Subject = SubjectShort & {
  id: number;
  uses_cefr: boolean;
};

export type Course = {
  id: number;
  title: string;
  subject: SubjectShort;
  level: string;
  language: string;
  price: string;
  educator_name: string;
  lesson_count: number;
  created_at: string;
};

export type LessonOutline = {
  id: number;
  order: number;
  title: string;
  lesson_type: "video" | "pdf" | "quiz";
  duration_minutes: number | null;
  is_free_preview: boolean;
};

// GET /courses/<id>/ returns the list fields plus these.
export type CourseDetail = Course & {
  description: string;
  lessons: LessonOutline[];
};

// A time slot nobody has booked yet (tutors and mentors share them).
export type FreeSlot = {
  id: number;
  starts_at: string;
  ends_at: string;
  price: string;
};

export type TutorSubject = SubjectShort & {
  min_level: string;
  max_level: string;
};

export type Tutor = {
  id: number;
  name: string;
  hourly_rate: string;
  languages: string[];
  subjects: TutorSubject[];
  rating_avg: string;
  rating_count: number;
};

export type TutorDetail = Tutor & {
  bio: string;
  free_slots: FreeSlot[];
};

export type Mentor = {
  id: number;
  name: string;
  topics: string;
  default_price: string;
  languages: string[];
  rating_avg: string;
  rating_count: number;
};

export type MentorDetail = Mentor & {
  bio: string;
  free_slots: FreeSlot[];
};

// The list and the detail endpoint return the same fields for lectures.
export type Lecture = {
  id: number;
  title: string;
  description: string;
  subject: SubjectShort;
  language: string;
  lecture_type: "recorded" | "live";
  video_file: string | null;
  starts_at: string | null;
  duration_minutes: number | null;
  speaker_name: string;
  created_at: string;
};

// All level values the backend accepts (Level in backend/apps/courses/models.py).
export const LEVELS = [
  "beginner", "intermediate", "advanced", "a1", "a2", "b1", "b2", "c1", "c2",
];
