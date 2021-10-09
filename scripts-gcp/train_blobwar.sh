sudo docker-compose up -d
sudo docker-compose exec app pip3 install -e ./environments/blobwar
sudo docker-compose  exec app mpirun -np 8 python3 train.py -r  -e blobwar -o best -oe 3