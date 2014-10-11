#!/bin/sh

ALGORITHMS="puzzl L L-dynamic"
SERVER="192.168.10.16"

function launch() {
  echo "launching $1.py"
  dir=`pwd`
  osascript <<EOF
tell application "Terminal"
  activate
  do script with command "cd $dir; pypy $1.py local:$SERVER"
end tell
EOF
}

curl http://$SERVER:8000/ -o problem.json

for algo in $ALGORITHMS
do
  launch $algo
done
