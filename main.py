"""
This is the main entry point into the game framework.
To use it, you need to execute it like so:
python3 main.py path/to/game path/to/AI
The idea is that this framework will be useful for all of the example
games in this repo, so it needs to be largely game-agnostic.
"""

from importlib.machinery import SourceFileLoader
import os
import sys
import ui.ui as ui

def load_module_from_path(path):
    """
    Takes a python module of the form path/to/module and returns
    the actual module after importing it.
    """
    module_fname = path.split(os.sep)[-1]
    if module_fname.endswith(".py"):
        module_name = module_fname[:-3]
    else:
        module_name = module_fname
    module = SourceFileLoader(module_name, path).load_module()
    return module


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE: python3 " + sys.argv[0] +\
                " path/to/game path/to/ai" + os.linesep)
        exit(1)
    else:
        try:
            game_module = load_module_from_path(sys.argv[1])
        except Exception as e:
            print("Problem loading game module.")
            print(e)
            raise e
        try:
            ai_module = load_module_from_path(sys.argv[2])
        except Exception as e:
            print("Problem loading ai module.")
            print(e)
            raise e

        ui.game_module = game_module
        ui.ai_module = ai_module
        ui.start_game()


