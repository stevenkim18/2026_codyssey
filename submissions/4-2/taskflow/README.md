# TaskFlow

프로젝트 안에 할 일을 등록하고, 상태·우선순위·마감일을 관리하는 개인용 생산성 서비스입니다.

현재는 Supabase 연결 전 단계로, React 화면 구조와 라우팅을 먼저 구성한 상태입니다.

## 기술 스택

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Supabase 예정
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
- 프로젝트 목록·상세·생성·수정 화면 뼈대
- 할 일 상세·생성·수정 화면 뼈대
- Not Found 페이지
- Project와 Task TypeScript 타입
- 공통 레이아웃과 재사용 UI 컴포넌트

## 다음 구현 단계

1. Supabase 프로젝트와 테이블 생성
2. 이메일·비밀번호 회원가입과 로그인 연결
3. 보호 라우트와 사용자별 데이터 접근 설정
4. 프로젝트 CRUD 연결
5. 할 일 CRUD 연결
6. 로딩·에러·빈 상태와 폼 검증 보완
7. Vercel 배포
