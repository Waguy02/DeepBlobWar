sudo docker-compose up -d
sudo docker-compose  exec app mpirun -np 7 python3 train.py -o rules  -e blobwar -oe 4 -ru -b -r