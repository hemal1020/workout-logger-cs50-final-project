# Workout Logger
#### Video Demo: https://youtu.be/7CsV8kyAOyQ?si=ZqHBrFZs4nJ_wYHK
#### Description:
Workout Logger is a command-line program I made to keep track of my gym workouts. I used to forget how much weight I lifted in my previous sessions, and sometimes I couldn't remember how many sets or reps I had completed. Because of this, it was hard to keep track of my progress. I wanted something simple that could help me organize my workouts, so I decided to build this program.

With Workout Logger, I can save my exercises along with the number of sets, reps, and weight I use. I can also check my workout history, find my heaviest lift for a particular exercise, and see how much total weight I have lifted each week. These features make it easier for me to keep everything in one place.

When I run the program, it shows a menu with five options: log a workout, view history, view a personal record, view weekly volume, and quit. I can choose different options as many times as I want until I decide to exit. My workout data is saved in a file called workouts.csv, which the program creates automatically when I save my first workout.

The main code is written in project.py. I divided the program into different functions so each one has a specific job. The validate_entry function checks the information I enter and makes sure the values are valid. The save_workout function saves the workout to the CSV file, and load_workouts reads the saved information when I need it. The personal_record function finds the heaviest weight I have recorded for an exercise, while weekly_volume calculates my total workout volume for each week.

I also wrote tests in test_project.py to make sure the functions work correctly. I tested valid and invalid inputs, saving and loading workouts, finding personal records, and calculating weekly volume. For file-related tests, I used pytest's tmp_path fixture so that the tests would not change my actual workout data.

I chose CSV because it is easy to use, does not require extra libraries, and lets me open my data in a spreadsheet if needed. I also used separate functions to make the code easier to test and maintain. Dates are saved in YYYY-MM-DD format, and I allow a weight of zero for exercises that do not require extra weights, such as push-ups.

One challenge was making sure the program handled incorrect input and missing files properly instead of crashing. Testing the functions separately helped me find and handle these situations.

There are still a few things I would like to improve. Right now, I cannot edit or delete a workout, and the program only supports kilograms. If I work on it more, I would like to add those features and include charts to make tracking progress easier.

Overall, this project gave me a chance to practice Python while building something useful for my everyday life. It also helped me understand the importance of testing code and organizing a program into smaller, manageable functions.

