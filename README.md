# PROJECT: We&Olufsen
## 소개
- 서울의 다양한 실외, 실내활동을 한눈에 보여주는 사이트
    - 다양한 활동 카테고리 제시
    - 위치 기반 가까운 장소 추천 기능
    - 사용자의 찜을 기반으로 맞춤 추천하는 ML 기능
        - UBCF, IBCF 알고리즘
    
- FE [Github](https://github.com/JJongsKim/Seoul-Walk)

## 팀 인원
![](members.png)

## 개발 기간
- 개발 기간 : 2023-10-15 ~ 2023-12-06
- 협업 툴 : Github, Notion


## 기술 스택
|                                                Language                                                |                                                Framwork                                                |                                               Database                                               |                                                     ENV                                                      |                                                   HTTP                                                   |                                                  Deploy                                                 |
| :----------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------: |:------------------------------------------------------------------------------------------------------: |
| <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> | <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> | <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=black"> | <img src="https://img.shields.io/badge/miniconda3-44A833?style=for-the-badge&logo=anaconda&logoColor=white"> | <img src="https://img.shields.io/badge/postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white"> | <img src="https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white"> 
 
 
## 모델링
![](dbdiagram.png)


## 사이트 시연 영상


## API 명세서
<img width="797" alt="스크린샷 2022-07-30 오후 3 33 59" src="https://private-user-images.githubusercontent.com/91110192/288770976-57e4c706-95a7-4e3c-9da4-7c5e1bd8ccda.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDE5NTU3MjIsIm5iZiI6MTcwMTk1NTQyMiwicGF0aCI6Ii85MTExMDE5Mi8yODg3NzA5NzYtNTdlNGM3MDYtOTVhNy00ZTNjLTlkYTQtN2M1ZTFiZDhjY2RhLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjA3VDEzMjM0MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTVlMmI5ODMzYzdiNzRiMWZhMzQwNmFhNWZlYjk3ODk3NWQ1ZmQxZDhjYjNiMmNiMDMxNDBjZDgyMDUwODkzMTMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.vUmt8inrgeQYyRwqZ-_dBfqUR8mzGvbl2wSiZ0h9Q00">
<img width="789" alt="스크린샷 2022-07-30 오후 3 33 51" src="https://private-user-images.githubusercontent.com/91110192/288771033-87001abd-1754-4a26-b8d9-7429a8260700.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDE5NTU3MjIsIm5iZiI6MTcwMTk1NTQyMiwicGF0aCI6Ii85MTExMDE5Mi8yODg3NzEwMzMtODcwMDFhYmQtMTc1NC00YTI2LWI4ZDktNzQyOWE4MjYwNzAwLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjA3VDEzMjM0MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWM3NDc0NGI5ZDM1NDU5ODg5ZmQ1YTc3ODY4NjFkMGEwNmM5Njg5YWY1ZDA5ZmNkOTU5NjE3NTEzY2ZkNTc3YjEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.X7oxhZtFx4qJYMG14bu2GjBGdESBilkt7ycbdkjYqvc">
<img width="793" alt="스크린샷 2022-07-30 오후 3 33 35" src="https://private-user-images.githubusercontent.com/91110192/288771290-00bc2ef1-8259-44c5-8fa0-d91ef1d41f5c.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDE5NTU3MjIsIm5iZiI6MTcwMTk1NTQyMiwicGF0aCI6Ii85MTExMDE5Mi8yODg3NzEyOTAtMDBiYzJlZjEtODI1OS00NGM1LThmYTAtZDkxZWYxZDQxZjVjLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjA3VDEzMjM0MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTk4NDVmZmI0ZjEyZDNkNTc5ZTA3NjE5YzBlMGIwZmVmM2IxYTBlY2FjOTg0NWM1NjQ0YWU4YjRhMTQ4ZDI5OTcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.oCoqPXitiPeri9cdVpXqMmqxsSO8f4y1NuCRt5br_QU">

* [서울산책 API](https://seoyun.oopy.io/c8bb95c7-558e-4ae4-966d-4353ad337e58)를 보시면, 자세한 API를 확인 가능합니다.