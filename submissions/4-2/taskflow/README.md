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
- Vercel 예정

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
- 프로젝트 조회·생성·수정·보관
- 할 일 조회·생성·수정·삭제
- 대시보드 통계와 최근 할 일
- 현재 로그인한 사용자에게 샘플 프로젝트·할 일을 추가하는 기능
- 로딩·에러·빈 상태와 폼 검증
- Not Found 페이지
- Project와 Task TypeScript 타입
- 공통 레이아웃과 재사용 UI 컴포넌트

## 다음 확인 단계

1. Supabase에서 이메일 자동 확인과 `projects`, `tasks` RLS 정책을 확인합니다.
2. 테스트 계정을 만든 후 프로젝트와 할 일 CRUD를 직접 확인합니다.
3. 다른 계정으로 로그인해 이전 계정의 데이터가 보이지 않는지 확인합니다.
4. Vercel 배포 시 `.env.local`의 두 환경변수를 프로젝트 환경변수에 등록합니다.
