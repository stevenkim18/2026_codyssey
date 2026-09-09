# 리소스 정리 체크리스트

정리 완료 시각: 2026-09-09 10:54 KST

- [x] EC2 `i-083e781aa1de18a3f` 상태 `Terminated` 확인
- [x] 연결된 EBS 볼륨 삭제 확인: 서울 리전 Volumes 목록 0개
- [x] Elastic IP 미사용 확인: Auto-assigned public IPv4만 사용했고, Elastic IP 목록 0개
- [x] Internet Gateway `igw-04f1f15eba9ae5a16` Detach 및 Delete 완료
- [x] Public Subnet `subnet-0ab6adec610ded58f` 삭제 완료
- [x] Main Route Table 및 기본 Network ACL은 VPC 삭제와 함께 제거됨
- [x] VPC `vpc-070340517eb948973` 삭제 완료
- [x] VPC 내 Security Group `sg-097e8d51044fa6ce4`도 VPC 삭제와 함께 제거됨
- [x] NAT Gateway 미생성
- [x] ELB/ALB 미생성
- [x] RDS 미생성
- [x] Key Pair는 비용이 발생하지 않아 증빙 및 재학습용으로 유지. 필요 없으면 EC2 Key Pairs에서 `cloud-mission-key`를 삭제할 수 있음.
- [ ] Billing Dashboard 확인 권장: 청구 데이터 반영에는 시간이 걸릴 수 있음.
