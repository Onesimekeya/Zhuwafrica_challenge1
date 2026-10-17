from decimal import Decimal, ROUND_HALF_UP


class SusuGroup:

  def __init__(self, weekly_contribution):
    contrib = Decimal(str(weekly_contribution))
    if contrib <= 0:
      raise ValueError(
          "Type the weekly contribution amount, that must be more than 0 [Ex: 50]."
      )
    self.weekly_contribution = contrib
    self.members = []
    self.contributions = (
        {}
    )
    self.payout_history = []  # [(week_number, member_id, amount)]
    self.current_week = 1

  def add_member(self, member_id):
    if not member_id or not str(member_id).strip():
      raise ValueError("Can't be empty.")
    if member_id in self.members:
      raise ValueError(
          f"The member '{member_id}' is already in the groupe."
      )

    self.members.append(member_id)

  def get_due_amount(self, week_number, member_id):
    return self.weekly_contribution

  def get_paid_amount(self, week_number, member_id):
    return self.contributions.get(week_number, {}).get(
        member_id, Decimal("0.00")
    )

  def record_contribution(self, week_number, member_id, amount):
    if member_id not in self.members:
      raise ValueError(f"Unknown member : '{member_id}'")

    pay_amount = Decimal(str(amount))
    if pay_amount <= 0:
      raise ValueError("The pay amount must be more than zero.")

    if week_number not in self.contributions:
      self.contributions[week_number] = {}

    current_paid = self.get_paid_amount(week_number, member_id)
    due = self.get_due_amount(week_number, member_id)
    remaining_due = due - current_paid

    if pay_amount > remaining_due:
      raise ValueError(
          f"Payment above what a member owes that week."
          f" ({remaining_due})"
      )

    new_total = current_paid + pay_amount
    self.contributions[week_number][member_id] = new_total

  def close_week(self):
    unpaid_report = {}
    all_paid_in_full = True

    for member in self.members:
      paid = self.get_paid_amount(self.current_week, member)
      due = self.get_due_amount(self.current_week, member)
      if paid < due:
        all_paid_in_full = False
        unpaid_report[member] = due - paid

    if not all_paid_in_full:
      return {
          "success": False,
          "message": (
              "We can't close the week because there are member who still owe "
          ),
          "unpaid": unpaid_report,
      }

    total_pot = self.weekly_contribution * len(self.members)

    recipient_index = (self.current_week - 1) % len(self.members)
    recipient = self.members[recipient_index]

    self.payout_history.append(
        (self.current_week, recipient, total_pot.quantize(Decimal("0.00")))
    )

    result_recipient = recipient
    result_pot = total_pot

    self.current_week += 1

    return {
        "success": True,
        "message": (
            f"Week {self.current_week - 1} closed successfully. Pot of"
            f" {result_pot} paid to {result_recipient}."
        ),
        "recipient": result_recipient,
        "pot": result_pot,
    }

  def show_report(self):

    report_data = {
        "current_week": self.current_week,
        "fully_paid": [],
        "owes": {},
        "payout_history": self.payout_history,
    }

    for member in self.members:
      paid = self.get_paid_amount(self.current_week, member)
      due = self.get_due_amount(self.current_week, member)
      if paid >= due:
        report_data["fully_paid"].append(member)
      else:
        report_data["owes"][member] = due - paid

    return report_data