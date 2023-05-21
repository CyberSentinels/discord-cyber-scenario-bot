docker rm dev-cyberscenariobot --force
docker rmi dev-cyberscenariobot
docker build . -t dev-cyberscenariobot
