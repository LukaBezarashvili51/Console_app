import sys
import json
from diarybook import Diary, DiaryBook
from util import read_from_json_into_application


class Menu:

    def __init__(self):
        self.diarybook = DiaryBook()
        self.load_diaries_from_file()
        self.users = []
        self.current_user = None
        self.choices = {
            "1": self.show_diaries,
            "2": self.add_diary,
            "3": self.search_diaries,
            "4": self.populate_database,
            "5": self.sort_by_id,
            "6": self.sort_by_memo,
            "7": self.quit
        }

    def display_menu(self):
        print(""" 
                     Notebook Menu  
                    1. Show diaries
                    2. Add diary
                    3. Search diaries
                    4. Populate database
                    5. Sort by id
                    6. Sort by memo
                    7. Quit program
                    """)

    def run(self):
        self.load_users()
        self.register_or_login()
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def show_diaries(self, diaries=None):
        if not diaries:
            diaries = self.diarybook.diaries
        for diary in diaries:
            print(f"{diary.id}-{diary.memo}")

    def add_diary(self):
        memo = input("Enter a memo: ")
        tags = input("Add tags: ")
        self.diarybook.new_diary(memo, tags)
        print("Your note has been added")
        with open('data.json', 'r') as file:
            existing_diaries = json.load(file)
        new_diary_entry = {
            "memo": memo,
            "tags": tags
        }
        existing_diaries.append(new_diary_entry)
        with open('data.json', 'w') as file:
            json.dump(existing_diaries, file, indent=4)

    def search_diaries(self):

        filter_text = input("Search for:  ")
        diaries = self.diarybook.search_diary(filter_text)
        for diary in diaries:
            print(f"{diary.id}-{diary.memo}")

    def sort_by_id(self):
        sorted_diaries = sorted(self.diarybook.diaries, key=lambda x: x.id)
        self.show_diaries(sorted_diaries)

    def sort_by_memo(self):
        sorted_diaries = sorted(self.diarybook.diaries, key=lambda x: x.memo)
        self.show_diaries(sorted_diaries)

    def quit(self):

        print("Thank you for using diarybook today")
        sys.exit(0)

    def populate_database(self):
        diaries1 = read_from_json_into_application('data.json')
        for diary in diaries1:
            self.diarybook.diaries.append(diary)

    def load_users(self):
        try:
            with open('users.json', 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = []

    def save_users(self):
        with open('users.json', 'w') as file:
            json.dump(self.users, file)

    def register_or_login(self):
        while True:
            choice = input("Do you want to register (1) or login (2)? ")
            if choice == "1":
                self.register_user()
                break
            elif choice == "2":
                if self.login_user():
                    break
                else:
                    print("Invalid username or password. Please try again.")
            else:
                print("Invalid choice. Please try again.")

    def register_user(self):
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        user = {"username": username, "password": password}
        self.users.append(user)
        self.save_users()

        print("Registration successful. Please login.")

    def login_user(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        for user in self.users:
            if user["username"] == username and user["password"] == password:
                self.current_user = user
                print("Login successful. Welcome, {}!".format(username))
                return True

        return False

    def load_diaries_from_file(self):
        try:
            with open('data.json', 'r') as file:
                diaries_data = json.load(file)
                for diary_entry in diaries_data:
                    memo = diary_entry["memo"]
                    tags = diary_entry["tags"]
                    self.diarybook.new_diary(memo, tags)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    Menu().run()

