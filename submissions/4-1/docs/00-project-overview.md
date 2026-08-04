# 프로젝트 개요와 평가 준비

## 1. 30초 소개

이 프로젝트는 외부 프레임워크 없이 HTML, CSS, JavaScript만으로 만든 반응형 개인 포트폴리오입니다. 페이지 구조는 시맨틱 HTML로 작성했고, CSS Flexbox와 Grid로 반응형 레이아웃을 구현했습니다. JavaScript에서는 사용자의 이벤트가 상태를 바꾸고, 그 상태에 맞춰 DOM을 다시 갱신하는 흐름을 직접 구현했습니다.

특히 다크 모드, 모바일 메뉴, 문의 폼, GitHub API 프로젝트 목록을 통해 브라우저에서 실제로 일어나는 이벤트·상태·렌더링의 관계를 확인할 수 있도록 만들었습니다.

## 2. 파일 구조

```text
4-1/
├── index.html              # 페이지 구조
├── css/style.css           # 변수, 레이아웃, 반응형, 시각 효과
├── js/main.js              # 이벤트, 상태, API, 폼 검증
├── images/profile.svg      # 프로필 이미지
├── images/*.png            # 제출용 스크린샷
├── docs/                   # 평가·학습 설명 자료
└── README.md               # 실행·배포·기능 요약
```

평가 항목별 상세 설명은 다음 문서에서 확인할 수 있습니다.

- 항목 2: [`06-evaluation-item2.md`](./06-evaluation-item2.md)
- 항목 3: [`07-evaluation-item3.md`](./07-evaluation-item3.md)
- 항목 4: [`08-evaluation-item4.md`](./08-evaluation-item4.md)

## 3. 요구사항과 구현 위치

| 요구사항 | 구현 위치 | 설명할 핵심 |
| --- | --- | --- |
| 시맨틱 HTML | `index.html` | `header`, `nav`, `main`, `section`, `article`, `footer`로 의미에 맞게 구조화 |
| 반응형 레이아웃 | `css/style.css` | 모바일·태블릿·데스크톱 대응, 768px·1024px 브레이크포인트 |
| Flexbox/Grid | `css/style.css` | 네비게이션은 Flexbox, 프로젝트 카드는 Grid |
| 햄버거 메뉴 | `js/main.js` | 클릭 → `active` 클래스 변경 → 메뉴 표시 변경 |
| 다크 모드 | `js/main.js`, `css/style.css` | 테마 상태 변경 → `data-theme` 변경 → CSS 변수 변경 → 저장 |
| GitHub API | `js/main.js` | `fetch` → JSON → `filter`/`slice`/`map` → 카드 렌더링 |
| API 상태 처리 | `index.html`, `js/main.js` | 로딩·성공·에러·빈 상태별 UI 전환 |
| 폼 검증 | `index.html`, `js/main.js` | 입력값 검증 → 근처 에러 메시지 → 성공 메시지 |
| 스크롤 애니메이션 | `js/main.js`, `css/style.css` | Intersection Observer가 `is-visible` 클래스를 추가 |

## 4. 핵심 흐름

이 프로젝트의 핵심은 “사용자 이벤트 → 상태 변경 → 화면 업데이트”입니다.

```text
사용자 행동
  ↓
이벤트 핸들러(addEventListener)
  ↓
상태 변경(class, data-theme, hidden, localStorage 등)
  ↓
DOM 업데이트(textContent, innerHTML, classList)
  ↓
사용자에게 변경된 화면 표시
```

### 흐름 1: 다크 모드

```text
테마 버튼 클릭
→ 현재 테마 확인
→ light/dark 상태 결정
→ body.dataset.theme 변경
→ CSS 변수 적용
→ localStorage에 저장
```

### 흐름 2: GitHub 프로젝트

```text
페이지 로드
→ 로딩 상태 표시
→ GitHub API fetch
→ 응답 성공 여부 확인
→ 비포크·비아카이브 저장소 필터링
→ 프로젝트 카드 HTML 생성
→ 성공 상태로 화면 갱신
```

실패하면 에러 메시지와 재시도 버튼을 표시하고, 저장소 배열이 비어 있으면 빈 상태 메시지를 표시합니다.

### 흐름 3: 문의 폼

```text
입력 또는 제출
→ 각 필드의 값 확인
→ 빈 값·이메일 형식 검사
→ 오류가 있으면 필드 근처에 메시지 표시
→ 모두 유효하면 기본 제출을 막고 성공 메시지 표시
```

## 5. 평가 시 시연 순서

1. 데스크톱 화면에서 전체 섹션과 네비게이션 앵커를 보여줍니다.
2. 모바일 화면으로 줄여 햄버거 메뉴를 열고 닫습니다.
3. 다크 모드를 전환한 뒤 새로고침해 설정이 유지되는지 확인합니다.
4. Projects에서 GitHub API로 카드가 생성되는 것을 설명합니다.
5. 문의 폼을 빈 상태로 제출해 오류를 보여줍니다.
6. 잘못된 이메일을 입력한 뒤 형식 검사를 보여줍니다.
7. 정상 값을 입력해 성공 메시지를 보여줍니다.
8. 스크롤 60px·300px 기준의 네비게이션과 맨 위로 버튼을 보여줍니다.

## 6. 자주 받을 질문과 답변

### 왜 React를 사용하지 않았나요?

이 과제의 목표가 React 이전에 필요한 DOM 조작, 이벤트, 비동기 처리의 원리를 익히는 것이기 때문입니다. React는 이 흐름을 컴포넌트와 상태라는 방식으로 추상화하지만, 이 프로젝트에서는 브라우저 API를 직접 사용했습니다.

### 가장 중요한 구현 흐름은 무엇인가요?

다크 모드, GitHub API, 문의 폼에서 이벤트 또는 비동기 요청이 발생하고, 상태가 바뀐 뒤, `classList`, `hidden`, `textContent`, `innerHTML`로 화면을 갱신합니다.

### API가 실패하면 어떻게 되나요?

`response.ok`가 `false`이면 오류를 발생시키고 `catch`에서 에러 상태를 표시합니다. 사용자는 다시 시도 버튼으로 API 요청을 재실행할 수 있습니다.

### 프로젝트에서 직접 바꿔야 하는 값은 무엇인가요?

`js/main.js`의 `portfolioConfig.githubUsername`, `index.html`의 이름·이메일·소셜 링크를 본인의 정보로 확인하면 됩니다.
