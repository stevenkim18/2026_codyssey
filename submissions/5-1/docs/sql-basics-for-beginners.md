# SQL 기초를 처음 배우는 사람을 위한 설명서

이 문서는 SQL을 처음 보는 사람도 프로젝트 관리 툴의 쿼리를 읽고 설명할 수 있도록 만든 자료다.

SQL은 데이터베이스에게 질문하거나 부탁하는 언어라고 생각하면 된다.

- “진행 중인 프로젝트를 보여줘.”
- “이 할 일은 누구에게 담당되어 있어?”
- “프로젝트별로 할 일이 몇 개야?”
- “이 조건으로 자주 찾으니 더 빨리 찾을 수 있게 해줘.”

이 문서의 예시는 현재 프로젝트의 다음 테이블을 기준으로 한다.

- members: 회원
- projects: 프로젝트
- tasks: 할 일
- project_members: 프로젝트 참여 회원

## 1. SQL 문장은 긴 문장이 아니라 주문서다

SQL을 식당 주문서처럼 생각해 보자.

~~~sql
SELECT name, email
FROM members
WHERE name = '이서연'
ORDER BY name ASC
LIMIT 1;
~~~

위 문장을 우리말로 읽으면 다음과 같다.

> members 테이블에서 이름과 이메일을 가져오되, 이름이 이서연인 사람만 골라서 이름순으로 정렬하고 1명만 보여줘.

각 줄의 역할은 다음과 같다.

| SQL | 쉬운 뜻 |
| --- | --- |
| SELECT | 무엇을 보여줄까? |
| FROM | 어느 테이블에서 찾을까? |
| WHERE | 어떤 조건의 행만 고를까? |
| ORDER BY | 어떤 순서로 줄을 세울까? |
| LIMIT | 몇 개까지만 보여줄까? |

SQL을 작성할 때는 보통 다음 순서로 생각한다.

1. 어떤 테이블에서 찾을지 정한다.
2. 어떤 조건으로 고를지 정한다.
3. 어떤 열을 보여줄지 정한다.
4. 어떤 순서로 정렬할지 정한다.
5. 결과를 몇 개로 제한할지 정한다.

SQL 문장의 기본 끝에는 세미콜론을 붙인다.

~~~sql
SELECT name
FROM members;
~~~

### 1.1 별표와 열 이름

~~~sql
SELECT *
FROM members;
~~~

별표는 모든 열을 보여 달라는 뜻이다. 연습할 때는 편하지만, 실제 서비스에서는 필요한 열만 적는 편이 좋다. 불필요한 데이터를 가져오지 않아도 되고, 쿼리의 의도도 더 잘 드러난다.

~~~sql
SELECT id, name, email
FROM members;
~~~

이 쿼리는 회원의 ID, 이름, 이메일만 보여 준다.

### 1.2 문자열과 숫자

문자열은 작은따옴표로 감싼다.

~~~sql
WHERE status = 'ACTIVE'
WHERE name = '이서연'
~~~

숫자는 보통 따옴표 없이 쓴다.

~~~sql
WHERE priority >= 4
WHERE id = 2
~~~

문자열인 ACTIVE를 따옴표 없이 쓰면 SQL은 ACTIVE를 열 이름으로 오해할 수 있다.

### 1.3 조건 연결하기

AND는 조건을 모두 만족해야 한다.

~~~sql
SELECT id, title, priority
FROM tasks
WHERE status <> 'DONE'
  AND priority >= 4;
~~~

뜻은 다음과 같다.

> 완료되지 않았고, 우선순위가 4 이상인 할 일을 찾아줘.

OR는 여러 조건 중 하나만 만족해도 된다.

~~~sql
SELECT id, name
FROM projects
WHERE status = 'ACTIVE'
   OR status = 'PLANNING';
~~~

IN은 여러 값 중 하나인지 확인할 때 편하다.

~~~sql
WHERE status IN ('TODO', 'IN_PROGRESS')
~~~

### 1.4 LIKE로 검색하기

LIKE는 글자 일부를 찾을 때 사용한다.

~~~sql
SELECT id, name, email
FROM members
WHERE name LIKE '%지%';
~~~

퍼센트 기호는 “앞이나 뒤에 어떤 글자가 더 있어도 된다”는 뜻이다.

- '%지%': 어디에든 지가 포함됨
- '지%': 지로 시작함
- '%지': 지로 끝남

현재 프로젝트의 Q02는 이름에 지가 포함된 회원을 찾는 쿼리다.

### 1.5 NULL은 빈 문자열이 아니다

NULL은 “값이 없음”을 뜻한다. 빈 문자열이나 숫자 0과 다르다.

잘못된 방법:

~~~sql
WHERE completed_at = NULL
~~~

NULL인지 확인할 때는 IS NULL을 사용한다.

~~~sql
SELECT id, title
FROM tasks
WHERE completed_at IS NULL;
~~~

값이 있는 행은 IS NOT NULL로 찾는다.

~~~sql
SELECT id, title
FROM tasks
WHERE completed_at IS NOT NULL;
~~~

## 2. SELECT, INSERT, UPDATE, DELETE

이 네 가지는 데이터베이스에서 가장 기본적인 동작이다. 냉장고에 비유하면 다음과 같다.

| SQL | 냉장고 비유 | 실제 뜻 |
| --- | --- | --- |
| SELECT | 냉장고를 열어 확인하기 | 데이터 조회 |
| INSERT | 새 음식을 넣기 | 데이터 추가 |
| UPDATE | 음식의 라벨을 바꾸기 | 데이터 수정 |
| DELETE | 음식을 버리기 | 데이터 삭제 |

### 2.1 SELECT: 읽기

~~~sql
SELECT id, name, status, due_date
FROM projects
WHERE status = 'ACTIVE'
ORDER BY due_date ASC;
~~~

현재 프로젝트의 Q01이다. ACTIVE 프로젝트만 골라 마감일이 빠른 순서로 보여 준다.

### 2.2 INSERT: 추가하기

~~~sql
INSERT INTO members (name, email, password_hash)
VALUES ('새 회원', 'new@example.com', 'demo_hash');
~~~

새 회원 한 명을 추가한다.

INSERT할 때 주의할 점은 두 가지다.

1. 컬럼 순서와 VALUES 값의 순서를 맞춘다.
2. FK가 있는 테이블은 부모 데이터부터 넣는다.

현재 프로젝트의 입력 순서는 다음과 같다.

~~~text
members → projects → tasks → project_members
~~~

tasks에는 project_id와 assignee_id가 있기 때문에, 참조하는 프로젝트와 회원이 먼저 존재해야 한다.

### 2.3 UPDATE: 수정하기

~~~sql
UPDATE tasks
SET status = 'DONE',
    completed_at = '2026-08-11 18:00:00'
WHERE id = 1;
~~~

1번 할 일을 완료 상태로 바꾼다.

UPDATE에서 가장 위험한 실수는 WHERE를 빼먹는 것이다.

~~~sql
UPDATE tasks
SET status = 'DONE';
~~~

이렇게 실행하면 모든 할 일이 완료 상태가 될 수 있다. 따라서 UPDATE 전에는 같은 조건으로 SELECT를 먼저 실행하는 습관이 좋다.

~~~sql
SELECT id, title, status
FROM tasks
WHERE id = 1;
~~~

현재 프로젝트의 Q12는 UPDATE를 실행하고 결과를 확인한 뒤 ROLLBACK한다.

### 2.4 DELETE: 삭제하기

~~~sql
DELETE FROM project_members
WHERE project_id = 1
  AND member_id = 3;
~~~

1번 프로젝트에서 3번 회원의 참여 관계만 삭제한다.

DELETE도 WHERE를 빼먹으면 매우 위험하다.

~~~sql
DELETE FROM tasks;
~~~

위 쿼리는 모든 할 일을 삭제한다. 평가나 실습에서는 삭제 전에 SELECT로 삭제 대상이 맞는지 확인해야 한다.

### 2.5 트랜잭션과 ROLLBACK

현재 Q12와 Q13은 다음처럼 작성되어 있다.

~~~sql
BEGIN TRANSACTION;

UPDATE tasks
SET status = 'DONE'
WHERE id = 1;

SELECT id, title, status
FROM tasks
WHERE id = 1;

ROLLBACK;
~~~

BEGIN TRANSACTION은 “지금부터 하나의 작업 묶음으로 처리하자”는 뜻이다.

ROLLBACK은 “이 작업 묶음을 취소하고 원래 상태로 돌아가자”는 뜻이다.

과제에서는 UPDATE와 DELETE가 실행되는 것을 보여주면서 샘플 데이터를 계속 사용할 수 있도록 ROLLBACK을 사용했다. 실제 서비스에서 변경을 확정하려면 COMMIT을 사용한다.

## 3. JOIN은 서로 다른 표를 붙이는 기능이다

### 3.1 JOIN을 우편함에 비유하기

회원 표와 할 일 표가 따로 있다고 생각해 보자.

members:

| id | name |
| --- | --- |
| 1 | 김민준 |
| 2 | 이서연 |
| 3 | 박지훈 |

tasks:

| id | assignee_id | title |
| --- | --- | --- |
| 101 | 1 | 요구사항 정리 |
| 102 | 2 | 화면 설계 |
| 103 | 1 | 테스트 작성 |

tasks에는 담당자의 이름이 없고 assignee_id만 있다. members에는 이름이 있지만 어떤 할 일을 맡았는지 모른다.

두 표의 공통 번호인 다음 값을 이용하면 붙일 수 있다.

~~~text
tasks.assignee_id = members.id
~~~

이렇게 번호가 같은 행을 찾아서 한 줄로 보여 주는 것이 JOIN이다.

### 3.2 JOIN의 기본 모양

~~~sql
SELECT
    tasks.title,
    members.name
FROM tasks
INNER JOIN members
    ON members.id = tasks.assignee_id;
~~~

읽는 방법:

> tasks에서 할 일 제목을 가져오고, members에서 담당자 이름을 가져와. 두 테이블에서 members.id와 tasks.assignee_id가 같은 행끼리 연결해.

ON은 “어떤 열끼리 연결할지”를 알려 주는 부분이다.

### 3.3 별명 AS 사용하기

테이블 이름이 길거나 여러 번 나오면 AS로 별명을 붙인다.

~~~sql
SELECT
    t.title,
    m.name AS assignee_name
FROM tasks AS t
INNER JOIN members AS m
    ON m.id = t.assignee_id;
~~~

이제 t는 tasks, m은 members를 뜻한다.

AS는 결과 열에 읽기 쉬운 이름을 붙일 때도 쓸 수 있다.

~~~sql
m.name AS assignee_name
~~~

결과 열 이름이 name 대신 assignee_name으로 표시된다.

## 4. INNER JOIN: 양쪽에 모두 있는 것만 가져오기

### 4.1 아주 쉬운 비유

반 친구 명단과 급식 신청 명단이 있다고 하자.

- INNER JOIN: 두 명단에 모두 있는 친구만 보여 준다.
- 한 명단에만 있는 친구는 빠진다.

즉, “연결 상대가 반드시 있는 데이터만 보고 싶다”면 INNER JOIN을 사용한다.

### 4.2 프로젝트의 Q05

~~~sql
SELECT
    t.id AS task_id,
    t.title AS task_title,
    p.name AS project_name,
    t.status,
    t.due_date
FROM tasks AS t
INNER JOIN projects AS p
    ON p.id = t.project_id
ORDER BY p.id, t.id;
~~~

tasks의 project_id와 projects의 id가 같은 행을 연결한다.

할 일 1번을 예로 들면:

~~~text
tasks.id = 1
tasks.project_id = 1
projects.id = 1
projects.name = 팀 협업 보드
~~~

따라서 결과에는 다음처럼 나온다.

~~~text
요구사항 정리 | 팀 협업 보드
~~~

### 4.3 담당자 이름 가져오기: Q06

~~~sql
SELECT
    t.id AS task_id,
    t.title AS task_title,
    m.name AS assignee_name
FROM tasks AS t
INNER JOIN members AS m
    ON m.id = t.assignee_id
ORDER BY m.id, t.id;
~~~

tasks에는 담당자 번호만 있으므로, 회원 이름을 보여 주려면 members와 연결해야 한다.

할 일 1번의 assignee_id가 2라면:

~~~text
tasks.assignee_id = 2
members.id = 2
members.name = 이서연
~~~

결과는 “요구사항 정리 - 이서연”처럼 읽을 수 있다.

### 4.4 INNER JOIN을 언제 쓰는가

- 담당 회원이 반드시 존재하는 할 일만 보고 싶을 때
- 프로젝트 정보가 연결된 할 일만 보고 싶을 때
- 연결이 끊긴 잘못된 데이터를 숨기고 정상적인 연결만 확인할 때

현재 스키마는 FK로 잘못된 연결을 막기 때문에 Q05~Q07의 INNER JOIN 결과가 안정적으로 나온다.

## 5. LEFT JOIN: 왼쪽 표는 전부 보여 주기

### 5.1 아주 쉬운 비유

선생님이 반 전체 명단을 가지고 있고, 숙제를 제출한 학생 명단과 비교한다고 하자.

- INNER JOIN: 숙제를 제출한 학생만 보여 준다.
- LEFT JOIN: 반 전체를 보여 주고, 숙제를 안 낸 학생은 제출 칸을 비워 둔다.

LEFT JOIN에서는 FROM 뒤에 먼저 쓴 테이블이 왼쪽이다.

~~~sql
FROM projects AS p
LEFT JOIN tasks AS t
    ON t.project_id = p.id
~~~

이 경우 projects가 왼쪽이다. 따라서 할 일이 하나도 없는 프로젝트도 결과에 남는다.

### 5.2 작은 예시

projects:

| id | name |
| --- | --- |
| 1 | 앱 만들기 |
| 2 | 책 읽기 |
| 3 | 운동하기 |

tasks:

| id | project_id | title |
| --- | --- | --- |
| 101 | 1 | 화면 만들기 |
| 102 | 1 | 버튼 만들기 |
| 103 | 2 | 1장 읽기 |

프로젝트 3번은 할 일이 없다.

INNER JOIN 결과:

| project_name | task_title |
| --- | --- |
| 앱 만들기 | 화면 만들기 |
| 앱 만들기 | 버튼 만들기 |
| 책 읽기 | 1장 읽기 |

LEFT JOIN 결과:

| project_name | task_title |
| --- | --- |
| 앱 만들기 | 화면 만들기 |
| 앱 만들기 | 버튼 만들기 |
| 책 읽기 | 1장 읽기 |
| 운동하기 | NULL |

운동하기 프로젝트도 살아 있는 것이 핵심이다.

### 5.3 프로젝트의 Q08

~~~sql
SELECT
    p.id AS project_id,
    p.name AS project_name,
    COUNT(t.id) AS task_count
FROM projects AS p
LEFT JOIN tasks AS t
    ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY task_count DESC, p.id ASC;
~~~

이 쿼리는 “모든 프로젝트별 할 일 개수”를 구한다.

- projects를 왼쪽에 둔다.
- tasks를 project_id로 붙인다.
- 프로젝트별로 묶는다.
- 연결된 할 일 ID를 센다.
- 할 일이 없는 프로젝트도 0개로 보여 줄 수 있다.

### 5.4 왜 COUNT(*)가 아니라 COUNT(t.id)인가

할 일이 없는 프로젝트가 있다고 하자.

LEFT JOIN 결과는 내부적으로 대략 이렇게 생긴다.

| p.name | t.id |
| --- | --- |
| 운동하기 | NULL |

COUNT는 NULL을 세지 않는다.

~~~sql
COUNT(t.id)
~~~

그러므로 결과가 0이 된다.

반대로 다음은 LEFT JOIN으로 만들어진 행 자체를 셀 수 있다.

~~~sql
COUNT(*)
~~~

그래서 “연결된 할 일의 실제 개수”를 구할 때는 COUNT(t.id)가 안전하다.

### 5.5 LEFT JOIN에서 WHERE를 조심하기

다음 쿼리를 보자.

~~~sql
SELECT p.name, t.title
FROM projects AS p
LEFT JOIN tasks AS t
    ON t.project_id = p.id
WHERE t.status = 'TODO';
~~~

WHERE에서 오른쪽 테이블인 t의 조건을 걸면, t가 NULL인 프로젝트가 WHERE에서 탈락한다. 그러면 결과적으로 할 일이 있는 프로젝트만 남아 INNER JOIN처럼 보일 수 있다.

왼쪽 프로젝트를 모두 유지하면서 연결 조건을 제한하고 싶다면 조건을 ON 안에 넣는다.

~~~sql
SELECT p.name, t.title
FROM projects AS p
LEFT JOIN tasks AS t
    ON t.project_id = p.id
   AND t.status = 'TODO';
~~~

초보자가 LEFT JOIN에서 가장 많이 하는 실수 중 하나다.

## 6. GROUP BY: 같은 종류끼리 상자에 담기

### 6.1 GROUP BY를 상자에 비유하기

할 일을 프로젝트별 상자에 담는다고 생각하자.

~~~text
1번 프로젝트 상자: 할 일 2개
2번 프로젝트 상자: 할 일 2개
3번 프로젝트 상자: 할 일 2개
...
~~~

GROUP BY는 같은 project_id를 가진 할 일을 같은 상자에 넣는 역할이다.

~~~sql
SELECT project_id, COUNT(id)
FROM tasks
GROUP BY project_id;
~~~

이 결과는 “각 프로젝트 상자에 할 일이 몇 개 들어 있는가”를 알려 준다.

### 6.2 집계 함수

| 함수 | 어린이식 설명 | 예 |
| --- | --- | --- |
| COUNT | 몇 개인지 세기 | 할 일 개수 |
| SUM | 숫자를 모두 더하기 | 완료 여부를 1과 0으로 바꾼 합 |
| AVG | 평균 내기 | 평균 우선순위 |
| MAX | 가장 큰 값 찾기 | 가장 높은 우선순위 |
| MIN | 가장 작은 값 찾기 | 가장 빠른 마감일 |

### 6.3 Q09: 회원별 업무량

~~~sql
SELECT
    m.id AS member_id,
    m.name,
    COUNT(t.id) AS assigned_task_count,
    SUM(CASE WHEN t.status = 'DONE' THEN 1 ELSE 0 END)
        AS completed_task_count
FROM members AS m
LEFT JOIN tasks AS t
    ON t.assignee_id = m.id
GROUP BY m.id, m.name
ORDER BY assigned_task_count DESC;
~~~

이 쿼리를 말로 읽으면 다음과 같다.

> 모든 회원을 기준으로 담당 할 일을 붙이고, 회원별로 상자를 나눈 뒤, 담당 업무 수와 완료 업무 수를 세어 줘.

CASE는 작은 판정문이다.

~~~text
할 일 상태가 DONE이면 1
그 외에는 0
~~~

예를 들어 이서연에게 할 일이 세 개 있고 그중 두 개가 DONE이면:

~~~text
COUNT = 3
SUM = 1 + 1 + 0 = 2
~~~

결과는 담당 업무 3개, 완료 업무 2개가 된다.

### 6.4 Q10: 프로젝트별 평균 우선순위

~~~sql
SELECT
    p.id AS project_id,
    p.name AS project_name,
    ROUND(AVG(t.priority), 2) AS average_priority
FROM projects AS p
INNER JOIN tasks AS t
    ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY average_priority DESC;
~~~

프로젝트별로 할 일을 묶은 뒤 priority의 평균을 구한다.

예를 들어 어떤 프로젝트의 우선순위가 5와 3이면:

~~~text
(5 + 3) / 2 = 4
~~~

ROUND는 평균 결과를 보기 좋게 반올림하는 함수다.

### 6.5 GROUP BY에 컬럼을 적는 이유

다음처럼 프로젝트 이름만 SELECT하고 id로 GROUP BY할 수 있다.

~~~sql
SELECT p.name, COUNT(t.id)
FROM projects AS p
LEFT JOIN tasks AS t ON t.project_id = p.id
GROUP BY p.id, p.name;
~~~

프로젝트 ID와 이름을 함께 GROUP BY한 이유는 한 프로젝트를 정확하게 하나의 그룹으로 만들기 위해서다.

집계 함수가 아닌 일반 컬럼을 SELECT할 때는 그 컬럼도 GROUP BY 기준에 포함하는 습관을 들이면 안전하다.

### 6.6 WHERE와 HAVING의 차이

WHERE는 상자에 담기 전에 하나하나 검사한다.

~~~sql
WHERE status <> 'DONE'
~~~

HAVING은 상자에 담고 개수를 센 뒤 상자 자체를 검사한다.

~~~sql
HAVING COUNT(t.id) >= 2
~~~

예를 들어 할 일이 2개 이상인 프로젝트만 찾는다.

~~~sql
SELECT p.name, COUNT(t.id) AS task_count
FROM projects AS p
LEFT JOIN tasks AS t ON t.project_id = p.id
GROUP BY p.id, p.name
HAVING COUNT(t.id) >= 2;
~~~

## 7. 검색, 정렬, 집계, 랭킹

실무 요구를 SQL로 바꿀 때는 다음 네 가지 질문을 순서대로 생각한다.

1. 어떤 테이블에서 찾을까?
2. 어떤 조건으로 골라낼까?
3. 어떤 단위로 묶을까?
4. 어떤 순서로 보여 줄까?

### 7.1 검색

이름에 지가 들어간 회원을 찾는 Q02다.

~~~sql
SELECT id, name, email
FROM members
WHERE name LIKE '%지%'
ORDER BY name ASC;
~~~

WHERE로 조건을 걸고 LIKE로 일부 글자를 검색한다.

### 7.2 정렬

마감일이 빠른 업무부터 보여 주려면 다음처럼 쓴다.

~~~sql
ORDER BY due_date ASC
~~~

- ASC: 오름차순. 작은 값이나 빠른 날짜부터
- DESC: 내림차순. 큰 값이나 늦은 날짜부터

같은 마감일 안에서 우선순위가 높은 업무를 먼저 보려면 정렬 기준을 두 개 적는다.

~~~sql
ORDER BY due_date ASC, priority DESC;
~~~

### 7.3 상위 N개

가장 빨리 끝내야 할 업무 5개만 보고 싶다면 LIMIT을 사용한다.

~~~sql
SELECT id, title, priority, due_date
FROM tasks
ORDER BY due_date ASC, priority DESC
LIMIT 5;
~~~

ORDER BY 없이 LIMIT만 쓰면 어떤 5개가 나올지 일정하지 않을 수 있다. “상위 5개”에는 무엇을 기준으로 위에 둘지 정하는 ORDER BY가 함께 필요하다.

### 7.4 집계

프로젝트별 업무 개수는 COUNT와 GROUP BY로 구한다.

~~~sql
SELECT project_id, COUNT(id) AS task_count
FROM tasks
GROUP BY project_id
ORDER BY task_count DESC;
~~~

업무량이 많은 순서로 프로젝트를 정렬했으므로 이것도 간단한 랭킹이다.

### 7.5 순위 번호 붙이기

순위 숫자까지 표시하려면 SQLite의 RANK를 사용할 수 있다.

~~~sql
SELECT
    p.name,
    COUNT(t.id) AS task_count,
    RANK() OVER (ORDER BY COUNT(t.id) DESC) AS task_rank
FROM projects AS p
LEFT JOIN tasks AS t
    ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY task_rank, p.id;
~~~

COUNT가 큰 프로젝트부터 1등, 2등처럼 번호를 붙인다.

- RANK: 동점이면 같은 순위, 다음 순위에 빈 번호가 생길 수 있음
- DENSE_RANK: 동점이어도 다음 순위를 빠짐없이 붙임
- ROW_NUMBER: 동점이어도 각 행에 서로 다른 번호를 붙임

현재 제출한 Q08은 task_count를 계산하고 정렬하는 쿼리이고, 위 RANK 예시는 랭킹을 확장하는 학습용 예시다.

## 8. 인덱스: 책 뒤의 찾아보기

### 8.1 인덱스 비유

두꺼운 책에서 “고양이”라는 단어를 찾는다고 하자.

- 인덱스가 없으면 책의 1쪽부터 끝까지 읽어야 한다.
- 인덱스가 있으면 책 뒤의 찾아보기에서 고양이의 페이지를 찾고 바로 이동한다.

데이터베이스 인덱스도 비슷하다. WHERE나 JOIN으로 자주 찾는 컬럼에 길을 만들어 둔다.

### 8.2 현재 프로젝트의 인덱스

Q14는 다음 인덱스를 만든다.

~~~sql
CREATE INDEX IF NOT EXISTS idx_tasks_assignee_status
ON tasks (assignee_id, status);
~~~

프로젝트 관리 툴에서 자주 할 것 같은 질문은 다음과 같다.

> 이 담당자의 TODO 업무를 보여 줘.

~~~sql
SELECT id, title, due_date
FROM tasks
WHERE assignee_id = 10
  AND status = 'TODO';
~~~

이런 검색을 빠르게 하기 위해 담당자와 상태를 함께 인덱스에 넣었다.

### 8.3 EXPLAIN QUERY PLAN

인덱스를 만들었다고 실제로 사용하는 것은 아니다. SQLite가 어떤 방법으로 검색하는지 확인할 수 있다.

~~~sql
EXPLAIN QUERY PLAN
SELECT id, title, due_date
FROM tasks
WHERE assignee_id = 10
  AND status = 'TODO';
~~~

결과에 다음처럼 보인다.

~~~text
SEARCH tasks USING INDEX idx_tasks_assignee_status
~~~

뜻은 다음과 같다.

> tasks 테이블을 찾을 때 idx_tasks_assignee_status 인덱스를 사용했다.

### 8.4 어떤 컬럼이 인덱스 후보인가

다음처럼 자주 쓰는 컬럼이 후보가 된다.

- WHERE에서 자주 검색하는 컬럼
- JOIN의 ON에서 자주 연결하는 컬럼
- ORDER BY에서 자주 정렬하는 컬럼
- 이메일처럼 특정 값을 빠르게 찾는 컬럼
- 데이터가 많고 검색 결과를 많이 줄여 주는 컬럼

예를 들어 이메일로 회원을 찾는다면 email이 좋은 후보가 된다.

~~~sql
SELECT id, name
FROM members
WHERE email = 'seoyeon@example.com';
~~~

현재 schema.sql에서 email에 UNIQUE를 적용했기 때문에 중복 방지와 빠른 검색에 사용할 구조가 마련되어 있다.

### 8.5 인덱스를 모든 컬럼에 만들면 안 되는 이유

인덱스는 공짜가 아니다.

- 인덱스도 저장 공간을 사용한다.
- INSERT할 때 인덱스도 함께 갱신해야 한다.
- UPDATE나 DELETE 때도 인덱스를 수정해야 한다.
- 데이터가 아주 적으면 인덱스보다 전체를 읽는 것이 빠를 수 있다.

그래서 “자주 검색되고, 인덱스를 이용하면 많이 줄어드는 컬럼”에만 만든다.

### 8.6 복합 인덱스의 순서

idx_tasks_assignee_status는 두 컬럼을 이 순서로 만든다.

~~~text
assignee_id → status
~~~

따라서 다음 검색에 특히 잘 맞는다.

~~~sql
WHERE assignee_id = 10
  AND status = 'TODO'
~~~

또는 첫 번째 컬럼만 사용하는 다음 검색에도 활용될 수 있다.

~~~sql
WHERE assignee_id = 10
~~~

반면 두 번째 컬럼인 status만 단독으로 검색하는 경우에는 이 인덱스를 충분히 활용하지 못할 수 있다.

~~~sql
WHERE status = 'TODO'
~~~

이것을 복합 인덱스의 왼쪽부터 사용한다는 의미로 이해하면 된다.

## 9. 현재 프로젝트의 쿼리와 개념 연결

| 쿼리 | 사용 개념 | 한 문장 설명 |
| --- | --- | --- |
| Q01 | WHERE, ORDER BY | ACTIVE 프로젝트를 마감일순으로 조회 |
| Q02 | LIKE, ORDER BY | 이름에 특정 글자가 들어간 회원 검색 |
| Q03 | WHERE, AND, ORDER BY | 높은 우선순위의 미완료 업무 조회 |
| Q04 | ORDER BY, LIMIT | 마감일이 빠른 5개 업무 조회 |
| Q05 | INNER JOIN | 할 일과 프로젝트 연결 |
| Q06 | INNER JOIN | 할 일과 담당 회원 연결 |
| Q07 | INNER JOIN | 프로젝트와 소유자 연결 |
| Q08 | LEFT JOIN, COUNT, GROUP BY | 모든 프로젝트의 업무량 집계 |
| Q09 | LEFT JOIN, COUNT, SUM, CASE, GROUP BY | 회원별 담당·완료 업무량 집계 |
| Q10 | INNER JOIN, AVG, GROUP BY | 프로젝트별 평균 우선순위 계산 |
| Q11 | IN 서브쿼리 | ACTIVE 프로젝트의 미완료 업무 조회 |
| Q12 | UPDATE, TRANSACTION, ROLLBACK | 업무를 완료 상태로 바꾼 뒤 취소 |
| Q13 | DELETE, TRANSACTION, ROLLBACK | 프로젝트 참여 관계를 지운 뒤 취소 |
| Q14 | CREATE INDEX, EXPLAIN | 담당자·상태 검색용 인덱스 확인 |
| Q15 | AVG 서브쿼리 | 전체 평균보다 높은 우선순위 업무 조회 |

## 10. 초보자 연습 문제

### 문제 1

ACTIVE 또는 PLANNING 상태인 프로젝트의 이름과 상태를 보여 줘라.

정답:

~~~sql
SELECT name, status
FROM projects
WHERE status IN ('ACTIVE', 'PLANNING');
~~~

### 문제 2

할 일 제목과 담당자 이름을 함께 보여 줘라.

정답:

~~~sql
SELECT
    t.title,
    m.name AS assignee_name
FROM tasks AS t
INNER JOIN members AS m
    ON m.id = t.assignee_id;
~~~

### 문제 3

프로젝트별 할 일 개수를 보여 줘라.

정답:

~~~sql
SELECT
    project_id,
    COUNT(id) AS task_count
FROM tasks
GROUP BY project_id;
~~~

### 문제 4

완료되지 않은 업무 중 우선순위가 5인 업무를 마감일순으로 보여 줘라.

정답:

~~~sql
SELECT id, title, priority, due_date
FROM tasks
WHERE status <> 'DONE'
  AND priority = 5
ORDER BY due_date ASC;
~~~

### 문제 5

회원별 담당 업무 수를 보여 줘라. 담당 업무가 없는 회원도 보여 줘라.

정답:

~~~sql
SELECT
    m.name,
    COUNT(t.id) AS task_count
FROM members AS m
LEFT JOIN tasks AS t
    ON t.assignee_id = m.id
GROUP BY m.id, m.name;
~~~

여기서 회원을 모두 보여 주기 위해 LEFT JOIN을 사용하고, 실제 업무 ID만 세기 위해 COUNT(t.id)를 사용했다.

## 11. 평가에서 말할 때의 설명 순서

질문을 받으면 다음 순서로 답하면 된다.

1. 먼저 쉬운 말로 뜻을 말한다.
2. 그 다음 현재 프로젝트의 테이블이나 컬럼을 예로 든다.
3. 마지막으로 실제 Q 번호를 보여 준다.

예시: “LEFT JOIN이 뭔가요?”

> LEFT JOIN은 왼쪽 표의 데이터를 전부 유지하면서 오른쪽 표를 붙이는 방식입니다. 이 프로젝트의 Q08에서는 projects를 왼쪽에 두었기 때문에 할 일이 없는 프로젝트도 결과에 남겨야 합니다. 그래서 projects LEFT JOIN tasks를 사용했고, COUNT(t.id)로 할 일이 없는 프로젝트를 0개로 표시할 수 있게 했습니다.

예시: “인덱스가 뭔가요?”

> 인덱스는 책 뒤의 찾아보기처럼 검색할 위치를 미리 정리한 자료구조입니다. Q14에서는 담당자와 상태로 업무를 자주 검색한다고 가정해 tasks의 assignee_id와 status에 복합 인덱스를 만들었습니다. EXPLAIN QUERY PLAN 결과에서 이 인덱스를 사용하는 것도 확인했습니다.

예시: “GROUP BY가 뭔가요?”

> GROUP BY는 같은 기준의 행을 한 그룹으로 묶는 기능입니다. Q08에서는 project_id가 같은 할 일을 프로젝트별 상자에 담고 COUNT로 개수를 셉니다. 그래서 프로젝트마다 할 일이 몇 개인지 알 수 있습니다.

## 12. 평가 전 실행 방법

프로젝트 루트에서 다음 순서로 실행한다.

~~~bash
cd submissions/5-1
sqlite3 project-management.sqlite3 < schema.sql
sqlite3 project-management.sqlite3 < seed.sql
sqlite3 -header -box project-management.sqlite3 < queries.sql
~~~

실행 결과는 ../results/query-results.txt와 비교한다.

현재 샘플 데이터 행 수는 다음과 같다.

~~~text
members: 10
projects: 10
tasks: 20
project_members: 21
~~~

## 13. 평가 직전 체크리스트

- [ ] SQL 문장의 SELECT, FROM, WHERE, ORDER BY, LIMIT 역할을 설명할 수 있다.
- [ ] 데이터베이스와 엑셀의 차이를 설명할 수 있다.
- [ ] 왜 회원·프로젝트·할 일을 테이블로 나눴는지 설명할 수 있다.
- [ ] PK와 FK의 차이를 설명할 수 있다.
- [ ] 1:N과 N:M 관계를 실제 컬럼으로 설명할 수 있다.
- [ ] INNER JOIN과 LEFT JOIN의 결과 차이를 설명할 수 있다.
- [ ] Q08에서 COUNT(t.id)를 사용한 이유를 설명할 수 있다.
- [ ] GROUP BY와 COUNT, SUM, AVG를 설명할 수 있다.
- [ ] WHERE와 HAVING의 차이를 설명할 수 있다.
- [ ] SELECT, INSERT, UPDATE, DELETE의 사용 시점을 설명할 수 있다.
- [ ] 검색, 정렬, 집계, 랭킹 문제를 SQL로 바꾸는 순서를 설명할 수 있다.
- [ ] 인덱스의 장점과 비용을 설명할 수 있다.
- [ ] 복합 인덱스의 컬럼 순서가 중요한 이유를 설명할 수 있다.
- [ ] Q05, Q08, Q09, Q10, Q14를 실제 파일에서 찾아 설명할 수 있다.
- [ ] UPDATE와 DELETE에 WHERE가 필요한 이유를 설명할 수 있다.
- [ ] SQLite에서 PRAGMA foreign_keys = ON이 필요한 이유를 설명할 수 있다.

