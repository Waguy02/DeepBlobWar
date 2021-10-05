if "%1"==""  goto DefaultSize
docker-compose exec app pip3 python3 play.py -s %1
goto End
:DefaultSize
docker-compose exec app pip3 python3 play.py
:End
