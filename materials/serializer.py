from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lesson_set = LessonSerializer(many=True)

    def get_count_lesson_in_course(self, lesson):
        return Lesson.object.filter(course=lesson.course).count()

    class Meta:
        model = Course
        fields = ("title", "description", "count_lesson_in_course", "lesson_set")
