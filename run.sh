#!/bin/bash

tmux rename-window Spotiply
while :
do
    python3 "$(dirname "$0")/main.py"
done
