from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, Follow, Course, Lesson

from django.urls import reverse

# python manage.py test  # запуск всех тестов
# python manage.py test college.tests  # запуск тестов конкретного приложения
# python manage.py test college.tests.LessonsTestCase # запуск тестов конкретного класса
# python manage.py test college.tests.CourseTestCase.test_course_retrieve  # запуск конкретного теста
class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            title="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test_lesson", course=self.course, owner=self.user
        )
        self.follow = Follow.objects.create(courses=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("college:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.course.title
        )

    def test_course_create(self):
        url = reverse("college:course-list")
        data = {"title": "Курс1", "description": "Описание курса1", "video_url": "https://www.youtube.com/s"}
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("college:course-detail", args=(self.course.pk,))
        data = {"title": "Курс", "description": "Описание курса", "video_url": "https://www.youtube.com/"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Курс")

    def test_course_delete(self):
        url = reverse("college:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("college:course-list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        res = len(result[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res, 8)

    def test_follow(self):
        url = reverse("users:follow_check", args=(self.course.pk,))
        data = {"id": self.course.pk}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "подписка удалена")


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            title="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test_lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("college:lesson_retriv", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("college:lesson_crete")
        print(self.course.id)
        data = {"title": "Урок", "description": "Описание урока", "course": self.course.id, "video_url": "https://www.youtube.com/1",}
        response = self.client.post(url, data)
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("college:lesson_update", args=(self.lesson.pk,))
        data = {"title": "Урок3", "description": "Описание урока3", "video_url": "https://www.youtube.com/1",}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Урок3")

    def test_lesson_delete(self):
        url = reverse("college:lesson_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("college:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        res = len(result[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(res, 6)