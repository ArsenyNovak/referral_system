from django.contrib.auth import get_user_model
from rest_framework import serializers

from refsys.models import ClientUser

User = get_user_model()

class NumberSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=20)

    def validate_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Номер должен состоять только из цифр (375331234567).")
        if len(value) < 10:
            raise serializers.ValidationError("В номере телефона должно быть не менее 10 цифр.")
        return value


class CheckNumberSerializer(serializers.Serializer):
    number = serializers.CharField(label='Номер телефона')
    code = serializers.CharField(label='Код', max_length=4, min_length=4)

    def validate_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Номер должен состоять только из цифр (375331234567).")
        if len(value) < 10:
            raise serializers.ValidationError("В номере телефона должно быть не менее 10 цифр.")
        return value


class ListOtherCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'invite_code', 'other_code']

class ClientSerializer(serializers.ModelSerializer):
    referals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'invite_code', 'other_code', 'referals']
        read_only_fields = ['username', 'invite_code', 'referals']

    def validate_other_code(self, value):
        if self.instance and self.instance.other_code:
            if value != self.instance.other_code:
                raise serializers.ValidationError("Изменение поля other_code запрещено, если оно уже заполнено.")
        if not ClientUser.objects.filter(invite_code=value).exists():
            raise serializers.ValidationError("нет пользователя с таким инвайт-кодом")
        return value

    def get_referals(self, obj):
        linked_users = User.objects.filter(other_code=obj.invite_code)
        return list(linked_users.values_list('username', flat=True))
