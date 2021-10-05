if [ $# -eq 0 ]
  then
  docker-compose exec app pip3 python3 play.py
else
  docker-compose exec app pip3 python3 play.py -s "$1"
fi

