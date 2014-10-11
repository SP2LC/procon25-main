#!/bin/bash

ALGORITHMS=("puzzl.py" "L.py 3-3" "L-dynamic.py 4-4" "a_star.py")
SERVER="192.168.10.16"

function launch() {
  echo "launching $1 $2"
  dir=`pwd`
  osascript <<EOF
tell application "Terminal"
  activate
  do script with command "cd $dir; pypy $1 local:$SERVER $2"
end tell
EOF
}

curl http://$SERVER:8000/ -o problem.json

for (( i = 0; i < ${#ALGORITHMS[@]}; i++ ))
do
  algo=${ALGORITHMS[$i]}
  launch $algo
done
