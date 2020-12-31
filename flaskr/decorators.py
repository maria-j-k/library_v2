from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(perm):
    def decorator(f)
    @wraps(f)
    def inner(*args, **kwargs):
        if not current_user.can(perm):
            abort(403)
            return f(*args, **kwargs)
        return inner
    return decorator


# role_required
