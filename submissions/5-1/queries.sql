-- 프로젝트 관리 툴 핵심 SQL 쿼리
-- 실행 전 schema.sql과 seed.sql을 순서대로 실행한다.
-- SQLite 기준이며, Q12와 Q13은 결과 확인 후 ROLLBACK하여 샘플 데이터를 보존한다.

PRAGMA foreign_keys = ON;

-- Q01. 진행 중인 프로젝트만 조회한다.
SELECT id, name, status, due_date
FROM projects
WHERE status = 'ACTIVE'
ORDER BY due_date ASC;

-- Q02. 이름에 '지'가 포함된 회원을 이름순으로 조회한다.
SELECT id, name, email
FROM members
WHERE name LIKE '%지%'
ORDER BY name ASC;

-- Q03. 우선순위가 높은 미완료 할 일을 마감일순으로 조회한다.
SELECT id, title, status, priority, due_date
FROM tasks
WHERE status <> 'DONE' AND priority >= 4
ORDER BY due_date ASC;

-- Q04. 전체 할 일 중 가장 최근 마감일이 빠른 5개를 조회한다.
SELECT id, title, status, priority, due_date
FROM tasks
ORDER BY due_date ASC, priority DESC
LIMIT 5;

-- Q05. 할 일과 소속 프로젝트를 함께 조회한다. (INNER JOIN)
SELECT
    t.id AS task_id,
    t.title AS task_title,
    p.name AS project_name,
    t.status,
    t.due_date
FROM tasks AS t
INNER JOIN projects AS p ON p.id = t.project_id
ORDER BY p.id, t.id;

-- Q06. 할 일과 담당 회원을 함께 조회한다. (INNER JOIN)
SELECT
    t.id AS task_id,
    t.title AS task_title,
    m.name AS assignee_name,
    m.email AS assignee_email,
    t.status
FROM tasks AS t
INNER JOIN members AS m ON m.id = t.assignee_id
ORDER BY m.id, t.id;

-- Q07. 프로젝트와 소유자 정보를 함께 조회한다. (INNER JOIN)
SELECT
    p.id AS project_id,
    p.name AS project_name,
    m.name AS owner_name,
    p.status,
    p.due_date
FROM projects AS p
INNER JOIN members AS m ON m.id = p.owner_id
ORDER BY p.due_date ASC;

-- Q08. 할 일이 없는 프로젝트도 포함하여 프로젝트별 할 일 수를 집계한다. (LEFT JOIN, COUNT, GROUP BY)
SELECT
    p.id AS project_id,
    p.name AS project_name,
    COUNT(t.id) AS task_count
FROM projects AS p
LEFT JOIN tasks AS t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY task_count DESC, p.id ASC;

-- Q09. 회원별 담당 할 일 수와 완료한 할 일 수를 집계한다. (COUNT, SUM, GROUP BY)
SELECT
    m.id AS member_id,
    m.name,
    COUNT(t.id) AS assigned_task_count,
    SUM(CASE WHEN t.status = 'DONE' THEN 1 ELSE 0 END) AS completed_task_count
FROM members AS m
LEFT JOIN tasks AS t ON t.assignee_id = m.id
GROUP BY m.id, m.name
ORDER BY assigned_task_count DESC, m.id ASC;

-- Q10. 프로젝트별 할 일의 평균 우선순위를 계산한다. (AVG, GROUP BY)
SELECT
    p.id AS project_id,
    p.name AS project_name,
    ROUND(AVG(t.priority), 2) AS average_priority
FROM projects AS p
INNER JOIN tasks AS t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY average_priority DESC, p.id ASC;

-- Q11. ACTIVE 프로젝트에 속한 미완료 할 일을 서브쿼리로 조회한다. (SUBQUERY)
SELECT id, project_id, title, status, due_date
FROM tasks
WHERE status <> 'DONE'
  AND project_id IN (
      SELECT id
      FROM projects
      WHERE status = 'ACTIVE'
  )
ORDER BY due_date ASC;

-- Q12. 특정 할 일을 완료 상태로 수정하고 결과를 확인한다. (UPDATE)
-- 샘플 데이터가 계속 재사용되도록 확인 후 ROLLBACK한다.
BEGIN TRANSACTION;

UPDATE tasks
SET status = 'DONE',
    completed_at = '2026-08-11 18:00:00'
WHERE id = 1 AND status <> 'DONE';

SELECT id, title, status, completed_at
FROM tasks
WHERE id = 1;

ROLLBACK;

-- Q13. 프로젝트 참여자를 삭제하고 결과를 확인한다. (DELETE)
-- 샘플 데이터가 계속 재사용되도록 확인 후 ROLLBACK한다.
BEGIN TRANSACTION;

DELETE FROM project_members
WHERE project_id = 1 AND member_id = 3;

SELECT project_id, member_id, role
FROM project_members
WHERE project_id = 1
ORDER BY member_id;

ROLLBACK;

-- Q14. 담당자와 상태로 자주 검색하는 할 일 조회를 위해 인덱스를 만든다.
-- assignee_id와 status를 함께 사용하는 검색 조건의 조회 성능 향상을 위한 인덱스다.
CREATE INDEX IF NOT EXISTS idx_tasks_assignee_status
ON tasks (assignee_id, status);

EXPLAIN QUERY PLAN
SELECT id, title, due_date
FROM tasks
WHERE assignee_id = 10 AND status = 'TODO';

-- Q15. 평균 우선순위보다 높은 우선순위의 할 일을 조회한다. (집계 서브쿼리)
SELECT id, title, priority, status
FROM tasks
WHERE priority > (
    SELECT AVG(priority)
    FROM tasks
)
ORDER BY priority DESC, id ASC;
