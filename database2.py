import pandas as pd
import time


students_df = pd.read_csv(
    r"C:\Users\mbv16\Downloads\list.txt",
    header=None,
    names=["StLastName", "StFirstName", "Grade", "Classroom", "Bus"],
    skipinitialspace=True
)

teachers_df = pd.read_csv(
    r"C:\Users\mbv16\Downloads\teachers.txt",
    header=None,
    names=["TLastName", "TFirstName", "Classroom"],
    skipinitialspace=True
)

# Приводимо ПІБ до верхнього регістру для зручності пошуку
students_df["StLastName"] = students_df["StLastName"].str.upper()
students_df["StFirstName"] = students_df["StFirstName"].str.upper()
teachers_df["TLastName"] = teachers_df["TLastName"].str.upper()
teachers_df["TFirstName"] = teachers_df["TFirstName"].str.upper()

#Знайти клас і викладача за прізвищем студента
def find_student_classroom(lastname):
    result = []
    matches = students_df[students_df["StLastName"] == lastname]
    for _, s in matches.iterrows():
        ts = teachers_df[teachers_df["Classroom"] == s["Classroom"]]
        for _, t in ts.iterrows():
            result.append({
                "StLastName": s["StLastName"],
                "StFirstName": s["StFirstName"],
                "Grade": s["Grade"],
                "Classroom": s["Classroom"],
                "Bus": s["Bus"],
                "TLastName": t["TLastName"],
                "TFirstName": t["TFirstName"]
            })
    return result

#Знайти автобус за прізвищем студента
def find_student_bus(lastname):
    matches = students_df[students_df["StLastName"] == lastname]
    return matches[["StFirstName", "Bus"]].to_dict(orient="records")

#Знайти список учнів викладача
def find_teacher_students(t_lastname, t_firstname):
    classes = teachers_df[
        (teachers_df["TLastName"] == t_lastname) &
        (teachers_df["TFirstName"] == t_firstname)
    ]["Classroom"].unique()
    return students_df[students_df["Classroom"].isin(classes)].to_dict(orient="records")

#Знайти учнів за номером автобуса
def find_students_by_bus(bus_num):
    return students_df[students_df["Bus"] == bus_num].to_dict(orient="records")

#Знайти учнів за рівнем класу (Grade)
def find_students_by_grade(grade):
    return students_df[students_df["Grade"] == grade].to_dict(orient="records")

#Додати нового студента
def add_student():
    global students_df
    st_ln = input("Прізвище студента: ").upper()
    st_fn = input("Ім’я студента: ").upper()
    grade = int(input("Клас (Grade): "))
    classroom = int(input("Номер класної кімнати (Classroom): "))
    bus = int(input("Номер автобуса: "))

    new_student = {
        "StLastName": st_ln,
        "StFirstName": st_fn,
        "Grade": grade,
        "Classroom": classroom,
        "Bus": bus
    }

    students_df = pd.concat([students_df, pd.DataFrame([new_student])], ignore_index=True)
    print("Студента додано!")

#За номером класу (Grade): всі учні
def find_students_by_grade_number(grade):
    return students_df[students_df["Grade"] == grade].to_dict(orient="records")

#За номером класної кімнати (Classroom): всі викладачі
def find_teachers_by_classroom(classroom):
    return teachers_df[teachers_df["Classroom"] == classroom].to_dict(orient="records")

#За номером класу (Grade): усі викладачі, які викладають учнів цього класу
def find_teachers_by_grade(grade):
    classes = students_df[students_df["Grade"] == grade]["Classroom"].unique()
    return teachers_df[teachers_df["Classroom"].isin(classes)].to_dict(orient="records")


if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("1. Знайти клас і викладача за прізвищем студента")
        print("2. Знайти автобус за прізвищем студента")
        print("3. Знайти список учнів викладача")
        print("4. Знайти учнів за номером автобуса")
        print("5. Знайти учнів за рівнем класу (Grade)")
        print("6. Додати нового студента")
        print("7. Знайти учнів за номером класу (Grade)")
        print("8. Знайти викладачів за номером класної кімнати (Classroom)")
        print("9. Знайти викладачів, які викладають учнів певного класу (Grade)")
        print("0. Вихід")

        choice = input("Ваш вибір: ")
        start = time.time()

        if choice == "0":
            print("До побачення!\n")
            break

        elif choice == "1":
            ln = input("Прізвище студента: ").upper()
            res = find_student_classroom(ln)

        elif choice == "2":
            ln = input("Прізвище студента: ").upper()
            res = find_student_bus(ln)

        elif choice == "3":
            tln = input("Прізвище вчителя: ").upper()
            tfn = input("Ім’я вчителя: ").upper()
            res = find_teacher_students(tln, tfn)

        elif choice == "4":
            bus = int(input("Номер автобуса: "))
            res = find_students_by_bus(bus)

        elif choice == "5":
            grade = int(input("Рівень класу (Grade): "))
            res = find_students_by_grade(grade)

        elif choice == "6":
            add_student()
            res = []

        elif choice == "7":
            grade = int(input("Рівень класу (Grade): "))
            res = find_students_by_grade_number(grade)

        elif choice == "8":
            cls = int(input("Номер класної кімнати (Classroom): "))
            res = find_teachers_by_classroom(cls)

        elif choice == "9":
            grade = int(input("Рівень класу (Grade): "))
            res = find_teachers_by_grade(grade)

        else:
            print("Невірний вибір.")
            continue

        # Вивести результати і час пошуку
        elapsed = (time.time() - start) * 1000
        for r in res:
            print(r)
        print(f"{len(res)} Результатів за {elapsed:.2f}ms")
