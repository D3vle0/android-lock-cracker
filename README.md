# android-lock-cracker

<p align="center">
  <img width="230" src="./img/lock.png">
</p>

<p align="center"><b>안드로이드 기기의 잠금을 해제하세요!</b></p>

## 개요

2022학년도 1학기 공업일반 1인 1프로젝트 과제입니다.  
- 연구 주제: 안드로이드 포렌식: 안드로이드의 잠금 화면에 대한 탐구
- 연구 내용
    1. 간단한 안드로이드 역사
    2. 안드로이드 시스템의 화면 잠금 종류
    3. 잠금 화면 무력화 방법
    4. 패턴, PIN 알아내기
    5. 패턴, PIN을 알아내는 크래킹 프로그램 개발
    6. 해킹 문제 개발

## 크래킹 툴 사용법

### 설치

```sh
git clone https://github.com/d3vle0/android-lock-cracker
cd android-lock-cracker
pip3 install python-dotenv
```

https://developer.android.com/studio/releases/platform-tools?hl=ko  
이곳에서 ADB (Android Debug Bridge) 를 다운받습니다.

https://drive.google.com/file/d/1lqEwuR0ZDDjS_gJ3wqiKmGsWJsm53nj0/view?usp=sharing  
이곳에서 rainbow table 데이터베이스를 프로젝트 루트 경로에 다운받습니다.

### .env 세팅

adb 바이너리의 경로를 `.env`에 기입합니다.

```sh
ADB_PATH = ...
```

### 실행

```sh
# 잠금 무력화
python3 crack.py --del
# PIN 
python3 crack.py --pin 길이
# 패턴
python3 crack.py --pattern
# 도움말
python3 crack.py -h
python3 crack.py --help
```

### 주의 사항

- 루팅 작업이 된 기기만 작동합니다.
- Android 4.4 이하 버전에서만 작동합니다.

## CTF 문제 세팅

### Docker 설치

```sh
curl -fsSL https://get.docker.com/ | sh
sudo service docker start
```

### Docker 이미지 빌드

```sh
cd ctf/settings
sudo chmod +x start.sh
cd ../
sudo chmod +x run-docker.sh
sudo ./run-docker.sh
```

### nc 서버 접속

```sh
nc <주소> 3000
```