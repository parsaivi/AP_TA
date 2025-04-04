import random
import csv


def assign_teams(ta_ids, main_ta_ids, num_teams=65):
    """

    Randomly assign teams to people, ensuring teams are distributed as evenly as possible.

    Args:
        ta_ids: List of ta's id
        main_ta_ids: List of dedicated ta's id

    Returns:
        Dictionary mapping team numbers to assigned people
        Dictionary mapping people to their assigned teams
    """
    # Calculate how many teams each person should get
    num_people = len(ta_ids) + len(main_ta_ids)
    num_tas = len(ta_ids)
    num_main_tas = len(main_ta_ids)
    teams_per_person = num_teams // num_people
    remaining_teams = num_teams % num_people
    all_ta_ids = ta_ids + main_ta_ids

    # Prepare assignments dictionaries
    team_assignments = {}  # team number -> person
    person_assignments = {person: [] for person in all_ta_ids}  # person -> list of teams

    # Assign teams_per_person to each person
    all_teams = list(range(1, num_teams + 1))
    random.shuffle(all_teams)

    # First give everyone their fair share
    for person in all_ta_ids:
        teams_for_person = []
        for _ in range(teams_per_person):
            if all_teams:
                team = all_teams.pop()
                teams_for_person.append(team)
                team_assignments[team] = person

        person_assignments[person] = teams_for_person

    # Distribute remaining teams to some people randomly
    people_for_extras = random.sample(main_ta_ids, remaining_teams)
    for person in people_for_extras:
        if all_teams:
            team = all_teams.pop()
            person_assignments[person].append(team)
            team_assignments[team] = person

    return team_assignments, person_assignments


def export_to_csv(team_assignments, filename="team_assignments.csv"):
    """
    Export team assignments to a CSV file that can be opened in Google Sheets
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Team Number", "Assigned To"])

        for team_num in sorted(team_assignments.keys()):
            writer.writerow([team_num, team_assignments[team_num]])

    print(f"Team assignments exported to {filename}")

# Example usage
if __name__ == "__main__":
    # Replace with your actual list of 30-35 people
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

    # Run the assignment
    team_to_person, person_to_teams = assign_teams(ta_list, ta_main_list)

    # Export results to CSV (can be opened in Google Sheets)
    export_to_csv(team_to_person)

