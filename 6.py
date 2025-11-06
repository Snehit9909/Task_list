import json
from collections import Counter, defaultdict
from datetime import datetime

def load_data(file):
    with open(file, 'r') as f:
        return json.load(f)

def get_week(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("Week %W")

def weekly_report(data):
    weeks = defaultdict(Counter)
    for entry in data:
        if entry["done"]:
            week = get_week(entry["date"])
            weeks[week][entry["habit"]] += 1
    return weeks

def print_report(weeks):
    for week, habits in sorted(weeks.items()):
        print(f"\n{week}")
        for habit, count in habits.items():
            print(f"  {habit}: {count} times")

if __name__ == "__main__":
    data = load_data("habit.json")
    report = weekly_report(data)
    print_report(report)
