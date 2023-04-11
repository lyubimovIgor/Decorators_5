import re
import csv
from pprint import pprint
import logging

# Создание и настройка логгера
logging.basicConfig(filename='phonebook.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_file(file_name):
    with open(file_name, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts = list(rows)
    return contacts

def fix_initials(contacts_list):
    # Логирование
    logging.info('Fixing initials')
    contacts_list_upd =[]
    for contact in contacts_list:
        pattern = r'[\s,]'
        full_name = (re.split(pattern, ' '.join(contact[:3])))[:3]
        info = contact[3:]
        contact = full_name + info
        contacts_list_upd.append(contact)
    return contacts_list_upd

def fix_phones(contacts_list):
    # Логирование
    logging.info('Fixing phones')
    contacts_list_upd = []
    for contact in contacts_list:
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?\-?\s*(\d{3})\-?'\
                r'(\d{2})\-?(\d+)(\s*)\(*([доб.]*)?\s*(\d{4})?\)*'
        phone_exist = re.search(pattern, contact[-2])
        if phone_exist is not None:
            result = re.sub(pattern, r'+7(\2)\3-\4-\5\6\7\8', contact[-2])
            contact[-2] = result
        contacts_list_upd.append(contact)
    return contacts_list_upd

def merge_doubles(contacts_list):
    # Логирование
    logging.info('Merging doubles')
    contacts_to_del = []
    for contact in contacts_list:
        pattern = ', '.join([contact[0], (contact[1])])
        start_slice = contacts_list.index(contact) + 1
        for element in contacts_list[start_slice:]:
            full_name = ', '.join([element[0], (element[1])])
            result = re.search(pattern, full_name)
            if result is not None:
                if contact[2] == '':
                    contact[2] = element[2]
                if contact[3] == '':
                    contact[3] = element[3]
                if contact[4] == '':
                    contact[4] = element[4]
                if contact[5] == '':
                    contact[5] = element[5]
                if contact[6] == '':
                    contact[6] = element[6]
                contacts_to_del.append(element)
    contacts_list_upd = [contact for contact in contacts_list if contact not in contacts_to_del]
    return contacts_list_upd

def write_to_file(contacts_list):
    # Логирование
    logging.info('Writing to file')
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

if __name__ == '__main__':
    # Логирование
    logging.info('Starting phonebook application')
    address_book = read_file('phonebook_raw.csv')
    address_book = fix_initials(address_book)
    address_book = fix_phones(address_book)
    address_book = merge_doubles(address_book)
    pprint(address_book)
    write_to_file(address_book)
    # Логирование
    logging.info('Phonebook application successfully completed')
