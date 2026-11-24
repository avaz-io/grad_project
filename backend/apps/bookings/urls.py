from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("tutors", views.TutorViewSet, basename="tutor")
router.register("mentors", views.MentorViewSet, basename="mentor")

urlpatterns = router.urls
