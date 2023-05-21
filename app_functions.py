import os
import random
import json

data_folder = "data/"
settings_file = os.path.join(data_folder, "settings.json")
list_selection_file = os.path.join(data_folder, "list_selection.json")

def save_settings(f, elo_weight, elo_start):
    settings = {
        "f": f,
        "elo_weight": elo_weight,
        "elo_start": elo_start
    }
    with open(settings_file, "w") as file:
        json.dump(settings, file)

def load_settings():
    try:
        with open(settings_file, "r") as file:
            settings = json.load(file)
        return settings["f"], settings["elo_weight"], settings["elo_start"]
    except (FileNotFoundError, json.JSONDecodeError):
        return 400, 20, 1000

def load_list_selection():
    try:
        with open(list_selection_file, "r") as file:
            list_selection = json.load(file)
    except FileNotFoundError:
        list_selection = []
    return list_selection

def use_list(f, elo_weight, elo_start, list_selection):
    print("Select a list:")
    for i, list_name in enumerate(list_selection, start=1):
        print(f"{i}. {list_name}")

    selection = int(input("Enter the number of the list: "))

    try:
        list_name = list_selection[selection - 1]
        with open(f"data/{list_name}.json", "r") as file:
            my_list = json.load(file)
    except (IndexError, FileNotFoundError):
        print("Invalid selection. Please try again.")
        return

    if not my_list:
        print("The list is empty.")
        choice = input("Do you want to add items to the list? (y/n): ")
        if choice.lower() == "y":
            number_items = int(input("Number of items to add: "))
            for _ in range(number_items):
                name = input("Enter Name: ")
                item = [name, 100, 0]
                my_list.append(item)
        else:
            print("Exiting...")
            return

    number_rounds = int(input("Number of rounds: "))

    for round in range(number_rounds):
        my_list.sort(key=lambda x: x[2])  # Sort the list based on the number of rounds
        second_lowest_rounds = my_list[1][2]  # Number of rounds of the second lowest item
        filtered_list = [item for item in my_list if item[2] <= second_lowest_rounds]  # Filter the items
        
        print("Round:", round + 1)
        item1, item2 = random.choices(filtered_list, weights=None, k=2)

        while item2 == item1:
            item2 = random.choice(filtered_list)  # Use filtered_list instead of my_list

        print(item1[0], "vs.", item2[0])
        pick = int(input("Enter 1 or 2: "))

        if pick == 1:
            winner = item1
            loser = item2
        elif pick == 2:
            winner = item2
            loser = item1
        else:
            print("Wrong input")
            continue

        exp = elo(winner[1], loser[1], f)
        score = elo_weight * (1 - exp)
        winner[1] += score
        loser[1] -= score
        print(winner[0], "+", "{:.3f}".format(score), loser[0], "-", "{:.3f}".format(score), "\n")
        winner[2] += 1
        loser[2] += 1

    my_list.sort(key=lambda x: x[1], reverse=True)

    with open(f"data/{list_name}.json", "w") as file:
        json.dump(my_list, file)

    print("Final List:")
    for i, item in enumerate(my_list):
        name = item[0]
        elo_score = "{:.3f}".format(item[1])
        print(f"{i + 1}. {name} ({elo_score})")

def create_list(f, elo_start, list_selection):
    # Create List
    list_name = input("Enter the name for the new list: ")
    my_list = []
    list_selection.append(list_name)

    number_items = int(input("Number of items to add: "))
    for _ in range(number_items):
        name = input("Enter Name: ")
        item = [name, elo_start, 0]
        my_list.append(item)

    with open(f"data/{list_name}.json", "w") as file:
        json.dump(my_list, file)

    with open(list_selection_file, "w") as file:
        json.dump(list_selection, file)

def edit_list(f, elo_start, list_selection):
    # Edit List (Add items)
    print("Select a list:")

    for i, list_name in enumerate(list_selection, start=1):
        print(f"{i}. {list_name}")

    selection = int(input("Enter the number of the list: "))

    try:
        list_name = list_selection[selection - 1]
        with open(f"data/{list_name}.json", "r") as file:
            my_list = json.load(file)
    except (IndexError, FileNotFoundError):
        print("Invalid selection. Please try again.")
        return

    print("Edit List:")
    print("1. Add items - 2. Reset Elo")
    edit_choice = input("Enter your choice: ")

    if edit_choice == "1":
        number_items = int(input("Number of items to add: "))
        for _ in range(number_items):
            name = input("Enter Name: ")
            item = [name, elo_start, 0]
            my_list.append(item)
    elif edit_choice == "2":
        for item in my_list:
            item[1] = elo_start
            item[2] = 0
    else:
        print("Invalid choice. Returning to the main menu.")
        return

    with open(f"data/{list_name}.json", "w") as file:
        json.dump(my_list, file)

def update_settings():
    # Settings
    f = int(input("Enter the value for f (default 400): "))
    elo_weight = int(input("Enter the value for elo_weight (default 100): "))
    elo_start = int(input("Enter the value for elo_start (default 3000): "))
    save_settings(f, elo_weight, elo_start)

def elo(a, b, f):
    exp = 1 / (1 + 10 ** ((b - a) / f))
    return exp
