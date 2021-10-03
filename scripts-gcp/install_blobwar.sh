sudo chmod -R 777 ../*
sudo docker-compose up -d
sudo docker-compose exec app pip3 install -e ./environments/blobwar
