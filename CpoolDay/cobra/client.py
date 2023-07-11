import argparse, requests, os, sys, time, random
from colorama import Fore
from typing import Dict, List

##config
TestMandatorys: List[str] = ['compilation', 'tests']

class TraceParser:
    def __init__(self, Trace) -> None:
        self.winSize = os.get_terminal_size()
        self.Trace: Dict = Trace
        if not isinstance(Trace, Dict):
            raise ValueError('Trace is not Valid')
        for mandatory in TestMandatorys:
            if not mandatory in  self.Trace.keys():
                raise ValueError('Trace is not Valid')
        for line in (r"""
 $$$$$$\                                $$\ $$$$$$$\                            $$\      $$\                     $$\ $$\
$$  __$$\                               $$ |$$  __$$\                           $$$\    $$$ |                    $$ |\__|
$$ /  \__| $$$$$$\   $$$$$$\   $$$$$$\  $$ |$$ |  $$ | $$$$$$\  $$\   $$\       $$$$\  $$$$ | $$$$$$\  $$\   $$\ $$ |$$\
$$ |      $$  __$$\ $$  __$$\ $$  __$$\ $$ |$$ |  $$ | \____$$\ $$ |  $$ |      $$\$$\$$ $$ |$$  __$$\ $$ |  $$ |$$ |$$ |
$$ |      $$ /  $$ |$$ /  $$ |$$ /  $$ |$$ |$$ |  $$ | $$$$$$$ |$$ |  $$ |      $$ \$$$  $$ |$$ /  $$ |$$ |  $$ |$$ |$$ |
$$ |  $$\ $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |$$  __$$ |$$ |  $$ |      $$ |\$  /$$ |$$ |  $$ |$$ |  $$ |$$ |$$ |
\$$$$$$  |$$$$$$$  |\$$$$$$  |\$$$$$$  |$$ |$$$$$$$  |\$$$$$$$ |\$$$$$$$ |      $$ | \_/ $$ |\$$$$$$  |\$$$$$$  |$$ |$$ |
 \______/ $$  ____/  \______/  \______/ \__|\_______/  \_______| \____$$ |      \__|     \__| \______/  \______/ \__|\__|
          $$ |                                                  $$\   $$ |
          $$ |                                                  \$$$$$$  |
          \__|                                           _3WW_   \______/""").split('\n'):
            self.shellPrint(random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]) + line)
            time.sleep(0.2)
        time.sleep(0.2)
        self.shellPrint(Fore.RESET)
        self.dump()

    def dump(self):
        self.shellPrint('=' * self.winSize.columns)
        self.shellPrint('[COMPILATION]')
        self.printDict(self.Trace['compilation'])
        for bin, tests in self.Trace['tests'].items():
            self.shellPrint(Fore.RESET)
            self.shellPrint('=' * self.winSize.columns)
            self.shellPrint(f'[{bin}]')
            self.printDict(tests)

    @staticmethod
    def shellPrint(Prompt: str) -> None:
        sys.stdout.write(f'{Prompt}\n')

    def printDict(self, dict: Dict) -> None:
        for key, value in dict.items():
            self.shellPrint((Fore.RED if 'KO' in value else Fore.GREEN) + f'{key}: {value}')

parser = argparse.ArgumentParser(description="Script de parsing d'arguments")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--register", action="store_true", help="Effectue l'action d'enregistrement")
group.add_argument("--result", action="store_true", help="Effectue l'action de résultat")

args = parser.parse_args()

if args.register:
    TraceParser.shellPrint(requests.post(f'http://193.70.40.62:5000/register/{input("give your git username: ")}', timeout=10).json())
elif args.result:
    TraceParser(requests.get(f'http://193.70.40.62:5000/mouli/{input("give your git username: ")}', timeout=10).json())
