"""Fill the database with demo data for local development and the evaluation demo.

Usage:  python manage.py seed_demo

Safe to run many times: every row is looked up by a natural key first
(username, slug, title, ...) and only created if it is missing.
"""
from datetime import datetime, time, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.bookings.models import AvailabilitySlot, MentorProfile, TutorProfile, TutorSubject
from apps.courses.models import Course, Lesson, Subject
from apps.lectures.models import Lecture

# All demo accounts share this password. That is why the command refuses to
# run when DEBUG is off (production) unless --force is given.
DEMO_PASSWORD = "demo12345"

SUBJECTS = [
    # slug, name_en, name_uz, uses_cefr
    ("english", "English", "Ingliz tili", True),
    ("math", "Mathematics", "Matematika", False),
    ("physics", "Physics", "Fizika", False),
    ("programming", "Programming", "Dasturlash", False),
    ("history", "History", "Tarix", False),
]

EDUCATORS = [
    # username, first name, last name
    ("demo_educator_1", "Nodira", "Karimova"),
    ("demo_educator_2", "Jasur", "Rahimov"),
]

COURSES = [
    # title, subject slug, level, language, price, educator index
    ("English Grammar Basics", "english", "a2", "uz", "0.00", 0),
    ("IELTS Writing Task 2", "english", "b2", "en", "25.00", 0),
    ("Speaking with Confidence", "english", "b1", "en", "15.00", 0),
    ("Algebra for Beginners", "math", "beginner", "uz", "0.00", 1),
    ("Calculus I", "math", "intermediate", "en", "30.00", 1),
    ("Mechanics Made Simple", "physics", "beginner", "ru", "10.00", 1),
    ("Electricity and Magnetism", "physics", "advanced", "en", "35.00", 1),
    ("Python from Zero", "programming", "beginner", "uz", "20.00", 0),
    ("Web Development with Django", "programming", "intermediate", "en", "40.00", 0),
    ("History of Central Asia", "history", "beginner", "uz", "0.00", 1),
]

LESSONS = [
    # title, type, duration in minutes, free preview
    ("Introduction", "video", 10, True),
    ("Main topic", "video", 25, False),
    ("Reading material", "pdf", None, False),
    ("Check your knowledge", "quiz", 10, False),
]

LECTURES = [
    # title, subject slug, language, type, days from today (live only)
    ("How to learn a language fast", "english", "en", "recorded", None),
    ("Why mathematics matters", "math", "uz", "recorded", None),
    ("Your first program", "programming", "uz", "recorded", None),
    ("Studying abroad: Q&A", "english", "en", "live", 7),
    ("Physics in everyday life", "physics", "ru", "live", 14),
]

TUTORS = [
    # username, first, last, hourly rate, languages, [(subject, min level, max level)]
    ("demo_tutor_1", "Aziza", "Yusupova", "15.00", ["uz", "en"], [("english", "a1", "b2")]),
    ("demo_tutor_2", "Bekzod", "Tursunov", "20.00", ["en"], [("english", "b1", "c2")]),
    ("demo_tutor_3", "Dilshod", "Ergashev", "12.00", ["uz", "ru"],
     [("math", "beginner", "advanced"), ("physics", "beginner", "intermediate")]),
    ("demo_tutor_4", "Malika", "Saidova", "18.00", ["uz", "en"], [("programming", "beginner", "intermediate")]),
    ("demo_tutor_5", "Otabek", "Nazarov", "10.00", ["uz"], [("history", "beginner", "advanced")]),
]

MENTORS = [
    # username, first, last, topics, default price, languages
    ("demo_mentor_1", "Kamola", "Ismoilova", "university applications, scholarships", "0.00", ["uz", "en"]),
    ("demo_mentor_2", "Sardor", "Aliyev", "career in IT, CV review", "10.00", ["uz", "ru"]),
    ("demo_mentor_3", "Gulnora", "Hasanova", "study planning, exam preparation", "5.00", ["en"]),
]

# Each tutor and mentor gets a one-hour slot at these hours on the next few days.
SLOT_DAYS_AHEAD = [1, 2, 3]
SLOT_HOURS = [10, 15]


class Command(BaseCommand):
    help = "Create demo subjects, courses, lectures, tutors and mentors. Safe to run twice."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", action="store_true", help="Run even when DEBUG is off (not for production)."
        )

    @transaction.atomic  # all or nothing: a failure halfway leaves the database unchanged
    def handle(self, *args, force=False, **options):
        if not settings.DEBUG and not force:
            raise CommandError("DEBUG is off. Demo users have a known password; use --force if you are sure.")

        self.created = 0
        subjects = self.seed_subjects()
        educators = [self.get_user(u, f, l, "educator") for u, f, l in EDUCATORS]
        self.seed_courses(subjects, educators)
        self.seed_lectures(subjects, educators[0])
        self.seed_tutors(subjects)
        self.seed_mentors()

        self.stdout.write(self.style.SUCCESS(
            f"Demo data ready ({self.created} new rows). Demo users' password: {DEMO_PASSWORD}"
        ))

    # ---------- helpers ----------

    def count(self, created):
        """Keep track of how many rows were really created (0 on a second run)."""
        if created:
            self.created += 1

    def get_user(self, username, first_name, last_name, role):
        user, created = get_user_model().objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@example.com",
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
            },
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
        self.count(created)
        return user

    def create_slots(self, host, price):
        # Times are fixed hours on whole days, so running again on the same day finds
        # the same slots. Running on a later day only adds the new future slots.
        today = timezone.localdate()
        for days in SLOT_DAYS_AHEAD:
            for hour in SLOT_HOURS:
                starts_at = timezone.make_aware(datetime.combine(today + timedelta(days=days), time(hour)))
                _, created = AvailabilitySlot.objects.get_or_create(
                    host=host,
                    starts_at=starts_at,
                    defaults={"ends_at": starts_at + timedelta(hours=1), "price": price},
                )
                self.count(created)

    # ---------- one method per kind of data ----------

    def seed_subjects(self):
        subjects = {}
        for slug, name_en, name_uz, uses_cefr in SUBJECTS:
            subject, created = Subject.objects.get_or_create(
                slug=slug, defaults={"name_en": name_en, "name_uz": name_uz, "uses_cefr": uses_cefr}
            )
            self.count(created)
            subjects[slug] = subject
        return subjects

    def seed_courses(self, subjects, educators):
        for title, subject_slug, level, language, price, educator_index in COURSES:
            course, created = Course.objects.get_or_create(
                title=title,
                educator=educators[educator_index],
                defaults={
                    "subject": subjects[subject_slug],
                    "description": f"A demo course: {title}.",
                    "level": level,
                    "language": language,
                    "price": price,
                    "status": Course.Status.APPROVED,
                },
            )
            self.count(created)
            for order, (lesson_title, lesson_type, minutes, preview) in enumerate(LESSONS, start=1):
                _, created = Lesson.objects.get_or_create(
                    course=course,
                    order=order,
                    defaults={
                        "title": lesson_title,
                        "lesson_type": lesson_type,
                        "duration_minutes": minutes,
                        "is_free_preview": preview,
                    },
                )
                self.count(created)

    def seed_lectures(self, subjects, speaker):
        today = timezone.localdate()
        for title, subject_slug, language, lecture_type, days_ahead in LECTURES:
            starts_at = None
            if lecture_type == Lecture.LectureType.LIVE:
                starts_at = timezone.make_aware(datetime.combine(today + timedelta(days=days_ahead), time(18)))
            _, created = Lecture.objects.get_or_create(
                title=title,
                defaults={
                    "created_by": speaker,
                    "subject": subjects[subject_slug],
                    "description": f"A free demo lecture: {title}.",
                    "language": language,
                    "lecture_type": lecture_type,
                    "starts_at": starts_at,
                    "duration_minutes": 60,
                    "is_published": True,
                },
            )
            self.count(created)

    def seed_tutors(self, subjects):
        for username, first, last, rate, languages, teaches in TUTORS:
            user = self.get_user(username, first, last, "tutor")
            profile, created = TutorProfile.objects.get_or_create(
                user=user,
                defaults={
                    "bio": f"Hi, I am {first}. I teach online in small, friendly steps.",
                    "hourly_rate": rate,
                    "languages": languages,
                    "verification_status": "verified",
                },
            )
            self.count(created)
            for subject_slug, min_level, max_level in teaches:
                _, created = TutorSubject.objects.get_or_create(
                    tutor=profile,
                    subject=subjects[subject_slug],
                    defaults={"min_level": min_level, "max_level": max_level},
                )
                self.count(created)
            self.create_slots(user, rate)

    def seed_mentors(self):
        for username, first, last, topics, price, languages in MENTORS:
            user = self.get_user(username, first, last, "mentor")
            _, created = MentorProfile.objects.get_or_create(
                user=user,
                defaults={
                    "bio": f"Hi, I am {first}. Book a session and let's plan your next step.",
                    "topics": topics,
                    "default_price": price,
                    "languages": languages,
                    "verification_status": "verified",
                },
            )
            self.count(created)
            self.create_slots(user, price)
