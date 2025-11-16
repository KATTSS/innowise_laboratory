current_year = 2025
def main():
    user_name = ask_user_name()
    birth_year_str = ask_birth_year()
    birth_year = int(birth_year_str)
    current_age=current_year-birth_year
    hobbies = ask_hobbies()
    life_stage = generate_profile(current_age)
    profile_summary = {"Name" : user_name,"Age" : current_age,"Life stage" : life_stage,"Hobbies" : hobbies}
    print_profile(profile_summary)

def ask_user_name():
    user_name = input("Enter your full name: ")
    while not user_name:
        user_name = input("Enter your full name: ")
    return user_name

def generate_profile(age):
    if age >= 20:
        return "Adult"
    elif 13 <= age <= 19:
        return "Teenager"
    else :
        return "Child"

def ask_hobbies():
    hobbies_list = []
    while True:
        hobbies_str = input("Enter a favourite hobby or type 'stop' to finish: ")
        if not hobbies_str:
            continue
        if hobbies_str.lower() == "stop":
            break
        hobbies_list.append(hobbies_str)
    return hobbies_list

def ask_birth_year():
    birth_year_str = int(input("Enter your birth year: "))
    while birth_year_str > current_year:
        birth_year_str = int(input("Enter your birth year: "))
    return birth_year_str

def print_profile(profile):
    print("---")
    for key, value in profile.items():
        if key == "Hobbies":
            if not value:
                print("You didn't mention any hobbies")
                break
            else :
                print(f"Favourite hobbies({len(value)}):")
                for hobby in value:
                    print(f"- {hobby}")
                break
        print(f"{key}: {value}")
    print("---")

main()
