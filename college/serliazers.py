from rest_framework import serializers

from college.models import Course, Lesson
from college.validators import validate_not_forbidden

from users.models import Follow


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_not_forbidden])

    class Meta:
        model = Lesson
        # fields = "__all__"
        exclude = ['owner']


class CourseSerializer(serializers.ModelSerializer):
    follow = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    video_url = serializers.URLField(validators=[validate_not_forbidden])


    class Meta:
        model = Course
        fields = "__all__"

    @staticmethod
    def get_lesson_count(obj):
        return obj.lessons.count()


    def get_follow(self, obj):
        user = self.context['request'].user
        return Follow.objects.filter(user=user, courses=obj).exists()  # Проверяем, если есть запись о подписке