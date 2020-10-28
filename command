docker stop flask-userinfo
docker rm flask-userinfo
docker stop mariadbtest
docker rm mariadbtest
docker build -t cph1c06/flask-userinfo .
docker run --name mariadbtest -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mypass -d mariadb/server:10.3
sleep 10 
docker run --name flask-userinfo --link mariadbtest:3306 -p 5000:5000 -it --entrypoint python3 cph1c06/flask-userinfo -m pytest 
#docker run -ti --rm -v $(pwd):/apps alpine/flake8:3.8.4 *.py