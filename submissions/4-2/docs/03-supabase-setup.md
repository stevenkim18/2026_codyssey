# Supabase 설정과 구현 작업 가이드

이 문서는 TaskFlow에 Supabase를 연결하기 위해 필요한 설정과 구현 순서를 정리한 문서입니다.

현재 TaskFlow는 다음 상태입니다.

- React + TypeScript + Vite 설정 완료
- Tailwind CSS 설정 완료
- React Router 설정 완료
- 화면과 라우트 뼈대 구성 완료
- Supabase 클라이언트 연결 완료
- 인증과 실제 CRUD 구현 완료

이번 단계의 목표는 다음과 같습니다.

    회원가입
      ↓
    로그인
      ↓
    현재 사용자 확인
      ↓
    사용자별 프로젝트 조회
      ↓
    프로젝트별 할 일 CRUD

## 1. Supabase를 사용하는 이유

TaskFlow에서는 프로젝트와 할 일을 브라우저의 임시 배열이 아닌 원격 데이터베이스에 저장해야 합니다.

Supabase를 사용하면 다음 기능을 이용할 수 있습니다.

- 이메일·비밀번호 인증
- PostgreSQL 데이터베이스
- JavaScript/TypeScript 클라이언트
- Row Level Security
- 브라우저에서 사용할 수 있는 REST 방식 데이터 접근

참고 공식 문서:

- React Quickstart: https://supabase.com/docs/guides/getting-started/quickstarts/reactjs
- JavaScript 클라이언트 초기화: https://supabase.com/docs/reference/javascript/initializing
- 회원가입: https://supabase.com/docs/reference/javascript/auth-signup
- 비밀번호 로그인: https://supabase.com/docs/reference/javascript/auth-signinwithpassword
- Row Level Security: https://supabase.com/docs/guides/database/postgres/row-level-security

## 2. Supabase 프로젝트 생성

### 2-1. 프로젝트 만들기

Supabase Dashboard에서 새 프로젝트를 생성합니다.

권장 값:

| 항목 | 값 |
| --- | --- |
| 프로젝트 이름 | taskflow |
| 데이터베이스 비밀번호 | 별도로 안전하게 보관 |
| 리전 | 사용자와 가까운 리전 |
| 사용 목적 | 학습·개인 프로젝트 |

데이터베이스 비밀번호는 나중에 브라우저 코드나 GitHub에 작성하지 않습니다.

### 2-2. 이메일 인증 비활성화

이번 프로젝트에서는 이메일 인증을 사용하지 않기로 했습니다.

Supabase Dashboard에서 이메일 인증 설정을 비활성화합니다.

    Authentication
      → Providers 또는 Settings
      → Email
      → Confirm email 비활성화

설정이 꺼져 있으면 회원가입 직후 세션을 받아 바로 대시보드로 이동할 수 있습니다. Supabase 문서에서도 이메일 확인 설정에 따라 회원가입 후 session 반환 여부가 달라진다고 설명합니다.

주의할 점:

- 이 설정은 학습 과제의 편의를 위한 것입니다.
- 실제 서비스에서는 이메일 인증을 켜는 편이 안전합니다.
- 설정을 바꾸면 기존 테스트 계정의 상태가 영향을 받을 수 있습니다.

## 3. API URL과 키 확인

Supabase Dashboard에서 프로젝트의 API 설정을 확인합니다.

필요한 값:

- Project URL
- Publishable key

브라우저에서 사용할 키는 publishable key 또는 프로젝트 화면에 표시되는 anon 키입니다.

절대 사용하면 안 되는 키:

- service_role key
- secret key

service_role key는 RLS를 우회할 수 있으므로 브라우저 코드나 VITE 환경변수에 넣으면 안 됩니다.

## 4. TaskFlow에 Supabase 클라이언트 설치

TaskFlow 폴더에서 실행합니다.

    cd submissions/4-2/taskflow
    npm install @supabase/supabase-js

설치 후 package.json의 dependencies에 다음 패키지가 추가되어야 합니다.

    @supabase/supabase-js

## 5. 환경변수 설정

TaskFlow 루트에 .env.local 파일을 만듭니다.

    submissions/4-2/taskflow/.env.local

내용은 다음과 같은 형식으로 작성합니다.

    VITE_SUPABASE_URL=여기에_Project_URL
    VITE_SUPABASE_PUBLISHABLE_KEY=여기에_Publishable_Key

실제 키를 이 문서나 GitHub에 작성하지 않습니다.

### 5-1. .gitignore 확인

.gitignore에 다음과 같은 규칙이 포함되어 있는지 확인합니다.

    .env
    .env.local
    .env.*.local

확인 명령어:

    rg -n "\.env" .gitignore

환경변수 파일이 Git에 올라가면 키를 즉시 교체해야 할 수 있습니다.

### 5-2. Vite 환경변수 규칙

Vite에서 브라우저 코드가 읽을 수 있는 환경변수는 VITE_ 접두사가 필요합니다.

올바른 예:

    VITE_SUPABASE_URL
    VITE_SUPABASE_PUBLISHABLE_KEY

잘못된 예:

    SUPABASE_URL
    SUPABASE_SERVICE_ROLE_KEY

service_role 키는 VITE_ 접두사를 붙여서도 사용하지 않습니다.

## 6. Supabase 클라이언트 파일 만들기

파일을 생성합니다.

    src/lib/supabase.ts

내용:

    import { createClient } from "@supabase/supabase-js"

    const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
    const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY

    if (!supabaseUrl || !supabasePublishableKey) {
      throw new Error("Supabase 환경변수가 설정되지 않았습니다.")
    }

    export const supabase = createClient(
      supabaseUrl,
      supabasePublishableKey,
    )

이 파일의 역할은 Supabase 클라이언트를 한 번 생성하고, 다른 파일에서 재사용하는 것입니다.

다른 파일에서는 다음처럼 사용합니다.

    import { supabase } from "../lib/supabase"

개발 서버는 환경변수 변경 후 다시 시작해야 합니다.

    npm run dev

## 7. TypeScript 환경변수 타입

Vite의 환경변수에 타입을 추가하려면 다음 파일을 사용합니다.

    src/vite-env.d.ts

내용:

    /// <reference types="vite/client" />

    interface ImportMetaEnv {
      readonly VITE_SUPABASE_URL: string
      readonly VITE_SUPABASE_PUBLISHABLE_KEY: string
    }

    interface ImportMeta {
      readonly env: ImportMetaEnv
    }

이 타입은 환경변수 이름을 잘못 입력했을 때 TypeScript가 알려주는 데 도움이 됩니다.

## 8. 데이터베이스 테이블 생성

Supabase Dashboard의 SQL Editor에서 아래 SQL을 실행합니다.

### 8-1. projects 테이블

    create table public.projects (
      id uuid primary key default gen_random_uuid(),
      user_id uuid not null references auth.users(id) on delete cascade,
      name text not null check (char_length(trim(name)) > 0),
      description text,
      color text not null default 'blue'
        check (color in ('blue', 'green', 'yellow', 'red', 'purple', 'gray')),
      is_archived boolean not null default false,
      created_at timestamptz not null default now(),
      updated_at timestamptz not null default now()
    );

### 8-2. tasks 테이블

    create table public.tasks (
      id uuid primary key default gen_random_uuid(),
      user_id uuid not null references auth.users(id) on delete cascade,
      project_id uuid not null references public.projects(id) on delete cascade,
      title text not null check (char_length(trim(title)) > 0),
      description text,
      status text not null default 'todo'
        check (status in ('todo', 'in_progress', 'done')),
      priority text not null default 'medium'
        check (priority in ('low', 'medium', 'high')),
      due_date date,
      created_at timestamptz not null default now(),
      updated_at timestamptz not null default now()
    );

### 8-3. 조회 성능을 위한 인덱스

    create index projects_user_id_idx
      on public.projects(user_id);

    create index tasks_user_id_idx
      on public.tasks(user_id);

    create index tasks_project_id_idx
      on public.tasks(project_id);

프로젝트와 할 일을 사용자 ID와 프로젝트 ID로 자주 조회하므로 인덱스를 추가합니다.

## 9. Row Level Security 설정

RLS는 데이터베이스 행마다 접근 가능 여부를 확인하는 기능입니다.

이번 프로젝트의 원칙:

- 사용자는 자신의 프로젝트만 조회할 수 있습니다.
- 사용자는 자신의 프로젝트만 생성·수정할 수 있습니다.
- 사용자는 자신의 할 일만 조회할 수 있습니다.
- 사용자는 자신의 할 일만 생성·수정·삭제할 수 있습니다.
- 할 일을 추가할 때 선택한 프로젝트도 자신의 프로젝트인지 확인합니다.

### 9-1. RLS 활성화

    alter table public.projects enable row level security;
    alter table public.tasks enable row level security;

### 9-2. projects 정책

    create policy "projects_select_own"
    on public.projects
    for select
    to authenticated
    using ((select auth.uid()) = user_id);

    create policy "projects_insert_own"
    on public.projects
    for insert
    to authenticated
    with check ((select auth.uid()) = user_id);

    create policy "projects_update_own"
    on public.projects
    for update
    to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

    create policy "projects_delete_own"
    on public.projects
    for delete
    to authenticated
    using ((select auth.uid()) = user_id);

프로젝트 보관은 `is_archived`를 true로 변경해 목록에서 숨기는 기능이고, 프로젝트 삭제는 연결된 할 일과 함께 영구 삭제하는 기능입니다. `tasks.project_id`에 `on delete cascade`가 설정되어 있어 프로젝트 삭제 시 하위 할 일도 함께 삭제됩니다.

### 9-3. tasks 정책

    create policy "tasks_select_own"
    on public.tasks
    for select
    to authenticated
    using ((select auth.uid()) = user_id);

    create policy "tasks_insert_own_project"
    on public.tasks
    for insert
    to authenticated
    with check (
      (select auth.uid()) = user_id
      and exists (
        select 1
        from public.projects
        where projects.id = project_id
          and projects.user_id = (select auth.uid())
      )
    );

    create policy "tasks_update_own_project"
    on public.tasks
    for update
    to authenticated
    using ((select auth.uid()) = user_id)
    with check (
      (select auth.uid()) = user_id
      and exists (
        select 1
        from public.projects
        where projects.id = project_id
          and projects.user_id = (select auth.uid())
      )
    );

    create policy "tasks_delete_own"
    on public.tasks
    for delete
    to authenticated
    using ((select auth.uid()) = user_id);

RLS에서는 select, insert, update, delete에 필요한 정책을 각각 확인해야 합니다. 특히 update는 기존 행을 읽을 수 있는 select 정책도 함께 필요합니다.

## 10. 인증 구현 순서

### 10-1. useAuth 훅

파일:

    src/hooks/useAuth.ts

관리할 상태:

    user
    isLoading
    error

구현할 기능:

- 앱 시작 시 현재 세션 조회
- 로그인
- 회원가입
- 로그아웃
- 인증 상태 변경 감지

Supabase 클라이언트는 기본적으로 세션을 저장하고, auth 상태 변경을 감지할 수 있습니다.

### 10-2. 회원가입

회원가입 함수의 기본 흐름:

    이메일과 비밀번호 검증
      ↓
    isSubmitting = true
      ↓
    supabase.auth.signUp 호출
      ↓
    에러면 메시지 표시
      ↓
    성공하면 dashboard로 이동
      ↓
    마지막에 isSubmitting = false

회원가입 호출 형태:

    await supabase.auth.signUp({
      email,
      password,
    })

이번 프로젝트는 이메일 인증을 사용하지 않으므로, 성공 직후 세션이 있는지 확인하고 dashboard로 이동합니다.

### 10-3. 로그인

로그인 호출 형태:

    await supabase.auth.signInWithPassword({
      email,
      password,
    })

로그인 성공 시:

    /dashboard로 이동

로그인 실패 시:

- 사용자에게 이해하기 쉬운 메시지 표시
- 비밀번호 입력 상태 유지 또는 초기화
- 제출 중 상태 해제

### 10-4. 로그아웃

로그아웃 호출 형태:

    await supabase.auth.signOut()

로그아웃 성공 후:

    /login으로 이동

## 11. 보호 라우트

Supabase 연결 후 다음 페이지는 로그인한 사용자만 접근할 수 있어야 합니다.

    /dashboard
    /projects
    /projects/new
    /projects/:id
    /projects/:id/edit
    /projects/:id/tasks/new
    /tasks/:id
    /tasks/:id/edit

비로그인 사용자가 접근하면 /login으로 이동합니다.

반대로 로그인한 사용자가 /login이나 /signup으로 접근하면 /dashboard로 이동합니다.

보호 라우트는 인증 상태를 확인하는 동안 잠시 Loading 화면을 보여줘야 합니다.

    인증 상태 확인 중
      ↓
    로딩 표시
      ↓
    로그인 사용자 있음 → 페이지 표시
    로그인 사용자 없음 → /login 이동

## 12. 프로젝트 CRUD 구현 순서

### 12-1. projectApi.ts

파일:

    src/lib/projectApi.ts

분리할 함수:

    getProjects()
    getProjectById(id)
    createProject(input)
    updateProject(id, input)
    archiveProject(id)

각 함수는 Supabase 요청만 담당하고, 화면 표시나 라우팅은 담당하지 않습니다.

### 12-2. useProjects.ts

파일:

    src/hooks/useProjects.ts

관리할 상태:

    projects
    isLoading
    error

구현할 흐름:

- 목록 조회
- 프로젝트 생성 후 목록 갱신
- 프로젝트 수정 후 상세 또는 목록 갱신
- 프로젝트 보관 후 목록에서 숨김
- 로딩·에러 상태 관리

## 13. 할 일 CRUD 구현 순서

### 13-1. taskApi.ts

파일:

    src/lib/taskApi.ts

분리할 함수:

    getTasksByProject(projectId)
    getTaskById(id)
    createTask(input)
    updateTask(id, input)
    deleteTask(id)

### 13-2. useTasks.ts

파일:

    src/hooks/useTasks.ts

관리할 상태:

    tasks
    isLoading
    error
    selectedStatus
    selectedPriority

구현할 흐름:

- 프로젝트별 할 일 조회
- 할 일 생성
- 할 일 수정
- 상태 변경
- 우선순위 변경
- 할 일 삭제
- 삭제 후 목록 갱신

## 14. 구현 완료 내용

다음 파일과 기능이 `taskflow/src`에 반영되었습니다.

| 영역 | 구현 내용 |
| --- | --- |
| 환경변수 | `src/vite-env.d.ts`에서 Vite 환경변수 타입 정의 |
| Supabase | `src/lib/supabase.ts`에서 클라이언트 초기화 |
| 인증 | `src/contexts/AuthContext.tsx`, `src/contexts/useAuth.ts`에서 세션 유지·회원가입·로그인·로그아웃 구현 |
| 보호 라우트 | `src/components/ProtectedRoute.tsx`에서 비로그인 사용자를 로그인 페이지로 이동 |
| 프로젝트 API | `src/lib/projectApi.ts`에서 조회·생성·수정·보관 구현 |
| 할 일 API | `src/lib/taskApi.ts`에서 조회·생성·수정·삭제 구현 |
| 화면 연결 | 대시보드, 프로젝트, 할 일 페이지를 Supabase 데이터와 연결 |

## 15. 구현 후 확인 순서

1. `taskflow/.env.local`에 `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`가 있는지 확인합니다.
2. `npm run dev`로 개발 서버를 다시 시작합니다.
3. 회원가입 후 대시보드로 이동하는지 확인합니다.
4. 프로젝트를 만들고 프로젝트 상세에서 할 일을 추가합니다.
5. 할 일의 상태·우선순위·마감일을 수정하고 삭제합니다.
6. 프로젝트를 보관한 뒤 기본 프로젝트 목록에서 사라지는지 확인합니다.
7. 두 번째 계정으로 로그인하여 첫 번째 계정의 데이터가 보이지 않는지 확인합니다.

검증 명령어:

```bash
npm run lint
npm run build
```
- 로딩·에러·빈 상태 관리

## 14. 폼 검증 규칙

### 회원가입

- 이메일 필수
- 이메일 형식 확인
- 비밀번호 필수
- 비밀번호 최소 8자
- 비밀번호 확인 일치

### 로그인

- 이메일 필수
- 비밀번호 필수

### 프로젝트

- 프로젝트 이름 필수
- 프로젝트 이름 공백만 입력 불가
- 설명은 선택

### 할 일

- 제목 필수
- 제목 공백만 입력 불가
- 설명은 선택
- 상태는 todo, in_progress, done 중 하나
- 우선순위는 low, medium, high 중 하나
- 마감일은 선택

## 15. 로딩·에러·빈 상태 처리

### 로딩 상태

데이터 요청을 시작하면 Loading 컴포넌트를 표시합니다.

예:

    프로젝트 목록을 불러오는 중입니다.

### 에러 상태

요청에 실패하면 ErrorState를 표시합니다.

예:

    프로젝트를 불러오지 못했습니다.
    다시 시도

### 빈 상태

성공적으로 조회했지만 데이터가 없으면 EmptyState를 표시합니다.

예:

    아직 프로젝트가 없습니다.
    첫 번째 프로젝트 만들기

### 제출 중 상태

회원가입·로그인·등록·수정·삭제 중에는 버튼을 비활성화합니다.

이렇게 해야 사용자가 버튼을 여러 번 눌러 중복 요청을 보내는 것을 막을 수 있습니다.

## 16. 구현 체크리스트

### Supabase 기본 설정

- [ ] Supabase 프로젝트를 생성했다.
- [ ] 이메일 인증을 비활성화했다.
- [ ] Project URL을 확인했다.
- [ ] Publishable key를 확인했다.
- [ ] service_role key를 사용하지 않았다.
- [ ] @supabase/supabase-js를 설치했다.
- [ ] .env.local을 생성했다.
- [ ] .env.local이 .gitignore에 포함되어 있다.
- [ ] supabase.ts를 생성했다.

### 데이터베이스

- [ ] projects 테이블을 생성했다.
- [ ] tasks 테이블을 생성했다.
- [ ] projects와 tasks의 외래 키를 설정했다.
- [ ] status와 priority check 조건을 설정했다.
- [ ] RLS를 활성화했다.
- [ ] projects 정책을 추가했다.
- [ ] tasks 정책을 추가했다.
- [ ] 다른 사용자의 데이터가 조회되지 않는지 확인했다.

### 인증

- [ ] 회원가입이 동작한다.
- [ ] 이메일 인증 없이 가입 직후 로그인 상태가 된다.
- [ ] 로그인이 동작한다.
- [ ] 새로고침 후 세션이 유지된다.
- [ ] 로그아웃이 동작한다.
- [ ] 보호 라우트가 동작한다.
- [ ] 로그인하지 않은 사용자가 dashboard에 접근할 수 없다.

### 프로젝트

- [ ] 프로젝트를 생성할 수 있다.
- [ ] 프로젝트 목록을 조회할 수 있다.
- [ ] 프로젝트 상세를 조회할 수 있다.
- [ ] 프로젝트를 수정할 수 있다.
- [ ] 프로젝트를 보관할 수 있다.
- [ ] 프로젝트가 없을 때 빈 상태가 표시된다.

### 할 일

- [ ] 프로젝트에 할 일을 추가할 수 있다.
- [ ] 프로젝트별 할 일을 조회할 수 있다.
- [ ] 할 일 상세를 조회할 수 있다.
- [ ] 할 일을 수정할 수 있다.
- [ ] 상태를 변경할 수 있다.
- [ ] 우선순위를 변경할 수 있다.
- [ ] 마감일을 설정할 수 있다.
- [ ] 할 일을 삭제할 수 있다.
- [ ] 삭제 후 목록이 갱신된다.

## 17. 자주 발생하는 문제

### 환경변수가 undefined인 경우

확인할 내용:

- 파일 이름이 .env.local인지 확인
- 변수 이름이 VITE_로 시작하는지 확인
- 변수 이름의 철자가 정확한지 확인
- 개발 서버를 재시작했는지 확인

### 회원가입 후 session이 없는 경우

확인할 내용:

- Supabase의 Confirm email 설정
- 회원가입 이메일 인증이 아직 켜져 있는지
- 올바른 Supabase 프로젝트의 URL과 키를 사용했는지

### RLS 정책 오류가 발생하는 경우

대표적인 오류:

    new row violates row-level security policy

확인할 내용:

- 로그인된 세션이 있는지
- insert 데이터의 user_id가 auth.uid()와 같은지
- 해당 project_id가 현재 사용자 소유인지
- select 정책도 함께 추가했는지
- 정책의 대상 role이 authenticated인지

### 프로젝트는 보이는데 할 일이 안 보이는 경우

확인할 내용:

- tasks.project_id가 올바른 프로젝트 ID인지
- tasks.user_id가 현재 사용자 ID인지
- tasks 테이블의 select 정책이 있는지
- Supabase 쿼리의 필터가 올바른지

## 18. 완료 후 검증 명령어

TaskFlow 폴더에서 실행합니다.

    cd submissions/4-2/taskflow
    npm run lint
    npm run build

개발 서버 실행:

    npm run dev

브라우저 테스트 순서:

    /signup
      ↓
    /login
      ↓
    /dashboard
      ↓
    /projects
      ↓
    프로젝트 생성
      ↓
    프로젝트 상세
      ↓
    할 일 생성
      ↓
    할 일 수정·상태 변경·삭제

## 19. 다음 실제 작업

가장 먼저 할 일은 다음 세 가지입니다.

1. Supabase Dashboard에서 프로젝트를 생성합니다.
2. 이메일 인증을 비활성화합니다.
3. SQL Editor에서 projects와 tasks 테이블 및 RLS 정책을 생성합니다.

그 다음 TaskFlow 코드에서 다음 작업을 진행합니다.

1. @supabase/supabase-js 설치
2. .env.local 작성
3. src/lib/supabase.ts 생성
4. useAuth.ts 구현
5. 회원가입·로그인 연결
6. 보호 라우트 연결
7. projectApi.ts와 useProjects.ts 구현
8. taskApi.ts와 useTasks.ts 구현

이 순서를 지키면 화면, 인증, 데이터베이스, CRUD를 한 번에 섞지 않고 단계별로 확인할 수 있습니다.
