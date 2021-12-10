sudo docker-compose down
sudo git pull
sudo docker-compose up --build -d
sudo docker exec -it lettetosanta_app_1 nginx && nginx -s reload
