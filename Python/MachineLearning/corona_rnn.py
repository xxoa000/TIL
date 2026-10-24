from keras.models import Sequential
from keras.layers import SimpleRNN, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import math
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv

""" 2. 데이터 받아오기
    github 에서 해당 데이터를 받아오는 코드. """
!git clone http://github.com/yhlee1627//deeplearning.git

""" 파일을 읽어오는 코드.
    read_csv: pandas 라이브러리의 함수, 파일을 읽어온다.
    usesols=[3]: 사용할 데이터의 인덱스 위치
    engine='python': 사용할 언어 """
dataframe = read_csv('/Users/didi/Desktop/MTest/11_Python/deeplearning/corona_daily.csv', usecols=[3], engine='python', skipfooter=3)

print(dataframe)

""" dataframe 은 현재 각 데이터의 설명과 데이터 순서 값이 포함된 상태
    -> 필요한 확진자 수 데이터만 가져오기 위해 .values 사용. """
dataset = dataframe.values

""" 정규화를 위해 두 번째 행의 값을 32비트 실수형으로 바꾼다.
    .astype(): 배열 원소의 자료형을 변환하는 메서드.
    float32: 32비트(하나당 4바이트) 실수형 <-> JAVA 의 float 과 비슷.
    float64: 64비트(하나당 8바이트) 실수형 <-> JAVA 의 double 과 비슷.
    정규화의 이유? -> 더 정확한 성능을 위해 소숫점 단위까지 보기 위함. """
dataset = dataset.astype('float32')



""" 2.1 test: 폴더 실제 저장경로 확인 코드 """
from pathlib import Path

print("현재 작업 폴더:", Path.cwd())
print("CSV 파일 존재 여부:", Path("deeplearning/corona_daily.csv").exists())



""" 3. 데이터 정규화 및 분류하기
    MinMaxScaler(): 사이킷런 라이브러리의 데이터 전처리 함수.
                    데이터를 0~1 사이의 숫자로 조정(스케일링)한다. """
scaler = MinMaxScaler(feature_range=(0,1))

""" 데이터를 정규화 """
Dataset = scaler.fit_transform(dataset)

""" 훈련 데이터와 검증 데이터를 split 하여 분리
    test_size=0.2: 검증 데이터 비율
    shuffle=True 는 무작위 추출.
    shuffle=False 는 순차 추출."""
train_data, test_data = train_test_split(Dataset, test_size=0.2, shuffle=False)

""" 훈련 데이터 갯수와 검증 데이터 갯수를 출력. """
print(len(train_data), len(test_data))



""" 4. 데이터 형태 변경하기 """
def create_dataset(dataset, look_back):
    x_data = []
    y_data = []

    """ 앞선 3일치로 다음날을 예측하기 때문에 10일차의 데이터가 필요하다면 인자는 7이 된다.
        look_back: 연속되는 데이터 개수. """
    for i in range(len(dataset)-look_back):
        data = dataset[i:(i+look_back), 0]
        """ x_data 에 0~2행(1~3일차)의 값이 들어갔다면,
            y_data 는 그 다음날인 3행(4일차)의 값이 들어가야 한다. """
        x_data.append(data)
        y_data.append(dataset[i+look_back, 0])

    return np.array(x_data), np.array(y_data)



""" 5. 입력 데이터 생성하기.
    모델에 입력할 수 있는 데이터를 정리하는 과정 """

look_back = 3

""" 훈련 데이터 생성. 해당 함수 호출 시 2개의 배열을 얻게 된다.
    첫 번째는 3일치의 연속된 값(x_data)
    두 번째는 인공지능이 학습할 값(y_data).
    x_data 를 x_train 데이터로, y_data 는 y_train 데이터로 넣는다. """
x_train, y_train = create_dataset(train_data, look_back)

""" 검증 데이터 생성. 이하 로직은 비슷하다. """
x_test, y_test = create_dataset(test_data, look_back)

""" 입력 데이터 / 출력 데이터
    x_train / y_train
    x_test / y_test"""
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)



""" 6. 인공지능 모델에 넣어 줄 형태로 변환하기 
    2차원 배열 -> 3차원 배열로 변환하는 과정. 
    86x3 형태의 배열을 86x1x3 의 형태로 변환한다."""

""" x_train.shape() 의 값은 (86,3) 이다. 
    이 중 첫 번째 인덱스[0]를 첫 번째 인자에, 두 번째 인덱스[1]를 세 번째 인자로 전달한다. """
X_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
X_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

print(X_train.shape)
print(X_test.shape)



""" 7. 인공지능 모델 만들기 
    시퀀셜 모델 사용."""
model = Sequential()

""" SimpleRNN(순환신경망) 사용.
    input_shape는 데이터의 형태를 결정."""
model.add(SimpleRNN(3, input_shape=(1,look_back)))

""" 최종 예측값. 즉, 확진자 수 = 하나의 값이므로 1 노드 """
model.add(Dense(1, activation="linear"))

""" 인공지능을 계산하는 방법.
    loss(손실함수)는 mse(평균 제곱 오차)로 설정.
    adam 옵티마이저 사용. """
model.compile(loss='mse', optimizer='adam')

""" 생성된 모델을 요약 """
model.summary()



""" 8. 모델 학습시키기
    X_train: 입력 데이터
    y_train: 출력 데이터
    epochs: 반복 횟수
    batch_size: 한 번에 학습시킬 데이터 양
    verbose: 학습 진행 경과를 표시하는 설정. 1로 설정시 간단히만 알려줌. """
model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=1)



""" 9. 데이터 예측하기
    실제 데이터를 예측한 값과, 실제 데이터의 값 차이를 보기 위해
    예측값, 실젯값을 다시 정규화 이전 데이터로 변환해야 함."""

""" predict(): 모델에 데이터를 넣어서 결괏값을 생성하는 함수. """
trainPredict = model.predict(X_train)
testPredict = model.predict(X_test)

""" 0~1 사이의 값으로 되어 있는 정규화된 값을 다시 자연수 형태로 변환.
    inverse_transform() 함수 사용. """
TrainPredict = scaler.inverse_transform(trainPredict)
Y_train = scaler.inverse_transform([y_train])
TestPredict = scaler.inverse_transform(testPredict)
Y_test = scaler.inverse_transform([y_test])

print(trainPredict)



""" 10. 모델 정확도 살펴보기 
    모델이 예측한 값과 실젯값에 어느 정도 차이가 있는지 확인.
    RMSE: root mean squared error, 평균 제곱근 오차
        오차를 제곱하여 정수만 얻음 -> 평균값 계산 -> 평균값의 제곱근=원래 오차의 평균이 된다. """

""" 훈련 데이터 예측 정확도 테스트 """
trainScore = math.sqrt(mean_squared_error(Y_train[0], TrainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))

""" 검증 데이터 예측 정확도 테스트 """
testScore = math.sqrt(mean_squared_error(Y_test[0], TestPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))



""" 11. 결과를 그래프로 확인하기 """

""" 훈련 데이터를 예측한 값을 저장하기 위해, 기존 데이터를 복제하여 넘파이 배열 생성.
    실제 데이터와 예측 데이터를 하나의 그림에서 비교하기 위함. """
trainPredictPlot = np.empty_like(dataset)
""" 만들어진 배열의 모든 값을 nan 으로 설정함. -> 배열을 깨끗하게 만들기 위해. """
trainPredictPlot[:,:] = np.nan
""" 훈련데이터 예측값을 배열에 넣는 코드. look_back(3) 만큼은 건너뛰고 그 다음부터 데이터를 넣는다.
    즉, 첫번째 값=4일차 확진자 수. """
trainPredictPlot[look_back:len(TrainPredict)+look_back,:] = TrainPredict

""" 검증데이터 역시 동일한 로직으로 처리.
    단, 훈련데이터의 예측값+3일치 예측값을 건너뛴 이후 순서부터 값을 넣는다. """
testPredictPlot = np.empty_like(dataset)
testPredictPlot[:,:] = np.nan
testPredictPlot[len(TrainPredict)+(look_back)*2:len(dataset),:] = TestPredict

""" 파란색 선: dataset=전체 데이터 
    주확색 선: trainPredictPlot=훈련 예측값
    초록색 선: testPredictPlot=검증 예측값"""
plt.plot(dataset)
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()
