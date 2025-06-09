from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import User, Payment, Follow, Donation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        # fields = (
        #     "id",
        #     "email",
        #     "username",
        #     "phone_number",
        #     "avatar",
        #     "city",
        # )


class UserProfilePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', "avatar",)  # Общая информация, доступная всем


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class FollowSerializer(ModelSerializer):
    follow_check = SerializerMethodField()

    def get_follow_check(self, instance):
        if instance.follow_courses.all().first():
            return instance.follow_courses.all().first().course
        return 0

    class Meta:
        model = Follow
        fields = "__all__"


class DonationSerializer(ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"
