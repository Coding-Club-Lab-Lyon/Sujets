import requests, sys, os, json, getpass
from typing import Dict, List
from colorama import Fore, Style


##config
TestMandatorys: List[str] = ['compilation', 'tests']
cobraPaswsd: str = getpass.getpass('Give cobra password: ')
keysOrderTests: List[str] = ["my_print_ascii", "my_print_n_ascii", "my_print_revert", "my_char_replace", "my_get_char_repeat", "my_absolute", "my_square", "my_little_bistro", "my_print_square", "my_average", "my_get_words", "my_rotate_alpha", "my_sort", "my_get_value"]

class TraceParser:
    def __init__(self, Trace, index) -> None:
        self.winSize = os.get_terminal_size()
        if index:
            self.Trace: Dict = Trace[index - 1]
            for mandatory in TestMandatorys:
                if not mandatory in  self.Trace.keys():
                    raise ValueError('Trace is not Valid')
            self.shellPrint(Fore.RESET)
            self.dump()
        else:
            for i in range(len(Trace)):
                self.shellPrint('Trace ' + str(i))
                self.Trace: Dict = Trace[i]
                for mandatory in TestMandatorys:
                    if not mandatory in  self.Trace.keys():
                        raise ValueError('Trace is not Valid')
                self.shellPrint(Fore.RESET)
                self.dump()

    def dump(self):
        self.shellPrint('=' * self.winSize.columns)
        self.shellPrint('[COMPILATION]')
        self.printDict(self.Trace['compilation'])
        binsTests = {key: self.Trace['tests'][key] for key in keysOrderTests if key in self.Trace['tests']}
        for bin, tests in binsTests.items():
            self.shellPrint(Fore.RESET)
            self.shellPrint('=' * self.winSize.columns)
            self.shellPrint(f'[{bin}]')
            self.printDict(tests)
        self.shellPrint(Fore.RESET)
        self.shellPrint('=' * self.winSize.columns)

    @staticmethod
    def shellPrint(Prompt: str) -> None:
        sys.stdout.write(f'{Prompt}\n')

    def printDict(self, dict: Dict) -> None:
        for key, value in dict.items():
            self.shellPrint((Fore.RED if 'KO' in value else Fore.GREEN) + f'{key}: {value}')


def display_menu(options):
    print("Choose an option:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    print()

def get_user_choice(options):
    while True:
        try:
            choice = input("Enter the number of your choice ('q' to quit, 'm' to go back to the menu): ")
            if choice == 'q':
                sys.exit("You have quit the program.")
            elif choice == 'm':
                return None
            choice = int(choice)
            if choice < 1 or choice > len(options):
                print("Please enter a valid number.")
                continue
            return choice
        except ValueError:
            print("Please enter a valid number.")

def handle_mouli_option():
    while True:
        print("Option 'mouli' selected.")
        print("Two additional options available:")
        print("1. All")
        print("2. User")
        print()
        choice = get_user_choice(["All", "User"])
        if choice is None:
            break
        if choice == 1:
            print(Fore.YELLOW + 'Rsponse: \n')
            print(requests.post('http://193.70.40.62:5000/mouli', json={"psswd":cobraPaswsd}).json())
            print(Style.RESET_ALL)
        elif choice == 2:
            print("Option 'User' selected.")
            user_input = input("Enter username: ")
            print(Fore.YELLOW + 'Rsponse: \n')
            print(requests.post(f'http://193.70.40.62:5000/mouli/{user_input}', json={"psswd":cobraPaswsd}).json())
            print(Style.RESET_ALL)
        break

def handle_get_result_option():
    print("Option 'get result' selected.")
    username = input("Enter username: ")
    number = input("Enter a number: ")
    print(Fore.YELLOW + f"{username} Trace: {number}" + Style.RESET_ALL)
    TraceParser(requests.get(f'http://193.70.40.62:5000/mouli/{username}').json(), int(number))

def handle_manual_option():
    options = ["post", "get", "delete"]
    display_menu(options)
    choice = get_user_choice(options)
    if choice == 1:
        print('\n'+ Fore.YELLOW + json.dumps(requests.post(f'http://193.70.40.62:5000/{input("Enter request: /")}').json(), indent=4) + Style.RESET_ALL + '\n')
    if choice == 2:
        print('\n'+ Fore.YELLOW + json.dumps(requests.get(f'http://193.70.40.62:5000/{input("Enter request: /")}').json(), indent=4) + Style.RESET_ALL + '\n')
    if choice == 3:
        print('\n'+ Fore.YELLOW + json.dumps(requests.delete(f'http://193.70.40.62:5000/{input("Enter request: /")}').json(), indent=4) + Style.RESET_ALL + '\n')

def main():
    global cobraPaswsd
    while True:
        options = ["play mouli", "get result", "manual request", "set cobra password"]
        print(Fore.YELLOW + "========== MENU ==========" + Style.RESET_ALL)
        display_menu(options)
        choice = get_user_choice(options)

        if choice is None:
            continue

        if choice == 1:
            handle_mouli_option()
        elif choice == 2:
            handle_get_result_option()
        elif choice == 3:
            handle_manual_option()
        elif choice == 4:
            cobraPaswsd = getpass.getpass('Give cobra password: ')

if __name__ == "__main__":
    main()
