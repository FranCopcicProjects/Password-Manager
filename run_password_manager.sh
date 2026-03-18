#!/bin/bash

python3 -m pip install pycryptodome

python3 main.py init mAsterPasswrd
python3 main.py put mAsterPasswrd www.fer.hr neprobojnAsifrA
python3 main.py get mAsterPasswrd www.fer.hr
python3 main.py get wrongPasswrd www.fer.hr
python3 main.py put mAsterPasswrd www.fer.hr novaLozinka123
python3 main.py get mAsterPasswrd www.fer.hr
python3 main.py get mAsterPasswrd www.github.com