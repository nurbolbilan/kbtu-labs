from entering_from_console import insert
from update import *
from query import *
from delete import *

while True:
    action = action = input("Enter action: \n 1. Input data \n 2. Update data \n 3. Output data \n 4. Delete data \n 5. exit \n")
    if action == '1':
        name = input("Enter your name : ")
        phone = input("Enter your phone number : ")
        insert(name, phone)
    elif action == '2':
        answer2 = input("What do you want to update your data? (name/phone) : ")
        if answer2 == "name":
            user_id = input("Enter your user id : ")
            name = input("Enter your name : ")
            update_for_name(name, user_id)
        elif answer2 == "phone":
            user_id = input("Enter your user id : ")
            phone = input("Enter your phone number : ")
            update_for_phone(phone, user_id)
        else:
            print("Invalid input")
            continue
    elif action == '3':
        action = input(
            "Enter action: \n 1. output all phone \n 2. output all name \n 3. find user phone \n 4. find user name \n")
        if action == '1':
            phone_list = all_phone()
            for row in phone_list:
                print(row)
        elif action == '2':
            name = all_name()
            print(name)
        elif action == '4':
            user_id = int(input("Enter id : "))
            name = find_user_name(user_id)
            print(name)
        elif action == '3':
            user_id = int(input("Enter id : "))
            phone = find_user_phone(user_id)
            print(phone)
        else:
            print("Invalid input")
    elif action == '4':
        action = int(input("Enter action : \n 1. Delete by name \n 2. Delete by phone \n 3. Exit \n"))
        if action == 1:
            name = input("Enter name : ")
            delete_by_name(name)
        elif action == 2:
            phone = input("Enter phone number : ")
            delete_by_phone(phone)
        elif action == 3:
            break
        else:
            print("Invalid input")
    elif action == '5':
        break
    else:
        print("Invalid input")
