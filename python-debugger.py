import os
import sys

def check_file(file_path):
    if not os.path.isfile(file_path):
        return f"Error: File not found ({file_path})"

    with open(file_path, "r") as f:
        try:
            compile(f.read(), file_path, "exec")
        except SyntaxError as e:
            return f"Error: {e.msg} ({os.path.abspath(e.filename)}, line {e.lineno})"
    return f"{file_path} file is error-free"

def fix_file(file_path, print_result=True):
    with open(file_path, "r") as f:
        try:
            compile(f.read(), file_path, "exec")
            if print_result:
                print(f"{file_path} has no errors.")
            return True
        except SyntaxError as e:
            if print_result:
                print(f"Error: {e.msg} ({os.path.abspath(e.filename)}, line {e.lineno})")
                print(f"File: {e.filename}\nLine: {e.text.strip()}\n{' '*(e.offset-1)}^")
                print("Starting error-fixing process...")

    fixed_file = os.path.splitext(file_path)[0] + "_fixed.py"
    with open(file_path, "r") as f:
        lines = f.readlines()

    with open(fixed_file, "w") as ff:
        for e in sys.path:
            ff.write(f"import sys\nif '{e}' not in sys.path:\n\tsys.path.append('{e}')\n")

        for line_num, line in enumerate(lines, 1):
            fixed_line = line
            try:
                compile(fixed_line, file_path, "exec")
            except SyntaxError as e:
                fixed_line = line[:e.offset] + line[e.offset:].replace("\t", " "*4)
            ff.write(fixed_line)

    if print_result:
        print(f"Error fixed: {fixed_file}")
    return False

def get_options():
    print("Options:")
    print("1. Show errors")
    print("2. Fix errors")
    print("3. Fix errors and save to a new file")
    print("4. Quit program")

    option = input("Which operation would you like to perform? (1/2/3/4): ")
    while option not in ["1", "2", "3", "4"]:
        print("Invalid option, please try again.")
        option = input("Which operation would you like to perform? (1/2/3/4): ")
    return option

def main():
    while True:
        file_path = input("Enter file path: ")
        result = check_file(file_path)
        print(result)

        if "Error" not in result:
            option = get_options()

            if option == "1":
                fix_file(file_path)
            elif option == "2":
                fix_file(file_path)
            elif option == "3":
                fix_file(file_path)
                print("File saved.")
            elif option == "4":
                print("Program terminated.")
                break

if __name__ == "__main__":
    main()
