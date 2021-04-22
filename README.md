## 🌟프로젝트 팀명

- KLUSH

## 프로젝트 개요

- 위코드 1차 클론코딩 프로젝트로 핸드메이드 코스메틱 브랜드인 러쉬 코리아의 웹사이트를 모티브로 한 프로젝트입니다.

## 프로젝트 멤버

1. 프론트엔드

- 정새미
- 김희열
- 김태현

2. 백엔드

- 김현영
- 이병재
- 황수민

## 프로젝트 소개

### 개발 기간
2021.04.12 ~ 2021.04.23

### Stack

#### Backend
- Python, Django, bcrypt, pyjwt, MySQL, AqueryTool, AWS EC2, AWS RDS

#### Communication Tool
- Slack, Trello, Github, Postman

## 작업 내용

### 모델링
- AqueryTool을 이용한 ERD 작성

### 엔드포인트 구현
#### 김현영
- 메인 페이지 Nav바 카테고리 데이터 전달 
- 메인 페이지 상품 리스트 데이터 전달  
- 상품 페이지 카테고리 별 상품 데이터 전달
  - Query Parameter를 사용하여 검색, 정렬, 필터 기능 구현

#### 황수민
- 회원가입: 정규표현식 작성하여 조건 부여, 비밀번호 암호화
- 로그인: 토큰 발행, 로그인 데코레이터
- 댓글 CRUD
- 장바구니 CRUD

#### 이병재
- 제품 상세 페이지 상품 데이터 전달
- 제품에 별점 부여,출력 데이터 전달
- 장바구니 CRUD 코드 리팩토링

### 배포
- AWS EC2에 가상환경 구축하여 프로젝트 배포
- AWS RDS에 데이터베이스 구축

## References
- 이 프로젝트는 [러쉬 코리아](https://lush.co.kr/main/index.php)를 참고하여 학습목적으로 만들었습니다.
- 이 프로젝트에서 사용한 이미지는 모두 [unsplashed](https://unsplash.com/)에서 가져온 이미지입니다.
