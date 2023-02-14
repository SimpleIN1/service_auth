
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, password_changed
from django.db.models import Q
from django.conf import settings

from rest_framework import serializers, exceptions, status
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class BaseOverrideSerializer(serializers.Serializer):
    def is_valid(self, *, raise_exception=False):
        # This implementation is the same as the default,
        # except that we use lists, rather than dicts, as the empty case.
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = []
                self._errors = exc.detail
            else:
                self._errors = []

        if self._errors and raise_exception:
            raise ValidationError({'fields': self.errors})

        return not bool(self._errors)


class EmailSerializer(BaseOverrideSerializer):
    email = serializers.EmailField()


class PasswordSerializer(BaseOverrideSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    re_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        data = super(PasswordSerializer, self).validate(attrs)
        # print(attrs)
        # print(data)
        password = data.get('password', None)
        re_password = data.get('re_password', None)

        if password is not None and re_password is not None:
            if data['password'] != data['re_password']:
                raise serializers.ValidationError({'re_password': settings.ERRORS['fields_error']['16']})

            del data['re_password']
        # elif password is None:
        #     pass
        # elif re_password is None:
        #     raise serializers.ValidationError({'re_password': settings.ERROR['fields_error']['15']})

        return data

    def validate_password(self, password):
        validate_password(password, user=User)
        return super(PasswordSerializer, self).validate(password)




class UserSerializer(EmailSerializer, PasswordSerializer):
    last_name = serializers.CharField(
        max_length=150,
    )
    first_name = serializers.CharField(
        max_length=150,
    )
    middle_name = serializers.CharField(
        max_length=150,
        required=False,
    )
    organization_name = serializers.CharField(
        max_length=400,
    )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):

        # instance.email = validated_data.pop('email', instance.email)

        instance.last_name = validated_data.pop('last_name', instance.last_name)
        instance.first_name = validated_data.pop('first_name', instance.first_name)
        instance.middle_name = validated_data.pop('middle_name', instance.middle_name)
        instance.organization_name = validated_data.pop('organization_name', instance.organization_name)

        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        instance.save()

        # return super().update(instance, validated_data)
        return instance

    def validate_email(self, email):
        if self.context.__contains__('request'):
            request = self.context['request']
            if request.method == 'POST':
                if User.objects.filter(Q(email=email)).exists():
                    raise serializers.ValidationError(settings.ERRORS['fields_error']['18'])
        elif self.instance is not None:
            instance = self.instance
            if User.objects.filter(Q(email=email) & ~Q(id=instance.id)).exists():
                raise serializers.ValidationError(settings.ERRORS['fields_error']['18'])
        return email


class JwtLoginSerializer(EmailSerializer):
    password = serializers.CharField(max_length=128)


class UUIDSerializer(BaseOverrideSerializer):
    uuid = serializers.UUIDField()


class ResetPasswordSerializer(
    EmailSerializer,
    PasswordSerializer,
    UUIDSerializer
):
    pass


class ConfirmVerifyEMailSerializer(
    UUIDSerializer,
    EmailSerializer
):
    pass
