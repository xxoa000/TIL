""" 1. 숫자 생성 인공지능 만들기

    생성 신경망을 사용하여 숫자 생성 인공지능을 만든다.
    그리고 생성 신경망 중 GAN(적대 신경망) 이라는 기법을 사용한다.
    
    GAN(Generative Adversarial Network) : 판별자 신경망 / 생성자 신경망 2개의 신경망으로 구성되어 있다.
        생성자는 진짜처럼 그럴듯한 가짜 그림을 생성하며,
        판별자는 진짜 그림과 가짜 그림을 구별한다.
        2개의 신경망을 사용하여 새로운 그림을 생성해 내는 기법이 바로 '생성적 적대 신경망'이다.
"""



""" 2. 개발환경 만들기 """

from keras.models import Model, Sequential

""" LeakyReLU 함수와 ReLU 함수의 차이:
        ReLU 함수는 0 보다 작은 값이 들어오면 무조건 0을 반환.
        LeakyReLU 함수는 0 보다 작은 값이 들어오면 음수값을 반환한다."""
from keras.layers import Dense, Input, LeakyReLU
from keras.optimizers import Adam
from keras.datasets import mnist

""" tqdm: 모델 학습을 시각적으로 보여 주는 라이브러리.
        진행을 나타내는 아랍어(taqadum)에서 따온 이름이다."""
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt



""" 3. 데이터 불러오기 """

""" 훈련 데이터 - 픽셀 값으로 구성된 이미지 데이터와, 이미지 데이터가 나타내는 숫자가 무엇인지 알려주는 데이터.
    검증 데이터 - 이미지 데이터와, 이미지 데이터가 나타내는 숫자가 무엇인지 알려 주는 데이터. """
(x_train, y_train),(x_test, y_test) = mnist.load_data()

""" 데이터 정규화. 
    데이터를 실수값으로 변환 -> -1~1 사이의 값으로 변경. """
x_test = (x_test.astype(np.float32)-127.5) / 127.5

""" 28x28 형태인 데이터를 1열(784x1)로 나타내기 위해 데이터 형태 변환."""
mnist_data = x_test.reshape(10000, 784)

print(mnist_data.shape)
len(mnist_data)



"""4. 생성자 신경망 만들기"""

def create_generator():
    generator = Sequential()

    """ 첫 번째 층.
        units=256: 256개의 노드
        input_dim=100: 모델에 입력하는 값 100, 100개의 픽셀을 넣을 것이라는 의미. """
    generator.add(Dense(units=256, input_dim=100))
    generator.add(LeakyReLU(0.2))                       # 음수값은 특정한 기울기를 보인다. 0.2는 기울기 설정

    """ 두 번째 층. """
    generator.add(Dense(units=512))                     # 첫 번째 층의 노드 갯수 = 512
    generator.add(LeakyReLU(0.2))

    """ 마지막 층(출력층). """
    generator.add(Dense(units=784, activation='tanh'))  # 출력층의 노드 수는 784, 활성화 함수는 tanh. 
    return generator

g = create_generator()
g.summary()



"""5. 판별자 신경망 만들기"""

def create_discriminator():
    discriminator = Sequential()

    """ 첫 번째 층. """
    discriminator.add(Dense(units=512, input_dim=784))
    discriminator.add(LeakyReLU(0.2))

    """ 두 번째 층. """
    discriminator.add(Dense(units=256))
    discriminator.add(LeakyReLU(0.2))

    """ 마지막 층(출력층). 
        판별자의 역할은 데이터의 진위 여부 판단. """
    discriminator.add(Dense(units=1, activation='sigmoid'))
    discriminator.compile(loss='binary_crossentropy',
                        optimizer=Adam(learning_rate=0.0002, beta_1=0.5))
    return discriminator

d = create_discriminator()
d.summary()



"""6. GAN 생성 함수 만들기"""

def create_gan(discriminator, generator):
    discriminator.trainable = False         # 판별자가 학습하지 못하도록 막는 코드
    gan_input = Input(shape=(100,))         # 100의 값 데이터, 두번째 인자가 빈 이유는 총 데이터 개수를 넣기 위함.
    x = generator(gan_input)
    gan_output = discriminator(x)           # GAN의 결괏괎 데이터를 정의해주는 코드.

    """ 생성적 적대 신경망 GAN 모델 만들기.
        inputs=gan_input: 입력값, 생성자 신경망이 만든 그림.
        outputs=gan_output: 출력값, 판별자 신경망이 판단한 결과. """
    gan = Model(inputs=gan_input, outputs=gan_output)

    """ 신경망의 오차값을 줄이는 방법.
        출력값의 모습 자체가 맞는지 틀린지 둘 중 하나로 나오기 때문에
        이진 분류에 사용하는 binary_crossentropy 사용. """
    gan.compile(loss='binary_crossentropy', optimizer='adam')
    return gan

gan = create_gan(d, g)          # d: 판별자 신경망, g: 생성자 신경망
gan.summary()



"""7. 결과 확인 함수 만들기"""

def plot_generated_images(generator):

    """ 생성자에 넣어 줄 노이즈값 생성.
        균일한 값을 생성할 수 있도록 넘파이의 랜덤값 생성 라이브러리 중 정규 분포 함수를 사용.
        loc=0: 평균이 0.
        scale=1: 평균에서 1만큼씩 떨어져 있는 값(-1~1 사이의 값)
        size=[100, 100]: 노이즈 100개 생성. 이 함수를 호출할 때마다 100개의 그림을 그려달라는 의미. """
    noise = np.random.normal(loc=0, scale=1, size=[100, 100])

    """ 앞에서 만든 노이즈값(noise)을 신경망에 넣어서 값을 예측하라(predict(noise))는 명령어. """
    generated_images = generator.predict(noise)
    generated_images = generated_images.reshape(100, 28, 28)        # 1줄 배열인 784 형태를 -> 그림의 형태로 변환.
    plt.figure(figsize=(10,10))                                     # 그 후 그림 크기를 10x10 로 정함.

    """ 100개의 그림을 그리기 위한 반복문. """
    for i in range(generated_images.shape[0]):
        plt.subplot(10, 10, i+1)                                    # 그림의 위치를 정해 주는 코드.
        plt.imshow(generated_images[i], interpolation='nearest')    # 이미지를 출력.
        plt.axis('off')                                             # 그림 이름을 넣지 않는다는 의미.
    
    plt.tight_layout()                                              # 그림을 화면에 보여주는 명령어.



"""8. 생성적 적대 신경망 훈련시기키"""

batch_size = 128            # 한 번에 몇 개의 그림을 학습시킬지.
epochs = 100                # 신경망을 몇 번 반복 학습 시킬지 결정.

for e in tqdm(range(epochs)):

    """ 생성자에 줄 노이즈값. 균일한 값을 생성할 수 있도록 정규 분포 함수를 사용.
        첫 번째 인자 0: 평균이 0이라는 의미.
        두 번째 인자 1: 평균에서 1만큼씩 떨어져 있는 값(-1 ~ 1 사이 값)을 생성하라는 의미.
        세 번째 인자 [batch_size, 100]: batch_size 개수만큼 생성, 생성 데이터는 각각 숫자 100개씩 구성되어 있단 의미. """
    noise = np.random.normal(0,1, [batch_size, 100])
    generated_images = g.predict(noise)     # 생성자 모델에 노이즈를 입력, 생성자 신경망이 그림을 그린 후 결과를 저장.
    
    """ 실제 MNIST 데이터셋(1만개)에서 128개만 랜덤으로 뽑는 코드.
        학습할 때마다 다양한 모양의 손글씨를 인공지능이 학습하도록 하기 위함."""
    image_batch = mnist_data[
        np.random.randint(                  # 1만 개의 데이터 중에서 배치 사이즈 만큼 랜덤으로 추출한다는 의미.
            low=0,                      
            high=mnist_data.shape[0],
            size=batch_size
        )
    ]
    X = np.concatenate([image_batch, generated_images]) # 진짜 그림과 생성한 그림을 합침.
    
    y_dis = np.zeros(2*batch_size)                      # 판별자에 전달할 결괏괎(256). zeros를 사용하여 값을 0으로 만듬.
    y_dis[:batch_size] = 1                              # 앞의 128개는 실젯값(진짜 그림)이므로 1을 넣어줌.
    d.trainable = True                                  # trainable: 신경망이 훈련 가능하도록 할지 아닌지 결정하는 함수.
    d.train_on_batch(X, y_dis)                          # 판별자 학습. X: 입력 데이터, y_dis: 출력 데이터
    
    noise = np.random.normal(0,1, [batch_size, 100])    # 새 노이즈 값.
    y_gan = np.ones(batch_size)                         # gan 에 넣을 값은 모두 1로 설정 > 판별자가 진짜 그림인 줄 알도록.
    d.trainable = False                                 # 판별자가 더 이상 학습할 수 없도록 함. 이제부턴 판별만.
    gan.train_on_batch(noise, y_gan)                    # 노이즈 값을 입력으로 넣고, 출력값을 모두 진짜(1) 처럼 넣어 학습.

    if e == 1 or e % 1000 == 0:
        plot_generated_images(g)                        # 생성자가 만든 그림을 보여줌, 인자 g는 생성자 신경망.
