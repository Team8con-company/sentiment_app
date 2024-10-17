# 기업 이미지 감성분석
**사용 데이터** : 네이버 뉴스 기사 크롤링(최근 100개)   
**기업 기준** : 코스피 시가총액 상위 100개 기업   
   
**사용 기술 및 프레임워크**    
- **감성분석 모델** : klue/bert-base   
- **프레임워크** : Django   
- **DB** : MySQL DB (GCP로 원격 접속 연결)   

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

