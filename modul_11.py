import datetime
import re
from collections import UserDict

def _now():
    return datetime.datetime.today()

def _create_date(*, year, month, day):
    return datetime.datetime(year=year, month=month, day=day).date()




class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        print("Perform some validation")
        self._value = f"Overriden {value}"

class Birthday(Field):
    @property
    def value(self) -> datetime.datetime.date:
        return self._value

    @value.setter
    def value(self, value):
        self._value = datetime.datetime.strptime(value, "%d-%m-%Y")

    def __repr__(self):
        return datetime.datetime.strftime(self._value, "%d-%m-%Y")

class AddressBook(UserDict):
    __items_per_page = None


    def items_per_page(self, value):
        self.__items_per_page = value

    items_per_page = property(fget=None, fset=items_per_page)


    def add_contact(self, name: Name, phone: Phone = None):
        contact = Record(name=name, phone=phone)
        self.data[name.value] = contact

    def add_record(self, record: "Record"):
        self.data[record.name.value] = record

    def find_by_name(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None

    def find_by_phone(self, phone: str):
        for record in self.data.values():
            if phone in [number.value for number in record.phones]:
                return record
            return None

    def __iter__(self):
        self.page = 0
        return self

    def __next__(self):
        records = list(self.data.items())
        start_index = self.page * self.__items_per_page
        end_index = (self.page + 1) * self.__items_per_page
        self.page += 1
        if len(records) > end_index:
            to_return = records[start_index:end_index]
        else:
            if len(records) > start_index:
                to_return = records[start_index: len(records)]
            else:
                to_return = records[:-1]
        self.page += 1
        return [{record[1], record[0]} for record in to_return]


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None ):
        self.name: Name = name
        self.phones: list[Phone] = [phone] if phone is not None else []
        self.birthday = birthday

    def days_to_birthday(self):
        now = _now()
        if self.birthday is not None:
            birthday: datetime.datetime.date = self.birthday.value.date()
            next_birthday = _create_date(year=now.year, month=birthday.month, day=birthday.day)
            if birthday < next_birthday:
                next_birthday = _create_date(year=next_birthday.year + 1, month=next_birthday.month, day=next_birthday.day)
            return (next_birthday - birthday).days
        return None


    def add_phone(self, phone_number: Phone):
        self.phones.append(phone_number)


    def change_phone(self, old_number: Phone, new_number: Phone):
        try:
            self.phones.remove(old_number)
            self.phones.append(new_number)
        except ValueError:
            return f"{old_number} does not exist"


    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"{phone} does not exist"


if __name__ == "__main__":
    addr = AddressBook()
    for x in range(35):
        addr.add_record(Record(Name(f"name_{x}")))
    gen = iter(addr)
    print(next(gen))