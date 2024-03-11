from rest_framework import serializers
from user.models import ClientUser, Member, Plan, HashUserPassword


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class HashedPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashUserPassword
        fields = "__all__"


# class PlanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Plan
#         fields = "__all__"
