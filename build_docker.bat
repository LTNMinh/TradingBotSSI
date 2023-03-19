@echo off 
SET pwd=%cd%
cd trading_bot_utils
python setup.py bdist_wheel sdist
cd %pwd%