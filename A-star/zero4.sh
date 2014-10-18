#!/bin/bash

#ALGORITHMS=("a_star.py" "puzzl.py" "rl-puzzl.py" "tree_puzzle.py") #"dynamic.py" "tree-L.py 3-3" "tree-L.py 3-4" "tree-L.py 4-4" "L.py 3-3" "L.py 3-4" "L.py 4-4")
ALGORITHMS=("puzzl.py")
SERVER="192.168.2.7"

function launch() {
  echo "launching $1 $2"
  dir=`pwd`
  if [ `uname` = "Darwin" ]
  then
    # Macの場合
    osascript <<EOF
tell application "Terminal"
  activate
  do script with command "cd $dir; pypy $1 zero4:$SERVER $2"
end tell
EOF
  elif [ `uname` = "Linux" ]
  then
    # Linuxの場合
    gnome-terminal -e "bash -c 'cd $dir; pypy $1 zero4:$SERVER $2; read'"
  fi
}

if [ -e zero4-problem.json ]
then
  echo "deleting old zero4-problem.json"
  rm zero4-problem.json
fi
if [ -e zero4-timing ]
then
  rm zero4-timing
fi

for (( i = 0; i < ${#ALGORITHMS[@]}; i++ ))
do
  algo=${ALGORITHMS[$i]}
  launch $algo
done

curl http://$SERVER:8000/zero4 -o zero4-problem.json
if [ -e zero4-problem.json ]
then
  touch zero4-timing
else
  echo "download error"
  exit 1
fi

