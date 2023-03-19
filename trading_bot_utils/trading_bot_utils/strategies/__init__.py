import importlib
import os
from inspect import getmembers, isclass

dir_path = os.path.dirname(os.path.realpath(__file__))
for file in os.listdir(dir_path):
    if file.endswith(".py"):
        module_name = file[:-3]
        if module_name != "__init__":
            module_name = f"trading_bot_utils.strategies.{module_name}"
            my_module = importlib.import_module(module_name)
            module_dict = my_module.__dict__
            my_class = getmembers(my_module, isclass)
            for c in my_class:
                if module_name == c[1].__module__:
                    globals().update({c[0]: c[1]})