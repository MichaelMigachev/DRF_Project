from rest_framework import serializers

from college.models import Course, Lesson
from college.validators import validate_not_forbidden


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_not_forbidden])

    class Meta:
        model = Lesson
        # fields = "__all__"
        exclude = ['owner']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    video_url = serializers.URLField(validators=[validate_not_forbidden])

    class Meta:
        model = Course
        fields = "__all__"

    @staticmethod
    def get_lesson_count(obj):
        return obj.lessons.count()
