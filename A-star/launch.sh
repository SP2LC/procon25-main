#!/bin/bash

ALGORITHMS=("puzzl.py" "L.py 3-3" "L-dynamic.py 4-4" "a_star.py")
SERVER="192.168.2.3"

function launch() {
  echo "launching $1 $2"
  dir=`pwd`
  if [ `uname` = "Darwin" ]
  then
    # Macの場合
    osascript <<EOF
tell application "Terminal"
  activate
  do script with command "cd $dir; pypy $1 local:$SERVER $2"
end tell
EOF
  elif [ `uname` = "Linux" ]
  then
    # Linuxの場合
    gnome-terminal -e "bash -c 'cd $dir; pypy $1 local:$SERVER $2; read'"
  fi
}

for (( i = 0; i < ${#ALGORITHMS[@]}; i++ ))
do
  algo=${ALGORITHMS[$i]}
  launch $algo
done

if [ -e problem.json ]
then
  echo "deleting old problem.json"
  rm problem.json
fi
if [ -e timing ]
then
  rm timing
fi
curl http://$SERVER:8000/ -o problem.json
if [ -e problem.json ]
then
  touch timing
else
  echo "download error"
  exit 1
fi

