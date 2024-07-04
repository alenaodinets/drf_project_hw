from django.urls import path
from rest_framework.routers import SimpleRouter
from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonRetrieveAPIView,
    LessonListApiView,
    LessonDestroyAPIView,
    LessonUpdateAPIView,
    SubscriptionAPIView,
    PaymentCreateAPIView,
)

app_name = MaterialsConfig.name
router = SimpleRouter()
router.register("", CourseViewSet)


urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons_update"
    ),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lessons_delete",
    ),
    path("course/<int:pk>/subscribe/", SubscriptionAPIView.as_view(), name="subscribe"),
    path("payment/create", PaymentCreateAPIView.as_view(), name="payment_create"),
]

urlpatterns += router.urls
