import os
from dotenv import load_dotenv
from data_manager import DataManager


class Customer:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.email = ""

    def register(self):
        print("Welcome to Nicole's Flight Club.")
        print("We find the best flight deals and email you.")
        self.first_name = input("What is your first name? \n")
        self.last_name = input("What is your last name? \n")
        email = "email1"
        confirm_email = "email2"
        while email != confirm_email:
            email = input("What is your email address? \n")
            confirm_email = input("Type your email address again for confirmation: \n")
            if email != confirm_email:
                print("Please provide your email address again!")
        self.email = email
        print("Welcome to the club!")


load_dotenv()

# create the Data Manager:
data_manager = DataManager(os.getenv('SHEETY_ENDPOINT'), os.getenv('SHEETY_BEARER_TOKEN'))

# Register new customer
new_customer = Customer()
new_customer.register()
data_manager.add_user(new_customer)
