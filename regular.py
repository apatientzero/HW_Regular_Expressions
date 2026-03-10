import csv
import re
from pprint import pprint


def normalize_name(lastname, firstname, surname):
    """Combines the full name from three parts"""
    full_name = ' '.join([lastname, firstname, surname]).split()
    normalized = ['', '', '']
    if len(full_name) >= 1:
        normalized[0] = full_name[0]
    if len(full_name) >= 2:
        normalized[1] = full_name[1]
    if len(full_name) >= 3:
        normalized[2] = ' '.join(full_name[2:])
    return normalized


def format_phone(phone):
    """The phone to the format +7(999)999-99-99 or +7(999)999-99-99 доб.9999"""
    # Убираем всё, кроме цифр
    digits = re.sub(r'\D', '', phone)

    # Если номер начинается с 8 и имеет 11 цифр — заменяем 8 на 7
    if len(digits) == 11 and digits.startswith('8'):
        digits = '7' + digits[1:]
    # Если номер 10-значный (без кода страны), добавляем 7
    elif len(digits) == 10:
        digits = '7' + digits

    # Форматируем основной номер
    if len(digits) >= 11:
        formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        # Добавочный номер (если есть)
        if len(digits) > 11:
            ext = digits[11:]
            formatted += f" доб.{ext}"
        return formatted
    return phone  # если не удалось распознать — возвращаем как есть


# Чтение исходного файла
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Словарь для хранения уникальных контактов: ключ — (Фамилия, Имя)
contacts_dict = {}

for contact in contacts_list[1:]:  # пропускаем заголовок
    lastname, firstname, surname = normalize_name(contact[0], contact[1], contact[2])
    key = (lastname, firstname)

    # Приводим телефон к нужному формату
    phone = contact[5]
    if phone:
        phone = format_phone(phone)

    # Если контакт уже есть — объединяем данные
    if key in contacts_dict:
        existing = contacts_dict[key]
        # Заполняем пустые поля, если они есть
        if not existing[2] and surname:
            existing[2] = surname
        if not existing[3] and contact[3]:
            existing[3] = contact[3]
        if not existing[4] and contact[4]:
            existing[4] = contact[4]
        if not existing[5] and phone:
            existing[5] = phone
        if not existing[6] and contact[6]:
            existing[6] = contact[6]
    else:
        # Новый контакт
        contacts_dict[key] = [
            lastname,
            firstname,
            surname,
            contact[3],  # organization
            contact[4],  # position
            phone,
            contact[6]  # email
        ]

# Формируем итоговый список с заголовком
result = [contacts_list[0]]  # сохраняем заголовок
result.extend(contacts_dict.values())

# Сохраняем результат
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)

pprint(result)