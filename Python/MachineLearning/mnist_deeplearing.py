"""1. 개발환경 만들기 ------------------------------------------------------"""
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
import numpy as np
import matplotlib.pyplot as plt


"""2. 데이터셋 불러오기. ------------------------------------------------------
.load_data(): MNIST 데이터셋에서 데이터를 불러오는 함수.
MNIST 데이터셋은 이미 네 부분으로 나뉘어 있는데
첫 번째 부분을 x_train 으로 (훈련 데이터), 두 번째 부분을 y_train 으로 (검증 데이터), 
세 번째 부분을 x_test 로 (훈련 데이터), 네 번째 부분을 y_test (검증 데이터) 로 불러오는 명령어다. 
-> 이때 값은 모두 numpy 를 사용함."""
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print("x_train shape", x_train.shape)
print("y_train shape", y_train.shape)
print("x_test shape", x_test.shape)
print("y_test shape", y_test.shape)


"""3. MNIST 데이터셋에서 X 형태 바꾸기. ------------------------------------------------------
28x28 형태인 다차원 배열 x_train 데이터를 1x784 짜리 1차원 배열로 바꾸는 명령어.
이때 .reshape() 는 numpy 명령어.
(* 변수의 소/대문자 구분에 주의할 것.)"""
X_train = x_train.reshape(60000, 784)
X_test = x_test.reshape(10000, 784)

"""정규화: 정수를 실수로 형변환.
정규화 하는 이유는 데이터 학습이 더 잘되도록 하기 위해."""
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

"""0~255 사이의 값을 0~1 사이의 값으로 바꾸기 위해 나누기 255 하여 다시 담는다."""
X_train /= 255
X_test /= 255

print("X Training matrix shape", X_train.shape)
print("X Testing matrix shape", X_test.shape)


"""4. MNIST 데이터셋에서 Y 형태 바꾸기. ------------------------------------------------------
수치형 데이터 -> 범주형 데이터로 변환하는 과정 = 원-핫 인코딩(one-hot incoding).
레이블(정답)을 0,1,2,3,4... 처럼 숫자로 알려주는 것이 아니라 배열에서 False 인덱스는 0으로, True 인덱스는 1로 표기하는 방식.
ex) 3 = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]"""
Y_train = to_categorical(y_train, 10)
Y_test = to_categorical(y_test, 10)

print("Y Training matrix shape", Y_train.shape)
print("Y Testing matrix shape", Y_test.shape)


"""5. 인공지능 모델 설계하기 ------------------------------------------------------
시퀀셜 모델은 레이어를 나타내는 Layer 부분, 레이어의 모습을 나타내는 Output Shape 부분,
각 노드와 변향을 연결하는 가중치의 수를 나타내는 Param 부분으로 나뉘어 있다.

첫 번째 레이어는 512개의 노드, 총 401,920(=784*512+512) 
-> 784개의 입력층, 512 개의 은닉층으로 각각 연결되어 있어 784*512 만큼의 가중치와, 은닉층 각 노드 수 만큼 편향(512)이 있기 때문.
두 번째 레이어는 256개의 노드, 총 131,328(=512*256+256)
마지막 레이어는 0~9 숫자를 구분하는 10개의 노드, 총 2570(=256*10+10)개의 파라미터가 있다.
"""
model = Sequential()

model.add(Dense(512, input_shape=(784,)))
model.add(Activation('relu'))

model.add(Dense(256))
model.add(Activation('relu'))

model.add(Dense(10))
model.add(Activation('softmax'))

model.summary()


"""6. 모델 학습시키기 ------------------------------------------------------
데이터를 이용하여 심층 신경망을 딥러닝으로 학습시킨다.
핵심은 오차줄이기! 오차를 줄이는데는 경사하강법(SGD)을 이용."""
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, Y_train, batch_size=128, epochs=10, verbose=1)


"""7. 모델 정확도 살펴보기 ------------------------------------------------------
.evaluate(): 모델 정확도를 평가할 수 있는 함수
  첫 번째 인자 -> 테스트 할 데이터.
  두 번째 인자 -> 테스트 할 데이터의 정답.
  이걸로 loss(오차값) 과 accuracy(정확도)를 알 수 있다."""
score = model.evaluate(X_test, Y_test)
print('Test score:', score[0])
print('Test accuracy:', score[1])


"""8. 모델 학습 결과 확인하기 ------------------------------------------------------
.predict(): model의 결과를 예측하는 함수
.argmax(): 여러 데이터 중에서 가장 큰 값이 어디에 있는지 나타내는 함수.
  axis=0 -> 각 열(세로)에서 가장 큰 수를 고름.
  axis=1 -> 각 행(가로)에서 가장 큰 수를 고름."""
predicted_classes = np.argmax(model.predict(X_test), axis=1)

"""predicted_classes: 예측값. / y_test: 실제값.
만약 동일하다면(==) -> 1, crrect_indices
다르다면(!=) -> 0, incorrect_indices.

.nonzero(): numpy 함수. 배열에서 0이 아닌 값 -> 1 의 위치를 찾아낸다."""
correct_indices = np.nonzero(predicted_classes==y_test)[0]
incorrect_indices = np.nonzero(predicted_classes!=y_test)[0]


"""9. 잘 예측한 데이터 살펴보기 ------------------------------------------------------"""
plt.figure()
for i in range(9):
    """.subplot(): 그림의 위치를 정해주는 함수.
      첫 번째 인자 -> 그림의 가로 개수.
      두 번째 인자 -> 그림의 세로 개수.
      세 번째 인자 -> 순서."""
    plt.subplot(3,3,i+1)
    correct = correct_indices[i]

    """.imshow(): 보여줄 이미지의 내용을 내용을 담고 있다.
    앞서 2차원 배열을 1차원 배열로 변환했기 때문에, 다시 원래의 2차원 배열로 복원할 필요가 있음 -> .reshape(28,28)"""
    plt.imshow(X_test[correct].reshape(28,28), cmap='gray')

    """Predicted(예측값)과 Class(실제값)."""
    plt.title("Predicted {}, Class {}".format(predicted_classes[correct],
                                            y_test[correct]))

""".tight_layout(): 실제로 화면에 그림을 보여주기 위한 함수."""
plt.tight_layout()


"""10. 잘 예측하지 못한 데이터 살펴보기 ------------------------------------------------------"""
plt.figure()
for i in range(9):
    plt.subplot(3,3,i+1)
    incorrect = incorrect_indices[i]
    plt.imshow(X_test[incorrect].reshape(28,28), cmap='gray')
    plt.title("Predicted {}, Class {}".format(predicted_classes[incorrect],
                                            y_test[incorrect]))
plt.tight_layout()
