import random
import csv


def assign_students_to_tas(ta_ids, main_ta_ids, student_numbers):
    """
    Randomly assign students to TAs, ensuring students are distributed as evenly as possible.

    Args:
        ta_ids: List of ta's id
        main_ta_ids: List of dedicated ta's id
        student_numbers: List of student numbers

    Returns:
        Dictionary mapping student numbers to assigned TAs
        Dictionary mapping TAs to their assigned students
    """
    # Calculate how many students each TA should get
    num_students = len(student_numbers)
    num_people = len(ta_ids) + len(main_ta_ids)
    num_tas = len(ta_ids)
    num_main_tas = len(main_ta_ids)
    students_per_ta = num_students // num_people
    remaining_students = num_students % num_people
    all_ta_ids = ta_ids + main_ta_ids

    # Prepare assignments dictionaries
    student_assignments = {}  # student number -> TA
    ta_assignments = {ta: [] for ta in all_ta_ids}  # TA -> list of students

    # Assign students_per_ta to each TA
    # Make a copy and shuffle to ensure random assignment
    all_students = student_numbers.copy()
    random.shuffle(all_students)

    # First give everyone their fair share
    for ta in all_ta_ids:
        students_for_ta = []
        for _ in range(students_per_ta):
            if all_students:
                student = all_students.pop()
                students_for_ta.append(student)
                student_assignments[student] = ta

        ta_assignments[ta] = students_for_ta

    # Distribute remaining students to some TAs randomly
    # Prioritize main TAs for extra students if possible
    tas_for_extras = random.sample(main_ta_ids, min(remaining_students, len(main_ta_ids)))

    # If we need more TAs than available main TAs, add some regular TAs
    if remaining_students > len(main_ta_ids):
        extra_regular_tas_needed = remaining_students - len(main_ta_ids)
        tas_for_extras.extend(random.sample(ta_ids, extra_regular_tas_needed))

    for ta in tas_for_extras:
        if all_students:
            student = all_students.pop()
            ta_assignments[ta].append(student)
            student_assignments[student] = ta

    return student_assignments, ta_assignments


def export_to_csv(student_assignments, filename="student_ta_assignments.csv"):
    """
    Export student assignments to a CSV file that can be opened in Google Sheets
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Student Number", "Assigned TA"])

        for student_num in sorted(student_assignments.keys()):
            writer.writerow([student_num, student_assignments[student_num]])

    print(f"Student assignments exported to {filename}")


def print_statistics(ta_assignments):
    """
    Print statistics about the distribution of students to TAs
    """
    print("\n=== TA Assignment Statistics ===")
    student_counts = {}
    total_students = 0

    for ta, students in ta_assignments.items():
        count = len(students)
        student_counts[ta] = count
        total_students += count
        print(f"{ta}: {count} students")

    min_count = min(student_counts.values())
    max_count = max(student_counts.values())
    avg_count = total_students / len(ta_assignments)

    print(f"\nTotal students: {total_students}")
    print(f"Distribution: TAs have between {min_count} and {max_count} students")
    print(f"Average: {avg_count:.2f} students per TA")


# Example usage
if __name__ == "__main__":
    # TAs list from original code
    ta_list = [
        "MahMosTash",
        "samsammyz",
        "paradisem05",
        "ahmz1833",
        "Amirhmrz1",
        "Foad_Kh_Ab",
        "Kiarash_Sanei",
        "sananiroomand",
        "voidXD",
        "ali_mghds",
        "kasrahmi",
        "mollaee_nima",
        "Saleh627",
        "MehrshadDehghani82",
        "kshyst",
        "NewFKR1383"
    ]

    ta_main_list = [
        "Arshiaizd",
        "armatah",
        "rezaBPGL",
        "m20h03e",
        "Arefzarezade",
        "shaghayeghmir",
        "Mohaliza138",
        "TA_Tahmasebi",
        "hosna0sh",
        "SGHTA",
        "parsaivim",
        "Ma8hd2i",
        "pouria_gh83",
        "s_Ahmad_m_Awal",
        "ma_koohi"
    ]

    # Example student numbers - replace with actual list of student numbers
    # For this example, let's create 195 sample student numbers
    # You can replace this with actual student numbers
    student_numbers = [f"400{i:06d}" for i in range(1, 196)]

    # Run the assignment
    student_to_ta, ta_to_students = assign_students_to_tas(ta_list, ta_main_list, student_numbers)

    # Print statistics
    print_statistics(ta_to_students)

    # Export results to CSV (can be opened in Google Sheets)
    export_to_csv(student_to_ta)