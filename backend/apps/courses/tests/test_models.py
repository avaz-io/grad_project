import pytest
from django.db import IntegrityError, transaction

from apps.courses.models import Course, Enrollment, Lesson


@pytest.mark.django_db
def test_student_cannot_enrol_twice_in_same_course(student, course):
    Enrollment.objects.create(student=student, course=course)

    # transaction.atomic() keeps the test's own transaction usable after the error.
    with pytest.raises(IntegrityError), transaction.atomic():
        Enrollment.objects.create(student=student, course=course)

    assert Enrollment.objects.filter(student=student, course=course).count() == 1


@pytest.mark.django_db
def test_two_students_can_enrol_in_same_course(student, other_student, course):
    Enrollment.objects.create(student=student, course=course)
    Enrollment.objects.create(student=other_student, course=course)

    assert set(course.students.all()) == {student, other_student}


@pytest.mark.django_db
def test_lesson_order_is_unique_inside_a_course(course):
    Lesson.objects.create(course=course, title="Intro", lesson_type="video", order=1)

    with pytest.raises(IntegrityError), transaction.atomic():
        Lesson.objects.create(course=course, title="Also first?", lesson_type="pdf", order=1)


@pytest.mark.django_db
def test_course_price_cannot_be_negative(educator, subject):
    with pytest.raises(IntegrityError), transaction.atomic():
        Course.objects.create(
            educator=educator, subject=subject, title="Bad", level="beginner", language="en", price="-1"
        )
