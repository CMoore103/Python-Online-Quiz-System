import json

def load_user_data(filename = "Users.json"):

    """
    Try to load in user data from a JSON file
    :param filename : The file to load the user data from
    :return a dictionary containing a user's data
    """
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The file {filename} could not be retrieved")
        return {} #Return an empty dictionary if the file could not be found
    except json.JSONDecodeError:
        print("Error decoding the file: ")
        return {}
    
def save_user_data(data, filename = "Users.json"):
    """
    Saves a user's data to a JSON file
    :param data : The data to be saved to the file
    :param filename : The name of the file to save the data to
    """

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

