from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


# =========================
# USER MANAGER
# =========================

class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):

        if not phone:
            raise ValueError("Phone number is required")

        user = self.model(
            phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            phone,
            password,
            **extra_fields
        )


# =========================
# USER MODEL
# =========================

class User(AbstractBaseUser, PermissionsMixin):

    phone = PhoneNumberField(
        unique=True,
        db_index=True
    )

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )

    full_name = models.CharField(
        max_length=255
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"


# =========================
# CHILD MODEL
# =========================

class Child(models.Model):

    GRADE_CHOICES = [
        ("NURSERY", "Nursery"),
        ("LKG", "LKG"),
        ("UKG", "UKG"),

        ("1", "Class 1"),
        ("2", "Class 2"),
        ("3", "Class 3"),
        ("4", "Class 4"),
        ("5", "Class 5"),
        ("6", "Class 6"),
        ("7", "Class 7"),
        ("8", "Class 8"),
        ("9", "Class 9"),
        ("10", "Class 10"),
        ("11", "Class 11"),
        ("12", "Class 12"),
    ]

    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="children"
    )

    name = models.CharField(
        max_length=255
    )

    school_name = models.CharField(
        max_length=255,
        db_index=True
    )

    grade = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES
    )

    photo = models.ImageField(
        upload_to="children/photos/",
        blank=True,
        null=True
    )

    emergency_contact_name = models.CharField(
        max_length=255,
        blank=True
    )

    emergency_contact_phone = PhoneNumberField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "children"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.parent.full_name}"