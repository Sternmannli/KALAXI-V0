#!/usr/bin/env python3
"""
update_tracker.py - Interactive updater for PROJECT_TRACKER.md
Run this after completing tasks to mark them as done.
"""

import re
import os
from datetime import datetime

TRACKER_FILE = "PROJECT_TRACKER.md"

def read_file():
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        return f.read()

def write_file(content):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def update_last_updated(content):
    today = datetime.now().strftime("%Y-%m-%d")
    pattern = r"(\*\*Last updated:\*\* )\d{4}-\d{2}-\d{2}"
    replacement = r"\g<1>" + today
    return re.sub(pattern, replacement, content, count=1)

def extract_tasks(content):
    lines = content.splitlines()
    tasks = []
    bullet_pattern = re.compile(r"^(- \[([ x])\] (.*))")
    table_pattern = re.compile(r"^\|.*\| (☐|☑) (.*?) \|.*$")

    for i, line in enumerate(lines):
        m = bullet_pattern.match(line)
        if m:
            full_line = m.group(1)
            status = m.group(2)
            desc = m.group(3)
            if status == ' ':
                tasks.append((i, full_line, desc, False))
            continue

        m = table_pattern.search(line)
        if m:
            status_symbol = m.group(1)
            desc = m.group(2).strip()
            if status_symbol == '☐':
                tasks.append((i, line, desc, True))
    return tasks

def mark_task_done(line, is_table):
    if is_table:
        return line.replace("☐", "☑", 1)
    else:
        return line.replace("- [ ]", "- [x]", 1)

def main():
    print("\n🔧 PROJECT TRACKER UPDATER")
    print("===========================")

    if not os.path.exists(TRACKER_FILE):
        print(f"Error: {TRACKER_FILE} not found in current directory.")
        return

    content = read_file()
    tasks = extract_tasks(content)

    if not tasks:
        print("No pending tasks found. Great job!")
        return

    print("\nPending tasks:")
    for idx, (_, _, desc, _) in enumerate(tasks, 1):
        print(f"{idx}. {desc}")

    print("\nEnter the numbers of completed tasks (separated by spaces), or 0 to cancel:")
    choice = input("> ").strip()

    if choice == "0":
        print("No changes made.")
        return

    try:
        indices = [int(x) for x in choice.split()]
    except ValueError:
        print("Invalid input. Please enter numbers separated by spaces.")
        return

    to_mark = set(indices)
    lines = content.splitlines()

    for idx, (line_num, original_line, desc, is_table) in enumerate(tasks, 1):
        if idx in to_mark:
            lines[line_num] = mark_task_done(original_line, is_table)
            print(f"Marked: {desc}")

    new_content = "\n".join(lines)
    new_content = update_last_updated(new_content)

    write_file(new_content)
    print(f"\n✅ {TRACKER_FILE} updated. Don't forget to commit the change to GitHub.")

if __name__ == "__main__":
    main()
