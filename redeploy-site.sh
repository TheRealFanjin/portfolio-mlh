#!/bin/bash
cd ~/portfolio-mlh
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
systemctl daemon-reload
systemctl restart myportfolio
