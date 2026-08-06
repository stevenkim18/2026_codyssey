# TaskFlow

프로젝트 안에 할 일을 등록하고, 상태·우선순위·마감일을 관리하는 개인용 생산성 서비스입니다.

Supabase Auth와 Database를 연결해 개인별 프로젝트·할 일 데이터를 관리합니다.

## 기술 스택

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Supabase Auth / Database / RLS
- Vercel 배포 준비 완료

## 실행 방법

```bash
npm install
npm run dev
```

개발 서버 실행 후 터미널에 표시되는 주소를 브라우저에서 엽니다.

## 검증 명령어

```bash
npm run lint
npm run build
```

## 현재 구현된 내용

- Vite + React + TypeScript 프로젝트
- Tailwind CSS 설정
- React Router 기본 라우팅
- 랜딩·로그인·회원가입·대시보드 화면
- Supabase 클라이언트와 환경변수 타입
- 이메일·비밀번호 회원가입, 로그인, 로그아웃
- 로그인 사용자 전용 보호 라우트
- 프로젝트 조회·생성·수정·삭제·보관
- 할 일 조회·생성·수정·삭제
- 대시보드 통계와 최근 할 일
- 현재 로그인한 사용자에게 샘플 프로젝트·할 일을 추가하는 기능
- 로딩·에러·빈 상태와 폼 검증
- Not Found 페이지
- Project와 Task TypeScript 타입
- 공통 레이아웃과 재사용 UI 컴포넌트
- `useProjects` 커스텀 훅을 통한 프로젝트·할 일 목록 조회와 새로고침

## 구조와 구현 이유

- `pages`: URL 단위 화면과 화면 전용 상태를 관리합니다.
- `components`: `PageHeader`, 카드, 배지, 빈 상태, 로딩 상태, 에러 상태처럼 여러 화면에서 반복되는 UI를 재사용합니다.
- `hooks`: `useProjects`가 프로젝트와 할 일 목록을 함께 조회하고 로딩·에러·새로고침 상태를 관리합니다. 페이지가 Supabase 호출과 비동기 생명주기를 직접 알 필요가 없도록 분리했습니다.
- `lib`: Supabase API 함수와 오류 메시지 변환을 화면과 분리합니다.
- `contexts`: 인증 세션을 앱 전체에서 공유하고 보호 라우트와 인증 화면이 같은 상태를 사용하게 합니다.

### 데이터 흐름 설명

`/projects` 라우트가 `ProjectListPage`를 렌더링하면 `useProjects`의 `useEffect`가 실행됩니다. 훅은 `getProjects`와 `getTasks`를 병렬 조회하고 결과를 state에 저장합니다. state가 바뀌면 페이지가 다시 렌더링되어 로딩·에러·빈 상태 중 하나와 프로젝트 카드를 보여줍니다. 생성·수정·삭제는 각 폼 또는 상세 화면의 이벤트 핸들러가 `lib`의 API 함수를 호출한 뒤 `navigate` 또는 목록 재조회로 화면을 갱신합니다.

### Supabase를 선택한 이유

인증과 관계형 데이터를 한 서비스에서 구성하고, `user_id`와 RLS 정책으로 사용자별 프로젝트·할 일 데이터를 제한하기 위해 Supabase를 선택했습니다. 구현 과정에서는 세션 조회가 비동기로 완료되기 전에 보호 라우트가 렌더링되지 않도록 `AuthProvider`의 로딩 상태를 사용했고, 프로젝트 삭제 시 연결된 할 일이 함께 삭제되도록 외래 키의 `on delete cascade` 설정을 전제로 했습니다.

## 다음 확인 단계

1. Supabase에서 이메일 자동 확인과 `projects`, `tasks`의 select/insert/update/delete RLS 정책을 확인합니다.
2. 테스트 계정을 만든 후 프로젝트와 할 일 CRUD를 직접 확인합니다.
3. 다른 계정으로 로그인해 이전 계정의 데이터가 보이지 않는지 확인합니다.
4. Vercel 배포 시 `.env.local`의 두 환경변수를 프로젝트 환경변수에 등록하고 배포 URL에서 새로고침·CRUD를 확인합니다.
