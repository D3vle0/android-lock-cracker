FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN sed -e 's/\/\/archive.ubuntu.com\/ubuntu/\/\/mirror.kakao.com\/ubuntu/g' /etc/apt/sources.list > ~/sources.list && mv ~/sources.list /etc/apt/sources.list

RUN apt-get update
RUN apt-get install net-tools xinetd python3 python3-pip curl netcat -y
RUN pip3 install python-dotenv

RUN useradd -d /home/android android -s /bin/bash
RUN mkdir /home/android

RUN chown -R root:android /home/android
RUN chmod 750 /home/android

ADD ./prob/help.py /home/android/help.py
ADD ./prob/main.py /home/android/main.py
ADD ./prob/prob.py /home/android/prob.py
ADD ./prob/flag /flag

RUN chown root:android /flag
RUN chmod 440 /flag

RUN curl -o /home/android/GestureRainbowTable.db http://146.56.134.145:31337/file/GestureRainbowTable.db
RUN echo "RAINBOWTABLE_PATH=/home/android/GestureRainbowTable.db" >> .env

ADD ./settings/android.xinetd /etc/xinetd.d/prob
ADD ./settings/start.sh /start.sh