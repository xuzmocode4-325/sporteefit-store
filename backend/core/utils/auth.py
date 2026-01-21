def is_admin(user):
    return user.is_staff or user.is_superuser