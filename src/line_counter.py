"""
This program counts the number of lines in python
files in the current directory and all subdirectories.
"""

import os


def count_lines(fname):
    """
    Counts the number of lines in a file.
    """
    num_lines = 0
    with open(fname) as f:
        for line in f:
            num_lines += 1
    return num_lines


def count_python_lines(startpath):
    """
    Counts the number of lines in all python
    files in the current directory and all subdirectories.
    """
    total_lines = 0
    for root, _, files in os.walk(startpath):
        for file in files:
            if file.endswith(".py"):
                num_lines = count_lines(os.path.join(root, file))
                print(f"{os.path.join(root, file)} has {num_lines} lines")
                total_lines += num_lines

    print(f"Total number of lines: {total_lines}")


if __name__ == "__main__":
    count_python_lines(".")
