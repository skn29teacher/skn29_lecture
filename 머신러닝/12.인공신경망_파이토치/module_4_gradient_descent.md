# 모듈 4. 최적화의 핵심: 기울기(Gradient)와 경사하강법

**기울기 = 손실함수를 가중치로 미분한 값** 입니다.  
그리고 미분을 하는 이유는 정확히 하나입니다:

> **"가중치를 어느 방향으로, 얼마만큼 바꾸면 손실이 줄어드는가?"**

---

## 4.1 미분의 기본 개념부터 다시

네, 이해하신 방향이 정확합니다.

1. 두 점 사이 기울기(평균변화율)는
$$
\frac{f(x+h)-f(x)}{h}
$$
2. 여기서 $h$를 0에 아주 가깝게 보내면, 두 점은 사실상 한 점 근처가 됩니다.
3. 그때의 기울기가 바로 **접선 기울기**, 즉 **미분값**입니다.

$$
f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}
$$

정리하면:

- 미분 = 한 점에서의 순간 변화율
- 기울기 = 그 순간 변화율의 값
- 딥러닝에서는 그 대상을 손실함수로 바꾼 것:
$$
\text{Gradient}=\frac{\partial L}{\partial W}
$$

---

## 4.2 수식 유도 

모델을 가장 단순하게 두겠습니다.

- 모델: $\hat{y}=Wx$ (bias 생략)
- 손실(한 샘플): $L=(y-\hat{y})^2=(y-Wx)^2$

이제 $W$로 미분하면:

$$
\frac{dL}{dW}
= 2(y-Wx)\cdot\frac{d(y-Wx)}{dW}
= 2(y-Wx)\cdot(-x)
= -2x(y-Wx)
$$

이 값이 바로 **기울기**입니다.

---

## 4.3 왜 이 식이 "변화량"이 되나?

경사하강법 업데이트:

$$
W_{\text{new}} = W_{\text{old}} - \eta \frac{dL}{dW}
$$

여기서

- $\eta$ : 학습률(보폭)
- $\frac{dL}{dW}$ : 현재 위치에서 손실이 가장 빨리 증가하는 방향
- 그래서 앞에 `-`를 붙여 반대 방향으로 이동

즉, 실제 가중치 변화량은

$$
\Delta W = -\eta\frac{dL}{dW}
$$

이고, 이게 질문하신 "**가중치가 얼마만큼 변해야 손실이 줄어드는가**"에 대한 직접 답입니다.

---

## 4.4 샘플 데이터로 숫자 증명

샘플 하나를 두고 직접 계산해보겠습니다.

- 데이터: $(x,y)=(2,4)$
- 초기 가중치: $W=1$
- 학습률: $\eta=0.1$

### Step 0

1. 예측값: $\hat{y}=Wx=1\times2=2$
2. 손실: $L=(4-2)^2=4$
3. 기울기:
$$
\frac{dL}{dW}=-2x(y-Wx)=-2\cdot2\cdot(4-2)=-8
$$
4. 업데이트:
$$
W_{\text{new}}=1-0.1\times(-8)=1.8
$$

### Step 1 (한 번 더)

1. 예측값: $\hat{y}=1.8\times2=3.6$
2. 손실: $L=(4-3.6)^2=0.16$

기울기도 한 번 더 계산하면:
$$
\frac{dL}{dW}=-2\cdot2\cdot(4-3.6)=-1.6
$$

업데이트:
$$
W_{\text{new}}=1.8-0.1\times(-1.6)=1.96
$$

### Step 2 (한 번 더 진행)

1. 예측값: $\hat{y}=1.96\times2=3.92$
2. 손실: $L=(4-3.92)^2=0.0064$

손실이 **4 → 0.16 → 0.0064**로 계속 감소했습니다.  
즉, 미분으로 얻은 기울기를 사용하면 실제로 손실이 줄어듭니다.

---

## 4.5 부호 해석만 기억하면 쉬움

기울기 부호는 방향만 알려줍니다.

| 기울기 | 의미 | 업데이트 결과 |
|:---:|:---:|:---:|
| $+$ | $W$를 늘리면 손실 증가 | $W$를 줄임 |
| $-$ | $W$를 늘리면 손실 감소 | $W$를 늘림 |
| 0 | 평평함 | 거의 멈춤 |

---

## 4.6 과일값 계산으로 보는 체인룰(연쇄법칙)

`밑바닥부터 시작하는 딥러닝` 스타일로 아주 직관적으로 보면:

- 사과 가격: 100원
- 사과 개수: 2개
- 소비세: 1.1
- 최종 금액: 
$$
z=(100\times2)\times1.1
$$

### 1) 순전파(앞으로 계산)

1. $a=100\times2=200$
2. $z=a\times1.1=220$

### 2) "최종금액이 1원 변할 때, 사과 가격은 얼마나 변하나?"

우리가 원하는 것은 $\frac{\partial z}{\partial 100}$ 입니다.

여기서 체인룰:

$$
\frac{\partial z}{\partial 100}
=
\frac{\partial z}{\partial a}
\cdot
\frac{\partial a}{\partial 100}
$$

각 항은 매우 쉽습니다.

- $\frac{\partial z}{\partial a}=1.1$  (세금 곱하기)
- $\frac{\partial a}{\partial 100}=2$  (개수 2개 곱하기)

따라서

$$
\frac{\partial z}{\partial 100}=1.1\times2=2.2
$$

의미: **사과 1개 가격이 1원 오르면 최종금액은 2.2원 오른다**는 뜻입니다.

### 3) 경사하강법과 연결

신경망도 구조가 똑같습니다.

- 출력(손실)까지 가는 길이 여러 연산으로 이어져 있고
- 각 구간의 "로컬 변화율(미분)"을 곱해서
- 최종적으로 $\frac{\partial L}{\partial W}$를 구합니다.

즉, 체인룰은  
**"출력 오차가 앞단 가중치까지 어떻게 전파되는지 계산하는 규칙"** 이고,  
이 값으로 $W \leftarrow W-\eta\frac{\partial L}{\partial W}$ 업데이트를 수행합니다.

---

## 4.7 신경망(은닉층 1개, 출력층 1개)에서 체인룰이 실제로 어떻게 작동하나

이제 딥러닝 형태로 확장해보겠습니다.

- 입력: $x$
- 은닉층: $z_1=w_1x+b_1,\; h=\sigma(z_1)$
- 출력층: $z_2=w_2h+b_2,\; \hat{y}=\sigma(z_2)$
- 손실: $L=\frac{1}{2}(\hat{y}-y)^2$

핵심은 출력층에서 시작한 오차가 체인룰로 은닉층까지 전파된다는 점입니다.

### 출력층 가중치 미분 (완전히 쪼개서)

출력층 경로:
$$
w_2 \rightarrow z_2 \rightarrow \hat{y} \rightarrow L
$$

#### Step O-1) 식 다시 쓰기

- $z_2 = w_2h+b_2$
- $\hat{y}=\sigma(z_2)$
- $L=\frac{1}{2}(\hat{y}-y)^2$

#### Step O-2) 로컬 미분 1: $\frac{\partial L}{\partial \hat{y}}$

$$
L=\frac{1}{2}(\hat{y}-y)^2
$$

- 왜 이렇게 되나: 제곱함수 미분 규칙 $d(u^2)/du=2u$ 사용
- $u=(\hat{y}-y)$ 이므로
$$
\frac{\partial L}{\partial \hat{y}}
=
\frac{1}{2}\cdot 2(\hat{y}-y)\cdot \frac{\partial(\hat{y}-y)}{\partial \hat{y}}
=
(\hat{y}-y)\cdot 1
=
\hat{y}-y
$$

#### Step O-3) 로컬 미분 2: $\frac{\partial \hat{y}}{\partial z_2}$

$$
\hat{y}=\sigma(z_2)=\frac{1}{1+e^{-z_2}}
$$

- 왜 이렇게 되나: 시그모이드의 기본 미분 공식
$$
\frac{d\sigma(z)}{dz}=\sigma(z)(1-\sigma(z))
$$
그래서
$$
\frac{\partial \hat{y}}{\partial z_2}
=
\hat{y}(1-\hat{y})
$$

#### Step O-4) 로컬 미분 3: $\frac{\partial z_2}{\partial w_2}$

$$
z_2=w_2h+b_2
$$

- 왜 이렇게 되나: $h,b_2$를 상수로 보고 $w_2$로 미분
- 선형식 $aw+b$를 $w$로 미분하면 계수 $a$
$$
\frac{\partial z_2}{\partial w_2}=h
$$

#### Step O-5) 결합 1: 출력 오차 신호 만들기

먼저 앞의 두 항을 묶어서
$$
\delta_2 \equiv \frac{\partial L}{\partial z_2}
=
\frac{\partial L}{\partial \hat{y}}
\frac{\partial \hat{y}}{\partial z_2}
=
(\hat{y}-y)\hat{y}(1-\hat{y})
$$

#### Step O-6) 결합 2: 최종 $w_2$ 기울기

$$
\frac{\partial L}{\partial w_2}
=
\frac{\partial L}{\partial z_2}
\frac{\partial z_2}{\partial w_2}
=
\delta_2 \cdot h
=
(\hat{y}-y)\hat{y}(1-\hat{y})h
$$

즉, 출력층은 **(손실→출력) 오차 신호를 먼저 만든 뒤, 마지막에 입력 $h$를 곱해 가중치 기울기**를 만듭니다.

### 은닉층 가중치 미분 (완전히 쪼개서)

은닉층 경로:
$$
w_1 \rightarrow z_1 \rightarrow h \rightarrow z_2 \rightarrow \hat{y} \rightarrow L
$$

#### Step H-1) 은닉층 관련 식

- $z_1=w_1x+b_1$
- $h=\sigma(z_1)$
- $z_2=w_2h+b_2$

#### Step H-2) 로컬 미분 A: $\frac{\partial z_2}{\partial h}$

$$
z_2=w_2h+b_2
$$

- 왜 이렇게 되나: $w_2,b_2$를 상수로 보고 $h$로 미분
$$
\frac{\partial z_2}{\partial h}=w_2
$$

#### Step H-3) 로컬 미분 B: $\frac{\partial h}{\partial z_1}$

$$
h=\sigma(z_1)
$$

- 왜 이렇게 되나: 시그모이드 미분 공식 그대로
$$
\frac{\partial h}{\partial z_1}=h(1-h)
$$

#### Step H-4) 로컬 미분 C: $\frac{\partial z_1}{\partial w_1}$

$$
z_1=w_1x+b_1
$$

- 왜 이렇게 되나: $x,b_1$를 상수로 보고 $w_1$로 미분
$$
\frac{\partial z_1}{\partial w_1}=x
$$

#### Step H-5) 결합 1: 출력층 오차를 은닉출력 $h$로 전달

이미 만든 $\delta_2=\frac{\partial L}{\partial z_2}$를 사용하면
$$
\frac{\partial L}{\partial h}
=
\frac{\partial L}{\partial z_2}
\frac{\partial z_2}{\partial h}
=
\delta_2 w_2
$$

#### Step H-6) 결합 2: 은닉 pre-activation($z_1$)까지 전달

$$
\delta_1 \equiv \frac{\partial L}{\partial z_1}
=
\frac{\partial L}{\partial h}
\frac{\partial h}{\partial z_1}
=
\delta_2 w_2 h(1-h)
$$

#### Step H-7) 결합 3: 최종 $w_1$ 기울기

$$
\frac{\partial L}{\partial w_1}
=
\frac{\partial L}{\partial z_1}
\frac{\partial z_1}{\partial w_1}
=
\delta_1 x
=
(\hat{y}-y)\hat{y}(1-\hat{y})w_2h(1-h)x
$$

정리하면 은닉층은 **출력층 오차를 뒤에서 앞으로 전달하면서, 각 단계 로컬 미분을 순서대로 곱해 최종 기울기**를 만듭니다.

가중치 업데이트는 둘 다 동일합니다:
$$
w \leftarrow w-\eta\frac{\partial L}{\partial w}
$$

---

## 4.8 코드 연계 (`module_4_gradient_descent.ipynb`)

노트북에서 위 내용을 그대로 확인합니다.

1. $f(x)=x^2$에서 수작업 경사하강법으로 최소점 이동 확인
2. 같은 업데이트가 `torch.optim.SGD`에서 동일하게 실행됨을 비교
3. 학습률(0.01, 0.1, 0.9) 바꿨을 때 수렴/진동 패턴 비교
4. $(x,y)=(2,4)$ 같은 단순 샘플에서 기울기 계산과 손실 감소를 숫자로 검증
5. 은닉층 1개 + 출력층 1개 네트워크에서 체인룰 수식 미분과 `autograd` 미분이 일치함을 증명
