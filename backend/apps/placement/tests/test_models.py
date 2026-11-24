import pytest
from django.db import IntegrityError, transaction

from apps.courses.models import Lesson
from apps.placement.models import PlacementTest, Question


@pytest.mark.django_db
def test_question_belongs_to_exactly_one_owner(subject, course):
    test = PlacementTest.objects.create(subject=subject, title="Math placement")
    lesson = Lesson.objects.create(course=course, title="Quiz 1", lesson_type="quiz", order=1)

    # Valid: one owner each.
    Question.objects.create(placement_test=test, text="2 + 2 = ?")
    Question.objects.create(lesson=lesson, text="3 + 3 = ?")

    # Invalid: no owner.
    with pytest.raises(IntegrityError), transaction.atomic():
        Question.objects.create(text="Orphan question")

    # Invalid: two owners.
    with pytest.raises(IntegrityError), transaction.atomic():
        Question.objects.create(placement_test=test, lesson=lesson, text="Both?")
