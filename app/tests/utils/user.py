from typing import Dict, Union

from faker import Faker

fake = Faker()


def random_user_dict() -> Dict[str, Union[str, int, bool]]:
    user_dict = {
        "full_name": fake.name(),
        "email": fake.free_email(),
        "password": fake.password(length=12),
        "is_active": False,
        "is_superuser": False
    }
    return user_dict


def random_active_user_dict() -> Dict[str, Union[str, int, bool]]:
    user_dict = random_user_dict()
    user_dict["is_active"] = True
    return user_dict


def random_active_superuser_dict() -> Dict[str, Union[str, int, bool]]:
    user_dict = random_active_user_dict()
    user_dict["is_superuser"] = True
    return user_dict