# React 상태 관리와 폼 UX

이 문서는 TaskFlow에서 입력값, 서버 데이터, 로딩·에러 상태를 어떻게 관리하는지 설명합니다.

## 1. 상태란 무엇인가

상태(State)는 화면에 영향을 주면서 시간이 지나거나 사용자 행동에 따라 바뀌는 값입니다.

예를 들어 다음 값은 상태입니다.

- 로그인 폼의 이메일
- 프로젝트 목록
- 할 일 목록
- 현재 입력 중인 제목
- 데이터를 불러오는 중인지 여부
- 에러 메시지

상태가 변경되면 React는 컴포넌트를 다시 렌더링하고, 새로운 상태에 맞는 화면을 보여줍니다.

## 2. `useState` 기본 사용법

```tsx
const [email, setEmail] = useState("")
```

두 값의 역할은 다릅니다.

- `email`: 현재 저장된 상태값
- `setEmail`: 상태를 변경하는 함수

입력값은 다음과 같이 연결합니다.

```tsx
<input
  value={email}
  onChange={(event) => setEmail(event.target.value)}
/>
```

사용자가 글자를 입력할 때마다 `onChange`가 실행되고 `email` 상태가 변경됩니다.

## 3. Controlled Component

React State가 input의 값을 직접 관리하는 컴포넌트를 Controlled Component라고 합니다.

```tsx
const [title, setTitle] = useState("")

<input
  value={title}
  onChange={(event) => setTitle(event.target.value)}
/>
```

이 방식의 장점은 다음과 같습니다.

- 현재 입력값을 항상 코드에서 알 수 있습니다.
- 제출 전에 값을 검증할 수 있습니다.
- 입력값을 초기화하거나 수정하기 쉽습니다.
- 다른 상태에 따라 입력 UI를 바꿀 수 있습니다.

TaskFlow의 로그인, 회원가입, 프로젝트 생성, 프로젝트 수정, 할 일 생성, 할 일 수정 폼이 모두 이 방식을 사용합니다.

## 4. 폼 제출 흐름

TaskFlow의 폼은 다음 순서로 동작합니다.

```text
사용자가 입력
  ↓
onChange로 State 변경
  ↓
사용자가 저장 버튼 클릭
  ↓
onSubmit 실행
  ↓
기본 새로고침 방지
  ↓
입력값 검증
  ↓
제출 중 상태 시작
  ↓
Supabase 요청
  ↓
성공하면 이동 또는 목록 갱신
실패하면 에러 표시
  ↓
제출 중 상태 종료
```

예시 구조는 다음과 같습니다.

```tsx
async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault()
  setError("")

  if (!title.trim()) {
    setError("제목을 입력해주세요.")
    return
  }

  setIsSubmitting(true)
  try {
    await createTask(user.id, input)
    navigate(`/projects/${projectId}`)
  } catch (requestError) {
    setError(getErrorMessage(requestError))
  } finally {
    setIsSubmitting(false)
  }
}
```

## 5. 입력값 검증

HTML의 `required` 속성만 사용하면 브라우저 수준의 기본 검증만 할 수 있습니다. TaskFlow에서는 저장 전에 JavaScript로도 중요한 값을 확인합니다.

```tsx
if (!name.trim()) {
  setError("프로젝트 이름을 입력해주세요.")
  return
}
```

`trim()`을 사용하는 이유는 공백만 입력한 값을 유효한 이름으로 처리하지 않기 위해서입니다.

회원가입에서는 다음을 검증합니다.

- 이메일 필수 입력
- 비밀번호 8자 이상
- 비밀번호 확인과 일치

프로젝트와 할 일에서는 다음을 검증합니다.

- 프로젝트 이름 필수 입력
- 할 일 제목 필수 입력
- 선택형 상태·우선순위 값 사용
- 선택하지 않은 마감일은 `null`로 저장

## 6. 제출 중 상태

네트워크 요청 중에는 사용자가 버튼을 여러 번 누르지 못하게 해야 합니다.

```tsx
<button type="submit" disabled={isSubmitting}>
  {isSubmitting ? "저장 중..." : "저장"}
</button>
```

TaskFlow에서 사용하는 제출 상태는 다음과 같습니다.

| 상태 | 버튼 표시 |
| --- | --- |
| 기본 | 저장 |
| 요청 중 | 저장 중... |
| 로그인 요청 중 | 로그인 중... |
| 회원가입 요청 중 | 가입 중... |
| 삭제 요청 중 | 삭제 중... |

버튼을 비활성화하면 중복 요청과 중복 데이터 생성을 줄일 수 있습니다.

## 7. 로딩·성공·빈 상태·에러 상태

서버 데이터를 사용하는 화면은 성공한 경우만 고려하면 안 됩니다.

### 로딩 상태

```tsx
if (isLoading) {
  return <p>데이터를 불러오고 있습니다...</p>
}
```

사용자는 요청이 진행 중인지 알 수 있어야 합니다.

### 빈 상태

```tsx
if (!isLoading && projects.length === 0) {
  return <EmptyState title="아직 프로젝트가 없습니다." />
}
```

데이터가 없는 것은 오류가 아니므로, 에러 메시지와 구분해서 안내해야 합니다.

### 에러 상태

```tsx
{error && <p role="alert">{error}</p>}
```

Supabase 권한 오류나 네트워크 오류가 발생했을 때 사용자가 실패 사실을 알 수 있어야 합니다.

### 성공 안내

샘플 데이터 생성처럼 작업 결과를 알려줄 필요가 있는 경우 성공 메시지를 표시합니다.

```tsx
setNotice("샘플 데이터를 추가했습니다.")
```

## 8. 서버 데이터와 폼 상태 구분하기

TaskFlow에서는 다음 상태를 분리해서 관리합니다.

| 종류 | 예시 | 역할 |
| --- | --- | --- |
| 서버 데이터 | `projects`, `tasks` | Supabase에서 조회한 데이터 |
| 폼 상태 | `title`, `description` | 사용자가 입력 중인 값 |
| UI 상태 | `isLoading`, `isSubmitting` | 화면 진행 상태 |
| 피드백 상태 | `error`, `notice` | 사용자에게 결과 전달 |

이들을 하나의 객체에 모두 넣지 않고 구분하면 어떤 값이 어떤 이유로 바뀌는지 이해하기 쉽습니다.

## 9. 비동기 요청과 `async/await`

Supabase 요청은 즉시 결과가 나오지 않기 때문에 비동기 함수로 처리합니다.

```tsx
try {
  const projects = await getProjects()
  setProjects(projects)
} catch (requestError) {
  setError(getErrorMessage(requestError))
}
```

- `await`: 요청이 끝날 때까지 결과를 기다립니다.
- `try`: 성공할 때 실행할 코드입니다.
- `catch`: 요청이 실패했을 때 실행할 코드입니다.
- `finally`: 성공과 실패에 관계없이 실행할 코드입니다.

`finally`에서 `isLoading`이나 `isSubmitting`을 false로 되돌리면 요청이 끝난 뒤 버튼과 화면이 정상 상태로 돌아옵니다.

## 10. 여러 데이터를 함께 불러오기

대시보드는 프로젝트와 할 일을 모두 필요로 합니다. 두 요청이 서로 의존하지 않으므로 `Promise.all`로 함께 요청합니다.

```tsx
const [projectData, taskData] = await Promise.all([
  getProjects(),
  getTasks(),
])
```

이렇게 하면 첫 번째 요청이 끝난 뒤 두 번째 요청을 시작하는 것보다 효율적으로 처리할 수 있습니다.

단, 둘 중 하나라도 실패하면 전체 `Promise.all`이 실패하므로 하나의 에러 상태로 안내합니다.

## 11. 폼과 API 책임 분리

페이지 컴포넌트가 Supabase 쿼리를 직접 작성하지 않고 API 파일로 분리했습니다.

```text
폼 이벤트
  ↓
페이지 컴포넌트의 handleSubmit
  ↓
src/lib/projectApi.ts 또는 taskApi.ts
  ↓
Supabase 요청
  ↓
결과를 State에 반영하거나 페이지 이동
```

이 구조의 장점은 다음과 같습니다.

- 화면 코드와 데이터 요청 코드가 분리됩니다.
- 같은 API 함수를 여러 페이지에서 재사용할 수 있습니다.
- Supabase 쿼리를 수정할 때 관련 파일을 찾기 쉽습니다.
- 평가 때 UI 처리와 데이터 처리의 책임을 설명하기 쉽습니다.

## 12. 인증 상태는 Context로 관리

로그인 사용자 정보는 여러 페이지와 레이아웃에서 필요하므로 `AuthContext`로 공유합니다.

```text
AuthProvider
  ├── AppLayout: 이메일 표시, 로그아웃
  ├── ProtectedRoute: 접근 권한 확인
  ├── LoginPage: 로그인
  ├── SignupPage: 회원가입
  └── DashboardPage: 현재 사용자 기준 데이터 조회
```

모든 상태를 전역으로 만들지 않고, 여러 컴포넌트가 공유해야 하는 인증 정보만 Context로 관리했습니다. 페이지에서만 사용하는 폼 입력값은 각 페이지의 `useState`로 관리합니다.

## 13. 평가 때 설명할 내용

### 왜 input의 값을 State로 관리하나요?

제출 시 현재 입력값을 확인하고 검증하기 위해서입니다. 또한 입력값을 초기화하거나 서버 저장 결과에 맞춰 화면을 변경할 수 있습니다.

### 왜 `isSubmitting`이 필요한가요?

네트워크 요청 중 중복 제출을 막고, 사용자에게 현재 작업이 진행 중임을 알려주기 위해 필요합니다.

### 로딩과 빈 상태는 어떻게 다른가요?

로딩은 아직 요청이 끝나지 않은 상태이고, 빈 상태는 요청은 성공했지만 데이터가 0개인 상태입니다.

### 왜 API 코드를 페이지와 분리했나요?

화면 표시와 데이터 접근의 책임을 분리해 코드 재사용성과 유지보수성을 높이기 위해서입니다.

### 모든 상태를 Context로 관리하지 않은 이유는 무엇인가요?

전역 공유가 필요한 인증 상태만 Context로 관리하고, 페이지에 한정된 폼과 목록 상태는 가까운 컴포넌트에서 관리하는 것이 단순하기 때문입니다.

## 관련 파일

- `taskflow/src/pages/LoginPage.tsx`
- `taskflow/src/pages/SignupPage.tsx`
- `taskflow/src/pages/ProjectNewPage.tsx`
- `taskflow/src/pages/ProjectEditPage.tsx`
- `taskflow/src/pages/TaskNewPage.tsx`
- `taskflow/src/pages/TaskEditPage.tsx`
- `taskflow/src/pages/DashboardPage.tsx`
- `taskflow/src/contexts/AuthContext.tsx`
- `taskflow/src/lib/projectApi.ts`
- `taskflow/src/lib/taskApi.ts`
