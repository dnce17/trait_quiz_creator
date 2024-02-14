import sys
import os
import pdfplumber
import json
from quiz import Quiz, Quizzee
from itertools import chain


IDENTIFIERS = {
    "bullets": ["• ", "● "],
    "sub_bullets_1": ["o ", "○ "],
    "sub_bullets_2": ["▪ ", "■ "]
}
EDGE_CASE_ESCAPE = "~o "
DEFAULT_JSON_NAME = "questions.json"
ARGV_LEN = [2,4]


def main():
    if argv_issue := check_cmd_args(sys.argv):
        sys.exit(argv_issue)

    # Stage 1: Convert quiz to json
    pdf_file = open_file(sys.argv[1])
    text_arr = get_text(pdf_file)
    quiz_items = filter_text(text_arr)

    # Compile questions, ans, and traits from arr into json
    make_json(compile_quiz(quiz_items))

    # Stage 2: Ensure traits to track are correct
    user = Quizzee()
    quiz = Quiz(DEFAULT_JSON_NAME, user)

    quiz.show_all_traits(ordered_list = True)
    while ask_user(
        "Are the traits to be tracked correct? Type and enter y/n: ", 
        "\nExiting program....Ensure your PDF doc has no misspelled traits and is correctly formatted.\n"
    ) == False:
        continue

    # Stage 3: Doing quiz
    while ask_user(
        "Type \"y\" to start the quiz or \"n\" if not: ",
        "\nExiting program....Quizzee not ready yet.\n"
    ) == False:
        continue

    if len(sys.argv) == 4:

    user.traits_to_track(quiz.get_all_traits())
    quiz.do_quiz()


def check_cmd_args(cmd_args):
    if check_argv_len(cmd_args) == False:
        print("error 1")
        return "usage: main.py path_to_file [csv_path_to_save_to] [result_header_name]"
    elif len(cmd_args) == 4 and has_csv_ext(cmd_args[2]) == False:
        print("error 2")
        return "Exiting program....Ensure csv file to save to has .csv extension"
    

def check_argv_len(cmd_args):
    if len(cmd_args) not in ARGV_LEN:
        return False


def has_csv_ext(csv_file_name):
    if os.path.splitext(csv_file_name)[1] != ".csv":
        return False


def open_file(f):
    try:
        file = pdfplumber.open(f)
    except FileNotFoundError: 
        sys.exit("File not found. Also ensure that extension is .pdf")
    
    return file


def get_text(f):
    lines_arr = []
    with f as pdf:
        for pg in pdf.pages:
            pdf_text = pg.extract_text(x_tolerance=1)
            # \n to get each line
            lines = pdf_text.split('\n')
            for _, line in enumerate(lines):
                lines_arr.append(line)
    
    return lines_arr


def filter_text(arr):
    # Remove everything before "---questions---"" in arr
    first_filter = remove_unrelated(arr)

    # Combine fragmented sentences that were split from line break
    quiz_items = combine_frag(first_filter)

    return quiz_items


def remove_unrelated(arr):
    try:
        # Search ---questions-- case-insensitive
        index = [item.lower().strip() for item in arr].index('---questions---')
    except ValueError:
        sys.exit("Ensure that ---questions--- is present in your PDF to help indicate where questions begin")

    return arr[index + 1:]


def combine_frag(arr):
    updated_arr = []
    for _, item in enumerate(arr):
        if item[0:2] in list(chain(*IDENTIFIERS.values())):
            # Append b/c "in IDENTIFIERS" means it's a new bullet (hence, new item in arr)
            updated_arr.append(item)
        else:
            # ~o is escape char to differentiate b/w o sub-bullet vs starting o in new line
            if item[0:3] == EDGE_CASE_ESCAPE:
                updated_arr[-1] += f" {item.replace('~', '')}"
            else:
                # Combine fragmented sentences together as 1 item in arr
                updated_arr[-1] += f" {item}"
    
    return updated_arr


def compile_quiz(arr):
    dict_arr = []
    dict = {
        "question": "",
        "choices_and_traits": []
    }

    for i, line in enumerate(arr):
        if line[0:2] in IDENTIFIERS["bullets"]:
            if i > 0:
                dict_arr.append(dict.copy())

            # Reset choices_and_traits if new question (aka new bullet)
            dict["question"] = line[2:]
            dict["choices_and_traits"] = []

        elif line[0:2] in IDENTIFIERS["sub_bullets_1"]:
            dict["choices_and_traits"].append([line[2:]])
        elif line[0:2] in IDENTIFIERS["sub_bullets_2"]:
            dict["choices_and_traits"][-1].append(line[2:].title())
        
        # Appends the last question to arr b/c no more new questions (bullets) after
        if i == len(arr) - 1:
            dict_arr.append(dict.copy())

    return dict_arr


def make_json(dict_arr):
    with open(DEFAULT_JSON_NAME, 'w') as output:
        json.dump(dict_arr, output, indent=2)


def ask_user(prompt_msg, exit_msg):
    prompt = input(prompt_msg).strip().lower()
    if prompt in ["y", "yes"]:
        return True
    elif prompt in ["n", "no"]:
        sys.exit(exit_msg)
    else:
        return False


if __name__ == "__main__":
    main()
    # if argv_issue := check_cmd_args(sys.argv):
    #     sys.exit(argv_issue)