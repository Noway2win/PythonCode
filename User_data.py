from datetime import date, datetime
from typing import NamedTuple
from typing import Optional
from urllib.parse import parse_qs

from custom_func import validate_age, name_validation


class User_name(NamedTuple):
    name: str
    surname: str
    age: int
    year: Optional[str]
    valid: Optional[bool]

    @classmethod
    def get_qs_info(cls, qs: str) -> "User_name":
        year = "Wrong Input"
        valid = True
        try:
            keys_and_values = parse_qs(qs, strict_parsing=True)
        except ValueError:
            name = "stranger"
            surname = "Didn't tell"
            age = 0
        name_list = keys_and_values.get("name", ["stranger"])
        name = name_list[0]
        surname_list = keys_and_values.get("surname", ["Didn't tell"])
        surname = surname_list[0]
        age_list = keys_and_values.get("age", [0])
        age = age_list[0]
        errors = {}

        validations = [
            ("name", name_validation, name),
            ("surname", name_validation, surname),
            ("age", validate_age, age),
        ]
        for field, validation, value in validations:
            try:
                validation(value)
            except ValueError as error:
                errors[field] = str(error)
        if "name" in errors:
            name = "Nope"

        if "surname" in errors:
            surname = "Wrong"

        if "age" not in errors:
            age = int(age)
            year = f"You was born at {datetime.now().year - age}"
        else:
            year = "Incorrect value of age"

        if errors:
            valid = False
        return User_name(name=name, surname=surname, age=age, year=year, valid=valid)

