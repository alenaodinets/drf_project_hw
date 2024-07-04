from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import VideoLinkValidator
from users.serializer import UserSerializer


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoLinkValidator(field="video_link")]


class CourseDetailSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lesson_set = LessonSerializer(many=True)
    subscription = SerializerMethodField()

    def get_count_lesson_in_course(self, lesson):
        return Lesson.object.filter(course=lesson.course).count()

    class Meta:
        model = Course
        fields = ("title", "description", "count_lesson_in_course", "lesson_set")


class SubscriptionSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"
