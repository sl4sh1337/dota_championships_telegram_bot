#!/bin/bash
python3 main.py>log 2>&1 &
python3 telegram.py>logtel 2>&1 &
python3 cleaner.py &
