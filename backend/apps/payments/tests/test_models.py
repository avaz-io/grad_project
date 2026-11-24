import pytest
from django.db import IntegrityError, transaction

from apps.courses.models import Enrollment
from apps.payments.models import Payment


@pytest.mark.django_db
def test_payment_for_an_enrollment_is_saved(student, course):
    enrollment = Enrollment.objects.create(student=student, course=course)

    payment = Payment.objects.create(
        user=student, enrollment=enrollment, amount=course.price, provider="fake"
    )

    assert payment.status == "pending"
    assert list(enrollment.payments.all()) == [payment]


@pytest.mark.django_db
def test_payment_must_have_exactly_one_target(student, course, booking):
    enrollment = Enrollment.objects.create(student=student, course=course)

    # Neither an enrolment nor a booking.
    with pytest.raises(IntegrityError), transaction.atomic():
        Payment.objects.create(user=student, amount="10.00", provider="fake")

    # Both at once.
    with pytest.raises(IntegrityError), transaction.atomic():
        Payment.objects.create(
            user=student, enrollment=enrollment, booking=booking, amount="10.00", provider="fake"
        )
