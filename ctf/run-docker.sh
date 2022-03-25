#!/bin/bash
NAME="android"

sudo docker kill $NAME
sudo docker rm $NAME
sudo docker build --tag $NAME:1 ./

PORT="-p 3000:3000"
OPTION="-dit"

DEV_OPTION="--cap-add=SYS_PTRACE --security-opt seccomp=unconfined"

sudo docker run $OPTION $PORT --name $NAME $NAME:1 /start.sh
sudo docker exec -it $NAME /bin/bash