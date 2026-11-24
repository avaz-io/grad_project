from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("subjects", views.SubjectViewSet, basename="subject")
router.register("courses", views.CourseViewSet, basename="course")

urlpatterns = router.urls
