prob_id=$1
server=$2

prob_file=`printf 'prob%d02d.ppm' $prob_id`

printf 'Downloading prob%02d from %s\n' $prob_id $server

if [ ! -d problems ]
then
  mkdir problems
fi

curl -o problems/$prob_file "http://$server/problem/$prob_file"

if [ -e problems/$prob_file ]
then
  echo "Success"
else
  echo "Failed"
fi
