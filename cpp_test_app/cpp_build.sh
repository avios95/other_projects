#!/bin/bash
if ! [ -d /root/task ]; then mkdir /root/task ; fi
if ! [ -d /root/task/cpp_test_app ]; then cd /root/task/ ; git clone https://github.com/fitsula/cpp_test_app.git ; fi
if ! [ -f `which docker 2>&1|awk '{print $1$2}'` ]; then  curl -sSL https://get.docker.com/ | sh  ; service docker start ; fi


cd /root/task/
echo "FROM gcc:latest
ADD ./cpp_test_app /root/build/app
WORKDIR /root/build/app/

RUN sed -i 's#Greeting.*#Greeting = \"Hi there\"#g' ./settings.conf && g++ ./main.cpp && ./a.out"  > Dockerfile

docker build -t docker-cpp   ./



docker tag docker-cpp:latest avios/cpp_test_image:latest
#docker login -u "myusername" -p "mypassword" docker.io
docker push avios/cpp_test_image:latest

   
