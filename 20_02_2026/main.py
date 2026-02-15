import json
import re

def edit_name(name:str) -> str:
    return name.strip().lower()

def edit_phone(phone:str) -> str:
    edit_number = re.sub(r'\D', '', phone)

    if not edit_number or len(edit_number)<2:
        return edit_number

    if edit_number[0] == '7':
        edit_number = '+' + edit_number
    elif edit_number[0] == '8':
        edit_number = "+7" + edit_number[1:]
    else:
        edit_number = "+7" + edit_number
    return edit_number


def validate_name(name: str) -> bool:
    if name == "" or len(name)<2:
        return False
    if any(char.isdigit() for char in name):
        return False
    return True

def validate_phone(phone: str) -> bool:
    digits = phone.replace('+', '')
    return 10 <= len(digits) <= 11

def create_json(name:str, phone:str) -> str:
    user_json = {
        "name": name.title(),
        "phone": phone
    }
    return json.dumps(user_json, ensure_ascii=False, indent=4)

def write_in_file(file_path:str, user_json:str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(user_json)

def input_data():
    while True:
        print("Введите имя:")
        name = edit_name(input(">>> "))
        print("Введите номер телефона:")
        phone = edit_phone(input(">>> "))

        if validate_name(name) and validate_phone(phone):
            user_json = create_json(name, phone)
            write_in_file("user_data.json", user_json)
            print("Файл успешно создан")
            break
        else:
            print("Введены не корректные данные. Попробуйте снова")
            continue

def output_data(json_data:str) -> None:
    try:
        data = json.loads(json_data)
        print(f"Статус: {data['status']}")

        for user in data['data']['users']:
            print(f"ID: {user['id']}, Имя: {user['name']}")

    except json.JSONDecodeError as e:
        print(f"Ошибка в формате JSON: {e}")
    except KeyError as e:
        print(f"Ошибка: отсутствует ключ {e} в структуре данных")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == '__main__':
    # input_data()
    response = """
    {
        "status": "OK",
        "data": {
            "users": [
                {"id": 1, "name": "Oleg"},
                {"id": 2, "name": "Maria"}
            ]
        }
    }
    """
    output_data(response)