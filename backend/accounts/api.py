import os
from ninja import Router, File, Form
from ninja.files import UploadedFile
from ninja.security import django_auth, django_auth_superuser
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from django.http import Http404
from django.db import IntegrityError
from core.utils.auth import is_admin
from core.schemas import MessageSchema
from .utils.tokens import user_tokenizer_generate
from .utils.emails import send_verification_email
from .models import Profile
from .schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserOutSchema,
    ProfileBaseSchema,
    AdminCreateUserSchema,
    AdminUserUpdateSchema,
)

import logging
logger = logging.getLogger(__name__)

User = get_user_model()
router = Router(tags=["Accounts"])

# -------------------------------------------------
# AUTHENTICATION
# -------------------------------------------------
# @router.get("/set-csrf-token", auth=None, response=MessageSchema)
# def get_csrf_token(request):
#     return {"detail": get_token(request)}

@router.get("/set-csrf-token", auth=None, response=MessageSchema)
@csrf_exempt
def set_csrf_token(request):
    """Sets the CSRF cookie for clients (Swagger UI / browsers)."""
    return {"detail": "CSRF totken set"}

@router.post(
    "/register", 
    response={
        201: MessageSchema, 
        400: MessageSchema, 
        422: MessageSchema, 
        500: MessageSchema
    }
)
def register(request, payload: UserRegisterSchema):
    """
    Collects new user credentials. Sends verification email after sign up.
    """
    try:
        # Check if username or email already exists (DB-level guard + friendly error)
        if User.objects.filter(username=payload.username).exists():
            return 422, {"detail": "Username already exists."}
        if User.objects.filter(email=payload.email).exists():
            return 422, {"detail": "Email already exists."}

        user = User.objects.create_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            is_active=False
        )
        
        try:
            result =  send_verification_email(request, user)
            logger.info(f"Email sending result: {result}")
        except Exception as template_err:
            logger.exception("Error rendering email template: %s", template_err)
            return 500, {"detail": "Internal server error (template rendering)."}

        if not result:
            logger.error("Failed to send email.")
            return 500, {"detail": "Error sending verification email"}
        
        logger.info("User saved successfully.")
        return 201, {"detail": "User created and email verification sent"}

    except IntegrityError as e:
        logger.exception(f"Database integrity error: {e}")
        return 422, {"detail": "Email or username already exists."}

    except ValidationError as e:
        logger.exception(f"Validation error: {e}")
        return 400, {"detail": "Invalid registration data."}

    except Exception as e:
        logger.exception(f"An error occurred during registration: {e}")
        return 500, {"detail": "Internal server error"}
    
@router.get(
        "/verify-email/{uidb64}/{token}", 
        response={
            400: MessageSchema, 
            404: MessageSchema, 
            500: MessageSchema
        }
    )
def verify_email(request, uidb64: str, token: str):
    # Decode UID
    try:
        if not uidb64 or not token:
            return 400, {"detail": "Missing verification data."}
        uid = urlsafe_base64_decode(uidb64).decode()
        uid = int(uid)
    except (TypeError, ValueError, OverflowError) as e:
        logger.error(f"Error decoding UID: {e}")
        return 400, {"detail": "Invalid verification data. (UID decode error)"}

    # Find user
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        logger.error(f"User with ID {uid} does not exist.")
        return 404, {"detail": "User not found."}

    # Check token and activate
    try:
        if user_tokenizer_generate.check_token(user, token):
            user.is_active = True
            user.save()
            return 200, {"detail": "Your account is now active!"}
        else:
            return 400, {"detail": "Invalid or expired verification token."}
    except Exception as e:
        logger.error(f"Token processing error: {e}")
        return 500, {"detail": "Verification failed due to server error."}

@router.post("/login", response={200: MessageSchema, 401: MessageSchema})
def login_view(request, payload: UserLoginSchema):
    identifier = payload.username or payload.email
    password = payload.password

    # Resolve username for authentication
    if "@" in identifier:
        try:
            user_obj = User.objects.get(email__iexact=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            raise HttpError(401, "Invalid credentials.")
    else:
        username = identifier

    # Authenticate using the resolved username
    user = authenticate(request, username=username, password=password)
    if user is None:
        raise HttpError(401, "Invalid credentials.")
    if not user.is_active:
        raise HttpError(401, "Account is inactive.")

    login(request, user)
    return 200, {"detail": "Login successful."}

@router.post("/logout", auth=django_auth, response={200: MessageSchema})
def logout_view(request):
    logout(request)
    return 200, {"detail": "Logged out successfully."}


# -------------------------------------------------
# PROFILE MANAGEMENT
# -------------------------------------------------
@router.get(
        "/profile", auth=django_auth, 
        response={200: UserOutSchema, 500: MessageSchema}
    )
def get_profile(request):
    try:
        profile = Profile.objects.filter(user=request.user).first()
        return {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "name": profile.name if profile else "",
            "surname": profile.surname if profile else "",
            "is_active": request.user.is_active,
            "is_staff": request.user.is_staff
        }
    except Exception:
        return 500, {"detail": "Internal server error"}

@router.patch(
        "/profile", auth=django_auth, 
        response={200: ProfileBaseSchema, 500: MessageSchema}
    )
def update_profile(
    request,
    name: str = Form(None),
    surname: str = Form(None),
):
    try:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        fields_to_update = []

        if name is not None:
            profile.name = name
            fields_to_update.append("name")

        if surname is not None:
            profile.surname = surname
            fields_to_update.append("surname")

        if fields_to_update:
            profile.save(update_fields=fields_to_update)

        # Ensure fresh data is returned (reload from DB)
        profile.refresh_from_db()
        return profile
    except Exception:
        return 500, {"detail": "Internal server error"}

@router.post("/upload-profile-image", auth=django_auth)
def upload_profile_image(request, image: UploadedFile = File(...)):
    """
    Handles authenticated user profile image uploads.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Ensure previous image replaced cleanly
    if profile.image:
        if default_storage.exists(profile.image.name):
            default_storage.delete(profile.image.name)

    # Save new image
    profile.image.save(image.name, image)
    profile.save()

    return {
        "detail": "Profile image uploaded successfully.",
        "image": profile.image.url,
    }

@router.delete("/profile", auth=django_auth, response={200: MessageSchema, 500: MessageSchema})
def delete_account(request):
    try:
        user = request.user
        user.delete()
        return 200, {"detail": "User account deleted successfully."}
    except:
        return 500, {"detail": "Internal server error."}

# -------------------------------------------------
# STAFF & ADMIN USER MANAGEMENT
# -------------------------------------------------

@router.post("/users", auth=django_auth, response={201: UserOutSchema, 403: MessageSchema})
def admin_create_user(request, payload: AdminCreateUserSchema):
    if not request.user.is_superuser:
        return 403, {"detail": "Only superadmins can create users."}
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
    )
    user.is_active = payload.is_active
    user.is_staff = payload.is_staff
    user.save()
    Profile.objects.create(
        user=user,
        name=payload.name,
        surname=payload.surname
    )
    return 201, {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "name": payload.name,
        "surname": payload.surname,
        "is_active": user.is_active,
        "is_staff": user.is_staff
    }

@router.get("/users/{user_id}", auth=django_auth, response={200: UserOutSchema, 403: MessageSchema})
def get_user_detail(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    if not (is_admin(request.user) or request.user.id == user.pk):
        return 403, {"detail": "Permission denied."}
    profile = Profile.objects.filter(user=user).first()
    return 200, {
        "id": user.pk,
        "username": user.username,
        "email": user.email,
        "name": profile.name if profile else "",
        "surname": profile.surname if profile else "",
        "is_active": user.is_active,
        "is_staff": user.is_staff
    }

@router.patch("/users/{user_id}", auth=django_auth, response={200: UserOutSchema, 403: MessageSchema})
def update_user_detail(request, user_id: int, data: AdminUserUpdateSchema):
    target_user = get_object_or_404(User, pk=user_id)
    if not (request.user.is_superuser or request.user.id == target_user.pk):
        return 403, {"detail": "Permission denied."}
    update_data = data.dict(exclude_unset=True)
    if "password" in update_data:
        target_user.set_password(update_data.pop("password"))
    for k, v in update_data.items():
        setattr(target_user, k, v)
    target_user.save()

    profile = Profile.objects.filter(user=target_user).first()
    return 200, {
        "id": target_user.pk,
        "username": target_user.username,
        "email": target_user.email,
        "name": profile.name if profile else "",
        "surname": profile.surname if profile else "",
        "is_active": target_user.is_active,
        "is_staff": target_user.is_staff,
    }

@router.delete("/users/{user_id}", auth=django_auth_superuser, response={200: MessageSchema, 403: MessageSchema})
def admin_delete_user(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    if not (request.user.is_superuser or request.user.id == user.pk):
        return 403, {"detail": "Permission denied."}
    user.delete()
    return 200, {"detail": "User deleted successfully."}