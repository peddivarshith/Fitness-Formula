import sqlite3
import regex as re
import datetime


# Connection
conn = sqlite3.connect("fitness_users_database.db", check_same_thread=False)
cu = conn.cursor()


# user login and signup functions
def create_table():
    cu.execute('CREATE TABLE IF NOT EXISTS users(firstname TEXT,lastname TEXT,password TEXT,emailID TEXT,phoneno INTEGER,age INTEGER,weight INTEGER,idnum INTEGER)')


def add_userdata(firstname, lastname, password, emailID, phoneno, age, weight):
    id_value = count() + 1
    cu.execute("INSERT INTO users values (?,?,?,?,?,?,?,?)", (firstname,
               lastname, password, emailID, phoneno, age, weight, id_value))
    conn.commit()


def workout_data(id, exercise, exercisename, times):
    time = datetime.datetime.today()
    time = time.strftime("%d:%m:%Y")
    cu.execute('CREATE TABLE IF NOT EXISTS workout'+str(id) +
               '(SubmissionDate TIMESTAMP,ExerciseType TEXT,ExerciseName TEXT,count INTEGER)')
    cu.execute('INSERT INTO workout'+str(id)+' values (?,?,?,?)',
               (time, exercise, exercisename, times))
    conn.commit()

###


def create_todo_table(id):
    cu.execute('CREATE TABLE IF NOT EXISTS todo_user'+str(id) +
               '(task TEXT,task_status TEXT,task_due_date DATE)')


def add_todo_task(id, task, task_status, task_due_date):
    cu.execute('INSERT INTO todo_user'+str(id)+' values (?,?,?)',
               (task, task_status, task_due_date))
    conn.commit()


def read_todo_task(id):
    cu.execute('SELECT * FROM todo_user'+str(id))
    data = cu.fetchall()
    return data


def view_unique_task(id):
    cu.execute('SELECT task,task_due_date from todo_user'+str(id))
    return cu.fetchall()


def get_task(id, task, task_due_date):
    cu.execute('SELECT * FROM todo_user'+str(id) +
               ' WHERE task=? and task_due_date=?', (task, task_due_date))
    return cu.fetchall()


def update_task(id, task, task_status, task_due_date, task1, task1_status, task1_due_date):
    cu.execute('UPDATE todo_user'+str(id)+' SET task=?, task_status=?, task_due_date=? WHERE task=? and task_status=? and task_due_date=? ',
               (task1, task1_status, task1_due_date, task, task_status, task_due_date))
    conn.commit()


def delete_task(id, task, task_status, task_due_date):
    cu.execute('DELETE FROM todo_user'+str(id) +
               ' WHERE task=? and task_status=? and task_due_date=? ', (task, task_status, task_due_date))
    conn.commit()


####

def send_workout_data(id):
    cu.execute("SELECT * FROM workout"+str(id))
    data = cu.fetchall()
    return data


def login_user(email, password):
    cu.execute(
        "SELECT * FROM users where emailID = ? AND password = ?", (email, password))
    data = cu.fetchall()
    return data


def count():
    cu.execute("SELECT COUNT(*) FROM USERS")
    value = cu.fetchall()
    return int(value[0][0])


def view_all_users():
    cu.execute("SELECT * FROM users")
    list_of_users = cu.fetchall()
    return list_of_users


def name(username):
    if re.fullmatch("^[A-Za-z][A-Z a-z 0-9]+", username) is None:
        return False
    else:
        return True


def email_id(email):
    if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) is None:
        return False
    else:
        return True


def mobilenumber(mobno):
    if re.fullmatch("^[6-9]\d{9}$", mobno) is None:
        return False
    else:
        return True


def query_workout_data(id, exercisetype):
    cu.execute('CREATE TABLE IF NOT EXISTS workout'+str(id) +
               '(SubmissionDate TIMESTAMP,ExerciseType TEXT,ExerciseName TEXT,count INTEGER)')
    cu.execute('SELECT ExerciseName,count FROM workout'+str(id) +
               ' where ExerciseType = ?;', (exercisetype,))
    data1 = cu.fetchall()
    return data1


def trace_workout_date(id):
    # dic ={"Back Exercises":["Bird Dog", "Superman T", "Superman Y"],
    #       "Back of Upper Arm Exercises":["Bent Over Tricep", "Overhead Tricep","Tricep Dip 1", "Tricep Dip 2"],
    #       "Chest Exercises":["Incline Pushup", "Plank Jacks", "Push Up"],
    #       "Front of Upper Arm Exercises":["Dumbbell Workout Left Arm", "Dumbbell Workout ", "Right Arm","Bicep Curl", "Hammer Curl", "Wide Curl"],
    #       "Lunge Exercises":["Lateral Lunge", "Reverse Lunge"],
    #       "Neck Exercises":["Neck Extension", "Neck Stretch"],
    #       "Leg Exercises":["Calf Raises", "Donkey Kicks", "High Knees"],
    #       "Shoulders Exercises":["Plank Up Down", "Shoulder Military Press","Triangle Push Ups"],
    #       "Squats Exercises":[ "Dumbbell DeadLift Squats", "Jump Squats", "Sumo Squats"],
    #     }
    cu.execute('CREATE TABLE IF NOT EXISTS workout'+str(id) +
               '(SubmissionDate TIMESTAMP,ExerciseType TEXT,ExerciseName TEXT,count INTEGER)')
    cu.execute('SELECT SubmissionDate,COUNT(count) FROM workout' +
               str(id)+' GROUP BY SubmissionDate')
    data = cu.fetchall()
    return data


def get_mobile_number(email, password):
    cu.execute(
        "SELECT phoneno FROM users WHERE emailID = ? AND password = ?", (email, password))
    data = cu.fetchall()
    return data[0][0]
