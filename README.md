# Keystroke Dynamics for 2FA

This project implements a keystroke authentication system using machine learning classifiers. Users can sign up by typing a predefined sentence, and their keystroke patterns (dwell time and flight time) are recorded and stored. During login, the system compares the user's keystroke pattern with the stored patterns to authenticate the user.

## Features

- Sign up: Users can sign up by typing a predefined sentence, which captures their keystroke patterns.
- Login: Users can log in by typing the same predefined sentence, and their keystroke patterns are compared with the stored patterns for authentication. Once logged in, the system will display the authentication results from each classifier.
- Machine Learning Classifiers: The system uses K-Nearest Neighbors (KNN), Support Vector Machines (SVM), Random Forest, and Decision Trees classifiers for authentication.
- Data Storage: User data, including usernames, hashed passwords, and keystroke patterns, are saved in a JSON file named `user_data.json`.
