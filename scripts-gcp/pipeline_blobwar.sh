sudo chmod -R 777 ../*
sudo docker-compose up -d
sudo docker-compose exec app pip3 install -e ./environments/blobwar
docker-compose  exec app mpirun -np 6 python3 train.py -r  -e blobwar -o best -oe 5