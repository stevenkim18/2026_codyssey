# Cloud Mission: EC2 웹 서비스 배포

## 개요
서울 리전(`ap-northeast-2`)에 VPC, Public Subnet, Internet Gateway, Route Table, Security Group, EC2/Nginx를 구성했다. 서비스 검증 후 과금 방지를 위해 모든 과금 대상 리소스를 정리했다. 따라서 아래 Public IP는 검증 당시 기록이며 현재는 사용하지 않는다.

## 최종 구성
- VPC: `cloud-mission-vpc` (`10.20.0.0/16`)
- Public Subnet: `cloud-mission-public-subnet` (`10.20.1.0/24`, ap-northeast-2a)
- Internet Gateway: `cloud-mission-igw`
- Route: `0.0.0.0/0 -> igw-04f1f15eba9ae5a16`
- Security Group: `cloud-mission-web-sg`
  - HTTP 80: `0.0.0.0/0`
  - SSH 22: `121.135.181.35/32`만 허용
- EC2: `cloud-mission-ec2`, Amazon Linux 2023, `t3.micro`, gp3 8 GiB
- IAM: 전용 사용자 `cloud-mission-user`, `AdministratorAccess` 미부여

## 외부 접속 검증 방식: B
- URL: `http://3.35.149.46/health`
- 검증 시각: 2026-09-09 10:49 KST
- 관측 결과: HTTP `200`, 응답 본문 `OK`

## 내부 검증
SSH로 접속해 확인한 결과:
```text
localhost_status=200
health=OK
nginx=active
```

## 재현 절차
1. 서울 리전을 선택한다.
2. VPC `10.20.0.0/16`과 Public Subnet `10.20.1.0/24`를 만든다.
3. Internet Gateway를 VPC에 연결하고, Main Route Table에 `0.0.0.0/0 -> IGW`를 추가한다.
4. Subnet의 Auto-assign public IPv4를 활성화한다.
5. Security Group에서 HTTP 80은 전체, SSH 22는 내 IP만 허용한다.
6. Amazon Linux 2023 `t3.micro`, 8 GiB EBS, 기존 Security Group, Key Pair를 선택해 EC2를 시작한다.
7. User data로 Nginx 설치, 시작, `/health` 파일 생성을 자동화한다.
8. 외부 `GET /health`와 SSH 내부 `curl http://localhost`로 검증한다.

## 증빙
- `docs/architecture.png`: 아키텍처
- `docs/screenshots/01-seoul-region.png`: 서울 리전
- `docs/screenshots/02-vpc-created.png`: VPC 생성
- `docs/screenshots/03-public-route.png`: IGW 기본 경로
- `docs/screenshots/04-security-group.png`: HTTP/SSH 인바운드 규칙
- `docs/screenshots/05-running-instance.png`: Running EC2와 Public IPv4
- `docs/screenshots/external-health-check.png`: 외부 `/health` 200 증빙
- `docs/screenshots/ssh-internal-verification.png`: SSH 내부 `curl` 및 Nginx 활성 상태 증빙
- `docs/screenshots/06-cleanup-confirmed.png`: VPC, Subnet, Security Group 삭제 성공 증빙
