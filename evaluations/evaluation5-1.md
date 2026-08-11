# 평가 대비 자료

## 과제 정보

- 과제: 정보를 깔끔하게 정리하는 디지털 서랍장 만들기
- 주제: 회원 기능이 있는 프로젝트 관리 툴
- DB: SQLite
- 핵심 테이블: `members`, `projects`, `tasks`, `project_members`
- 구현 범위: 백엔드 프레임워크 없이 SQL로 데이터 모델링, 입력, 조회, 수정, 삭제를 실습한다.

## 제출물 위치

- [README.md](../submissions/5-1/README.md)
- [schema.sql](../submissions/5-1/schema.sql)
- [seed.sql](../submissions/5-1/seed.sql)
- [queries.sql](../submissions/5-1/queries.sql)
- [erd.md](../submissions/5-1/erd.md)
- [query-results.txt](../submissions/5-1/results/query-results.txt)

## 1. 1분 소개 답변

> 제가 만든 결과물은 회원이 프로젝트를 만들고, 프로젝트에 참여한 회원에게 할 일을 배정할 수 있는 프로젝트 관리 툴 데이터베이스입니다. SQLite를 사용했고, 회원(`members`), 프로젝트(`projects`), 할 일(`tasks`), 프로젝트 참여 회원(`project_members`) 네 개의 테이블로 구성했습니다.
>
> 프로젝트와 할 일은 1:N 관계이고, 회원과 할 일도 담당자 기준으로 1:N 관계입니다. 회원과 프로젝트는 여러 명이 여러 프로젝트에 참여할 수 있으므로 `project_members` 연결 테이블을 사용해 N:M 관계로 설계했습니다. 모든 테이블에 PK를 두고, 프로젝트 소유자·할 일의 프로젝트·할 일 담당자에는 FK를 적용했습니다.
>
> `schema.sql`에서 테이블과 제약조건을 만들고, `seed.sql`에서 부모 테이블부터 샘플 데이터를 입력했습니다. `queries.sql`에는 기본 조회, INNER JOIN, LEFT JOIN, 집계, 서브쿼리, UPDATE, DELETE, 인덱스를 포함한 15개의 쿼리를 작성했으며, 실행 결과는 `results/query-results.txt`에 남겼습니다.

## 2. 과제 요구사항 충족 근거

| 요구사항 | 구현 내용 | 확인할 파일/쿼리 |
| --- | --- | --- |
| 로컬 DB 준비 | SQLite CLI로 실행 | `README.md` 실행 방법 |
| 최소 4개 테이블 | `members`, `projects`, `tasks`, `project_members` | `schema.sql` |
| PK 적용 | 네 테이블 모두 PK 보유 | `schema.sql` |
| 1:N 관계 2개 이상 | `members → projects`, `projects → tasks`, `members → tasks` | `erd.md`, `schema.sql` |
| N:M 관계 | `project_members` 연결 테이블 | `erd.md` |
| `NOT NULL` | 이름, 이메일, 제목, FK 등 | `schema.sql` |
| `UNIQUE` | `members.email` | `schema.sql` |
| FK 동작 | `PRAGMA foreign_keys = ON` 및 FK 선언 | `schema.sql`, 정합성 테스트 |
| 테이블당 10행 이상 | members 10, projects 10, tasks 20, project_members 21 | `seed.sql`, 실행 결과 |
| 기본 조회 4개 이상 | Q01~Q04 | `queries.sql` |
| JOIN 4개 이상 | INNER JOIN Q05~Q07, LEFT JOIN Q08 | `queries.sql` |
| 집계 3개 이상 | COUNT Q08, COUNT/SUM Q09, AVG Q10 | `queries.sql` |
| 서브쿼리 | ACTIVE 프로젝트 조회 Q11, 평균 우선순위 Q15 | `queries.sql` |
| 수정 및 삭제 | UPDATE Q12, DELETE Q13 | `queries.sql` |
| 인덱스 | `idx_tasks_assignee_status` 생성 및 실행 계획 확인 | Q14 |
| 실행 결과 | 쿼리별 결과 텍스트 저장 | `results/query-results.txt` |
| ERD | Mermaid ERD와 관계 설명 | `erd.md` |

## 3. 반드시 설명할 데이터베이스 개념

### 3.1 데이터베이스와 엑셀의 차이

엑셀은 표 형태로 데이터를 편집하기 좋은 도구이고, 데이터베이스는 관계와 규칙을 가진 데이터를 지속적으로 저장하고 조회하기 위한 시스템입니다.

이 프로젝트에서는 회원 이름이나 프로젝트 정보를 할 일마다 반복해서 저장하지 않고 각각의 테이블로 분리했습니다. 그러면 같은 회원의 이메일이나 프로젝트 이름이 여러 행에서 서로 다르게 수정되는 문제를 줄일 수 있습니다. 회원과 프로젝트의 연결은 FK와 `JOIN`으로 해결합니다.

다만 SQLite는 서버가 없는 파일 기반 DB라 설치가 쉽다는 장점이 있는 대신, 여러 사용자가 동시에 대량의 쓰기 작업을 하는 서비스에는 서버형 DB보다 적합하지 않을 수 있습니다. 이번 과제에서는 SQL과 관계 설계 학습이 목적이므로 SQLite를 선택했습니다.

### 3.2 테이블을 나눈 이유

테이블은 하나의 역할을 중심으로 나눴습니다.

- `members`: 회원이라는 주체의 정보
- `projects`: 프로젝트 자체의 정보
- `tasks`: 프로젝트에서 수행할 작업 정보
- `project_members`: 어떤 회원이 어떤 프로젝트에 참여하는지에 대한 관계 정보

모든 정보를 하나의 테이블에 넣으면 회원, 프로젝트, 할 일 정보가 반복되어 삽입·수정·삭제 시 이상 현상이 생길 수 있습니다. 프로젝트 참여처럼 회원과 프로젝트가 서로 여러 개씩 연결되는 관계는 별도의 연결 테이블로 분리했습니다.

### 3.3 PK와 FK

PK(Primary Key)는 테이블의 각 행을 유일하게 식별하는 값입니다. 이 프로젝트에서는 각 테이블의 `id`가 PK이고, `project_members`는 `(project_id, member_id)`를 묶은 복합 PK입니다.

FK(Foreign Key)는 다른 테이블의 PK를 참조해 테이블 사이의 연결과 참조 무결성을 보장하는 컬럼입니다.

- `projects.owner_id` → `members.id`
- `tasks.project_id` → `projects.id`
- `tasks.assignee_id` → `members.id`
- `project_members.project_id` → `projects.id`
- `project_members.member_id` → `members.id`

예를 들어 `tasks.project_id = 3`이면 `projects.id = 3`인 프로젝트에 속한 할 일이라는 뜻입니다. 존재하지 않는 프로젝트 ID를 넣으면 SQLite가 FK 오류를 발생시켜 잘못된 연결을 막습니다.

### 3.4 1:N과 N:M 관계

1:N은 부모 하나에 자식이 여러 개 연결되는 관계입니다.

- 한 회원은 여러 프로젝트를 소유할 수 있다: `members 1:N projects`
- 한 프로젝트에는 여러 할 일이 있을 수 있다: `projects 1:N tasks`
- 한 회원은 여러 할 일을 담당할 수 있다: `members 1:N tasks`

회원과 프로젝트의 참여 관계는 N:M입니다. 한 회원이 여러 프로젝트에 참여할 수 있고, 하나의 프로젝트에도 여러 회원이 참여할 수 있기 때문입니다. 관계형 DB에서는 이 관계를 직접 저장하기보다 `project_members(project_id, member_id)`라는 연결 테이블로 두 개의 1:N 관계로 풀어냅니다.

### 3.5 제약조건

- `NOT NULL`: 반드시 값이 있어야 하는 컬럼에 적용한다. 예를 들어 회원 이메일, 프로젝트 소유자, 할 일 제목은 비어 있으면 의미가 없으므로 `NOT NULL`이다.
- `UNIQUE`: 중복을 허용하지 않는 제약조건이다. `members.email`에 적용해 같은 이메일로 여러 회원이 만들어지는 것을 막는다.
- `CHECK`: 허용할 값을 제한한다. 프로젝트 상태는 `PLANNING`, `ACTIVE`, `ON_HOLD`, `DONE` 중 하나이고, 할 일 우선순위는 1~5 사이만 허용한다.
- `DEFAULT`: 값이 생략되었을 때 사용할 기본값이다. 프로젝트 상태나 생성 시각에 사용했다.
- 복합 PK: `project_members`에서 같은 회원이 같은 프로젝트에 중복 참여하는 것을 막는다.

### 3.6 부모 테이블부터 INSERT하는 이유

FK가 참조하는 행이 먼저 존재해야 하기 때문입니다. 따라서 `members`를 먼저 넣고, 그 다음 `projects`, `tasks`, `project_members` 순서로 입력했습니다.

예를 들어 `tasks.assignee_id = 2`를 넣으려면 먼저 `members.id = 2`인 회원이 있어야 합니다. 순서를 지키지 않으면 FK 제약조건에 의해 INSERT가 실패합니다.

## 4. SQL 문법과 실제 쿼리 설명

### 4.1 CRUD

| 명령 | 의미 | 이 프로젝트의 예 |
| --- | --- | --- |
| `CREATE` | DB 구조나 인덱스를 생성 | `schema.sql`의 `CREATE TABLE`, Q14의 `CREATE INDEX` |
| `INSERT` | 새로운 행을 추가 | `seed.sql`의 회원·프로젝트·할 일 입력 |
| `SELECT` | 데이터를 조회 | Q01~Q11, Q15 |
| `UPDATE` | 기존 행을 수정 | Q12에서 할 일을 완료 상태로 변경 |
| `DELETE` | 기존 행을 삭제 | Q13에서 프로젝트 참여자 삭제 |

Q12와 Q13은 `BEGIN TRANSACTION`으로 작업을 시작하고 결과를 `SELECT`로 확인한 뒤 `ROLLBACK`합니다. 과제에서 UPDATE와 DELETE의 동작을 보여주면서도 샘플 데이터가 사라지지 않도록 한 선택입니다.

### 4.2 WHERE, ORDER BY, LIMIT

- Q01은 `WHERE status = 'ACTIVE'`로 진행 중인 프로젝트만 걸러낸다.
- Q03은 완료되지 않았고 우선순위가 4 이상인 할 일을 찾는다.
- Q01, Q03, Q04는 `ORDER BY`로 마감일이나 우선순위를 정렬한다.
- Q04는 `LIMIT 5`로 마감일이 빠른 5개만 가져온다.

`WHERE`는 행을 필터링하고, `ORDER BY`는 결과 순서를 정하며, `LIMIT`은 결과 개수를 제한합니다.

### 4.3 INNER JOIN

INNER JOIN은 양쪽 테이블에 연결되는 행이 있는 경우만 결과에 포함합니다.

- Q05: `tasks.project_id = projects.id`로 할 일과 프로젝트 이름을 연결한다.
- Q06: `tasks.assignee_id = members.id`로 할 일과 담당 회원을 연결한다.
- Q07: `projects.owner_id = members.id`로 프로젝트와 소유자를 연결한다.

예를 들어 Q05의 할 일 1번은 `project_id = 1`이므로 프로젝트 1번인 “팀 협업 보드”와 연결됩니다.

### 4.4 LEFT JOIN

LEFT JOIN은 왼쪽 테이블의 행을 모두 유지하고, 오른쪽에 연결되는 데이터가 없으면 NULL로 채웁니다.

Q08은 모든 프로젝트를 기준으로 할 일 수를 집계합니다. 나중에 할 일이 하나도 없는 프로젝트가 생겨도 프로젝트 자체는 결과에 표시되어야 하므로 `projects LEFT JOIN tasks`를 사용했습니다.

`COUNT(t.id)`를 사용한 이유도 설명할 수 있어야 합니다. 연결된 할 일이 없으면 `t.id`가 NULL이므로 0으로 집계됩니다. 반대로 `COUNT(*)`를 사용하면 LEFT JOIN으로 만들어진 부모 행을 세어 1로 잘못 표시할 수 있습니다.

### 4.5 GROUP BY와 집계 함수

`GROUP BY`는 같은 기준의 행을 그룹으로 묶고, 집계 함수로 그룹별 요약값을 계산합니다.

- Q08: 프로젝트별 할 일 개수 - `COUNT(t.id)`
- Q09: 회원별 담당 할 일 개수 - `COUNT(t.id)`
- Q09: 회원별 완료 할 일 개수 - `SUM(CASE WHEN t.status = 'DONE' THEN 1 ELSE 0 END)`
- Q10: 프로젝트별 평균 우선순위 - `AVG(t.priority)`

Q09의 `CASE`는 완료된 행만 1로 바꾸고 나머지는 0으로 바꾼 뒤 `SUM`하는 방식입니다. 이를 통해 회원별 전체 업무량과 완료 업무량을 한 번에 볼 수 있습니다.

### 4.6 서브쿼리

서브쿼리는 하나의 SQL 안에 포함된 또 다른 SELECT입니다.

Q11의 안쪽 쿼리는 `status = 'ACTIVE'`인 프로젝트 ID 목록을 만들고, 바깥 쿼리는 그 목록에 포함되는 프로젝트의 미완료 할 일을 조회합니다.

Q15는 전체 할 일의 평균 우선순위를 먼저 구한 뒤, 그 평균보다 높은 우선순위의 할 일만 조회합니다. 실행 결과에서는 평균 3.5보다 높은 우선순위 4 또는 5인 할 일이 출력됩니다.

### 4.7 UPDATE와 DELETE

Q12는 할 일 1번의 `status`를 `DONE`으로 변경하고 완료 시각을 기록합니다. 실제 수정 전후를 확인하려면 먼저 현재 행을 조회하고, UPDATE 후 다시 조회하면 됩니다.

Q13은 `project_members`에서 프로젝트 1번과 회원 3번의 참여 관계를 삭제합니다. 프로젝트나 회원 자체를 삭제하는 것이 아니라 두 객체 사이의 참여 관계만 삭제하는 것이 핵심입니다.

### 4.8 인덱스

인덱스는 특정 조건으로 행을 자주 검색할 때 탐색 범위를 줄여 조회를 빠르게 하는 자료구조입니다. 대신 추가 저장 공간이 필요하고 INSERT, UPDATE, DELETE 시 인덱스도 갱신해야 하므로 모든 컬럼에 만들면 안 됩니다.

Q14에서는 담당자와 상태로 할 일을 자주 검색한다고 가정해 다음 복합 인덱스를 만들었습니다.

```sql
CREATE INDEX idx_tasks_assignee_status
ON tasks (assignee_id, status);
```

이후 `EXPLAIN QUERY PLAN` 결과에 `USING INDEX idx_tasks_assignee_status`가 표시되어 SQLite가 해당 인덱스를 사용했음을 확인했습니다.

## 5. SQLite 관련 설명

### 5.1 SQLite를 선택한 이유

SQLite는 별도 서버를 실행하지 않고 하나의 파일로 DB를 관리할 수 있어 설치와 실행이 간단합니다. 이번 과제는 API 서버 구현보다 테이블 설계와 SQL 작성이 목표이므로 적합했습니다.

### 5.2 `PRAGMA foreign_keys = ON`

SQLite는 연결마다 외래 키 기능을 명시적으로 활성화해야 하므로 스키마와 쿼리 파일에 `PRAGMA foreign_keys = ON`을 넣었습니다. 이 설정이 꺼져 있으면 FK를 선언해도 잘못된 참조가 허용될 수 있습니다.

### 5.3 날짜를 TEXT로 저장한 이유

SQLite는 다른 DB처럼 고정된 DATE 타입을 강제하지 않습니다. 이 프로젝트에서는 날짜를 `YYYY-MM-DD`, 일시를 `YYYY-MM-DD HH:MM:SS` 형식의 TEXT로 저장했습니다. 이 형식은 연·월·일 순서가 유지되므로 동일한 형식끼리는 문자열 정렬만으로도 시간순 정렬이 가능합니다.

### 5.4 트랜잭션과 ROLLBACK

트랜잭션은 여러 SQL 작업을 하나의 작업 단위로 묶는 기능입니다. `ROLLBACK`은 트랜잭션 시작 이후의 변경을 취소합니다. Q12와 Q13에서는 평가자가 UPDATE와 DELETE 결과를 확인할 수 있게 한 뒤 샘플 DB를 원래 상태로 되돌리기 위해 사용했습니다.

## 6. 결과물을 보며 설명할 수 있는 흐름

### 흐름 1: 회원이 프로젝트를 소유하고 할 일을 담당한다

1. `members.id = 2`인 이서연 회원이 있다.
2. `projects.owner_id = 2`인 프로젝트는 이서연이 소유한 프로젝트다.
3. `tasks.assignee_id = 2`인 할 일은 이서연에게 배정된 업무다.
4. Q06을 실행하면 할 일 ID 1, 3, 18이 이서연의 이름과 함께 조회된다.

### 흐름 2: 프로젝트별 업무량을 확인한다

1. `tasks.project_id`로 각 할 일을 프로젝트에 연결한다.
2. Q08에서 `projects`를 기준으로 `LEFT JOIN`한다.
3. `GROUP BY p.id, p.name`으로 프로젝트별 그룹을 만든다.
4. `COUNT(t.id)`로 프로젝트마다 할 일이 몇 개인지 계산한다.

### 흐름 3: 잘못된 데이터 입력을 막는다

1. `tasks.project_id = 999`처럼 존재하지 않는 프로젝트 ID를 입력한다.
2. `PRAGMA foreign_keys = ON` 상태이므로 FK 제약조건을 확인한다.
3. 참조 대상인 `projects.id = 999`가 없기 때문에 `FOREIGN KEY constraint failed`가 발생한다.

## 7. 예상 질문과 답변

### Q1. 왜 테이블을 3개가 아니라 4개로 만들었나요?

> 회원, 프로젝트, 할 일만으로도 기본 기능은 만들 수 있지만 회원과 프로젝트의 참여 관계를 표현하기 어렵습니다. 한 회원이 여러 프로젝트에 참여하고 한 프로젝트에도 여러 회원이 참여할 수 있으므로 N:M 관계를 `project_members` 연결 테이블로 분리했습니다. 이 테이블 덕분에 참여 역할과 참여 시각도 저장할 수 있습니다.

### Q2. `projects.owner_id`와 `project_members.member_id`는 중복 아닌가요?

> 둘은 의미가 다릅니다. `owner_id`는 프로젝트의 대표 소유자를 빠르게 가리키고, `project_members`는 프로젝트에 참여한 전체 회원과 각자의 역할을 관리합니다. 현재 샘플 데이터에서는 소유자도 `project_members`에 OWNER 역할로 함께 넣었습니다. 실제 서비스에서는 소유자가 참여자 목록에도 반드시 있어야 한다는 규칙을 애플리케이션 또는 추가 제약으로 보완할 수 있습니다.

### Q3. PK와 UNIQUE는 어떻게 다른가요?

> PK는 행을 대표하는 기본 식별자이고 테이블마다 기본적으로 하나의 PK를 둡니다. UNIQUE는 특정 컬럼의 중복을 막는 제약조건입니다. 이 프로젝트에서 각 `id`는 PK이고, `members.email`은 회원 이메일 중복을 막기 위한 UNIQUE입니다.

### Q4. `INNER JOIN`과 `LEFT JOIN`의 차이는 무엇인가요?

> INNER JOIN은 양쪽에 연결되는 데이터가 있는 행만 보여줍니다. LEFT JOIN은 왼쪽 테이블의 행을 모두 보존하고 연결 데이터가 없으면 NULL을 보여줍니다. 따라서 Q05처럼 연결된 할 일만 볼 때는 INNER JOIN을 쓰고, Q08처럼 할 일이 없는 프로젝트도 포함해야 할 때는 LEFT JOIN을 사용했습니다.

### Q5. Q08에서 `COUNT(*)`가 아니라 `COUNT(t.id)`를 사용한 이유는 무엇인가요?

> LEFT JOIN에서 할 일이 없는 프로젝트는 `t.id`가 NULL인 한 행으로 남습니다. `COUNT(*)`는 그 행도 세지만, `COUNT(t.id)`는 NULL을 세지 않기 때문에 할 일이 없는 프로젝트를 0건으로 정확히 표현할 수 있습니다.

### Q6. Q09의 `SUM(CASE ...)`는 무엇을 계산하나요?

> 각 할 일이 DONE이면 1, 아니면 0으로 바꾼 뒤 회원별로 합산합니다. 그래서 회원별 전체 담당 업무 수와 완료 업무 수를 동시에 계산할 수 있습니다.

### Q7. UPDATE와 DELETE를 실행하고 왜 ROLLBACK했나요?

> 과제 요구사항에 UPDATE와 DELETE가 포함되어 있어 실제 동작을 확인해야 합니다. 하지만 샘플 데이터를 계속 재실행할 수 있어야 하므로 트랜잭션 안에서 변경 결과를 확인한 뒤 ROLLBACK했습니다. 실제 서비스에서 저장해야 하는 작업이라면 COMMIT을 사용합니다.

### Q8. 인덱스는 왜 `assignee_id`, `status`에 만들었나요?

> 업무 관리 툴에서는 특정 담당자의 미완료 업무를 자주 조회할 수 있습니다. Q14처럼 두 컬럼을 함께 조건으로 검색하는 경우를 가정해 복합 인덱스를 만들었습니다. `EXPLAIN QUERY PLAN` 결과에서 해당 인덱스가 사용되는지 확인했습니다. 다만 인덱스는 저장 공간과 쓰기 비용이 있으므로 자주 검색되는 조건에 선별적으로 적용해야 합니다.

### Q9. 비밀번호를 왜 `password_hash`로 저장했나요?

> 비밀번호 원문을 그대로 저장하면 유출 시 위험하므로 원문 대신 해시 값을 저장해야 합니다. 현재 값은 SQL 실습을 위한 가짜 문자열이며 실제 회원 기능에서는 bcrypt, Argon2 같은 검증된 방식으로 해시한 값을 사용해야 합니다.

### Q10. 이 과제에서 백엔드 프레임워크를 사용하지 않은 이유는 무엇인가요?

> 과제의 핵심 목표가 API나 화면 개발이 아니라 데이터 모델링과 SQL이기 때문입니다. 그래서 Spring, Django, Express 같은 프레임워크 없이 SQLite CLI에서 스키마 생성, 데이터 입력, 조회, 수정, 삭제를 직접 실행했습니다.

## 8. 평가 전에 직접 실행할 명령

```bash
cd submissions/5-1

sqlite3 project-management.sqlite3 < schema.sql
sqlite3 project-management.sqlite3 < seed.sql
sqlite3 -header -box project-management.sqlite3 < queries.sql
```

실행 결과는 `results/query-results.txt`와 비교합니다. Q12와 Q13이 ROLLBACK을 사용하므로 같은 DB에서 쿼리를 반복 실행해도 샘플 데이터가 중복되거나 사라지지 않습니다.

## 9. 평가 직전 체크리스트

- [ ] 왜 SQLite를 선택했는지 설명할 수 있다.
- [ ] 네 테이블의 역할을 한 문장씩 설명할 수 있다.
- [ ] 각 PK와 FK의 참조 방향을 설명할 수 있다.
- [ ] 1:N과 N:M 관계의 차이를 설명할 수 있다.
- [ ] `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`의 역할을 설명할 수 있다.
- [ ] 부모 테이블부터 데이터를 입력한 이유를 설명할 수 있다.
- [ ] Q05~Q08의 JOIN 차이를 설명할 수 있다.
- [ ] Q08에서 `COUNT(t.id)`를 사용한 이유를 설명할 수 있다.
- [ ] Q09의 `SUM(CASE ...)`와 Q10의 `AVG`를 설명할 수 있다.
- [ ] Q11과 Q15의 서브쿼리 동작을 설명할 수 있다.
- [ ] Q12, Q13의 트랜잭션과 ROLLBACK을 설명할 수 있다.
- [ ] Q14에서 인덱스를 만든 이유와 `EXPLAIN QUERY PLAN` 결과를 설명할 수 있다.
- [ ] 실제 실행 명령과 결과 파일 위치를 알고 있다.

## 10. 현재 결과물의 한계와 개선 방향

평가에서 한계까지 솔직하게 설명하면 설계 의도를 더 잘 보여줄 수 있다.

- 현재는 SQL 실습 결과물이므로 회원가입·로그인 API나 권한 검증 로직은 구현하지 않았다.
- `password_hash`는 실습용 문자열이므로 실제 서비스에서는 안전한 비밀번호 해시 알고리즘을 적용해야 한다.
- 현재 스키마만으로는 프로젝트 소유자가 반드시 `project_members`에 OWNER로 존재해야 한다는 규칙까지 강제하지 않는다. 이 규칙은 애플리케이션 로직이나 별도 검증 쿼리로 보완할 수 있다.
- SQLite의 TEXT 날짜는 ISO 형식으로 저장한다는 규칙을 지켜야 문자열 정렬이 날짜 정렬과 일치한다.
- 사용자가 많아지고 동시 쓰기가 많아지면 PostgreSQL이나 MySQL로 이전하고, 인증·권한·마이그레이션 계층을 추가할 수 있다.
