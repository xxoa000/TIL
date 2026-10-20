# 개발환경 만들기
Python 3.11 버전 사용  
&emsp; (3.11 은 .org 설치 프로그램을 이용해서 설치한 파이썬 버전  
&emsp; 기존의 FastAPI 프로젝트는 homebrew 를 이용해 설치한 3.13.14 버전 사용중,  
&emsp; 3.9.6 은 mac 자체에 깔려있는 파이썬)

## .venv 가상환경 만들기
**.venv 가상환경을 만들어서 파이썬 버전 별로 라이브러리를 따로 관리하는 이유는?**  
&emsp; 프로젝트별로 필요한 버전 관리를 수월하게 하게 위함.  
&emsp; 다만 그만큼 SSD 용량을 더 사용한다.

1. 터미널에서 해당 폴더 위치로 들어가기, 혹은 vscode 에서 cmd+shfit+p
2. `Python: Create Enironment` 파이썬: 가상환경 만들기 클릭
3. 사용할 파이썬 버전 클릭 -> 초기 PyPI 라이브러리 설치는 건너뛰어도 됨
4. test: 해당 폴더에 .venv 가 제대로 들어가 있는지 확인하는 명령어  
   `python3 -c "import sys; print(sys.executable)"`  
   `python3 -m pip --version`

## 필요한 라이브러리 설치
`python3 -m pip install <라이브러리 이름>`
| 설치한 라이브러리 | 용도 |
| --- | --- |
| tensorflow | 딥러닝 심층 인공 신경망을 쉽게 만들수 있다. |
| keras | 텐서플로를 쉽게 쓸 수 있다. |
| numpy | 배열, 행렬 계산을 쉽게 할 수 있다. |
| matplotlib | 맷플로립. 그래프를 쉽게 그릴 수 있다. |
| scikit-learn (sklearn) | 머신러닝 모델을 학습하고 평가할 때 사용한다. |
| pandas | 데이터를 쉽게 다를 수 있다. |

`python3 -m pip show <라이브러리 이름>`  
&emsp; 필요한 라이브러리가 이미 설치되어 있는지 확인.  
&emsp; 설치된 라이브러리의 경우 설치된 버전, 제작자, 라이선스, 설치 경로, 의존 패키지 등도 같이 보여준다.  
&emsp; (pandas 같은 경우는 엄청 길다...)  
