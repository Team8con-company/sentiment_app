# 기업 이미지 감성분석
본 프로젝트는 기업 이미지의 긍정/부정을 판별하기 위해 뉴스 기사를 크롤링하고 감성 분석을 수행하는 종합적인 시스템을 개발하는 것을 목표로 한다. 프로젝트의 주요 구성 요소와 워크플로우는 다음과 같다:

### **데이터 수집**

- 뉴스 기사 크롤러를 개발하여 기업 관련 뉴스 제목, 링크, 작성 날짜를 수집한다.
- 크롤링된 데이터는 Google Cloud Platform(GCP)에 호스팅된 데이터베이스에 저장한다.

### **감성 분석**

- 머신러닝 모델을 개발하여 수집된 뉴스 제목의 감성(긍정, 부정, 중립)을 분류한다.
- 모델은 각 기업에 대한 뉴스의 긍정적 또는 부정적 감성을 판단한다.
- 분석 결과는 GCP 데이터베이스에 저장한다.

### **데이터 시각화**

- Django 웹 서버를 구축하여 분석 결과를 시각적으로 표현한다.
- 웹 페이지에서 데이터베이스에 저장된 감성 분석 결과를 불러와 긍정, 부정 비율을 집계한다.
- 기업별 빈출 키워드를 워드클라우드 형태로 표시한다.

### **시스템 아키텍처**

- GCP를 활용하여 원격 접속이 가능한 데이터베이스를 구성한다.
- 크롤러, 감성 분석 모듈, 웹 시각화 모듈을 분리하여 개발한다.
- 각 모듈은 GCP 데이터베이스를 통해 데이터를 공유하고 통합된다.   

이 프로젝트를 통해 기업들은 자사의 이미지가 언론에서 어떻게 비춰지고 있는지 실시간으로 모니터링하고 분석할 수 있다. 이는 기업의 평판 관리와 전략적 의사결정에 가치있는 인사이트를 제공할 수 있다. 
<img width="1280" alt="스크린샷 2024-10-17 17 58 45" src="https://github.com/user-attachments/assets/07a5b638-b4b9-4155-b3b0-21035e83fbf5">


---
**사용 데이터** : 네이버 뉴스 기사 크롤링(최근 100개)   
**기업 기준** : 코스피 시가총액 상위 100개 기업   
   
**사용 기술 및 프레임워크**    
- **감성분석 모델** : klue/bert-base   
- **프레임워크** : Django   
- **DB** : MySQL DB (GCP로 원격 접속 연결)

--- 

## 코드 사용법
1. `git clone https://github.com/Team8con-company/sentiment_app.git`
2. 가상환경 활성화 후, `pip install -r requirements.txt`
3. 테스트 서버 실행, `python manage.py runserver`
4. APP 이름은 search로, url에 `/search` 를 입력하면 된다.

## APP 구조
```
📦sentiment_app
 ┣ 📂search
 ┃ ┣ 📂management           # 더미데이터 생성파일
 ┃ ┃ ┗ 📂commands
 ┃ ┃ ┃ ┗ 📜generate_korean_dummy_data.py
 ┃ ┣ 📂migrations           # DB migration
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂static               # CSS
 ┃ ┃ ┣ 📂fonts
 ┃ ┃ ┃ ┗ 📜SB M.ttf
 ┃ ┃ ┗ 📂search
 ┃ ┃ ┃ ┗ 📂css
 ┃ ┃ ┃ ┃ ┗ 📜index.css
 ┃ ┣ 📂templates            # html
 ┃ ┃ ┗ 📂search
 ┃ ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py            
 ┃ ┣ 📜models.py            # DB model
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py              # url
 ┃ ┗ 📜views.py             # views
 ┣ 📂sentiment_app
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜settings.py          # 환경설정 파일
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜wsgi.py
 ┣ 📜.gitignore
 ┣ 📜db.sqlite3
 ┣ 📜manage.py
 ┗ 📜requirements.txt 
```

