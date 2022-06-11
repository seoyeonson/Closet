# TeamProj2

--저장시 부탁드립니다.--

1. Commit Summay는 반드시 본인이름#날짜/시간 으로 해주세요. (ex 손서연#5.21/14:00) 언제 어떤작업을 했는지 설명하기 쉬워집니다!

2. Description에는 최근 본인의 작성내용 -> 파일주소/명 수정내용(주석으로 꼭 표시) 해주세요. 다른사람이 변경내용을 빠르게 찾기 용이해집니다! ex) Test/main.html header 추가

3. 작업 전 항상 새로운 파일이 있는지 확인해주시고, 작업 후 업로드시에는 카톡방에 업로드 했다고 남겨주세요. 다른 사람이 새로운파일이 있는지 없는지 알기 쉬워집니다!

# DB에 더미데이터 저장하는법

1. pillow 모듈 설치 (ImageField 사용을 위해 필요)  
   cmd 관리자 권한으로 실행 > pip intall Pillow  
2. migration, migrate  
   터미널로 sqlite3 실행하여 테이블 생성된 것 확인  
3. 터미널로 sqlite3 에 연결, 외래키 활성화 하기  
   sqlite3 창에 PRAGMA foreign_keys; >> 결과값으로 0 또는 1 반환 (0:비활성화, 1:활성화)  
   PRAGMA foreign_keys = 1; 실행 후 직전 코드 다시 실행하여 활성화 되었는지 확인    
   참조 : https://thinking-jmini.tistory.com/12
5. 구글드라이브 > dummydata 폴더  
   DB_상품&카테고리.ipynb 파일 내 코드 순차적으로 모두 실행  
   ** products.xlsx 파일과, 우리프로젝트의 db.sqlite3 파일을 사용합니다. 본인 컴퓨터의 파일 경로로 꼭 수정해주세요. **  
6. 구글드라이브 > DML-category_code수정.ipynb 파일 내 코드 실행  
   ** 마찬가지로 파일경로를 수정하여 실행해주세요. **  
   
# 실행전 체크사항

1. django-mathfilters 설치
   ```pip install django-mathfilters```
   숫자 천단위마다 (,) 콤마 추가하는 template tag

2. ~/model/utils/FindAnswer
   tag_to_word() 안 디렉토리 경로 변경(74번째 줄)
   ```~/model/category/```

# flask-cors 에러날 경우

1. ```pip install -U flask-cors```