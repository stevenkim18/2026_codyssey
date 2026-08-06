# Evaluation 4-2 답변 정리

이 문서는 `evaluation4-2.md`의 항목 1~4를 평가자에게 설명하기 위한 답변 자료입니다. 단순히 기능이 있다고 말하는 것보다, 어떤 개념을 사용했고 내 코드의 어느 부분에서 그 개념이 동작하는지 함께 설명하는 것을 목표로 합니다.

답변할 때는 다음 순서로 말하면 좋습니다.

1. 개념을 짧게 정의합니다.
2. TaskFlow에서 그 개념을 사용한 이유를 말합니다.
3. 실제 파일과 상태·이벤트·렌더링의 연결을 짚습니다.
4. 선택한 방식의 장점과 한계를 덧붙입니다.

---

## 항목 1. 기능 구현 간단 확인

항목 1은 화면을 캡처해서 보여주기보다 라우트와 코드 구조를 기준으로 간단히 확인하면 됩니다.

### 1-1. 라우트와 Not Found

`src/App.tsx:19-35`에서 React Router의 `Routes`와 `Route`를 사용해 다음 경로를 연결했습니다.

| 구분 | 경로 | 역할 |
| --- | --- | --- |
| 공개 | `/` | 랜딩 페이지 |
| 공개 | `/login` | 로그인 |
| 공개 | `/signup` | 회원가입 |
| 보호 | `/dashboard` | 대시보드 |
| 보호 | `/projects` | 프로젝트 목록 |
| 보호 | `/projects/new` | 프로젝트 등록 |
| 보호 | `/projects/:id` | 프로젝트 상세 |
| 보호 | `/projects/:id/edit` | 프로젝트 수정 |
| 보호 | `/projects/:id/tasks/new` | 할 일 등록 |
| 보호 | `/tasks/:id` | 할 일 상세 |
| 보호 | `/tasks/:id/edit` | 할 일 수정 |
| 예외 | `*` | Not Found 페이지 |

`*` 경로가 `NotFoundPage`를 렌더링하므로 등록되지 않은 주소에서는 “페이지를 찾을 수 없습니다.” 화면이 표시됩니다. 보호 라우트는 `ProtectedRoute`가 인증 상태를 확인한 뒤 로그인하지 않은 사용자를 `/login`으로 이동시킵니다.

### 1-2. 조회와 CRUD

프로젝트와 할 일 각각에 대해 목록 조회, 상세 조회, 등록, 수정, 삭제 흐름이 있습니다.

| 데이터 | 목록 조회 | 상세 조회 | 등록 | 수정 | 삭제 |
| --- | --- | --- | --- | --- | --- |
| 프로젝트 | `getProjects` → `ProjectListPage` | `getProjectById` → `ProjectDetailPage` | `createProject` → `ProjectNewPage` | `updateProject` → `ProjectEditPage` | `deleteProject` → 프로젝트 상세의 삭제 버튼 |
| 할 일 | `getTasks`, `getTasksByProject` | `getTaskById` → `TaskDetailPage` | `createTask` → `TaskNewPage` | `updateTask` → `TaskEditPage` | `deleteTask` → 할 일 상세의 삭제 버튼 |

프로젝트는 삭제 외에 `archiveProject`를 이용한 보관도 지원합니다. 보관은 `is_archived` 값을 변경해 목록에서 숨기는 기능이고, 삭제는 실제 행을 삭제하는 기능입니다. 프로젝트와 할 일의 API 함수는 각각 `src/lib/projectApi.ts`, `src/lib/taskApi.ts`에 있고, 화면은 API 호출과 화면 상태 변경을 담당합니다.

### 1-3. 로딩·에러·빈 상태

공통 상태 컴포넌트는 다음 세 가지입니다.

- `LoadingState`: 요청 중임을 표시합니다. `message`, `fullPage` props로 화면에 맞게 재사용합니다.
- `ErrorState`: 요청 실패나 폼 오류를 표시합니다. `message`, `compact`, `onRetry` props를 받습니다.
- `EmptyState`: 요청은 성공했지만 데이터가 없을 때 제목, 설명, 액션을 표시합니다.

예를 들어 `ProjectListPage`는 다음 순서로 상태를 판단합니다.

```tsx
error가 있으면 ErrorState
isLoading이면 LoadingState
projects.length === 0이면 EmptyState
그 외에는 ProjectCard 목록
```

따라서 빈 배열을 오류로 오해하지 않고, “요청 실패”와 “정상적으로 조회했지만 데이터 없음”을 구분합니다.

### 1-4. 폼 검증과 제출 중 상태

프로젝트 이름과 할 일 제목은 필수값입니다. 폼 제출 핸들러에서 `trim()` 후 빈 문자열인지 확인하고, 빈 값이면 `setError`로 오류 메시지를 표시합니다. 이메일 입력에는 HTML의 `required`, `type="email"` 검증도 사용합니다.

제출 중에는 `isSubmitting`을 `true`로 변경합니다. 버튼의 `disabled` 속성을 켜고 “저장 중...”, “로그인 중...”, “가입 중...”처럼 문구를 바꾸어 중복 제출을 막고 현재 상태를 사용자에게 알려줍니다.

### 1-5. 배포 URL 확인 범위

코드 기준으로 라우트와 CRUD 구현은 확인할 수 있지만, 배포된 URL의 실제 CRUD 성공 여부는 Supabase 환경변수와 RLS 정책이 적용된 배포 환경에서 별도로 확인해야 합니다. 따라서 평가 때는 다음을 마지막으로 점검합니다.

- 배포 URL에서 `/projects`를 새로고침해도 SPA 라우팅이 유지되는가?
- 로그인 후 프로젝트와 할 일을 등록·수정·삭제할 수 있는가?
- 다른 계정으로 로그인했을 때 이전 계정의 데이터가 보이지 않는가?

---

## 항목 2. 컴포넌트·폴더 구조·커스텀 훅

### 2-1. 커스텀 훅이란?

커스텀 훅은 React의 기본 훅인 `useState`, `useEffect` 등을 조합해 반복되는 상태 관리와 로직을 함수로 분리한 것입니다. 이름이 `use`로 시작하고, UI를 직접 반환하기보다 상태와 이벤트 함수를 반환하는 것이 일반적입니다.

TaskFlow에서는 `src/hooks/useProjects.ts:15-60`의 `useProjects`가 프로젝트와 할 일 목록 조회 흐름을 담당합니다.

```tsx
const { projects, tasks, isLoading, error, reload } = useProjects(user?.id)
```

훅 내부에서는 다음을 관리합니다.

1. `projects`, `tasks` 서버 데이터
2. `isLoading` 요청 중 상태
3. `error` 요청 실패 메시지
4. `reloadToken`과 `reload` 목록 재조회 기능
5. `useEffect`의 `isMounted` 정리 로직

`getProjects`와 `getTasks`를 `Promise.all`로 병렬 조회하고, 성공하면 state에 저장합니다. 요청이 끝난 뒤 화면이 사라졌다면 state를 변경하지 않도록 `isMounted`를 확인합니다.

### 2-2. 왜 `useProjects`로 분리했는가?

프로젝트 목록과 대시보드는 모두 프로젝트와 할 일 목록을 필요로 합니다. 이 조회 로직을 각 페이지에 직접 작성하면 `useEffect`, 로딩 처리, 에러 처리, 언마운트 처리 코드가 반복됩니다.

그래서 데이터 조회와 그에 필요한 상태를 `useProjects`에 모았습니다. 페이지는 “어떤 데이터를 보여줄지”에 집중하고, 훅은 “데이터를 어떻게 가져오고 새로고침할지”를 담당합니다. 이 구조 덕분에 대시보드에서 샘플 데이터를 추가한 뒤 `reload()`를 호출해 같은 조회 흐름을 재사용할 수 있습니다.

평가에서 이렇게 답할 수 있습니다.

> 프로젝트와 할 일 조회는 목록 페이지와 대시보드에서 함께 필요하므로 `useProjects`로 분리했습니다. 훅 안에서 서버 데이터, 로딩, 에러, 재조회 상태를 관리하고 페이지에는 결과만 반환합니다. 페이지마다 같은 비동기 처리 코드를 반복하지 않고, 조회 정책을 한 곳에서 바꿀 수 있다는 점 때문에 커스텀 훅으로 분리했습니다.

### 2-3. 폴더를 나눈 이유

현재 구조는 다음과 같습니다.

```text
src/
├── pages/       URL 단위 화면
├── components/  여러 화면에서 재사용하는 UI
├── hooks/       데이터 조회·갱신과 상태를 묶은 커스텀 훅
├── lib/         Supabase API 함수와 공통 유틸리티
├── contexts/    앱 전체에서 공유하는 인증 상태
├── layouts/     공통 페이지 레이아웃
└── types/       Project, Task와 상태 타입
```

역할을 나눈 기준은 변경 이유입니다.

- 화면의 URL이나 화면 전용 상태가 바뀌면 `pages`를 수정합니다.
- 여러 화면에서 같은 모양과 동작을 재사용하면 `components`를 수정합니다.
- 데이터 조회 방식과 비동기 상태가 바뀌면 `hooks` 또는 `lib`를 수정합니다.
- 인증 세션처럼 여러 화면이 함께 사용해야 하는 값은 `contexts`에서 관리합니다.

이렇게 나누면 한 파일에 라우팅, 화면 마크업, Supabase 쿼리, 인증 상태가 모두 섞이지 않습니다.

### 2-4. 재사용 컴포넌트 8개와 분리 기준

`src/components`에는 다음 8개의 재사용 컴포넌트가 있습니다.

| 컴포넌트 | 재사용 기준 | 주요 props 또는 역할 |
| --- | --- | --- |
| `PageHeader` | 페이지마다 반복되는 제목 영역 | `eyebrow`, `title`, `description`, `action` |
| `ProjectCard` | 프로젝트 목록의 카드 표현 | `project`, `taskCount` |
| `TaskCard` | 대시보드·프로젝트 상세의 할 일 카드 | `task` |
| `StatusBadge` | 상태와 우선순위 표시 | `type`, `value` 유니언 타입 |
| `EmptyState` | 데이터가 없을 때의 공통 안내 | `title`, `description`, `action` |
| `LoadingState` | 요청 중 공통 안내 | `message`, `fullPage` |
| `ErrorState` | 요청 실패·폼 오류 공통 안내 | `message`, `compact`, `onRetry` |
| `ProtectedRoute` | 로그인 필요 화면의 접근 제어 | 인증 상태 확인 후 `Outlet` 또는 `Navigate` 렌더링 |

추가로 `AppLayout`은 모든 페이지에 공통 헤더와 `Outlet`을 제공하는 레이아웃 컴포넌트입니다.

컴포넌트를 나눈 기준은 단순히 파일 수를 늘리는 것이 아닙니다. 여러 화면에서 반복되거나, 하나의 명확한 역할이 있거나, props에 따라 다른 데이터를 표시해야 하는 단위를 분리했습니다. 예를 들어 `StatusBadge` 하나가 상태와 우선순위를 모두 표시하지만, `type`과 `value`의 타입을 통해 잘못된 조합을 줄입니다.

### 2-5. 공통 상태 UI가 실제로 사용되는 위치

- 목록: `ProjectListPage`에서 `LoadingState`, `ErrorState`, `EmptyState` 사용
- 대시보드: `DashboardPage`에서 `LoadingState`, `ErrorState`, `EmptyState` 사용
- 상세: `ProjectDetailPage`, `TaskDetailPage`에서 로딩·에러·빈 상태 사용
- 인증: `LoginPage`, `SignupPage`, `ProtectedRoute`에서 `LoadingState`, `ErrorState` 사용
- 폼: 프로젝트·할 일 등록/수정 페이지에서 `ErrorState`와 제출 중 버튼 사용

공통 컴포넌트에 `role="status"`, `aria-live="polite"`, `role="alert"`를 지정해 상태 변화가 보조 기술에도 전달되도록 했습니다.

---

## 항목 3. React 핵심 개념과 내 코드 설명

### 3-1. Props와 State의 차이

| 구분 | Props | State |
| --- | --- | --- |
| 소유자 | 부모 컴포넌트가 전달 | 해당 컴포넌트 또는 훅이 보유 |
| 변경 방법 | 자식이 직접 변경하지 않음 | `setState` 함수로 변경 |
| 목적 | 데이터를 전달하고 컴포넌트를 재사용 | 시간이 지나며 바뀌는 값을 기억하고 화면 갱신 |
| TaskFlow 예시 | `ProjectCard`의 `project`, `taskCount` | `useProjects`의 `projects`, `isLoading` |

`ProjectListPage`는 `useProjects`에서 받은 프로젝트를 `ProjectCard`에 props로 전달합니다.

```tsx
projects.map((project) => (
  <ProjectCard
    key={project.id}
    project={project}
    taskCount={taskCounts[project.id] ?? 0}
  />
))
```

`ProjectCard`는 전달받은 `project`를 직접 바꾸지 않고 화면에 표시만 합니다. 반대로 `TaskNewPage`의 `title`, `description`, `status`, `priority`, `dueDate`는 사용자가 입력하면서 바뀌므로 페이지의 state로 관리합니다.

상태를 둔 위치는 공유 범위에 따라 결정했습니다.

- 한 폼에서만 쓰는 값: 해당 페이지의 `useState`
- 목록 조회와 여러 목록 화면이 공유하는 데이터 흐름: `useProjects`
- 로그인 사용자와 세션: `AuthProvider`와 `useAuth` Context

모든 값을 전역 상태로 만들지 않고, 실제로 여러 컴포넌트가 공유해야 하는 인증 상태만 Context로 올렸습니다.

### 3-2. `useEffect`의 실행 시점과 의존성 배열

`useEffect`는 렌더링 결과가 화면에 반영된 뒤 API 요청, 이벤트 구독, 타이머처럼 렌더링 외부에서 일어나는 작업을 실행할 때 사용합니다.

의존성 배열의 의미는 다음과 같습니다.

- 배열 없음: 렌더링마다 실행될 수 있으므로 일반적으로 주의해서 사용합니다.
- `[]`: 컴포넌트가 마운트될 때 실행하고, 정리 함수는 언마운트될 때 실행하는 패턴입니다.
- `[id]`: 처음 실행되고 `id`가 이전 값과 달라질 때 다시 실행됩니다.
- `[reloadToken, userId]`: 사용자나 재조회 토큰이 바뀔 때 실행됩니다.

내 코드의 예시는 다음과 같습니다.

#### `useProjects`의 `[reloadToken, userId]`

`src/hooks/useProjects.ts:26-52`에서 `userId`가 준비되거나 바뀌면 프로젝트와 할 일을 다시 조회합니다. `reload()`는 `reloadToken`을 1 증가시키고, 그 state 변경이 effect를 다시 실행시킵니다.

```tsx
const reload = useCallback(() => {
  setReloadToken((token) => token + 1)
}, [])

useEffect(() => {
  // userId가 있으면 프로젝트와 할 일을 조회
}, [reloadToken, userId])
```

#### `TaskNewPage`의 `[id]`

`src/pages/TaskNewPage.tsx:27-47`에서 URL의 프로젝트 ID가 바뀌면 `getProjectById(id)`를 다시 호출해 `projectName`을 갱신합니다. 그래서 새 할 일 화면의 상단에 ID가 아니라 프로젝트 이름이 표시됩니다.

#### `AuthProvider`의 `[]`

`src/contexts/AuthContext.tsx:11-30`은 앱이 시작될 때 현재 세션을 한 번 확인하고, `onAuthStateChange` 구독을 등록합니다. 컴포넌트가 사라질 때 구독을 해제해 메모리 누수와 중복 이벤트를 방지합니다.

개발 모드의 `StrictMode`에서는 effect의 정리와 재실행이 추가로 일어날 수 있습니다. 그래서 비동기 요청이 끝난 뒤 컴포넌트가 아직 화면에 있는지 `isMounted`로 확인하고, 화면이 사라진 뒤 state를 변경하지 않도록 했습니다.

### 3-3. 비동기 요청의 네 가지 상태

`useProjects`의 조회 흐름은 다음과 같습니다.

1. **로딩**: 요청을 시작할 때 `setIsLoading(true)`를 호출합니다.
2. **성공**: `Promise.all`이 성공하면 `setProjects`, `setTasks`로 데이터를 저장합니다.
3. **실패**: `catch`에서 `setError(getErrorMessage(requestError))`로 사용자에게 보여줄 오류를 저장합니다.
4. **완료**: `finally`에서 `setIsLoading(false)`로 로딩을 종료합니다.

조회 성공 후 배열의 길이가 0이면 오류가 아니라 빈 상태입니다. `ProjectListPage`는 `projects.length === 0`일 때 `EmptyState`를 렌더링합니다. 즉, “서버 요청 자체가 실패한 경우”와 “성공했지만 아직 데이터가 없는 경우”를 다르게 표현합니다.

폼 요청도 같은 원칙을 사용합니다. `isSubmitting`으로 제출 중 상태를 관리하고, `try` 성공 시 이동하며, `catch`에서 `ErrorState`를 보여주고, `finally`에서 제출 중 상태를 해제합니다.

### 3-4. 상태 변경이 화면 변화로 이어지는 지점

#### 예시 1: 목록 조회 결과와 카드 렌더링

`useProjects`에서 `setProjects(projectData)`가 실행되면 `ProjectListPage`가 다시 렌더링됩니다. 그 결과 `projects.map(...)`이 새 배열을 기준으로 실행되어 프로젝트 카드가 화면에 나타납니다.

#### 예시 2: 입력 state와 controlled input

`TaskNewPage`의 제목 input은 `value={title}`로 state와 연결되어 있고, `onChange`에서 `setTitle(event.target.value)`를 호출합니다. 사용자가 입력할 때마다 state가 바뀌고, 다시 렌더링되면서 input에 현재 state가 표시됩니다.

#### 예시 3: 제출 중 state와 버튼 UI

`TaskNewPage`에서 제출 직전에 `setIsSubmitting(true)`를 호출합니다. 그러면 저장 버튼이 disabled가 되고 문구가 “저장 중...”으로 바뀝니다. 요청이 끝나면 `finally`에서 false로 바뀌어 다시 제출할 수 있습니다.

#### 예시 4: 대시보드 샘플 데이터 추가

`DashboardPage`의 `setIsSeeding(true)`는 샘플 데이터 버튼을 비활성화하고 “샘플 데이터 추가 중...”을 표시합니다. 생성이 끝나면 `setNotice`로 성공 메시지를 표시하고 `reload()`로 프로젝트·할 일 목록을 다시 불러옵니다.

#### 예시 5: 삭제 후 라우트 변화

`TaskDetailPage`에서 삭제 요청이 성공하면 `navigate(/projects/${task.project_id})`를 호출합니다. 삭제 버튼의 `isDeleting` 상태 변화와 성공 후 라우트 변화가 각각 화면의 버튼 상태와 현재 페이지를 바꿉니다.

---

## 항목 4. 하나의 기능 전체 흐름과 Supabase 선택 이유

### 4-1. “새 할 일 추가” 기능의 전체 흐름

이 기능은 라우팅 → 컴포넌트 → 상태 → 이벤트 → API 요청 → 렌더링 순서로 동작합니다.

```text
/projects/:id/tasks/new
        ↓
App.tsx의 Route + ProtectedRoute
        ↓
TaskNewPage 렌더링
        ↓
useEffect로 프로젝트 이름 조회
        ↓
입력 이벤트가 form state 변경
        ↓
submit 이벤트가 createTask 호출
        ↓
성공: 프로젝트 상세로 이동 / 실패: ErrorState 표시
        ↓
state와 URL 변화에 따라 화면 재렌더링
```

#### 1단계: 라우팅

`src/App.tsx:24-32`에서 다음 동적 라우트를 등록합니다.

```tsx
<Route path="/projects/:id/tasks/new" element={<TaskNewPage />} />
```

`/projects/abc/tasks/new`처럼 접근하면 `:id` 부분의 `abc`가 프로젝트 ID가 됩니다. 이 라우트는 `ProtectedRoute` 안에 있으므로 로그인하지 않은 사용자는 먼저 `/login`으로 이동합니다.

#### 2단계: 컴포넌트와 URL 파라미터

`TaskNewPage`는 `useParams()`로 `id`를 읽습니다. 이 ID는 새 할 일을 어느 프로젝트에 연결할지 결정하는 값입니다.

동시에 `getProjectById(id)`를 호출해 프로젝트 이름을 조회하고 `projectName` state에 저장합니다. 따라서 화면 상단에는 내부 식별자인 ID 대신 사용자가 이해할 수 있는 프로젝트 이름이 표시됩니다.

#### 3단계: 상태

`TaskNewPage`에서 관리하는 상태는 역할별로 나뉩니다.

| 상태 | 역할 |
| --- | --- |
| `projectName` | 상단에 표시할 프로젝트 이름 |
| `isProjectLoading` | 프로젝트 이름 조회 중인지 표시 |
| `projectError` | 프로젝트 조회 실패 메시지 |
| `title`, `description` | 입력 폼 값 |
| `status`, `priority`, `dueDate` | 할 일의 선택·날짜 값 |
| `error` | 등록 요청 또는 필수값 검증 오류 |
| `isSubmitting` | 등록 요청 중 중복 제출 방지 |

#### 4단계: 이벤트와 API 요청

input의 `onChange` 이벤트는 각 state setter를 호출합니다. 폼의 `onSubmit` 이벤트는 다음 순서로 처리됩니다.

1. 브라우저의 기본 제출을 막습니다.
2. `id`와 로그인 사용자가 있는지 확인합니다.
3. 제목을 `trim()`하고 비어 있으면 오류를 표시합니다.
4. `setIsSubmitting(true)`으로 버튼을 잠급니다.
5. `createTask(user.id, input)`을 호출합니다.
6. 성공하면 `/projects/${id}`로 이동합니다.
7. 실패하면 `getErrorMessage` 결과를 `ErrorState`에 표시합니다.
8. `finally`에서 `isSubmitting`을 false로 되돌립니다.

`createTask`는 `src/lib/taskApi.ts:47-55`에서 Supabase의 `tasks` 테이블에 `user_id`, `project_id`, 제목, 설명, 상태, 우선순위, 마감일을 insert합니다. 페이지는 Supabase 쿼리의 세부 문법을 몰라도 되고, API 함수는 데이터 요청만 담당합니다.

#### 5단계: 렌더링

`TaskNewPage`는 조건에 따라 서로 다른 화면을 렌더링합니다.

- 프로젝트 이름 조회 중: `LoadingState`
- 프로젝트 조회 실패: `ErrorState`
- 조회 성공: 입력 폼
- 폼 제출 중: disabled 상태의 “저장 중...” 버튼
- 등록 실패: 폼 내부의 `ErrorState`
- 등록 성공: 프로젝트 상세 라우트로 이동

즉, 이벤트 핸들러가 state를 변경하고, React가 그 state를 기준으로 화면을 다시 렌더링하는 구조입니다.

### 4-2. Supabase를 선택한 이유

TaskFlow는 로그인 사용자별로 프로젝트와 할 일을 저장해야 하므로 인증과 관계형 데이터베이스가 필요합니다. Supabase를 선택한 이유는 다음과 같습니다.

- Supabase Auth로 이메일·비밀번호 회원가입과 로그인을 구현할 수 있습니다.
- PostgreSQL 기반이라 `projects`와 `tasks`의 관계를 명확하게 설계할 수 있습니다.
- JavaScript 클라이언트로 React에서 CRUD 요청을 쉽게 보낼 수 있습니다.
- RLS(Row Level Security)로 사용자별 데이터 접근을 데이터베이스 수준에서 제한할 수 있습니다.
- 별도의 서버를 직접 구축하지 않고도 교육 과제의 전체 흐름을 구현할 수 있습니다.

React Router의 보호 라우트는 화면 접근만 제한합니다. 실제 데이터 보안은 Supabase RLS가 담당해야 합니다. 그래서 `user_id`를 저장하고, 프로젝트와 할 일의 select/insert/update/delete 정책을 별도로 설정했습니다.

### 4-3. Supabase 연동에서 설명할 수 있는 어려움과 해결

#### 어려움 1: 인증 상태는 즉시 알 수 없다

앱이 처음 시작될 때 세션 조회는 비동기입니다. 세션 확인이 끝나기 전에 보호 페이지를 렌더링하면 로그인한 사용자도 로그인 화면으로 잘못 이동할 수 있습니다.

그래서 `AuthProvider`에서 `isLoading`을 두고 `getSession()`이 끝날 때까지 상태를 확인합니다. `ProtectedRoute`는 로딩 중에는 `LoadingState`를 보여주고, 확인이 끝난 뒤에만 `Outlet` 또는 `/login` 이동을 결정합니다.

#### 어려움 2: 프론트엔드 보호 라우트만으로는 데이터가 보호되지 않는다

주소를 직접 입력하지 못하게 하는 것과 데이터베이스 행을 보호하는 것은 다릅니다. 사용자가 다른 프로젝트 ID를 요청할 수 있으므로 Supabase RLS에서도 `auth.uid()`와 `user_id`를 비교해야 합니다.

특히 update는 기존 행을 조회할 수 있는 select 정책과 수정할 수 있는 update 정책이 함께 필요합니다. 할 일 insert는 `project_id`가 현재 사용자의 프로젝트인지도 확인해야 합니다. 이 정책과 설명은 `03-supabase-setup.md`의 RLS 부분에 정리했습니다.

#### 어려움 3: 프로젝트와 할 일은 관계가 있다

할 일은 `project_id`로 프로젝트에 연결됩니다. 프로젝트를 삭제할 때 하위 할 일이 남으면 고아 데이터가 생길 수 있습니다. 그래서 데이터베이스 외래 키에 `on delete cascade`를 설정하고, 프로젝트 삭제 시 연결된 할 일도 함께 삭제되도록 했습니다. 보관 기능은 삭제 대신 `is_archived`만 변경하므로 복구 가능성이 있는 별도 동작입니다.

#### 어려움 4: 이메일 확인 설정에 따라 회원가입 결과가 달라진다

Supabase의 이메일 자동 확인 설정에 따라 회원가입 직후 session이 반환될 수도 있고, 이메일 확인 후 로그인해야 할 수도 있습니다. 코드에서는 `signUp`의 반환 session이 있으면 대시보드로 이동하고, 없으면 `/login?signup=complete`로 이동해 로그인 안내를 보여줍니다.

#### 어려움 5: 원격 요청은 항상 성공하지 않는다

네트워크 오류, 잘못된 환경변수, RLS 정책 오류가 발생할 수 있습니다. 그래서 API 함수에서 오류를 throw하고, 페이지나 훅에서 `try/catch/finally`로 로딩 종료와 사용자 메시지를 처리합니다. `getErrorMessage`는 Supabase 오류를 사용자에게 이해하기 쉬운 메시지로 바꾸는 역할을 합니다.

### 4-4. 평가에서 말할 수 있는 종합 답변

> 예를 들어 새 할 일 추가 기능은 `/projects/:id/tasks/new` 라우트가 `TaskNewPage`를 렌더링하는 것에서 시작합니다. 페이지는 `useParams`로 프로젝트 ID를 받고, `useEffect`에서 프로젝트 이름을 조회해 상단에 표시합니다. 사용자가 입력하면 controlled input의 state가 바뀌고, 제출하면 `createTask`가 Supabase의 tasks 테이블에 데이터를 저장합니다. 요청 중에는 `isSubmitting`으로 버튼을 잠그고, 성공하면 프로젝트 상세로 이동하며, 실패하면 에러 상태를 표시합니다. Supabase는 Auth, PostgreSQL, RLS를 한 서비스에서 사용할 수 있어 선택했고, 연동 과정에서는 비동기 인증 상태, 사용자별 RLS, 프로젝트와 할 일의 관계, 네트워크 오류를 처리하는 것이 핵심 과제였습니다.

---

## 평가 직전 확인할 것

- `npm run lint`와 `npm run build`가 통과하는지 확인합니다.
- Supabase에서 `projects`, `tasks`의 RLS 정책이 실제로 적용되었는지 확인합니다.
- 테스트 계정으로 프로젝트와 할 일의 등록·수정·삭제를 한 번씩 수행합니다.
- 다른 계정으로 로그인해 사용자별 데이터가 분리되는지 확인합니다.
- 배포 URL에서 동적 라우트를 새로고침해도 Not Found가 되지 않는지 확인합니다.

