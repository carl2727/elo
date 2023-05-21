import random
import json
from app_functions import *

# Load settings
f, elo_weight, elo_start = load_settings()

# Load list selection
list_selection = load_list_selection()

while True:
    print("\nMenu:")
    print("1. Use List - 2. Create List - 3. Edit List - 4. Settings - 5. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        use_list(f, elo_weight, elo_start, list_selection)

    elif choice == "2":
        create_list(f, elo_start, list_selection)

    elif choice == "3":
        edit_list(f, elo_start, list_selection)

    elif choice == "4":
        update_settings()

    elif choice == "5":
        break

    else:
        print("Invalid choice. Please try again.")
