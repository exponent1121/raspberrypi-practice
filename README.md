# 🍓 Raspberry Pi Hardware Interface & Sensor Control

미래제품연구회 스터디를 통해 진행한 라즈베리파이(Raspberry Pi) 기반 임베디드 시스템 제어 및 센서 인터페이스 실습 아카이브입니다. 
Linux 환경에서 다양한 센서 데이터를 수집하고 외부 API 및 웹 스트리밍으로 연동하는 시스템 통합 과정을 다뤘습니다.

## 🛠 개발 환경 (Environment)
* **Hardware:** Raspberry Pi 4 Model B
* **OS:** Raspbian OS (Linux)
* **Language:** `Python 3`
* **Network:** SSH / VNC 환경 구성

---

## 📂 실습 내용 (Contents)

### 1. GPIO 기본 제어 및 타이머 시스템 구축 (`/1_Basic_GPIO`)
* **사용 부품:** LED, Tactile Button, TM1637 (4-Digit 7-Segment Display)
* **구현 내용:** * `gpiozero` 라이브러리를 활용한 물리적 버튼 입력 및 LED 상태 제어.
  * TM1637 디스플레이를 연동하여 실시간 스터디 타이머 및 알람 로직 구현.

### 2. I2C 통신 기반 환경 데이터 수집 및 시각화 (`/2_I2C_Sensor_OLED`)
* **사용 부품:** SHTC3 (온습도 센서), OLED 디스플레이
* **구현 내용:** * I2C 통신 프로토콜을 활용하여 SHTC3 센서로부터 실시간 온도 및 습도 데이터 파싱.
  * 수집된 데이터를 I2C 기반 OLED 화면에 텍스트 및 그래픽 형태로 시각화 출력.

### 3. Telegram API를 활용한 스마트 알림 시스템 (`/3_Telegram_IoT`)
* **구현 내용:** * 하드웨어 센서 데이터와 소프트웨어 메신저를 결합한 IoT 스마트 시스템 기초 구현.
  * Telegram Bot API를 연동하여 특정 조건(예: 온도 변화, 타이머 종료 등) 발생 시 모바일 기기로 푸시 알림 전송 로직 구축.

### 4. 카메라 제어 및 웹 스트리밍 파이프라인 (`/4_Camera_Streaming`)
* **사용 부품:** Raspberry Pi Camera Module
* **구현 내용:** * `rpicam-apps`를 활용한 하드웨어 카메라 모듈 제어 및 이미지/비디오 캡처.
  * `ffmpeg`를 이용한 영상 인코딩(h264 -> mp4) 및 로컬 네트워크(8090 포트) 기반 실시간 웹 스트리밍 환경 구축.

---

## 💡 배운 점 및 핵심 역량 (Key Learnings)
* **Linux 환경 이해:** CLI 명령어를 통한 패키지 관리 및 SSH 원격 제어 환경에서의 개발 경험.
* **통신 프로토콜 숙지:** I2C 통신의 원리를 이해하고 실제 센서와 디스플레이 간의 데이터 파이프라인 구축.
* **시스템 통합 역량:** 센서(입력) -> 라즈베리파이(처리) -> OLED/Telegram(출력 및 알림)으로 이어지는 End
