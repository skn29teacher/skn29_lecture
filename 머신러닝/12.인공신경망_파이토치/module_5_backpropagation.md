# 모듈 5. 코어 마스터리: 연쇄 법칙과 오차역전파 (Backpropagation)

> [!IMPORTANT]
> **이 챕터는 인공신경망 전체 커리큘럼에서 가장 중요한 핵심 챕터입니다.**
> 이 원리를 한 번에 이해하면 그동안 블랙박스처럼 보이던 신경망 학습의 전체 퍼즐이 완성되고, 이후 CNN, RNN, Transformer 등 어떤 구조를 만나도 "아, 결국 같은 원리구나"라고 자신 있게 분석할 수 있게 됩니다.

## 5.1. 문제의 시작: 깊은 곳의 가중치는 어떻게 업데이트하나?

모듈 4에서 경사하강법을 배웠습니다. 핵심 공식은 다음이었습니다:

$$
W_{new} = W_{old} - \eta \cdot \frac{\partial L}{\partial W}
$$

출력층 바로 앞에 있는 가중치($W_2$)의 기울기 $\frac{\partial L}{\partial W_2}$는 비교적 쉽게 구할 수 있습니다. **하지만 은닉층 깊숙한 곳에 있는 $W_1$의 기울기는 어떻게 구할까요?**

손실($L$)은 $W_1$을 직접적으로 사용하지 않습니다. $W_1$이 은닉층 출력($h$)을 거치고, 그것이 다시 출력($\hat{y}$)을 거쳐서, 그 후에야 비로소 $L$에 영향을 미칩니다. 즉, 경로가 깁니다:

$$
W_1 \rightarrow z^{(1)} \rightarrow h \rightarrow z^{(2)} \rightarrow \hat{y} \rightarrow L
$$

이 긴 연결 경로를 따라 기울기를 역방향으로 전파하는 것이 바로 **오차역전파(Backpropagation)**이며, 이 때 사용하는 수학 도구가 **연쇄 법칙(Chain Rule)**입니다.

## 5.2. 용어 정리 (수학을 두려워하지 마세요!)

본격적인 유도 전에, 앞으로 계속 나올 핵심 용어/기호를 먼저 정리합니다. 낯선 기호가 나올 때마다 이 표로 돌아와 확인하세요.

| 기호 | 읽는 법 | 의미 |
|:---:|:---:|:---|
| $f'(x)$ 또는 $\frac{df}{dx}$ | "f 프라임 x" 또는 "df dx" | $x$가 아주 조금 변할 때 $f$가 얼마나 변하는지 (기울기) |
| $\frac{\partial L}{\partial W}$ | "편 L 편 W" | 여러 변수 중 $W$만 조금 바꿨을 때 $L$이 얼마나 변하는지 (편미분) |
| Chain Rule | 연쇄 법칙 | 합성함수를 미분하는 기법. 중간 다리를 끊어서 곱하기로 연결 |
| Gradient | 기울기(그래디언트) | 미분의 결과값. 방향과 크기 정보를 가짐 |
| Backpropagation | 오차역전파 | 출력의 오차를 거슬러 올라가며 각 가중치의 기울기를 계산하는 알고리즘 |

## 5.3. 연쇄 법칙(Chain Rule) 완전 정복

### 5.3.1. 합성 함수란?
함수 안에 함수가 들어있는 것입니다. 일상적 예시로 이해합시다.

> **"오늘 기온이 올라가면($x$) → 아이스크림 판매량이 늘어나고($u(x)$) → 편의점 매출이 올라간다($y(u)$)"**

기온($x$) → 아이스크림($u$) → 매출($y$), 이렇게 연결되어 있을 때 "기온이 매출에 미치는 영향"을 알고 싶다면?

### 5.3.2. 연쇄 법칙의 핵심 공식
각 구간의 영향을 따로 구해서 **곱하면** 됩니다!

$$
\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}
$$

> [!TIP]
> **직관적 이해:** 
> - 기온이 1도 오르면 아이스크림이 50개 더 팔린다 → $\frac{du}{dx} = 50$
> - 아이스크림 1개가 더 팔리면 매출이 1000원 는다 → $\frac{dy}{du} = 1000$
> - 그러면 기온이 1도 오르면 매출은? → $50 \times 1000 = 50,000$원 증가! 
> 
> **"중간 고리를 끊어서 각각 미분하고, 다시 곱하면 최종 답이 된다"** — 이것이 연쇄 법칙의 전부입니다.

### 5.3.3. 구체적 수식 예제
$y = (3x + 2)^2$ 를 미분해 봅시다.

**단계 1: 바깥 함수와 안쪽 함수 분리**
- 안쪽 함수(중간 다리): $u = 3x + 2$
- 바깥 함수: $y = u^2$

**단계 2: 각각 따로 미분**
- $\frac{dy}{du} = 2u$ (바깥 미분)
- $\frac{du}{dx} = 3$ (안쪽 미분)

**단계 3: 곱하기 (연쇄 법칙 적용)**

$$
\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx} = 2u \cdot 3 = 2(3x+2) \cdot 3 = 6(3x+2)
$$

끝입니다! 이것이 연쇄 법칙의 전체 메커니즘입니다.

## 5.4. 신경망에 연쇄 법칙 적용: 오차역전파 완전 유도

이제 이 연쇄 법칙을 우리가 모듈 2에서 만든 2층 신경망에 적용합니다. 수식이 길어 보이지만, 모든 단계가 위의 "끊고-미분하고-곱하기" 패턴의 반복일 뿐입니다.

### 5.4.1. 네트워크 구조 복기 (단일 뉴런으로 단순화)
이해를 돕기 위해 가장 단순한 1-1-1 구조(입력 1개, 은닉 1개, 출력 1개)로 시작합니다.

```
x  ──w₁──→  [z₁ = w₁x + b₁]  ──σ──→  h  ──w₂──→  [z₂ = w₂h + b₂]  ──σ──→  ŷ  ──→  L
```

**순전파 수식 정리:**

| 단계 | 수식 | 설명 |
|:---:|:---:|:---|
| ① | $z_1 = w_1 \cdot x + b_1$ | 은닉층 선형결합 |
| ② | $h = \sigma(z_1)$ | 은닉층 활성화 |
| ③ | $z_2 = w_2 \cdot h + b_2$ | 출력층 선형결합 |
| ④ | $\hat{y} = \sigma(z_2)$ | 출력층 활성화 |
| ⑤ | $L = (\hat{y} - y)^2$ | 손실 계산 (MSE 간소화) |

### 5.4.2. 역전파 Step 1: 출력층 가중치 $w_2$의 기울기 (완전히 쪼개기)

**목표:** $\frac{\partial L}{\partial w_2}$

**경로:** $w_2 \rightarrow z_2 \rightarrow \hat{y} \rightarrow L$

#### O-1) 식 정리

- $z_2 = w_2 h + b_2$
- $\hat{y} = \sigma(z_2)$
- $L = (\hat{y}-y)^2$

#### O-2) 로컬 미분 A: $\frac{\partial L}{\partial \hat{y}}$

$$
L=(\hat{y}-y)^2
$$

- 제곱 미분 규칙 $\frac{d(u^2)}{du}=2u$
- $u=(\hat{y}-y)$
$$
\frac{\partial L}{\partial \hat{y}}
=2(\hat{y}-y)\cdot \frac{\partial(\hat{y}-y)}{\partial\hat{y}}
=2(\hat{y}-y)\cdot 1
=2(\hat{y}-y)
$$

#### O-3) 로컬 미분 B: $\frac{\partial \hat{y}}{\partial z_2}$

$$
\hat{y}=\sigma(z_2)
$$

- 시그모이드 미분 공식 사용
$$
\frac{d\sigma(z)}{dz}=\sigma(z)(1-\sigma(z))
$$
따라서
$$
\frac{\partial \hat{y}}{\partial z_2}
=\sigma(z_2)(1-\sigma(z_2))
$$

#### O-4) 로컬 미분 C: $\frac{\partial z_2}{\partial w_2}$

$$
z_2=w_2h+b_2
$$

- $h,b_2$를 상수로 보고 $w_2$로 미분
- 선형식 $aw+b$를 $w$로 미분하면 계수 $a$
$$
\frac{\partial z_2}{\partial w_2}=h
$$

#### O-5) 결합 1: 출력 오차 신호 $\delta_2$

$$
\delta_2 \equiv \frac{\partial L}{\partial z_2}
=\frac{\partial L}{\partial \hat{y}}\frac{\partial \hat{y}}{\partial z_2}
=2(\hat{y}-y)\sigma(z_2)(1-\sigma(z_2))
$$

#### O-6) 결합 2: 최종 $\frac{\partial L}{\partial w_2}$

$$
\frac{\partial L}{\partial w_2}
=\frac{\partial L}{\partial z_2}\frac{\partial z_2}{\partial w_2}
=\delta_2\cdot h
=2(\hat{y}-y)\sigma(z_2)(1-\sigma(z_2))h
$$

### 5.4.3. 역전파 Step 2: 은닉층 가중치 $w_1$의 기울기 (완전히 쪼개기)

**목표:** $\frac{\partial L}{\partial w_1}$

**경로:** $w_1 \rightarrow z_1 \rightarrow h \rightarrow z_2 \rightarrow \hat{y} \rightarrow L$

#### H-1) 식 정리

- $z_1 = w_1x+b_1$
- $h=\sigma(z_1)$
- $z_2 = w_2h+b_2$

#### H-2) 로컬 미분 A: $\frac{\partial z_2}{\partial h}$

$$
z_2=w_2h+b_2
$$

- $w_2,b_2$를 상수로 보고 $h$로 미분
$$
\frac{\partial z_2}{\partial h}=w_2
$$

#### H-3) 로컬 미분 B: $\frac{\partial h}{\partial z_1}$

$$
h=\sigma(z_1)
$$

- 시그모이드 미분 공식 그대로
$$
\frac{\partial h}{\partial z_1}=\sigma(z_1)(1-\sigma(z_1))
$$

#### H-4) 로컬 미분 C: $\frac{\partial z_1}{\partial w_1}$

$$
z_1=w_1x+b_1
$$

- $x,b_1$를 상수로 보고 $w_1$로 미분
$$
\frac{\partial z_1}{\partial w_1}=x
$$

#### H-5) 결합 1: 출력 오차를 은닉 출력으로 전달

Step 1에서 구한 $\delta_2=\frac{\partial L}{\partial z_2}$를 재사용:
$$
\frac{\partial L}{\partial h}
=\frac{\partial L}{\partial z_2}\frac{\partial z_2}{\partial h}
=\delta_2w_2
$$

#### H-6) 결합 2: 은닉 pre-activation까지 전달

$$
\delta_1 \equiv \frac{\partial L}{\partial z_1}
=\frac{\partial L}{\partial h}\frac{\partial h}{\partial z_1}
=\delta_2w_2\sigma(z_1)(1-\sigma(z_1))
$$

#### H-7) 결합 3: 최종 $\frac{\partial L}{\partial w_1}$

$$
\frac{\partial L}{\partial w_1}
=\frac{\partial L}{\partial z_1}\frac{\partial z_1}{\partial w_1}
=\delta_1x
$$

모든 항을 펼치면:
$$
\frac{\partial L}{\partial w_1}
=2(\hat{y}-y)\sigma(z_2)(1-\sigma(z_2))w_2\sigma(z_1)(1-\sigma(z_1))x
$$

> [!IMPORTANT]
> **핵심 관찰 1:** $\delta_2$를 재활용하므로 계산이 중복되지 않습니다. 이것이 역전파의 계산 효율입니다.

> [!IMPORTANT]
> **핵심 관찰 2:** $\sigma(z)(1-\sigma(z)) \le 0.25$가 층마다 곱해지면 기울기가 작아집니다(기울기 소실).

### 5.4.4. 전체 역전파 흐름 한눈에 정리

```
순전파(Forward): x → z₁ → h → z₂ → ŷ → L
                 ─────────────────────────→

역전파(Backward): ∂L/∂w₁ ← ∂h/∂z₁ ← ∂z₂/∂h ← ∂ŷ/∂z₂ ← ∂L/∂ŷ
                 ←─────────────────────────────────────────────
                 (출력에서 계산한 기울기를 입력 방향으로 역순 전달)
```

**역전파의 본질을 한 문장으로:**
> "출력의 오차($L$)를 출발점으로 잡고, 연쇄 법칙으로 기울기를 한 층씩 역방향으로 곱해가며 전달하여, 모든 가중치가 오차를 줄이는 방향으로 업데이트될 기울기 값을 구하는 것"

## 5.5. 시그모이드 미분 공식은 어떻게 나온 건가요? (보너스)

시그모이드의 미분이 놀랍도록 깔끔하게 자기 자신으로 표현됩니다:

$$
\sigma(x) = \frac{1}{1+e^{-x}}
$$

$$
\sigma'(x) = \sigma(x) \cdot (1 - \sigma(x))
$$

**유도 과정 (관심 있는 분만):**

$$
\sigma'(x) = \frac{d}{dx}\left[\frac{1}{1+e^{-x}}\right] = \frac{e^{-x}}{(1+e^{-x})^2} = \frac{1}{1+e^{-x}} \cdot \frac{e^{-x}}{1+e^{-x}} = \sigma(x) \cdot (1 - \sigma(x))
$$

시그모이드 출력이 0.5일 때 미분 값이 최대 $0.25$, 양 끝(0이나 1에 가까울 때)에서는 거의 $0$이 됩니다. 이것이 기울기 소실의 수학적 유래입니다.

## 5.6. 코드 연계 증명 (블랙박스 타파)
세트로 제공되는 `module_5_backpropagation.ipynb`에서 다음을 실행합니다.
1. **수동 Backward:** 위에서 유도한 수식을 파이토치 텐서 연산으로 직접 코딩하여 $\frac{\partial L}{\partial w_1}$, $\frac{\partial L}{\partial w_2}$ 등의 기울기를 수작업으로 계산합니다.
2. **자동 Backward:** 파이토치의 `.backward()`를 호출하여 자동 미분을 실행합니다.
3. **완전 일치 증명:** `torch.allclose(수동_grad, 자동_grad)`로 오차가 없음을 입증하여, 수식으로 유도한 가설이 실제 파이토치 엔진 내부의 동작과 100% 일치함을 보여줍니다.
