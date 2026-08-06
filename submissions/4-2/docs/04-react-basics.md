# React 기본 개념과 TaskFlow 적용

이 문서는 React를 처음 접하는 사람이 TaskFlow의 코드를 설명할 수 있도록 React의 핵심 개념을 정리한 문서입니다.

## 1. React란 무엇인가

React는 사용자 인터페이스를 만들기 위한 JavaScript 라이브러리입니다. 화면을 작은 컴포넌트로 나누고, 데이터가 바뀌면 필요한 화면을 다시 렌더링하는 방식으로 웹 UI를 구성합니다.

React의 핵심 흐름은 다음과 같습니다.

```text
사용자 행동
  ↓
이벤트 핸들러 실행
  ↓
상태 변경
  ↓
컴포넌트 다시 렌더링
  ↓
변경된 화면 표시
```

TaskFlow에서 할 일 상태를 `todo`에서 `done`으로 변경하면, 상태 값이 바뀌고 상태 배지와 대시보드 통계가 새 값으로 표시됩니다.

## 2. React를 사용하는 이유

TaskFlow는 프로젝트 목록, 할 일 카드, 입력 폼, 로그인 상태처럼 화면의 데이터가 자주 바뀌는 서비스입니다. React를 사용하면 다음과 같은 장점이 있습니다.

- 화면을 역할별 컴포넌트로 나눌 수 있습니다.
- 데이터가 변경되었을 때 관련 화면을 다시 그리기 쉽습니다.
- 입력값과 로딩 상태를 코드로 관리할 수 있습니다.
- 여러 페이지에서 같은 UI를 재사용할 수 있습니다.
- React Router와 함께 SPA를 만들 수 있습니다.

React는 데이터베이스나 서버를 제공하는 기술은 아닙니다. TaskFlow에서는 React가 화면과 사용자 동작을 담당하고, Supabase가 인증과 데이터 저장을 담당합니다.

## 3. 컴포넌트

컴포넌트는 화면의 일부를 담당하는 함수입니다. 컴포넌트는 JSX를 반환하고, 필요한 데이터를 props로 받습니다.

```tsx
type GreetingProps = {
  name: string
}

function Greeting({ name }: GreetingProps) {
  return <h1>안녕하세요, {name}님</h1>
}
```

TaskFlow의 컴포넌트 예시는 다음과 같습니다.

| 파일 | 역할 |
| --- | --- |
| `src/components/ProjectCard.tsx` | 프로젝트 목록의 카드 표시 |
| `src/components/TaskCard.tsx` | 할 일 목록의 카드 표시 |
| `src/components/StatusBadge.tsx` | 상태와 우선순위 표시 |
| `src/components/PageHeader.tsx` | 페이지 제목과 설명 표시 |
| `src/components/EmptyState.tsx` | 데이터가 없을 때 표시 |
| `src/components/ProtectedRoute.tsx` | 로그인 여부에 따른 접근 제어 |

컴포넌트를 나누는 기준은 단순히 파일 개수를 늘리는 것이 아닙니다. 여러 곳에서 재사용되거나, 하나의 분명한 역할을 가지거나, 별도로 테스트할 가치가 있는 UI를 컴포넌트로 분리합니다.

## 4. JSX와 TSX

JSX는 JavaScript 안에서 HTML과 비슷한 문법으로 UI를 작성하는 방법입니다. TypeScript에서 JSX를 사용하면 TSX 파일이 됩니다.

```tsx
function EmptyMessage() {
  return <p className="text-slate-500">데이터가 없습니다.</p>
}
```

주의할 점은 다음과 같습니다.

- `class` 대신 `className`을 사용합니다.
- JavaScript 표현식은 `{}` 안에 작성합니다.
- 컴포넌트 이름은 대문자로 시작해야 합니다.
- 여러 요소를 반환할 때는 하나의 부모 요소로 감쌉니다.

TaskFlow에서는 Tailwind CSS 클래스를 `className`에 작성합니다.

## 5. Props

Props는 부모 컴포넌트가 자식 컴포넌트에 전달하는 읽기 전용 값입니다.

```tsx
<TaskCard task={task} />
```

`TaskCard`는 전달받은 `task`를 사용해 제목, 설명, 상태, 우선순위를 표시합니다.

```tsx
type TaskCardProps = {
  task: Task
}

function TaskCard({ task }: TaskCardProps) {
  return <h2>{task.title}</h2>
}
```

Props를 사용하는 이유는 컴포넌트 내부에 데이터를 고정하지 않고, 다른 데이터를 전달해 재사용하기 위해서입니다.

## 6. State와 `useState`

State는 컴포넌트가 기억하고 있어야 하는 값입니다. State가 변경되면 React는 해당 컴포넌트를 다시 렌더링합니다.

```tsx
const [title, setTitle] = useState("")

<input value={title} onChange={(event) => setTitle(event.target.value)} />
```

여기서:

- `title`: 현재 상태값
- `setTitle`: 상태를 변경하는 함수
- `useState("")`: 초기값이 빈 문자열이라는 의미

TaskFlow에서 State로 관리하는 값은 다음과 같습니다.

- 로그인 폼의 이메일과 비밀번호
- 프로젝트와 할 일 목록
- 입력 폼의 제목, 설명, 상태, 우선순위
- `isLoading`, `isSubmitting`, `isDeleting`
- 에러 메시지와 성공 안내 메시지

상태값을 직접 변경하면 안 됩니다.

```tsx
// 잘못된 예
title = "새 제목"

// 올바른 예
setTitle("새 제목")
```

React는 상태 변경 함수가 호출되어야 화면을 다시 그릴 수 있습니다.

## 7. 이벤트 처리

React에서는 이벤트에 함수를 연결해 사용자 동작을 처리합니다.

```tsx
<button type="button" onClick={() => void handleCreateDemoData()}>
  샘플 데이터 넣기
</button>
```

TaskFlow에서 사용하는 이벤트 예시는 다음과 같습니다.

| 이벤트 | 사용 위치 |
| --- | --- |
| `onClick` | 로그아웃, 삭제, 보관, 샘플 데이터 추가 |
| `onChange` | input, textarea, select 입력값 변경 |
| `onSubmit` | 로그인, 회원가입, 프로젝트·할 일 저장 |

폼을 제출할 때는 기본 브라우저 동작인 페이지 새로고침을 막습니다.

```tsx
function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault()
  // 데이터 저장
}
```

## 8. 조건부 렌더링

조건부 렌더링은 상태에 따라 다른 UI를 보여주는 방식입니다.

```tsx
{isLoading ? (
  <p>불러오는 중...</p>
) : tasks.length === 0 ? (
  <EmptyState />
) : (
  <TaskList tasks={tasks} />
)}
```

TaskFlow는 다음 상태를 구분해서 보여줍니다.

- 인증 확인 중: 인증 상태 확인 메시지
- 데이터 조회 중: 로딩 메시지
- 데이터 없음: 빈 상태 안내
- 요청 실패: 에러 메시지
- 데이터 있음: 카드와 통계 표시

## 9. 리스트 렌더링과 `key`

배열 데이터를 화면에 여러 개 표시할 때 `map`을 사용합니다.

```tsx
{tasks.map((task) => (
  <TaskCard key={task.id} task={task} />
))}
```

`key`는 React가 리스트의 각 항목을 구분하기 위한 값입니다. 데이터의 고유한 ID를 사용하는 것이 좋습니다. 배열의 순번을 key로 사용하면 항목의 추가·삭제·정렬 때 React가 변경 내용을 잘못 판단할 수 있습니다.

## 10. `useEffect`

`useEffect`는 컴포넌트 렌더링 외부에서 일어나는 작업을 처리할 때 사용합니다. 대표적인 예는 API 요청, 이벤트 구독, 타이머입니다.

TaskFlow의 대시보드는 화면이 표시될 때 Supabase에서 프로젝트와 할 일을 조회합니다.

```tsx
useEffect(() => {
  void loadDashboard()
}, [user?.id])
```

두 번째 인자인 의존성 배열의 값이 바뀌면 effect가 다시 실행됩니다. TaskFlow에서는 로그인한 사용자가 바뀌었을 때 데이터를 다시 조회하기 위해 `user?.id`를 사용합니다.

비동기 요청이 끝난 뒤 이미 화면이 사라진 컴포넌트의 상태를 변경하지 않도록 `isMounted` 플래그로 정리도 수행합니다.

```tsx
let isMounted = true

// 요청 완료 후
if (isMounted) setTasks(taskData)

return () => {
  isMounted = false
}
```

## 11. React의 렌더링 이해하기

React는 State나 Props가 변경되면 컴포넌트 함수를 다시 실행합니다. 이것은 전체 브라우저 페이지를 새로고침하는 것과 다릅니다.

1. `setTasks`가 호출됩니다.
2. React가 해당 컴포넌트를 다시 실행합니다.
3. 새로운 배열을 기준으로 JSX를 계산합니다.
4. 실제로 변경된 DOM 부분만 업데이트합니다.

그래서 할 일을 수정하거나 삭제한 뒤 State를 갱신하면 화면에 결과가 반영됩니다.

## 12. 평가 때 설명할 내용

### React를 사용한 이유는 무엇인가요?

프로젝트와 할 일처럼 데이터가 자주 변경되는 화면을 컴포넌트와 State 중심으로 관리하기 좋기 때문입니다.

### Props와 State의 차이는 무엇인가요?

Props는 부모가 전달하는 읽기 전용 값이고, State는 컴포넌트가 직접 관리하며 변경될 수 있는 값입니다.

### `useEffect`는 왜 사용했나요?

Supabase 데이터 조회와 인증 상태 구독처럼 렌더링 외부에서 발생하는 작업을 처리하기 위해 사용했습니다.

### 왜 컴포넌트를 나누었나요?

역할을 분리해 코드의 가독성과 재사용성을 높이고, 페이지가 지나치게 커지는 것을 방지하기 위해 나누었습니다.

## 관련 파일

- `taskflow/src/App.tsx`
- `taskflow/src/main.tsx`
- `taskflow/src/components/`
- `taskflow/src/pages/`
- `taskflow/src/contexts/`
