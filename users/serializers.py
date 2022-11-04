from typing import Dict, Any
from .models import Person, User
import base64


def serialize_person(person) -> Dict[str, Any]:
    user_id = person.user.id
    user = User.objects.filter(pk=user_id)[0]

    return {
        'email': user.email,
        # 'is_staff': user.is_staff,
        # 'is_active': user.is_active,
        # 'date_joined': user.date_joined.isoformat(),
        'avatar_link': person.avatar_link,
        'gender': person.gender,
        'name': person.name,
        'surname': person.surname,
        'patronymic': person.patronymic,
        'country': person.country,
        'city': person.city,
        'birth_date': person.birth_date,
        'career': person.career.title,
        'itn': person.itn
    }
