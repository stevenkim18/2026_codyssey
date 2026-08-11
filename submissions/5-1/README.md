# 프로젝트 관리 툴 데이터베이스

SQLite로 구현한 회원 기반 프로젝트 관리 툴의 데이터베이스 실습 결과물이다.

## 도메인 구조

- `members`: 회원과 로그인에 필요한 기본 정보
- `projects`: 회원이 소유하는 프로젝트
- `tasks`: 프로젝트에 속하고 회원에게 담당되는 할 일
- `project_members`: 프로젝트 참여 회원과 역할을 관리하는 연결 테이블

주요 관계는 다음과 같다.

```text
members 1:N projects       프로젝트 소유자
projects 1:N tasks          프로젝트별 할 일
members 1:N tasks           할 일 담당자
members N:M projects        project_members로 연결
```

`password_hash`에는 실습용 가짜 해시 값만 저장했다. 실제 서비스에서는 평문 비밀번호를 저장하지 않고, 검증된 해시 알고리즘으로 생성한 값만 저장해야 한다.

## 실행 방법

SQLite CLI에서 다음 순서로 실행한다.

```bash
sqlite3 project-management.sqlite3 < schema.sql
sqlite3 project-management.sqlite3 < seed.sql
sqlite3 -header -box project-management.sqlite3 < queries.sql
```

`queries.sql`의 `Q12`, `Q13`은 `UPDATE`와 `DELETE` 결과를 확인한 뒤 `ROLLBACK`한다. 따라서 샘플 데이터는 반복 실행할 수 있는 상태로 유지된다.

실행 결과는 [`results/query-results.txt`](results/query-results.txt)에 기록했다.

평가 대비 개념 설명은 [`docs/evaluation-guide.md`](docs/evaluation-guide.md)에 정리했다.
