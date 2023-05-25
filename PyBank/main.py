from csv import DictReader
from pathlib import Path
from typing import List


def main():
    """
    Script that calculates various financial analyses based on input data from a static location

    total_months: total number of changes from month to month, plus 1 for the first month

    net_total: sum of all profits and losses

    greatest_inc: greatest increase in earnings

    inc_month: the month of greatest_inc

    greatest_dec: greatest decrease in earnings

    dec_month: the month of greatest_dec

    avg_change: average of all earnings changes across all months
    """
    net_total: int = 0
    income_changes: List[int] = []
    greatest_inc: int = 0
    inc_month: str = ""
    greatest_dec: int = 0
    dec_month: str = ""

    with Path("Resources/budget_data.csv").open(mode="r", encoding="utf-8", newline="\n") as csv:
        field_names = csv.readline().strip().split(',') # ["Date", "Profit/Losses"]
        csvreader = DictReader(csv, fieldnames=field_names)
        prev_income: int = 0
        income: int = 0
        net_income: int = 0

        for line in csvreader:
            income = int(line["Profit/Losses"])
            net_total += income
            net_income = income - prev_income

            # month 1 can't have a change, there's no previous month to compare to
            if prev_income != 0:
                income_changes.append(net_income)

                if net_income > greatest_inc:
                    greatest_inc = net_income
                    inc_month = line["Date"]

                if net_income < greatest_dec:
                    greatest_dec = net_income
                    dec_month = line["Date"]

            prev_income = income

    # month 1 didn't have a change, so it wasn't stored. add it back here
    total_months: int = len(income_changes) + 1

    avg_change: int = sum(income_changes) / len(income_changes)

    analysis: str = (
        "Financial Analysis\n\n"
        "----------------------------\n\n"
        f"Total Months: {total_months}\n\n"
        f"Total: ${net_total}\n\n"
        f"Average Change: ${avg_change:.2f}\n\n"
        f"Greatest Increase in Profits: {inc_month} (${greatest_inc})\n\n"
        f"Greatest Decrease in Profits: {dec_month} (${greatest_dec})\n"
    )

    print(analysis)

    Path("analysis/analysis.txt").write_text(analysis,encoding="utf-8")


if __name__ == "__main__":
    main()
