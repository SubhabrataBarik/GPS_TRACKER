from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from .models import User, Child


# ==========================================
# CHILD SERIALIZER
# ==========================================

class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child

        fields = [
            "id",
            "name",
            "school_name",
            "grade",
            "photo",
            "emergency_contact_name",
            "emergency_contact_phone",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ==========================================
# USER READ SERIALIZER
# ==========================================

class UserSerializer(serializers.ModelSerializer):

    phone = PhoneNumberField()

    children = ChildSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = User

        fields = [
            "id",
            "phone",
            "email",
            "full_name",
            "is_verified",
            "children",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "is_verified",
            "created_at",
            "updated_at",
        ]


# ==========================================
# USER REGISTRATION SERIALIZER
# ==========================================

class UserRegistrationSerializer(serializers.ModelSerializer):

    phone = PhoneNumberField()

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )

    class Meta:
        model = User

        fields = [
            "phone",
            "email",
            "full_name",
            "password",
        ]

    def validate_email(self, value):

        if value:

            email = value.lower()

            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    "Email already exists"
                )

            return email

        return value

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


# ==========================================
# USER UPDATE SERIALIZER
# ==========================================

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "full_name",
            "email",
        ]

    def validate_email(self, value):

        user = self.instance

        if (
            value and
            User.objects.exclude(id=user.id)
            .filter(email=value)
            .exists()
        ):
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value


# ==========================================
# CHILD CREATE/UPDATE SERIALIZER
# ==========================================

class ChildCreateUpdateSerializer(serializers.ModelSerializer):

    emergency_contact_phone = PhoneNumberField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Child

        fields = [
            "name",
            "school_name",
            "grade",
            "photo",
            "emergency_contact_name",
            "emergency_contact_phone",
            "is_active",
        ]

    def create(self, validated_data):

        user = self.context["request"].user

        child = Child.objects.create(
            parent=user,
            **validated_data
        )

        return child