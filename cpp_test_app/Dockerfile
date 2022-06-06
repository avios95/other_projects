FROM gcc:latest
ADD ./cpp_test_app /root/build/app
WORKDIR /root/build/app/

RUN sed -i 's#Greeting.*#Greeting = "Hi there"#g' ./settings.conf && g++ ./main.cpp && ./a.out
