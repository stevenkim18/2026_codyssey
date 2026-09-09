# 트러블슈팅 보고서

## 사례: EC2 Instance Connect 브라우저 SSH 실패

| 항목 | 내용 |
|---|---|
| 증상 | EC2 콘솔의 **Connect**에서 브라우저 기반 EC2 Instance Connect 연결을 시도했으나 `SendSSHPublicKey failed` 오류가 발생했다. |
| 원인 가설 | 전용 IAM 사용자에게 EC2 Instance Connect의 임시 공개키 전송 권한이 없을 수 있다. |
| 검증 | 콘솔 오류 문구가 `SendSSHPublicKey failed`였고, 일반 SSH는 동일 인스턴스와 동일 보안 그룹에서 성공했다. |
| 조치 | 불필요한 권한을 추가하지 않고, 생성한 `cloud-mission-key.pem`와 SSH 22의 개인 IP 제한 규칙을 사용해 표준 OpenSSH로 접속했다. |
| 결과 | SSH 접속 후 `curl http://localhost`가 `200`, `/health`가 `OK`, `systemctl is-active nginx`가 `active`를 반환했다. |
| 재발 방지 | 배포 전 “관리 방식 확인” 항목을 체크한다. 브라우저 EC2 Instance Connect를 사용할 경우에는 별도 권한 검토가 필요하며, 단순 실습은 개인 IP 제한 SSH와 키 페어로 충분하다. |

## 추가 점검: 외부 접속이 안 될 때
1. EC2에 Public IPv4가 있는지 확인한다.
2. Subnet의 Route Table에 `0.0.0.0/0 -> IGW`가 있는지 확인한다.
3. IGW가 해당 VPC에 Attach되어 있는지 확인한다.
4. Security Group HTTP 80이 `0.0.0.0/0`인지 확인한다.
5. Nginx가 실행 중인지 `systemctl is-active nginx`으로 확인한다.
6. 인스턴스에서 `curl http://localhost`와 `curl http://localhost/health`를 실행한다.
