from django.db import IntegrityError
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Child
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ChildSerializer,
    ChildCreateUpdateSerializer,
)


# =========================================================
# HELPERS
# =========================================================

def make_user(phone="+919876543210", password="test12345", **extra):
    extra.setdefault("full_name", "Test Parent")
    return User.objects.create_user(phone=phone, password=password, **extra)


# =========================================================
# USER MANAGER TESTS
# =========================================================

class UserManagerTests(APITestCase):

    def test_create_user_requires_phone(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(phone="", password="test12345", full_name="No Phone")

    def test_create_user_hashes_password(self):
        user = make_user()
        self.assertNotEqual(user.password, "test12345")
        self.assertTrue(user.check_password("test12345"))

    def test_create_user_defaults(self):
        user = make_user()
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_verified)

    def test_create_superuser_sets_flags(self):
        admin = User.objects.create_superuser(
            phone="+919876500000",
            password="adminpass123",
            full_name="Admin",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_verified)

    def test_create_superuser_rejects_is_staff_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone="+919876500001",
                password="adminpass123",
                full_name="Admin",
                is_staff=False,
            )

    def test_create_superuser_rejects_is_superuser_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone="+919876500002",
                password="adminpass123",
                full_name="Admin",
                is_superuser=False,
            )


# =========================================================
# USER MODEL TESTS
# =========================================================

class UserModelTests(APITestCase):

    def test_str_representation(self):
        user = make_user(full_name="Jane Doe")
        self.assertEqual(str(user), f"Jane Doe ({user.phone})")

    def test_phone_must_be_unique(self):
        make_user(phone="+919876543210")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                phone="+919876543210",
                password="other12345",
                full_name="Duplicate",
            )

    def test_username_field_is_phone(self):
        self.assertEqual(User.USERNAME_FIELD, "phone")


# =========================================================
# CHILD MODEL TESTS
# =========================================================

class ChildModelTests(APITestCase):

    def setUp(self):
        self.parent = make_user()

    def test_child_linked_to_parent(self):
        child = Child.objects.create(
            parent=self.parent,
            name="Kiddo",
            school_name="Greenwood High",
            grade="5",
        )
        self.assertIn(child, self.parent.children.all())

    def test_str_representation(self):
        child = Child.objects.create(
            parent=self.parent,
            name="Kiddo",
            school_name="Greenwood High",
            grade="5",
        )
        self.assertEqual(str(child), f"Kiddo - {self.parent.full_name}")

    def test_default_is_active_true(self):
        child = Child.objects.create(
            parent=self.parent,
            name="Kiddo",
            school_name="Greenwood High",
            grade="5",
        )
        self.assertTrue(child.is_active)


# =========================================================
# SERIALIZER TESTS
# =========================================================

class UserRegistrationSerializerTests(APITestCase):

    def test_valid_data_creates_user(self):
        serializer = UserRegistrationSerializer(data={
            "phone": "+919876543210",
            "password": "test12345",
            "full_name": "Test Parent",
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertTrue(user.check_password("test12345"))

    def test_password_too_short_is_rejected(self):
        serializer = UserRegistrationSerializer(data={
            "phone": "+919876543210",
            "password": "short",
            "full_name": "Test Parent",
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_duplicate_phone_is_rejected(self):
        make_user(phone="+919876543210")
        serializer = UserRegistrationSerializer(data={
            "phone": "+919876543210",
            "password": "test12345",
            "full_name": "Another Parent",
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)

    def test_duplicate_email_is_rejected(self):
        make_user(phone="+919876543210", email="parent@example.com")
        serializer = UserRegistrationSerializer(data={
            "phone": "+919876543211",
            "password": "test12345",
            "full_name": "Another Parent",
            "email": "parent@example.com",
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_email_is_lowercased(self):
        serializer = UserRegistrationSerializer(data={
            "phone": "+919876543210",
            "password": "test12345",
            "full_name": "Test Parent",
            "email": "Parent@Example.COM",
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, "parent@example.com")

    def test_full_name_is_required(self):
        serializer = UserRegistrationSerializer(data={
            "phone": "+919876543210",
            "password": "test12345",
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn("full_name", serializer.errors)


class UserSerializerTests(APITestCase):

    def test_nested_children_included(self):
        parent = make_user()
        Child.objects.create(
            parent=parent,
            name="Kiddo",
            school_name="Greenwood High",
            grade="5",
        )
        data = UserSerializer(parent).data
        self.assertEqual(len(data["children"]), 1)
        self.assertEqual(data["children"][0]["name"], "Kiddo")

    def test_password_not_exposed(self):
        parent = make_user()
        data = UserSerializer(parent).data
        self.assertNotIn("password", data)


class UserUpdateSerializerTests(APITestCase):

    def test_updates_full_name_and_email(self):
        parent = make_user()
        serializer = UserUpdateSerializer(
            parent,
            data={"full_name": "Updated Name", "email": "new@example.com"},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.full_name, "Updated Name")
        self.assertEqual(updated.email, "new@example.com")

    def test_rejects_email_used_by_another_user(self):
        make_user(phone="+919876543210", email="taken@example.com")
        other = make_user(phone="+919876543211")
        serializer = UserUpdateSerializer(
            other,
            data={"email": "taken@example.com"},
            partial=True,
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_allows_keeping_own_email(self):
        parent = make_user(email="mine@example.com")
        serializer = UserUpdateSerializer(
            parent,
            data={"full_name": "Same Email", "email": "mine@example.com"},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)


class ChildSerializerTests(APITestCase):

    def test_expected_fields_present(self):
        parent = make_user()
        child = Child.objects.create(
            parent=parent,
            name="Kiddo",
            school_name="Greenwood High",
            grade="5",
        )
        data = ChildSerializer(child).data
        self.assertEqual(
            set(data.keys()),
            {
                "id", "name", "school_name", "grade", "photo",
                "emergency_contact_name", "emergency_contact_phone",
                "is_active", "created_at", "updated_at",
            },
        )


class ChildCreateUpdateSerializerTests(APITestCase):

    class _FakeRequest:
        def __init__(self, user):
            self.user = user

    def test_create_assigns_parent_from_context(self):
        parent = make_user()
        factory = APIRequestFactory()
        request = self._FakeRequest(parent)

        serializer = ChildCreateUpdateSerializer(
            data={
                "name": "Kiddo",
                "school_name": "Greenwood High",
                "grade": "5",
            },
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        child = serializer.save()
        self.assertEqual(child.parent, parent)


# =========================================================
# API TESTS — REGISTER
# =========================================================

class RegisterViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("accounts:register")

    def test_register_returns_tokens(self):
        response = self.client.post(self.url, {
            "phone": "+919876543210",
            "password": "test12345",
            "full_name": "Test Parent",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])
        self.assertEqual(response.data["user"]["phone"], "+919876543210")

    def test_register_with_duplicate_phone_fails(self):
        make_user(phone="+919876543210")

        response = self.client.post(self.url, {
            "phone": "+919876543210",
            "password": "test12345",
            "full_name": "Another Parent",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_short_password_fails(self):
        response = self.client.post(self.url, {
            "phone": "+919876543210",
            "password": "short",
            "full_name": "Test Parent",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_creates_user_in_db(self):
        self.client.post(self.url, {
            "phone": "+919876543210",
            "password": "test12345",
            "full_name": "Test Parent",
        }, format="json")

        self.assertTrue(User.objects.filter(phone="+919876543210").exists())


# =========================================================
# API TESTS — LOGIN
# =========================================================

class LoginViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("accounts:login")
        self.user = make_user(phone="+919876543210", password="test12345")

    def test_login_returns_tokens(self):
        response = self.client.post(self.url, {
            "phone": "+919876543210",
            "password": "test12345",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(self.url, {
            "phone": "+919876543210",
            "password": "wrongpassword",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_unknown_phone_fails(self):
        response = self.client.post(self.url, {
            "phone": "+919876500099",
            "password": "test12345",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_fields_fails(self):
        response = self.client.post(self.url, {
            "phone": "+919876543210",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user_rejected(self):
        # Django's ModelBackend.authenticate() rejects inactive users via
        # user_can_authenticate() before LoginView's own is_active check
        # ever runs, so this currently surfaces as a generic 401 rather
        # than the 403 "Account is disabled" branch in the view.
        self.user.is_active = False
        self.user.save()

        response = self.client.post(self.url, {
            "phone": "+919876543210",
            "password": "test12345",
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# =========================================================
# API TESTS — PROFILE
# =========================================================

class ProfileViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("accounts:profile")
        self.user = make_user(phone="+919876543210", password="test12345")
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_get_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_returns_own_profile(self):
        self._auth()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "+919876543210")

    def test_patch_updates_full_name(self):
        self._auth()
        response = self.client.patch(self.url, {"full_name": "New Name"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, "New Name")

    def test_patch_with_taken_email_fails(self):
        make_user(phone="+919876543211", email="taken@example.com")
        self._auth()
        response = self.client.patch(self.url, {"email": "taken@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# =========================================================
# API TESTS — LOGOUT
# =========================================================

class LogoutViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("accounts:logout")
        self.user = make_user(phone="+919876543210", password="test12345")
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_logout_blacklists_refresh_token(self):
        self._auth()
        response = self.client.post(self.url, {"refresh": str(self.refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_requires_authentication(self):
        response = self.client.post(self.url, {"refresh": str(self.refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_missing_refresh_fails(self):
        self._auth()
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_invalid_refresh_fails(self):
        self._auth()
        response = self.client.post(self.url, {"refresh": "not-a-real-token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# =========================================================
# API TESTS — TOKEN REFRESH
# =========================================================

class TokenRefreshViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("accounts:token_refresh")
        self.user = make_user(phone="+919876543210", password="test12345")

    def test_refresh_returns_new_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.url, {"refresh": str(refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_with_invalid_token_fails(self):
        response = self.client.post(self.url, {"refresh": "not-a-real-token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
