from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("lectures", views.LectureViewSet, basename="lecture")

urlpatterns = router.urls
