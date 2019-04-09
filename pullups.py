from cs50 import SQL
db = SQL("sqlite:///sparta.db")

def main():
    exercises = ["bench", "deadlift", "squat", "overheadpress", "pullups"]
    lifts = {}
    for exercise in exercises:
        lift = db.execute("SELECT sets, reps, kg, date FROM sets WHERE user_id = :user_id AND exercise = :exercise", user_id = 1, exercise = exercise)
        lifts[exercise] = lift[0]
    #print(lifts["deadlift"])
    x = lifts.items()
    for element in x:
        print(element)
if __name__ == "__main__":
    main()