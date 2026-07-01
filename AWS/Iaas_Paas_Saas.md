## 0. 핵심 질문

> "내 서버를 직접 만들 때, 운영체제까지 내가 관리해야 할까? 아니면 누군가 다 해주는 게 좋을까?"

이 질문에 대한 답이 곧 IaaS / PaaS / SaaS의 차이를 결정합니다.

---

## 1. IaaS / PaaS / SaaS 차이점

### 1.1 한눈에 보는 비교표

| 구분 | 내가 관리하는 영역 | 제공자가 관리하는 영역 | 대표 예시 |
|------|---------------------|--------------------------|-----------|
| **On-Premise** | 전부 (서버, 네트워크, OS, 미들웨어, 앱) | 없음 | 회사 자체 서버실 |
| **IaaS** (Infrastructure as a Service) | OS, 미들웨어, 런타임, 앱, 데이터 | 서버, 가상화, 스토리지, 네트워크 | **AWS EC2**, GCP Compute Engine |
| **PaaS** (Platform as a Service) | 앱 코드, 데이터 | OS, 미들웨어, 런타임, 서버 인프라 | AWS Elastic Beanstalk, Heroku |
| **SaaS** (Software as a Service) | 사용(설정값 정도만) | 전부 | Gmail, Slack, Notion |

### 1.2 비유로 이해하기 (피자 모델)

- **On-Premise** = 집에서 밀가루 반죽부터 시작해 피자를 직접 만든다 (모든 재료/오븐/공간을 내가 준비)
- **IaaS** = 부엌(오븐, 공간)만 빌려서 내가 요리한다 → **AWS EC2가 여기**
- **PaaS** = 반제품 도우와 토핑을 받아서 굽기만 한다 → **Elastic Beanstalk, Django용 PaaS**
- **SaaS** = 그냥 피자를 배달시켜 먹는다 → Gmail처럼 그냥 사용