from rest_framework import serializers

from users.models import User, Payment


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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
