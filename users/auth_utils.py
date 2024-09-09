import datetime

from core.settings import SECRET_KEY
import jwt

from .models import User


# defining access_token_generator function
def access_token_generator(user, days=29):
    """generates and returns an access token
    Args:
        user (User): The user for which the token will be generated
        days : Number of days the token will be valid
    Returns:
        str: access token
    """

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days, minutes=155),
        'iat': datetime.datetime.utcnow()
    }

    access_token = jwt.encode(payload,
                              SECRET_KEY, algorithm='HS256')

    return access_token


# defining refresh_token_generator function
def refresh_token_generator(user):
    """generates and returns an refresh token
    Args:
        user (User): The user for which the token will be generated
    Returns:
        str: refresh token
    """

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }

    refresh_token = jwt.encode(payload,
                               SECRET_KEY, algorithm='HS256')

    return refresh_token


def generate_username(full_name):
    # Extract first name and last name
    first_name, *last_name_parts = full_name.split()
    last_name = ' '.join(last_name_parts)

    # Generate preliminary username
    username = (first_name[0] + last_name).lower().replace(' ', '_')

    # Append numbers if necessary to make the username unique
    counter = 1
    while len(username) < 5 or User.objects.filter(username=username).exists():
        username = f"{username}{counter}"
        counter += 1

    return username
