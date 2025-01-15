import subprocess
import sys
import os

def run_command(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def print_success_message():
    success_art = r"""
  _____________ ____________ _________ ___________ _________ _________
 /   _____/    |   \_   ___ \\_   ___ \\_   _____//   _____//   _____/
 \_____  \|    |   /    \  \//    \  \/ |    __)_ \_____  \ \_____  \
 /        \    |  /\     \___\     \____|        \/        \/        \
/_______  /______/  \______  /\______  /_______  /_______  /_______  /
        \/                 \/        \/        \/        \/        \/
    """
    print(f"\033[92m{success_art}\033[0m")

def print_failure_message():
    failure_art = r"""
________________  .___.____     ____ ________________________
\_   _____/  _  \ |   |    |   |    |   \______   \_   _____/
 |    __)/  /_\  \|   |    |   |    |   /|       _/|    __)_
 |     \/    |    \   |    |___|    |  / |    |   \|        \
 \___  /\____|__  /___|_______ \______/  |____|_  /_______  /
     \/         \/            \/                \/        \/
    """
    print(f"\033[91m{failure_art}\033[0m")

def main() -> None:
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: ./tester <test_file> <main.py> [solver]")
        sys.exit(1)

    test_file = sys.argv[1]
    main_py = sys.argv[2]
    solver = sys.argv[3] if len(sys.argv) == 4 else None

    main_output = run_command(['python', main_py, test_file])
    with open('main_output.txt', 'w') as f:
        f.write(main_output)

    if solver:
        solver_output = run_command([solver, test_file])
        with open('solver_output.txt', 'w') as f:
            f.write(solver_output)

        diff_output = run_command(['diff', 'main_output.txt', 'solver_output.txt'])
        if diff_output:
            print(diff_output)
            print_failure_message()
        else:
            print_success_message()

        os.remove('solver_output.txt')
    else:
        print_success_message()

    os.remove('main_output.txt')

if __name__ == '__main__':
    main()