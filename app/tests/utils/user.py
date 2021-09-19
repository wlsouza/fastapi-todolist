from typing import Dict

from faker import Faker

fake = Faker()

def random_user_dict() -> Dict[str,str]:
    user_dict = {
        "full_name": fake.name(),
        "email": fake.free_email(),
        "password": fake.password(length=12)
    }
    return user_dict