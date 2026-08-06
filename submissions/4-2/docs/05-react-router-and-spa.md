# React Router와 SPA

이 문서는 TaskFlow의 페이지 이동 구조와 React Router를 사용하는 이유를 정리한 문서입니다.

## 1. SPA란 무엇인가

SPA는 Single Page Application의 줄임말입니다. 브라우저가 처음에 하나의 HTML을 받은 뒤, 이후 페이지 이동과 화면 변경을 JavaScript가 처리하는 방식입니다.

전통적인 웹 페이지 이동은 다음과 같습니다.

```text
링크 클릭
  ↓
새 HTML 요청
  ↓
브라우저 전체 페이지 새로고침
```

SPA의 이동은 다음과 같습니다.

```text
링크 클릭
  ↓
React Router가 주소 변경 처리
  ↓
필요한 컴포넌트만 표시
```

SPA에서는 페이지 전체가 새로고침되지 않기 때문에 화면 전환이 자연스럽고, 이미 유지하고 있는 UI 상태를 활용하기 쉽습니다.

## 2. React Router를 사용하는 이유

React 자체에는 URL에 따라 다른 컴포넌트를 보여주는 기능이 없습니다. React Router를 사용하면 주소와 화면을 연결할 수 있습니다.

TaskFlow에서는 다음과 같이 라우트를 구성했습니다.

| 경로 | 화면 | 접근 권한 |
| --- | --- | --- |
| `/` | 랜딩 페이지 | 누구나 |
| `/login` | 로그인 | 비로그인 사용자 |
| `/signup` | 회원가입 | 비로그인 사용자 |
| `/dashboard` | 대시보드 | 로그인 필요 |
| `/projects` | 프로젝트 목록 | 로그인 필요 |
| `/projects/new` | 프로젝트 생성 | 로그인 필요 |
| `/projects/:id` | 프로젝트 상세 | 로그인 필요 |
| `/projects/:id/edit` | 프로젝트 수정 | 로그인 필요 |
| `/projects/:id/tasks/new` | 할 일 생성 | 로그인 필요 |
| `/tasks/:id` | 할 일 상세 | 로그인 필요 |
| `/tasks/:id/edit` | 할 일 수정 | 로그인 필요 |
| `*` | Not Found | 누구나 |

## 3. `Routes`와 `Route`

`Routes` 안에 여러 `Route`를 작성해 URL과 컴포넌트를 연결합니다.

```tsx
<Routes>
  <Route path="/" element={<LandingPage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route path="/projects" element={<ProjectListPage />} />
</Routes>
```

- `path`: 브라우저 주소와 비교할 경로
- `element`: 해당 경로에서 표시할 React 컴포넌트

TaskFlow의 전체 라우트 설정은 `src/App.tsx`에 있습니다.

## 4. 공통 레이아웃과 중첩 라우트

TaskFlow는 모든 화면에 공통 헤더를 표시하기 위해 `AppLayout`을 사용합니다.

```tsx
<Route element={<AppLayout />}>
  <Route path="/" element={<LandingPage />} />
  {/* 여러 페이지 */}
</Route>
```

`AppLayout` 안의 `<Outlet />` 위치에 현재 경로의 페이지가 표시됩니다.

이 구조를 사용하면 헤더와 전체 배경을 각 페이지에 반복해서 작성하지 않아도 됩니다.

## 5. `Link`와 일반 `<a>`의 차이

React Router가 관리하는 SPA 내부 이동에는 `Link`를 사용합니다.

```tsx
<Link to="/projects">프로젝트</Link>
```

일반 `<a href="/projects">`는 브라우저가 새 문서를 요청하면서 페이지 전체를 다시 불러올 수 있습니다. 반면 `Link`는 React Router가 이동을 처리하므로 SPA의 흐름을 유지할 수 있습니다.

외부 사이트로 이동하거나 브라우저의 일반 링크 동작이 필요한 경우에는 `<a>`를 사용할 수 있습니다.

## 6. 동적 라우트와 `useParams`

프로젝트와 할 일의 상세 페이지는 데이터 ID가 주소에 포함됩니다.

```tsx
<Route path="/projects/:id" element={<ProjectDetailPage />} />
```

주소가 `/projects/abc-123`이라면 `:id` 부분에 `abc-123`이 들어갑니다.

페이지 컴포넌트에서는 `useParams`로 값을 가져옵니다.

```tsx
const { id } = useParams()
const project = await getProjectById(id)
```

TaskFlow에서는 이 ID를 Supabase 조회 조건에 사용합니다.

- `/projects/:id`: 해당 프로젝트 조회
- `/projects/:id/tasks/new`: 해당 프로젝트에 할 일 생성
- `/tasks/:id`: 특정 할 일 조회

## 7. `useNavigate`

코드 실행 결과에 따라 페이지를 이동해야 할 때 `useNavigate`를 사용합니다.

```tsx
const navigate = useNavigate()

await createProject(user.id, input)
navigate(`/projects/${project.id}`)
```

TaskFlow에서 사용하는 예시는 다음과 같습니다.

- 로그인 성공 후 `/dashboard` 이동
- 회원가입 성공 후 `/dashboard` 이동
- 프로젝트 생성 후 프로젝트 상세 이동
- 할 일 삭제 후 프로젝트 상세 이동
- 로그아웃 후 `/login` 이동

링크를 사용자가 직접 클릭하는 이동에는 `Link`, 저장·삭제 후 자동 이동에는 `useNavigate`를 사용합니다.

## 8. 보호 라우트

보호 라우트는 로그인한 사용자만 접근할 수 있는 라우트입니다.

TaskFlow에서는 다음 구조를 사용합니다.

```tsx
<Route element={<ProtectedRoute />}>
  <Route path="/dashboard" element={<DashboardPage />} />
  <Route path="/projects" element={<ProjectListPage />} />
</Route>
```

`ProtectedRoute`의 동작 순서는 다음과 같습니다.

1. Supabase의 세션 확인이 끝날 때까지 로딩 화면을 표시합니다.
2. 로그인한 사용자가 있으면 `<Outlet />`을 표시합니다.
3. 로그인한 사용자가 없으면 `/login`으로 이동합니다.
4. 원래 접근하려던 주소를 `state`에 저장해 로그인 후 돌아갈 수 있게 합니다.

```tsx
if (!user) {
  return <Navigate to="/login" state={{ from: location.pathname }} replace />
}
```

보호 라우트는 화면 접근을 제한하는 역할이고, 실제 데이터 보안은 Supabase RLS가 담당합니다. 프론트엔드 라우트만으로는 데이터 보안을 완성할 수 없습니다.

## 9. 로그인 사용자 전용 페이지 처리

로그인한 사용자가 `/login`이나 `/signup`에 접근하면 대시보드로 이동합니다.

```tsx
if (user) return <Navigate to="/dashboard" replace />
```

반대로 비로그인 사용자는 보호 라우트에서 로그인 페이지로 이동합니다. 이렇게 하면 사용자가 현재 상태에 맞지 않는 화면에 머무르지 않습니다.

## 10. Not Found 페이지

정의하지 않은 주소를 처리하기 위해 마지막에 와일드카드 라우트를 작성합니다.

```tsx
<Route path="*" element={<NotFoundPage />} />
```

잘못된 주소를 입력해도 빈 화면 대신 안내 페이지를 보여주는 것이 사용자 경험에 좋습니다.

## 11. Vite 개발 서버와 배포 주의점

개발 환경에서는 Vite가 존재하지 않는 SPA 경로에도 `index.html`을 반환해 React Router가 동작할 수 있습니다. 하지만 배포 서버에서도 모든 경로를 `index.html`로 연결하는 설정이 필요할 수 있습니다.

배포 후 `/projects/abc`를 새로고침했을 때 404가 발생하면 SPA fallback 설정을 확인해야 합니다.

또한 개발 서버는 반드시 `taskflow` 폴더에서 실행해야 합니다.

```bash
cd submissions/4-2/taskflow
npm run dev
```

## 12. 평가 때 설명할 내용

### 왜 SPA를 선택했나요?

프로젝트 목록과 상세, 폼 사이를 자주 이동하는 서비스이므로 페이지 전체를 새로고침하지 않고 자연스럽게 화면을 전환하기 위해 선택했습니다.

### `Link`와 `useNavigate`는 언제 사용하나요?

사용자가 직접 클릭하는 내부 링크에는 `Link`를 사용하고, 저장이나 삭제처럼 작업이 끝난 뒤 코드로 이동할 때는 `useNavigate`를 사용합니다.

### 보호 라우트만 있으면 데이터가 안전한가요?

아닙니다. 보호 라우트는 화면 접근만 제어합니다. 실제 데이터 접근은 Supabase RLS에서 사용자 ID 기준으로 제한해야 합니다.

### `:id`는 무엇인가요?

데이터마다 달라지는 값을 URL에 넣기 위한 동적 경로 파라미터입니다. TaskFlow에서는 프로젝트나 할 일의 UUID를 사용합니다.

## 관련 파일

- `taskflow/src/App.tsx`
- `taskflow/src/main.tsx`
- `taskflow/src/layouts/AppLayout.tsx`
- `taskflow/src/components/ProtectedRoute.tsx`
- `taskflow/src/pages/NotFoundPage.tsx`
