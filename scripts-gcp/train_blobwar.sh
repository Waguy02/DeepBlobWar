sudo docker-compose up -d
sudo docker-compose  exec app mpirun -np 7 python3 train.py -r  -e blobwar -o rules -oe 4 -ru