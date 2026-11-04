새 프로젝트 만들기.

# 전체 프로젝트 폴더 생성
`cd ~/원하는 폴더 위치로 이동`  
`mkdir 폴더명` : 폴더 생성  
`cd 폴더명`  

## Git 초기 설정
`git init -b main` : 로컬 Git 저장소 만들고 main 브랜치 만들기.  
&nbsp;&nbsp;&nbsp;&nbsp; `-b`: -initial-branch 의 축약어. 초기 브랜치 설정.  
`git status` : Git 생성 확인
`code .` : vscode 에서 폴더 열기  


## 프론트엔드 프로젝트 생성
`node -v` , `npm -v` : 현재 설치 버전 확인  
`npx create-next-app@latest frontend` : 프론트 프로젝트 생성  
추천 설정대로 설치하는 방법 과 직접 설정을 커스텀해서 설치하는 방법이 있음.  


### Docker compose 설정하기
Docker compose 로 lib 를 관리하되, vscode 도 해당 컨테이너와 연결할 수 있도록 확장프로그램 Dev Containers 설치.

#### frontend/Dockerfile 파일 작성
```
# Node.js 24 가 설치된 Linux 이미지를 기반으로 사용.
FROM node:24-bookworm-slim

# 컨테이너 내부 작업 폴더를 /app 으로 지정
WORKDIR /app

# 패키지 목록과 버전 기록을 작업 폴더에 복사
COPY package.json package-lock.json ./

# 기록된 버전대로 패키지 설치
RUN npm ci

# 프론트 소스를 작업 폴더에 복사
COPY . .

# 앱이 사용하는 포트를 문서화
# EXPOSE 만으로 맥에서 접속할 수 있는 건 아니고, 포트 연결은 Compose 가 설정한다.
EXPOSE 3000

# 컨테이너 시작 시 개발 서버 실행
# RUN 은 이미지를 만들 때, CMD 는 컨테이너를 실행할 때 사용한다.
# -- : 뒤에 있는 옵션을 npm 이 아니라 실제 개발 서버 명령에 전달한다는 뜻.
# 0.0.0.0 : 컨테이너 밖에서 들어오는 연결도 받을 수 있도록 지정한 주소.
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
```

#### frontend/.dockerignore 파일 작성
```
# 이 파일에는 이미지를 만들 때 복사 대상에서 제외할 항목을 적는다.
node_modules
.next
.git
.env*
npm-debug.log*
```

### 최상위 폴더 위치에서 compose.yaml 파일 작성
```
services:
    frontend:
        build:
            # build.context: frontend/Dockerfile 로 이미지 생성
            context: ./frontend
        ports:
            # 맥의 5175 port 를 컨테이너의 3000 port 에 연결
            - "127.0.0.1:5175:3000"
        volumes:
            # 왼쪽:오른쪽 -> 왼쪽의 저장공간을 오른쪽에 컨테이너 경로에 연결해라 라는 의미.
            # 로컬의 frontend 파일을 컨테이너 기본 폴더로 지정한 /app 과 연결.(Dockerfile 참고.)
            - ./frontend:/app
            # /app/node_modules: npm의 패키지 설치 방식
            # 운영체제가 달라져도 문제 없도록 설치한 외부 패키지는 컨테이너에도 따로 보관.
            - frontend_node_modules:/app/node_modules
            # /app/.next: Next.js 프로젝트 구조, 빌드 설명 
            # 작성한 소스를 브라우저와 서버에서 실행할 형태로 빌드한 결과물과, 다음 변환을 빠르게 처리하기 위해 쌓이는 캐시 등이 .next 폴더에 들어간다.
            - frontend_next:/app/.next

# Docker가 관리할 볼륨(저장공간) 이름을 정한다.
volumes:
    # 컨테이너용 패키지를 별도 보관 (Next.js, React, TypeScript 등)
    frontend_node_modules:
    # Next.js가 생성하는 빌드,캐시 파일을 별도 보관
    frontend_next:
```  

직접 터미널에서 컨테이너 내부 쉘을 확인하는 코드  
`docker compose exec frontend sh` : 최상위 폴더 위치에서 명령어 입력, frontend 쉘을 연다.  
`pwd` : 현재 위치 확인  
`ls -la` : 현재 폴더의 파일 목록 확인. -a 가 있어야 . 으로 시작하는 폴더도 보임  
`ls /` : 컨테이너의 최상의 폴더들 확인.  
`exit` : 쉘 나오기  


#### vscode - 컨테이너 연결하기
1. Cmd + Shift + P로 명령 팔레트를 열기.
2. Dev Containers: Attach to Running Container...를 검색해서 선택.
3. 목록에서 magic-webgame-frontend-1처럼 frontend가 포함된 컨테이너를 선택.
4. 새 VS Code 창이 열리면 파일 → 폴더 열기에서 /app을 연다.
컨테이너 내부의 가상공간이 열린다. 내부에서 작업하더라도 내 컴퓨터와는 소스를 공유한다.


## 백엔드 프로젝트 생성
```
root-project/
├── compose.yaml
├── frontend/
└── backend/
    ├── requirements.txt
    └── app/
        ├── __init__.py
        └── main.py
```
직접 폴더를 생성하는 방법과, 터미널 명령어를 이용해 만드는 방법이 있다.
```
mkdir -p backend/app
touch backend/requirements.txt backend/app/__init__.py backend/app/main.py
```

#### requirements.txt
```
# 설치할 파이썬 패키지(의존성 목록)를 적어두는 파일.
# 'python -m pip install -r requirement.txt' 명령어를 실행하면 목록에 있는 패키지를 설치한다.
# 추후 Dockerfile 파일에 해당 명령어를 넣어서 컨테이너 안에 설치할 예정임. """ 

# FastAPI: API 주소와 요청 처리 로직을 작성하는 프레임워크.
fastapi

# Uvicorn: FastAPI 앱을 실행하고 HTTP 요청을 받는 서버 프로그램.
# [standard]: 권장 추가 의존성도 함께 설치한다는 뜻.
uvicorn[standard]
```


#### main.py 파일 기본코드 작성
```
""" FastAPI 앱의 시작 파일. 

    1. fastapi에서 FastAPI 클래스를 import 한다.
    2. FastAPI()로 객체를 생성하고 app 변수에 넣는다.
    3. /health 요청을 처리할 함수를 정의한다.
    4. 함수 위에 @app.get("/health")를 붙여, GET /health 요청과 해당 함수를 연결한다.
    5. 함수는 파이썬 딕셔너리 {"status": "ok"}를 JSON 응답으로 반환하게 한다. """

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    """ 서버가 요청을 받고 응답할 수 있는지 확인하는 기능. 
        현재는 DB 연결, 유효성 검사 없이 오로지 응답 여부만 확인한다. """

    return {"status":"ok"}
```


#### backend/Dockfile 파일 작성
```
# Python 3.14 가 설치된 이미지를 사용
FROM python:3.14-slim

# 컨테이너 작업 위치 지정
WORKDIR /app

# 패키지 목록을 /app 에 복사
COPY requirements.txt ./

# 미리 작성해둔 requirements.txt 파일을 사용하여 컨테이너 이미지 안에 패키지 설치
RUN python -m pip install --no-cache-dir -r requirements.txt

# 맥의 backend/app 을 컨테이너의 /app/app 에 복사
COPY ./app ./app

# 서버가 사용할 포트 표시
EXPOSE 8000

# 컨테이너 시작 시 Uvicorn 으로 앱 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 최상위 폴더 위치에서 compose.yaml 파일에 backend 코드 추가
```
services:
    frontend:
        ...

    backend:
        build:
            # backend Dockerfile 로 이미지 생성
            context: ./backend
        ports:
            # 맥의 8002 를 컨테이너의 8000 에 연결
            - "127.0.0.1:8002:8000"
        volumes:
            # backend 소스를 연결해서 수정 사항 반영
            # 파이썬 패키지는 /app 바깥의 파이썬 설치 경로에 설치되므로,
            # 프론트의 node_modules 처럼 별도 볼륨을 추가할 필요할 필요는 없다.
            - ./backend:/app
```

`docker compose up --build -d backend` : 실행 후 Backend localhost의 docs 를 열어서 health ok 확인

#### vscode - 컨테이너 연결
Frontend 와 같은 방식으로 연결 후 확장프로그램 Python, Pylance 설치.
