from typing import Dict, Union

from faker import Faker

fake = Faker()

def random_task_dict() -> Dict[str, Union[str, bool]]:
    task_dict = {
        "title": fake.text(max_nb_chars=80),
        "description": fake.paragraph(),
        "is_done": False
    }
    return task_dict
