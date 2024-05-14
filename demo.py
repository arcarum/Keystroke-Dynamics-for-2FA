from pynput.keyboard import Listener, Key
import time
import json
import os
import numpy as np
import hashlib
import getpass
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

TERMINATION_KEYS = ['Key.enter', 'Key.esc']
sentence = "the quick brown fox jumps over the lazy dog"

start_times = {}
log = []

def set_key(key, t):
    start_times[str(key).lower()] = t

def get_key(key):
    return start_times[str(key).lower()]

def get_pop_key(key):
    return start_times.pop(str(key).lower())

def register_key(key, start_time, end_time):
    log.append([key, start_time, end_time])

def on_press(key):
    if str(key).lower() not in start_times:
        t = time.time()
        set_key(key, t)

def on_release(key):
    end_time = time.time()
    start_time = get_pop_key(key)
    duration = end_time - start_time
    if str(key) in TERMINATION_KEYS:
        return False
    register_key(str(key), start_time, end_time)

def start_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        print("\nEnter the sentence below:")
        print(sentence)
        listener.join()
        listener.stop()

    sentence_typed = input()
    if sentence_typed != sentence:
        return None

    features = calculate_features(log)
    return features

def calculate_features(log):
    features = []
    prev_character = None
    for i, entry in enumerate(log):
        new = {}
        character = entry[0]
        dwell_time = entry[2] - entry[1]

        if prev_character:
            key = f"{prev_character}-{character}"
            new[key] = flight

        flight = 0 if i == len(log) - 1 else log[i+1][1] - entry[2]

        new[character] = dwell_time
        prev_character = character
        features.append(new)

    return features

def choice():
    while True:
        print(f"\n=====================\nCHOOSE ONE")
        print(f"1. sign up \n2. login\n")
        choice = input("CHOICE: ")
        if choice == '1':
            sign_up()
        elif choice == '2':
            sign_in()
        else:
            print("Invalid Choice\n")

def load_user_data(filename):
    try:
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        else:
            return {}
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error loading user data: {e}")
        return {}

def save_user_data(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving user data: {e}")

def sign_up():
    global log
    log = []
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    time.sleep(1)
    features = start_listener()

    if features is None:
        print("Please type the correct sentence")
        return

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user_data = {}

    user_data[username] = {
        "password": hashed_password,
        "keystroke_log": features
    }

    filename = "user_data.json"

    existing_user_data = load_user_data(filename)
    if existing_user_data:
        existing_user_data.update(user_data)
        save_user_data(filename, existing_user_data)
    else:
        save_user_data(filename, user_data)

    print("Sign up successful")

def sign_in():
    global log
    log = []
    filename = "user_data.json"
    user_data = load_user_data(filename)

    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if username not in user_data or user_data[username]["password"] != hashed_password:
        print("Invalid username or password")
        return

    time.sleep(1)
    features = start_listener()
    
    X_train = []
    y_train = []
    for user, data in user_data.items():
        keystroke_log = data.get("keystroke_log")

        lst_keystroke = []
        for item in keystroke_log:
            for key, value in item.items():
                lst_keystroke.append(value)
        X_train.append(lst_keystroke)
        y_train.append(user)

    if features is None:
        print("Please type the correct sentence")
        return

    X_test = []
    new = []
    for item in features:
        for key,value in item.items():
            new.append(value)

    X_test.append(new)

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)

    if (len(X_train[0]) != len(X_test[0])):
        print("Please avoid making mistakes")
        return

    do_knn(X_train, y_train, X_test, username)
    do_random_forest(X_train, y_train, X_test, username)
    do_decision_tree(X_train, y_train, X_test, username)
    do_svm(X_train, y_train, X_test, username)


def do_knn(X_train, y_train, X_test, username):
    distance_metrics = ['euclidean', 'cosine']

    print()
    for metric in distance_metrics:
        knn = KNeighborsClassifier(n_neighbors=1, metric=metric)
        knn.fit(X_train, y_train)
        predictions = knn.predict(X_test)

        result = "FAIL"
        if (predictions[0] == username):
            result = "SUCCESS"
        print(f"[{result}]: KNN ({metric}): {predictions}\n")

def do_svm(X_train, y_train, X_test, username):

    if (len(y_train) < 2):
        print(f"[FAIL]: SVM: Number of classes must be greater than or equal 2\n")
        return

    svm = SVC()
    svm.fit(X_train, y_train)
    predictions = svm.predict(X_test)
    result = "FAIL"
    if (predictions[0] == username):
        result = "SUCCESS"
    print(f"[{result}]: SVM: {predictions}\n")

def do_random_forest(X_train, y_train, X_test, username):
    random_forest = RandomForestClassifier()
    random_forest.fit(X_train, y_train)
    predictions = random_forest.predict(X_test)
    result = "FAIL"
    if (predictions[0] == username):
        result = "SUCCESS"
    print(f"[{result}]: Random Forest: {predictions}\n")

def do_decision_tree(X_train, y_train, X_test, username):
    decision_tree = DecisionTreeClassifier()
    decision_tree.fit(X_train, y_train)
    predictions = decision_tree.predict(X_test)
    result = "FAIL"
    if (predictions[0] == username):
        result = "SUCCESS"
    print(f"[{result}]: Decision Trees: {predictions}\n")

def main():
    choice()

if __name__ == "__main__":
    main()
