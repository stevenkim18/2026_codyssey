# TaskFlow 초기 세팅 기록

이 문서는 TaskFlow 프로젝트에서 Supabase를 연결하기 전까지 진행한 초기 설정과 현재 상태를 정리한 문서입니다.

## 1. 프로젝트 위치

TaskFlow 앱은 다음 위치에 있습니다.

    submissions/4-2/taskflow/

주의할 점은 개발 서버를 반드시 이 폴더에서 실행해야 한다는 것입니다.

잘못된 실행 위치:

    submissions/4-2/

올바른 실행 위치:

    submissions/4-2/taskflow/

## 2. 현재 기술 스택

| 영역 | 선택 |
| --- | --- |
| 프레임워크 | React |
| 언어 | TypeScript |
| 개발 도구 | Vite |
| 스타일링 | Tailwind CSS |
| 라우팅 | React Router |
| 백엔드 | 아직 연결하지 않음 |
| 배포 | 추후 Vercel 예정 |

현재 설치된 주요 버전은 package.json을 기준으로 확인합니다.

- React 19
- Vite 8
- TypeScript 6
- Tailwind CSS 4
- React Router 8

## 3. 프로젝트 생성

Vite의 React TypeScript 템플릿으로 프로젝트를 생성했습니다.

    cd submissions/4-2
    npm create vite@latest taskflow -- --template react-ts
    cd taskflow
    npm install

프로젝트 생성 후 기본 개발 서버가 실행되는지 확인했습니다.

## 4. Tailwind CSS 설정

Tailwind CSS와 Vite 플러그인을 프로젝트에 직접 설치했습니다.

    npm install -D tailwindcss @tailwindcss/vite

taskflow/vite.config.ts에서 Tailwind 플러그인을 등록했습니다.

    import { defineConfig } from "vite"
    import react from "@vitejs/plugin-react"
    import tailwindcss from "@tailwindcss/vite"

    export default defineConfig({
      plugins: [react(), tailwindcss()],
    })

src/index.css에는 Tailwind CSS를 불러오도록 작성했습니다.

    @import "tailwindcss";

그리고 기본 전역 스타일을 추가했습니다.

- 기본 글꼴
- 배경색
- 최소 화면 너비
- box-sizing
- 폼 요소의 글꼴 상속

Tailwind 적용 여부는 App.tsx에서 다음과 같은 클래스를 사용해 확인했습니다.

    flex
    min-h-screen
    items-center
    justify-center
    bg-slate-100
    text-blue-600

## 5. React Router 설정

React Router를 설치했습니다.

    npm install react-router

src/main.tsx에서 BrowserRouter로 App을 감쌌습니다.

    <BrowserRouter>
      <App />
    </BrowserRouter>

src/App.tsx에서 Routes와 Route를 사용해 URL과 페이지 컴포넌트를 연결했습니다.

현재 연결된 라우트는 다음과 같습니다.

| 주소 | 페이지 |
| --- | --- |
| / | 랜딩 페이지 |
| /login | 로그인 |
| /signup | 회원가입 |
| /dashboard | 대시보드 |
| /projects | 프로젝트 목록 |
| /projects/new | 프로젝트 생성 |
| /projects/:id | 프로젝트 상세 |
| /projects/:id/edit | 프로젝트 수정 |
| /projects/:id/tasks/new | 할 일 생성 |
| /tasks/:id | 할 일 상세 |
| /tasks/:id/edit | 할 일 수정 |
| * | Not Found |

:id는 프로젝트나 할 일의 실제 ID가 들어가는 동적 라우트입니다.

## 6. 현재 폴더 구조

    taskflow/
    ├── src/
    │   ├── components/
    │   │   ├── EmptyState.tsx
    │   │   ├── PageHeader.tsx
    │   │   ├── ProjectCard.tsx
    │   │   ├── StatusBadge.tsx
    │   │   └── TaskCard.tsx
    │   ├── layouts/
    │   │   └── AppLayout.tsx
    │   ├── pages/
    │   │   ├── DashboardPage.tsx
    │   │   ├── LandingPage.tsx
    │   │   ├── LoginPage.tsx
    │   │   ├── NotFoundPage.tsx
    │   │   ├── ProjectDetailPage.tsx
    │   │   ├── ProjectEditPage.tsx
    │   │   ├── ProjectListPage.tsx
    │   │   ├── ProjectNewPage.tsx
    │   │   ├── SignupPage.tsx
    │   │   ├── TaskDetailPage.tsx
    │   │   ├── TaskEditPage.tsx
    │   │   └── TaskNewPage.tsx
    │   ├── types/
    │   │   └── database.ts
    │   ├── App.tsx
    │   ├── index.css
    │   └── main.tsx
    ├── index.html
    ├── package.json
    ├── package-lock.json
    └── vite.config.ts

## 7. 각 폴더의 역할

### components

여러 페이지에서 재사용할 UI 컴포넌트를 둡니다.

현재 작성된 컴포넌트:

- PageHeader: 페이지 제목·설명·액션 버튼 영역
- EmptyState: 데이터가 없을 때 표시
- StatusBadge: Task 상태와 우선순위 표시
- ProjectCard: 프로젝트 카드
- TaskCard: 할 일 카드

### layouts

여러 페이지에서 공통으로 사용하는 화면 틀을 둡니다.

AppLayout에는 다음 내용이 있습니다.

- TaskFlow 로고
- 대시보드 링크
- 프로젝트 링크
- 로그인 링크
- 현재 페이지를 표시하는 NavLink
- 자식 페이지가 표시되는 Outlet

### pages

URL에 연결되는 큰 화면을 둡니다.

현재 페이지들은 Supabase 연결 전 단계의 화면 뼈대입니다. 입력 폼의 저장 버튼과 로그인 버튼은 아직 실제 요청을 보내지 않습니다.

### types

데이터 구조와 상태 값의 TypeScript 타입을 둡니다.

현재 정의된 타입:

    TaskStatus = "todo" | "in_progress" | "done"

    TaskPriority = "low" | "medium" | "high"

    Project

    Task

### hooks와 lib

폴더만 만들어 둔 상태입니다.

나중에 다음 로직을 분리할 예정입니다.

- hooks/useAuth.ts
- hooks/useProjects.ts
- hooks/useTasks.ts
- lib/supabase.ts
- lib/projectApi.ts
- lib/taskApi.ts

## 8. 현재 화면 상태

### 랜딩 페이지

TaskFlow의 서비스 소개와 시작하기 링크를 표시합니다.

### 로그인 페이지

현재 UI만 구현되어 있습니다.

- 이메일 입력
- 비밀번호 입력
- 로그인 버튼
- 회원가입 링크

아직 Supabase Auth와 연결되지 않았습니다.

### 회원가입 페이지

현재 UI만 구현되어 있습니다.

- 이메일 입력
- 비밀번호 입력
- 비밀번호 확인 입력
- 회원가입 버튼
- 로그인 링크

이메일 인증을 사용하지 않는 방향으로 구현할 예정입니다.

### 대시보드

현재는 실제 데이터 대신 0으로 된 요약 카드를 표시합니다.

예정된 요약 정보:

- 전체 프로젝트 수
- 전체 할 일 수
- 완료한 할 일 수
- 오늘 마감인 할 일
- 최근 프로젝트

### 프로젝트 페이지

프로젝트 목록과 생성·상세·수정 화면의 뼈대를 만들었습니다.

현재는 실제 프로젝트 데이터가 없기 때문에 빈 상태 또는 예시 화면이 표시됩니다.

### 할 일 페이지

할 일 생성·상세·수정 화면의 뼈대를 만들었습니다.

현재 폼에는 다음 입력 UI가 있습니다.

- 제목
- 설명
- 상태
- 우선순위
- 마감일

## 9. 실행 방법

반드시 taskflow 폴더로 이동한 뒤 실행합니다.

    cd submissions/4-2/taskflow
    npm install
    npm run dev

브라우저에서 다음 주소를 엽니다.

    http://localhost:5173/

### 404가 발생했을 때

개발 서버를 submissions/4-2에서 실행하면 404가 발생할 수 있습니다. 그 폴더에는 TaskFlow의 index.html이 없기 때문입니다.

잘못된 방법:

    cd submissions/4-2
    npm run dev

올바른 방법:

    cd submissions/4-2/taskflow
    npm run dev

이미 잘못된 개발 서버가 실행 중이면 Ctrl+C로 종료한 뒤 올바른 폴더에서 다시 실행합니다.

## 10. 검증 명령어

코드 문법과 ESLint 규칙을 확인합니다.

    npm run lint

배포용 빌드가 가능한지 확인합니다.

    npm run build

현재 검증 결과:

- npm run lint 통과
- npm run build 통과

## 11. 아직 구현하지 않은 내용

현재는 초기 프론트엔드 구조만 완성된 상태입니다.

아직 구현하지 않은 내용:

- Supabase 프로젝트 연결
- Supabase Auth 회원가입
- Supabase Auth 로그인
- 로그아웃
- 보호 라우트
- projects 테이블 연결
- tasks 테이블 연결
- 프로젝트 CRUD
- 할 일 CRUD
- RLS 정책
- 로딩·에러·빈 상태의 실제 데이터 처리
- 폼 유효성 검증과 제출 중 상태
- Vercel 배포

## 12. 다음 구현 순서

### 1단계: Supabase 프로젝트 준비

- Supabase 프로젝트 생성
- 이메일 인증 없이 회원가입하도록 Auth 설정 확인
- projects 테이블 생성
- tasks 테이블 생성
- 환경변수 준비

### 2단계: 인증 연결

- lib/supabase.ts 생성
- useAuth.ts 커스텀 훅 작성
- 회원가입 연결
- 로그인 연결
- 로그아웃 연결
- 로그인 상태 확인
- 보호 라우트 연결

### 3단계: 프로젝트 데이터 연결

- useProjects.ts 작성
- 프로젝트 목록 조회
- 프로젝트 생성
- 프로젝트 수정
- 프로젝트 보관
- 프로젝트 상세 조회

### 4단계: 할 일 데이터 연결

- useTasks.ts 작성
- 프로젝트별 할 일 목록 조회
- 할 일 생성
- 할 일 상세 조회
- 할 일 수정
- 할 일 상태 변경
- 할 일 삭제

### 5단계: 사용자 경험 보완

- 필수값 검증
- 제출 중 버튼 비활성화
- 로딩 UI
- 에러 UI
- 빈 상태 UI
- 상태·우선순위 필터
- 프로젝트 진행률

### 6단계: 배포

- 환경변수 등록
- npm run build 확인
- Vercel 배포
- 배포 URL에서 회원가입·로그인·CRUD 테스트

## 13. 현재 단계의 완료 조건

- [x] React + TypeScript 프로젝트 생성
- [x] Tailwind CSS 설정
- [x] React Router 설치
- [x] 기본 레이아웃 구성
- [x] 주요 라우트 연결
- [x] 페이지 화면 뼈대 구성
- [x] Project·Task 타입 정의
- [x] ESLint 검사 통과
- [x] production build 통과
- [ ] Supabase 연결
- [ ] 실제 인증 구현
- [ ] 실제 CRUD 구현

