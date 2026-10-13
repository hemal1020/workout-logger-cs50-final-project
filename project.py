import csv
import os
from datetime import date

FILENAME = "workouts.csv"


def main():
    while True:
        print()
        print("1. Log a workout")
        print("2. View history")

        print("3. View personal record")
        print("4. View weekly volume")
        print("5. Quit")
        choice = input("Choose: ").strip()

        if choice == "5":
            break
        elif choice == "1":
            exercise = input("Exercise: ")
            sets = input("Sets: ")
            reps = input("Reps: ")
            weight = input("Weight: ")
            try:
                entry = validate_entry(exercise, sets, reps, weight)
            except ValueError as error:
                print(f"Invalid: {error}")
            else:
                save_workout(entry)
                print("Saved!")
        elif choice == "2":
            workouts = load_workouts()
            if workouts == []:
                print("No workouts logged yet")
            else:
                for workout in workouts:
                    print(
                        f"{workout['date']}  {workout['exercise']}  "
                        f"{workout['sets']}x{workout['reps']} @ {workout['weight']}"
                    )
        elif choice == "3":
            exercise = input("Exercise: ")
            record = personal_record(load_workouts(), exercise)
            if record is None:
                print("No workouts logged for that exercise")
            else:
                print(f"Personal record: {record} kg")
        elif choice == "4":
            totals = weekly_volume(load_workouts())
            if totals == {}:
                print("No workouts logged yet")
            else:
                for week in sorted(totals):
                    print(f"{week}: {totals[week]:,.0f} kg total")
        else:
            print("Invalid choice")


def save_workout(entry, filename=FILENAME):
    needs_header = not os.path.exists(filename) or os.path.getsize(filename) == 0
    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "exercise", "sets", "reps", "weight"])
        if needs_header:
            writer.writeheader()
        writer.writerow(entry)

def delete_workout(index, filename=FILENAME):
    workouts = load_workouts(filename)
    if index < 0 or index >= len(workouts):
        raise ValueError("Workout not found")
    del workouts[index]
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "exercise", "sets", "reps", "weight"])
        writer.writeheader()
        writer.writerows(workouts)

        
def load_workouts(filename=FILENAME):
    if not os.path.exists(filename):
        return []
    workouts = []
    with open(filename, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["sets"] = int(row["sets"])
            row["reps"] = int(row["reps"])
            row["weight"] = float(row["weight"])
            workouts.append(row)
    return workouts


def personal_record(workouts, exercise):
    exercise = exercise.strip().lower()
    weights = []
    for workout in workouts:
        if workout["exercise"] == exercise:
            weights.append(workout["weight"])
    if weights == []:
        return None
    return max(weights)

def exercise_progress(workouts, exercise):
    exercise = exercise.strip().lower()
    best = {}
    for workout in workouts:
        if workout["exercise"] == exercise:
            day = workout["date"]
            best[day] = max(best.get(day, 0), workout["weight"])
    return sorted(best.items())

def weekly_volume(workouts):
    totals = {}
    for workout in workouts:
        day = date.fromisoformat(workout["date"])
        year, week, _ = day.isocalendar()
        label = f"{year}-W{week:02}"
        volume = workout["sets"] * workout["reps"] * workout["weight"]
        totals[label] = totals.get(label, 0) + volume
    return totals


def validate_entry(exercise, sets, reps, weight):
    exercise = exercise.strip().lower()
    if exercise == "":
        raise ValueError("Exercise name cannot be empty")

    sets = int(sets)
    reps = int(reps)
    if sets <= 0:
        raise ValueError("Sets must be a positive whole number")
    if reps <= 0:
        raise ValueError("Reps must be a positive whole number")

    weight = float(weight)
    if weight < 0:
        raise ValueError("Weight cannot be negative")

    return {
        "date": date.today().isoformat(),
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight,
    }


if __name__ == "__main__":
    main()
