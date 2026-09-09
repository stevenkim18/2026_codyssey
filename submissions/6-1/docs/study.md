# AWS로 웹사이트를 인터넷에 배포하기

## 0. 우리가 하려는 것

이번 미션의 최종 목표는 아주 간단하다.

> **내가 만든 웹사이트를 AWS 서버에 올리고, 인터넷을 통해 누구나 접속할 수 있게 만든다.**

예를 들어 내 컴퓨터에서 웹사이트를 만들었다고 생각해보자.

```text
내 컴퓨터
└── 웹사이트
```

지금은 내 컴퓨터에서만 실행되기 때문에 다른 사람은 접속할 수 없다.

우리가 원하는 것은 다음과 같은 상태다.

```text
나 또는 다른 사용자
       │
       │ http://서버주소
       ▼
    Internet
       │
       ▼
   AWS의 서버
       │
       ▼
    웹사이트
```

이를 위해 AWS에서는 단순히 서버 한 대만 만드는 것이 아니라 여러 가지 요소를 함께 구성해야 한다.

```text
Internet
   │
   ▼
Internet Gateway
   │
   ▼
Route Table
   │
   ▼
Public Subnet
   │
   ▼
Security Group
   │
   ▼
EC2
   │
   ▼
Nginx
```

처음 보면 복잡해 보이지만 각각 하나씩 이해하면 어렵지 않다.

---

# 1. 먼저 알아야 하는 인터넷의 기본 원리

AWS를 배우기 전에 먼저 인터넷에서 컴퓨터끼리 어떻게 통신하는지 이해해야 한다.

## 1.1 Client와 Server

웹 서비스에는 크게 **Client와 Server**가 있다.

Client는 서비스를 사용하는 쪽이고 Server는 요청을 받아 처리하는 쪽이다.

예를 들어 Chrome에서 웹사이트에 접속하면:

```text
Chrome                       Server
Client                       EC2
  │                           │
  │ ------ HTTP 요청 -------> │
  │                           │
  │ <----- HTTP 응답 -------- │
```

Chrome은 Client이고 AWS EC2는 Server가 될 수 있다.

---

# 2. IP 주소

인터넷에서 컴퓨터를 찾아가기 위해서는 주소가 필요하다.

이것이 **IP Address**다.

예를 들어:

```text
15.164.123.10
```

같은 주소가 있을 수 있다.

우리가 EC2를 생성하면 EC2에도 IP 주소가 생긴다.

## Private IP와 Public IP

AWS를 이해할 때 두 종류의 IP를 구분하는 것이 중요하다.

### Private IP

AWS VPC 내부에서 사용하는 주소다.

```text
10.0.1.10
```

인터넷에서는 이 주소로 직접 접근할 수 없다.

### Public IP

인터넷에서 접근할 수 있는 주소다.

```text
3.36.xxx.xxx
```

따라서 외부 사용자가 EC2에 직접 접속하려면 일반적으로 EC2에 인터넷에서 도달 가능한 Public IP가 필요하다.

```text
내 컴퓨터
     │
     │ 3.36.xxx.xxx
     ▼
 Internet
     │
     ▼
    EC2
```

---

# 3. Port란 무엇인가?

IP가 **건물 주소**라면 Port는 **건물 안의 문 번호**라고 생각할 수 있다.

한 서버에서는 여러 프로그램이 동시에 실행될 수 있기 때문이다.

대표적인 포트는 다음과 같다.

| Port | 용도 |
|---:|---|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |

예를 들어:

```text
3.36.xxx.xxx:80
```

은

> "3.36.xxx.xxx 서버의 80번 문으로 접속하겠다."

라는 의미로 이해할 수 있다.

---

# 4. HTTP

브라우저와 웹 서버가 웹에서 데이터를 주고받기 위해 사용하는 대표적인 프로토콜이 **HTTP**다.

예를 들어 브라우저에서

```text
http://3.36.xxx.xxx
```

로 접속하면 브라우저가 서버에 HTTP 요청을 보낸다.

```text
Browser
   │
   │ GET /
   ▼
Server
   │
   │ 200 OK
   ▼
Browser
```

정상적으로 처리됐다면 서버가 보통 `200 OK`를 반환한다.

이번 과제에서

```bash
curl http://localhost
```

또는

```bash
curl http://<Public-IP>/health
```

를 사용하는 이유도 HTTP 요청이 정상적으로 처리되는지 확인하기 위해서다.

---

# 5. EC2란?

이제 AWS로 넘어가자.

**EC2(Elastic Compute Cloud)**는 AWS에서 제공하는 가상 서버다.

쉽게 생각하면:

> **AWS 데이터센터에 있는 컴퓨터 한 대를 빌리는 것**

이라고 이해하면 된다.

```text
EC2
├── CPU
├── Memory
├── Disk
├── Linux
└── Network
```

EC2에 Ubuntu 같은 Linux를 설치하고 그 안에서 Nginx를 실행할 수 있다.

```text
EC2
└── Ubuntu
     └── Nginx
          └── Web Page
```

---

# 6. EBS

EC2에도 데이터를 저장할 디스크가 필요하다.

AWS에서 EC2에 연결해서 사용하는 대표적인 블록 스토리지가 **EBS(Elastic Block Store)**다.

쉽게 생각하면:

```text
EC2 = 컴퓨터
EBS = SSD/HDD
```

라고 생각하면 된다.

EC2를 삭제했더라도 설정에 따라 EBS가 남아 있을 수 있으므로 실습 종료 후 반드시 확인해야 한다.

이것이 리소스 정리 체크리스트에 **EC2와 EBS가 따로 있는 이유**다.

---

# 7. SSH

EC2를 만들었다면 서버를 관리해야 한다.

원격에 있는 Linux 서버에 접속할 때 대표적으로 사용하는 것이 **SSH**다.

```text
내 Mac
   │
   │ SSH :22
   ▼
Internet
   │
   ▼
EC2
```

예를 들어:

```bash
ssh ubuntu@<EC2-PUBLIC-IP>
```

처럼 접속한다.

SSH의 기본 Port는 **22번**이다.

하지만 SSH를 인터넷 전체에 공개하는 것은 위험하다.

따라서 이번 과제에서는:

```text
22 → 내 IP만 허용
```

하도록 설정한다.

---

# 8. Nginx와 웹 서버

EC2를 만들었다고 자동으로 웹사이트가 서비스되는 것은 아니다.

HTTP 요청을 받아주는 프로그램이 필요하다.

대표적인 프로그램이 **Nginx**다.

```text
사용자
   │
   │ HTTP :80
   ▼
EC2
   │
   ▼
Nginx
   │
   ▼
Web Page
```

Nginx를 설치하고 실행한 다음 EC2 내부에서

```bash
curl http://localhost
```

를 실행해볼 수 있다.

여기서 `localhost`는:

> **현재 내가 있는 컴퓨터 자신**

을 의미한다.

EC2에서 `localhost`로 요청하면:

```text
EC2
 │
 │ localhost:80
 ▼
Nginx
```

가 된다.

따라서 `curl localhost`가 성공하면 최소한 **EC2 내부에서는 Nginx가 정상적으로 동작하고 있다**는 것을 확인할 수 있다.

---

# 9. 그런데 이것만으로 인터넷 접속은 안 된다

여기서 AWS 초보자가 많이 헷갈린다.

```bash
curl http://localhost
```

가 성공했다고 해서 내 Mac의 Chrome에서 EC2에 접속할 수 있다는 뜻은 아니다.

외부 요청이 EC2까지 들어오기 위해서는 **네트워크 경로**가 필요하다.

여기서부터 VPC가 등장한다.

---

# 10. VPC

**VPC(Virtual Private Cloud)**는 AWS 안에 만드는 나만의 가상 네트워크다.

쉽게 말하면:

> **AWS 안에 만드는 나만의 네트워크 공간**

이라고 생각할 수 있다.

예를 들어:

```text
VPC
10.0.0.0/16

┌──────────────────────────────┐
│                              │
│       나의 AWS Network       │
│                              │
│                              │
└──────────────────────────────┘
```

EC2는 이 VPC 안에 배치된다.

---

# 11. CIDR

VPC를 만들 때 다음과 같은 값을 볼 수 있다.

```text
10.0.0.0/16
```

Subnet에서는:

```text
10.0.1.0/24
```

같은 값을 볼 수 있다.

이를 **CIDR**이라고 한다.

초보 단계에서는 복잡한 계산보다 다음 정도를 이해하면 충분하다.

> CIDR은 **이 네트워크에서 사용할 IP 주소의 범위**를 나타낸다.

예를 들어 큰 VPC 네트워크 안에서 더 작은 네트워크를 나눌 수 있다.

```text
VPC
10.0.0.0/16

├── Subnet A
│   10.0.1.0/24
│
└── Subnet B
    10.0.2.0/24
```

---

# 12. Subnet

**Subnet**은 VPC의 네트워크를 더 작은 단위로 나눈 것이다.

이번 과제에서는 **Public Subnet** 하나를 만든다.

```text
VPC
┌─────────────────────────────┐
│                             │
│   Public Subnet             │
│   ┌─────────────────────┐   │
│   │                     │   │
│   │       EC2           │   │
│   │                     │   │
│   └─────────────────────┘   │
│                             │
└─────────────────────────────┘
```

그런데 이름을 `Public Subnet`이라고 지었다고 자동으로 인터넷 연결이 되는 것은 아니다.

인터넷으로 나가는 **경로**가 있어야 한다.

---

# 13. Internet Gateway

VPC와 인터넷을 연결하기 위해 사용하는 것이 **Internet Gateway(IGW)**다.

쉽게 생각하면 VPC의 **인터넷 출입구**다.

```text
VPC
 │
 │
Internet Gateway
 │
 │
Internet
```

하지만 IGW를 VPC에 붙이는 것만으로는 충분하지 않다.

> "인터넷으로 가려는 트래픽은 IGW로 보내라."

라는 규칙도 필요하다.

그것이 **Route Table**이다.

---

# 14. Route Table

Route Table은 네트워크 트래픽을 **어디로 보낼 것인지 결정하는 규칙표**다.

이번 과제에서 가장 중요한 설정 중 하나가:

```text
0.0.0.0/0 → Internet Gateway
```

이다.

`0.0.0.0/0`은 여기서:

> **그 외 모든 IPv4 목적지**

라고 이해하면 된다.

따라서:

```text
0.0.0.0/0 → IGW
```

는 쉽게 말하면

> "VPC 내부 목적지가 아닌 인터넷 방향의 트래픽은 Internet Gateway로 보내라."

라는 의미다.

---

# 15. Public Subnet이 되는 조건

여기까지 연결하면 Public Subnet의 의미를 이해할 수 있다.

핵심적으로 인터넷 연결을 위해서는:

```text
Subnet
   │
   ▼
Route Table
   │
   │ 0.0.0.0/0
   ▼
Internet Gateway
   │
   ▼
Internet
```

같은 경로가 존재해야 한다.

그리고 EC2가 인터넷에서 직접 요청을 받으려면 Public IPv4 주소 등 인터넷에서 도달할 수 있는 주소도 필요하다.

따라서 단순히 Subnet 이름을:

```text
my-public-subnet
```

이라고 만드는 것이 중요한 것이 아니라 **실제 라우팅 구성이 중요하다.**

---

# 16. Security Group

이제 인터넷으로 연결되는 길을 만들었다.

그런데 모든 사람이 EC2의 모든 Port에 접근할 수 있게 하면 위험하다.

그래서 **Security Group(SG)**을 사용한다.

Security Group은 EC2 등에 적용하는 **상태 저장형 가상 방화벽**이라고 이해하면 된다.

이번 과제에서는 대략 다음과 같이 구성한다.

```text
Inbound

HTTP
80
0.0.0.0/0
→ 누구나 접속 가능

SSH
22
내 IP/32
→ 나만 접속 가능
```

반대로 이런 설정은 피해야 한다.

```text
All Traffic
0 - 65535
0.0.0.0/0
```

사실상 모든 사람이 모든 포트에 접근할 수 있도록 허용하는 것이기 때문이다.

---

# 17. 왜 HTTP는 열고 SSH는 제한할까?

웹사이트의 목적은 누구나 사용하는 것이다.

따라서:

```text
HTTP :80
↓
0.0.0.0/0
```

로 공개한다.

반면 SSH는 서버 관리자가 사용하는 기능이다.

```text
SSH :22
↓
내 IP만
```

허용하면 된다.

이것이 **필요한 것만 열어두는 보안 원칙**이다.

DB Port도 마찬가지다.

예를 들어:

```text
MySQL      3306
PostgreSQL 5432
```

같은 포트를 특별한 이유 없이:

```text
0.0.0.0/0
```

으로 공개하면 외부 공격에 노출될 수 있다.

---

# 18. 전체 네트워크 흐름 연결하기

지금까지 배운 내용을 하나로 연결해보자.

사용자가 브라우저에서:

```text
http://<EC2-PUBLIC-IP>
```

에 접속했다.

요청은 개념적으로 다음 구성들을 거쳐 EC2의 웹 서버에 도달한다.

```text
사용자 Browser
       │
       │ HTTP :80
       ▼
    Internet
       │
       ▼
Internet Gateway
       │
       │
       ▼
┌────────────── VPC ──────────────┐
│                                 │
│ Route Table                     │
│ 0.0.0.0/0 → IGW                │
│                                 │
│ Public Subnet                   │
│                                 │
│      Security Group             │
│      80 ← 0.0.0.0/0            │
│      22 ← 내 IP                 │
│             │                   │
│             ▼                   │
│         ┌─────────┐             │
│         │   EC2   │             │
│         │         │             │
│         │ Nginx   │             │
│         │  :80    │             │
│         └─────────┘             │
│                                 │
└─────────────────────────────────┘
```

이번 미션에서 **가장 중요한 그림**이다.

---

# 19. IAM

Security Group과 함께 중요한 보안 개념이 **IAM**이다.

하지만 Security Group과 IAM은 완전히 다른 문제를 해결한다.

## Security Group

Security Group은:

> **누가 네트워크를 통해 서버에 접근할 수 있는가?**

를 제어한다.

예:

```text
인터넷 사용자
      │
      │ Port 80 허용?
      ▼
     EC2
```

## IAM

IAM은:

> **누가 AWS에서 어떤 작업을 할 수 있는가?**

를 제어한다.

예를 들어:

```text
김승우
   │
   │ EC2 생성 가능?
   │ VPC 삭제 가능?
   │ Security Group 수정 가능?
   ▼
  AWS
```

이를 비교하면:

| 구분 | Security Group | IAM |
|---|---|---|
| 관리 대상 | 네트워크 접근 | AWS 권한 |
| 질문 | 서버의 80번 Port에 들어올 수 있는가? | EC2를 생성할 수 있는가? |
| 예 | HTTP 80 허용 | `ec2:RunInstances` 허용 |
| 핵심 | 네트워크 보안 | AWS 리소스 접근 제어 |

이 차이는 반드시 설명할 수 있어야 한다.

---

# 20. 최소 권한 원칙

IAM에서 매우 중요한 원칙이 **Least Privilege, 최소 권한 원칙**이다.

뜻은 간단하다.

> **업무에 필요한 권한만 부여한다.**

예를 들어 EC2와 VPC 실습만 하는 사람이 있다고 하자.

그 사람에게 AWS 전체 관리자 권한을 줄 필요는 없다.

```text
❌ AdministratorAccess

AWS의 거의 모든 서비스 관리 가능
```

대신:

```text
EC2 관련 필요한 작업
VPC 관련 필요한 작업
Security Group 관련 필요한 작업
Tag 관련 필요한 작업
```

정도만 허용한다.

실습과 관계없는:

```text
S3
RDS
Lambda
...
```

등의 권한까지 줄 이유는 없다.

이렇게 하면 계정이 실수하거나 탈취되더라도 피해 범위를 줄일 수 있다.

---

# 21. 외부 접속 검증

서버 구축이 완료되었다면 실제로 외부에서 접속되는지 확인해야 한다.

이번 과제에서는 두 가지 중 하나를 선택한다.

## 방법 A — 브라우저

```text
http://<PUBLIC-IP>
```

접속 후:

```text
Welcome to nginx!
```

같은 페이지가 나타나는지 확인한다.

## 방법 B — Health Check

```text
GET http://<PUBLIC-IP>/health
```

요청을 보내고:

```text
200 OK

OK
```

같은 고정 응답을 확인한다.

여기서 중요한 것은 단순히 스크린샷을 제출하는 것이 아니다.

> **왜 이 요청이 성공할 수 있었는지를 앞에서 배운 네트워크 구조로 설명할 수 있어야 한다.**

---

# 22. 장애가 발생하면 어떻게 해야 할까?

예를 들어:

```text
curl localhost
```

는 성공한다.

그런데 Mac의 Chrome에서:

```text
http://<PUBLIC-IP>
```

로 접속하면 실패한다.

어떻게 해야 할까?

초보자는 이것저것 설정을 바꾸기 쉽다.

하지만 좋은 트러블슈팅은:

```text
증상
 ↓
가설
 ↓
검증
 ↓
조치
 ↓
결과
 ↓
재발 방지
```

순서로 진행한다.

---

# 23. 외부 접속 장애 점검 순서

이번 평가에서는 다음 순서를 이해하는 것이 중요하다.

```text
① Routing
    ↓
② Security Group
    ↓
③ Public IP / DNS
    ↓
④ Server Process
    ↓
⑤ Log
```

## ① Routing 확인

먼저 네트워크 경로를 확인한다.

```text
Public Subnet
      │
      ▼
Route Table
      │
0.0.0.0/0 → IGW ?
      │
      ▼
Internet Gateway
```

IGW가 VPC에 연결되어 있는지도 확인한다.

## ② Security Group 확인

다음으로 HTTP 80이 허용되어 있는지 확인한다.

```text
80
TCP
0.0.0.0/0
```

## ③ Public IP 확인

EC2에 실제 Public IP가 있는지 확인한다.

Public IP가 없다면 인터넷 사용자가 해당 IP를 이용해 직접 접근할 수 없다.

## ④ Server Process 확인

EC2까지 요청이 들어오더라도 Nginx가 실행되고 있지 않으면 응답할 수 없다.

예를 들어:

```bash
curl http://localhost
```

를 사용해 서버 내부에서 먼저 확인할 수 있다.

## ⑤ Log 확인

그래도 문제가 해결되지 않으면 Nginx나 시스템 로그 등을 확인한다.

중요한 것은:

> **추측으로 설정을 계속 변경하는 것이 아니라 증거를 통해 가설을 검증하는 것**

이다.

---

# 24. 트러블슈팅 예시

예를 들어 다음 문제가 있다고 하자.

### 증상

```text
EC2에서 curl localhost → 성공

Mac에서 EC2 Public IP 접속 → 실패
```

### 가설

Nginx 자체는 정상일 가능성이 높다.

외부 네트워크 접근 문제일 수 있다.

### 검증

Security Group 확인:

```text
SSH 22 → 내 IP

HTTP 80 → 없음
```

### 원인

80번 Port가 열려 있지 않았다.

### 조치

```text
HTTP
TCP
80
0.0.0.0/0
```

추가.

### 결과

브라우저 접속 성공.

### 재발 방지

배포 체크리스트에:

```text
[ ] HTTP 80 Inbound 확인
```

항목 추가.

이것이 이번 과제에서 원하는 **가설 → 검증 기반 문제 해결**이다.

---

# 25. IAM 오류는 어떻게 해결할까?

이번에는 EC2를 생성하려는데:

```text
AccessDenied
```

오류가 발생했다고 생각해보자.

가장 쉬운 해결책처럼 보이는 것은:

```text
AdministratorAccess
```

를 주는 것이다.

하지만 이것은 좋은 해결 방법이 아니다.

먼저 오류 메시지를 확인한다.

예를 들어 특정 Action에 대한 권한이 부족하다는 것을 발견했다면:

```text
어떤 Action이 거부됐는가?
        ↓
어떤 Resource에 대한 권한인가?
        ↓
현재 IAM Policy 확인
        ↓
필요한 최소 권한 추가
        ↓
다시 실행
```

방식으로 해결한다.

즉:

> **문제가 생겼다고 권한을 크게 주는 것이 아니라 필요한 권한을 하나씩 찾아간다.**

---

# 26. Tag와 이름 규칙

AWS를 사용하다 보면 리소스가 많아진다.

예:

```text
EC2
VPC
Subnet
Security Group
Route Table
EBS
IGW
...
```

어떤 것이 이번 실습에서 만든 것인지 구분하기 어려워질 수 있다.

그래서 이름과 Tag를 사용한다.

예를 들어:

```text
Project = cloud-mission
Owner   = student01
Env     = practice
```

같은 Tag를 붙일 수 있다.

이렇게 하면 나중에:

> "이번 실습에서 만든 리소스가 무엇이지?"

를 쉽게 찾을 수 있다.

이는 과금 방지에도 중요하다.

---

# 27. AWS에서는 왜 리소스를 삭제해야 할까?

클라우드에서는 리소스를 생성해서 사용하는 만큼 비용이 발생할 수 있다.

따라서 실습이 끝났다고 EC2만 끄고 끝내면 안 된다.

확인해야 할 대표적인 리소스가 있다.

```text
EC2
EBS
Elastic IP
Internet Gateway
VPC
```

추가로 만들었다면:

```text
NAT Gateway
ALB
RDS
```

등도 확인한다.

특히 NAT Gateway나 Load Balancer 같은 일부 리소스는 계속 유지하면 비용이 발생할 수 있기 때문에 주의해야 한다.

---

# 28. Cleanup Checklist

실습이 끝나면 최소한 다음을 확인한다.

```text
[ ] EC2 종료/삭제 확인

[ ] EBS Volume 확인

[ ] Elastic IP Release 확인

[ ] Internet Gateway Detach/Delete

[ ] Subnet 확인

[ ] Route Table 확인

[ ] VPC 삭제

[ ] NAT Gateway 확인 (만들었다면)

[ ] ALB 확인 (만들었다면)

[ ] RDS 확인 (만들었다면)

[ ] Billing Dashboard 확인
```

그리고 이름이나 Tag를 기준으로 이번 실습에서 만든 리소스가 남아 있지 않은지 확인한다.

---

# 29. 서버가 한 대로 부족해진다면?

여기부터는 평가 항목 4의 응용 문제다.

현재 구조는:

```text
Internet
    │
    ▼
  EC2 1대
```

다.

사용자가 많아져 EC2 한 대로 처리하기 어려워졌다고 생각해보자.

서버를 두 대로 늘릴 수 있다.

```text
EC2 #1

EC2 #2
```

그런데 문제가 생긴다.

> 사용자의 요청을 어느 서버로 보내야 할까?

이때 **Load Balancer**를 사용할 수 있다.

AWS에서는 웹 트래픽에 **ALB(Application Load Balancer)**를 사용할 수 있다.

```text
              Internet
                  │
                  ▼
                 ALB
               /     \
              /       \
             ▼         ▼
          EC2 #1     EC2 #2
```

ALB가 들어오는 요청을 여러 EC2로 분배한다.

서버의 성능을 높이는 것만이 아니라 서버의 **개수를 늘리는 방식**을 일반적으로 Scale Out이라고 한다.

```text
1대
↓
2대
↓
3대
```

이번 과제에서 직접 구축할 필요는 없더라도:

> "트래픽이 증가해서 EC2를 두 대로 늘리면 어떻게 할 것인가?"

라는 질문에 이 정도 구조는 설명할 수 있어야 한다.

---

# 30. Security Group과 IAM 다시 구분하기

시험이나 평가에서 매우 중요한 부분이므로 다시 정리한다.

상황 1:

> 브라우저에서 EC2의 80번 Port에 접근할 수 없다.

먼저 확인할 대상:

**Security Group / Routing**

상황 2:

> AWS Console에서 EC2를 생성하려는데 AccessDenied가 발생한다.

먼저 확인할 대상:

**IAM**

즉:

```text
네트워크 접근 문제
        ↓
Security Group


AWS API/리소스 작업 권한 문제
        ↓
IAM
```

라고 구분하면 된다.

---

# 31. 이번 과제의 전체 구조

이제 처음부터 끝까지 다시 연결해보자.

## ① AWS에 네트워크를 만든다

```text
VPC
└── Public Subnet
```

## ② 인터넷 경로를 만든다

```text
Public Subnet
      │
      ▼
Route Table
0.0.0.0/0 → IGW
      │
      ▼
Internet Gateway
      │
      ▼
Internet
```

## ③ 서버를 만든다

```text
Public Subnet
└── EC2
     ├── Linux
     ├── EBS
     └── Nginx
```

## ④ 필요한 Port만 허용한다

```text
Security Group

80 → 0.0.0.0/0
22 → 내 IP
```

## ⑤ AWS 작업 권한도 제한한다

```text
IAM

필요한 EC2/VPC 관련 권한
        +
최소 권한 원칙
```

## ⑥ 외부에서 접속한다

```text
Browser
   │
   │ HTTP
   ▼
Internet
   │
   ▼
IGW
   │
   ▼
Route Table
   │
   ▼
Public Subnet
   │
   ▼
Security Group
   │
   ▼
EC2
   │
   ▼
Nginx
```

## ⑦ 문제가 발생하면 원인을 추적한다

```text
증상
 ↓
가설
 ↓
검증
 ↓
조치
 ↓
결과
 ↓
재발 방지
```

## ⑧ 실습이 끝나면 리소스를 정리한다

```text
Tag / 이름으로 추적
       ↓
리소스 삭제
       ↓
Billing 확인
```

---

# 32. 평가 항목 1 — 실제로 구축할 수 있는가?

첫 번째 평가에서는 **실제로 만들 수 있는지**가 중요하다.

확인해야 할 것은 다음과 같다.

### 네트워크

```text
VPC
Public Subnet
Internet Gateway
Route Table
0.0.0.0/0 → IGW
```

### 서버

```text
EC2
SSH 접속
Nginx 실행
```

### 보안

```text
80 → 0.0.0.0/0

22 → 내 IP
```

### 외부 접속

```text
http://<Public-IP>
```

또는:

```text
GET /health
→ 200 OK
```

### 리소스 정리

최소:

```text
EC2
EBS
EIP
IGW
VPC
```

를 추적하고 정리한다.

---

# 33. 평가 항목 2 — 내가 만든 것을 설명할 수 있는가?

단순히 AWS Console에서 따라 만드는 것만으로는 부족하다.

다음 질문에 자신의 말로 대답할 수 있어야 한다.

### Q. 인터넷에서 EC2까지 요청이 어떻게 들어오나요?

핵심:

```text
Internet
→ IGW
→ Public Subnet의 Routing
→ Security Group
→ EC2
→ Nginx
```

### Q. 왜 80은 공개하고 22는 공개하지 않았나요?

```text
80 = 서비스 사용자가 접근해야 함

22 = 서버 관리자만 필요
```

따라서 필요한 Port만 필요한 사용자에게 허용한다.

### Q. 외부 접속은 어떻게 확인했나요?

예:

```text
브라우저에서
http://<Public-IP>

접속 후 Nginx 페이지 확인
```

또는:

```text
GET /health
→ 200 OK
→ OK
```

### Q. 내가 만든 AWS 리소스는 어떻게 관리했나요?

예:

```text
Name
Tag
Checklist
```

를 사용해서 추적했다고 설명할 수 있다.

---

# 34. 평가 항목 3 — 왜 그렇게 구성했는지 이해하는가?

여기부터는 단순 암기보다 **이유**가 중요하다.

### Q. 왜 `0.0.0.0/0 → IGW`가 필요한가?

Public Subnet에서 인터넷 방향으로 가는 트래픽을 Internet Gateway로 보내기 위한 기본 경로이기 때문이다.

### Q. Security Group과 IAM의 차이는?

```text
Security Group
→ 네트워크 접근 제어

IAM
→ AWS 리소스/API 권한 제어
```

### Q. 왜 SSH를 `0.0.0.0/0`으로 열면 안 되는가?

인터넷의 누구나 SSH 포트에 접근을 시도할 수 있기 때문이다.

따라서:

```text
SSH 22
→ 관리자 IP/32
```

처럼 접근 범위를 제한한다.

### Q. 왜 가설 → 검증 순서로 장애를 해결하는가?

설정을 무작정 변경하면 무엇이 문제였는지 알 수 없고 새로운 문제를 만들 수도 있다.

따라서:

```text
증상 관찰
→ 원인 가설
→ 로그/설정으로 검증
→ 필요한 부분만 수정
```

한다.

---

# 35. 평가 항목 4 — 문제가 생겼을 때 응용할 수 있는가?

마지막 단계에서는 처음 보는 상황에 배운 원리를 적용할 수 있어야 한다.

### Q. 외부 접속이 안 됩니다. 무엇부터 확인하나요?

```text
Routing
   ↓
Security Group
   ↓
Public IP / DNS
   ↓
Server Process
   ↓
Log
```

### Q. IAM 권한 부족 오류가 발생했습니다.

```text
AccessDenied 확인
      ↓
실패한 Action 확인
      ↓
현재 Policy 확인
      ↓
필요한 최소 권한 확인
      ↓
해당 권한만 추가
```

AdministratorAccess부터 주지 않는다.

### Q. 사용자가 많아져 EC2를 2대로 늘리고 싶습니다.

```text
             Internet
                 │
                 ▼
                ALB
              /     \
             ▼       ▼
          EC2 #1   EC2 #2
```

처럼 Load Balancer를 두고 요청을 여러 서버로 분배하는 구조를 생각할 수 있다.

### Q. 예상하지 못한 AWS 비용이 발생했습니다.

먼저:

```text
Billing
   ↓
어떤 서비스에서 비용 발생?
   ↓
Region 확인
   ↓
Tag / 이름 확인
   ↓
실행 중인 Resource 확인
   ↓
불필요한 Resource 정리
```

순서로 추적한다.

특히:

```text
EC2
EBS
Elastic IP
NAT Gateway
Load Balancer
RDS
```

등의 리소스를 확인한다.

---

# 36. 최종적으로 이해해야 하는 핵심

이번 과제에서 AWS 서비스 이름을 전부 외우는 것이 가장 중요한 것은 아니다.

가장 중요한 것은 다음 질문에 답할 수 있는 것이다.

> **"내 컴퓨터의 브라우저에서 보낸 HTTP 요청이 어떻게 AWS EC2에서 실행 중인 Nginx까지 도착하는가?"**

그 과정을 설명할 수 있다면:

```text
IP
Port
HTTP

↓

VPC
Subnet
Route Table
Internet Gateway

↓

Security Group

↓

EC2
Nginx
```

가 서로 연결된 것이다.

여기에 AWS 자체의 작업 권한을 관리하는:

```text
IAM
↓
Least Privilege
```

를 별도의 보안 축으로 이해한다.

그리고 문제가 발생했을 때:

```text
증상
→ 가설
→ 검증
→ 조치
→ 결과
→ 재발 방지
```

방식으로 해결한다.

마지막으로 실습이 끝나면:

```text
Resource 확인
→ Cleanup
→ Billing 확인
```

까지 수행한다.

---

# 37. 평가 전 최종 체크

평가 전에 아래 질문에 자신의 말로 답할 수 있는지 확인해보자.

- VPC는 무엇인가?
- Subnet은 무엇인가?
- Public Subnet은 왜 Public한가?
- `0.0.0.0/0`은 무슨 뜻인가?
- Internet Gateway는 왜 필요한가?
- Route Table은 무슨 일을 하는가?
- Public IP와 Private IP는 무엇이 다른가?
- EC2는 무엇인가?
- EBS는 무엇인가?
- Nginx는 왜 필요한가?
- `localhost`는 무엇인가?
- Port 80과 22는 각각 무엇인가?
- Security Group은 무엇인가?
- 왜 80은 `0.0.0.0/0`으로 허용할 수 있는가?
- 왜 22는 내 IP로 제한해야 하는가?
- Security Group과 IAM은 무엇이 다른가?
- 최소 권한 원칙이란 무엇인가?
- `curl localhost`는 되는데 외부 접속이 안 되면 무엇을 확인해야 하는가?
- 장애 해결에서 왜 가설 → 검증 순서가 중요한가?
- EC2를 2대로 늘리면 왜 Load Balancer가 필요한가?
- 예상하지 못한 비용이 발생하면 무엇부터 확인해야 하는가?
- 실습 종료 후 어떤 AWS 리소스를 확인하고 삭제해야 하는가?

이 질문들을 단순히 정의만 외우는 것이 아니라 **서로 연결해서 설명할 수 있다면 이번 미션의 핵심 개념을 제대로 이해한 것이다.**