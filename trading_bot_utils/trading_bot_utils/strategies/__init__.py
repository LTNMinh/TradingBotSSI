import glob
import importlib
import os
from inspect import getmembers, isclass

dir_path = os.path.dirname(os.path.realpath(__file__))
list_files = glob.glob(f"{dir_path}/*.py")
for file in list_files:
    module_name = file.split("/")[-1][:-3]
    if module_name != "__init__":
        module_name = f"trading_bot_utils.strategies.{module_name}"
        my_module = importlib.import_module(module_name)
        module_dict = my_module.__dict__
        my_class = getmembers(my_module, isclass)
        for c in my_class:
            if module_name == c[1].__module__:
                globals().update({c[0]: c[1]})
