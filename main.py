#https://github.com/Onesimekeya/Zhuwafrica_challenge1.git


from susu_tracker import SusuGroup


def run_interactive_susu():
  print("--- Welcome to Susu Group ---")

  amount = input(
      "Enter the weekly contribution in GHS (ex: 50.00) : "
  )
  try:
    group = SusuGroup(float(amount))
    print(f"--> Group created with weekly contribution of {group.weekly_contribution} GHS.\n")
  except Exception as e:
    print(f"Error : {e}")
    return

  while True:
    print("\n--- MAIN MENU ---")
    print("-------------------")
    print("Choose what you want to do : ")
    print("1. Add a member")
    print("2. Record a contribution")
    print("3. Close the current week")
    print("4. Show report")
    print("5. Quit")

    choice = input("Choose a option (1-5) : ")

    if choice == "1":
      member_id = input("Enter Name ou member ID : ")
      try:
        group.add_member(member_id)
        print(f"--> Member '{member_id}' added successfully.")
      except Exception as e:
        print(f"Error : {e}")

    elif choice == "2":
      try:
        week = int(input(f"Number of the current week(current : {group.current_week}) : "))
        member_id = input("Membre ID : ")
        amount_paid = float(input("Amount paid : "))
        group.record_contribution(week, member_id, amount_paid)
        print("--> Contribution saved successfully.")
      except Exception as e:
        print(f"Error : {e}")

    elif choice == "3":
      print(f"Try to close the week {group.current_week}...")
      result = group.close_week()
      print(f"--> {result['message']}")
      if not result["success"]:
        print("Unpaid Details :", result["unpaid"])
      else:
        print(
            f"Pot paid to : {result['recipient']} (Amount :"
            f" {result['pot']} GHS)"
        )

    elif choice == "4":
      report = group.show_report()
      print("\n--- CURRENT REPORT ---")
      print(f"Current week : {report['current_week']}")
      print(f"Members has paid in full : {report['fully_paid']}")
      print("Members still owe :", report["owes"])
      print("Pay out history :", report["payout_history"])

    elif choice == "5":
      print("Program closed. Bye !")
      break
    else:
      print("Invalid option, could you please choose between 1 and 5.")


if __name__ == "__main__":
  run_interactive_susu()

