#!/bin/bash
tmux kill-server
cd ~/portfolio-mlh
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
tmux new-session -d -s mlh_server 'flask run --host=0.0.0.0'