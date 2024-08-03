from functools import wraps
from user_interaction import AddressBook, Record
import pickle

def input_error(func):
    @wraps(func)

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Not existing user name"
        except ValueError as v:
            return f'Error: {v}'
        except IndexError:
            return "Enter user name."
        except Exception as e:
            return f'Unknown error: {str(e)}'   

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):

    name, phone, *_ = args
    record = book.find(name)
    message = f"Contact {name} updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact {name} added."
    if phone:
        record.add_phone(phone)

    return message

@input_error
def change_contact(args, book: AddressBook):
    name, current_phone, new_phone = args
    record = book.find(name)

    if record is None:
        raise KeyError
    
    return record.edit_phone(current_phone, new_phone)

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]

    if not args:
        raise IndexError
    
    record = book.find(name)

    if record is None:
        raise KeyError
    
    return str(record)
             
def show_all(book: AddressBook):
    result = []

    for record in book.values():
        result.append(str(record))

    if not result:
        return 'You dont have any contacts'

    return '\n'.join(result)

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)

    if record is None:
        raise KeyError

    return record.add_birthday(birthday)

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError
    
    if record.birthday:
        return f"{name}'s birthday is {record.birthday.value}"
    else:
        return f"No birthday set for {name}"

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthday = book.get_upcoming_birthdays()
    
    result = []

    for birthday in upcoming_birthday:
        result.append(f"Upcoming birthday: {birthday['name']} on {birthday['congratulation_date']}")
        return '\n'.join(result)
    
    if not upcoming_birthday:
        return "No upcoming birthdays within the next 7 days."
    
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()