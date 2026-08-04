# JavaScript, DOM, 이벤트 설명 자료

## 1. JavaScript의 역할

HTML이 구조를, CSS가 표현을 담당한다면 JavaScript는 사용자의 행동에 따른 동작을 담당합니다. 이 프로젝트에서 JavaScript는 메뉴, 테마, 스크롤, API, 폼을 연결합니다.

## 2. `defer`와 실행 시점

```html
<script src="js/main.js" defer></script>
```

`defer`는 HTML을 먼저 읽고 문서 분석이 끝난 뒤 JavaScript를 실행하도록 합니다. 따라서 JavaScript가 실행될 때 `querySelector`로 찾는 HTML 요소가 준비되어 있습니다.

## 3. DOM 선택과 변경

- `querySelector`: 조건에 맞는 첫 번째 요소 하나를 선택합니다.
- `querySelectorAll`: 조건에 맞는 여러 요소를 선택합니다.
- `textContent`: 텍스트 내용을 변경합니다.
- `innerHTML`: HTML 문자열을 삽입합니다.
- `classList.add/remove/toggle`: 클래스를 추가·삭제·전환합니다.
- `setAttribute`: 접근성 속성이나 상태 속성을 변경합니다.

예를 들어 햄버거 메뉴는 다음 흐름으로 동작합니다.

```javascript
const isOpen = navMenu.classList.toggle("active");
navToggle.setAttribute("aria-expanded", String(isOpen));
```

클릭할 때마다 메뉴의 `active` 클래스가 바뀌고, CSS가 그 클래스에 따라 메뉴를 보이거나 숨깁니다.

## 4. 이벤트 처리

HTML에 `onclick`을 직접 작성하지 않고 JavaScript에서 이벤트를 연결했습니다.

```javascript
themeToggle.addEventListener("click", () => {
  const nextTheme = body.dataset.theme === "dark" ? "light" : "dark";
  setTheme(nextTheme);
});
```

이벤트 처리의 기본 구조는 다음과 같습니다.

```text
이벤트 대상 선택
→ addEventListener로 이벤트 연결
→ 이벤트 핸들러 함수 실행
→ 상태 변경
→ DOM 갱신
```

사용한 주요 이벤트는 다음과 같습니다.

- `click`: 메뉴, 테마, 재시도, 맨 위로 버튼
- `scroll`: 네비게이션과 맨 위로 버튼 표시 상태
- `input`: 폼 입력 중 실시간 검증
- `submit`: 폼 제출 검증

## 5. JavaScript 기본 문법

- `const`: 다시 대입하지 않는 변수
- `let`: 값이 바뀔 수 있는 변수
- 화살표 함수: 짧은 함수 표현식
- 템플릿 리터럴: 백틱으로 문자열과 변수를 함께 표현
- 구조분해 할당: 객체에서 필요한 값을 바로 추출

프로젝트 카드 함수에서 GitHub 객체의 값을 구조분해로 추출합니다.

```javascript
const createProjectCard = ({
  name,
  description,
  html_url: htmlUrl,
  language,
}, index) => `...`;
```

## 6. 배열 메서드

- `filter`: 포크와 아카이브 저장소를 제외합니다.
- `slice`: 최대 6개만 선택합니다.
- `map`: 저장소 객체를 프로젝트 카드 HTML로 변환합니다.
- `forEach`: 여러 DOM 요소에 이벤트를 연결합니다.
- `every`: 폼의 모든 필드가 유효한지 확인합니다.

```javascript
const visibleRepositories = repositories
  .filter(({ fork, archived }) => !fork && !archived)
  .slice(0, portfolioConfig.projectLimit);

projectsGrid.innerHTML = visibleRepositories.map(createProjectCard).join("");
```

## 7. 평가 질문

### `querySelector`와 `querySelectorAll`의 차이는 무엇인가요?

`querySelector`는 첫 번째 요소 하나를 반환하고, `querySelectorAll`은 조건에 맞는 여러 요소를 반환합니다. 여러 메뉴 링크나 폼 필드에 같은 이벤트를 연결할 때 `querySelectorAll`을 사용했습니다.

### 왜 `onclick` 대신 `addEventListener`를 사용했나요?

HTML과 JavaScript의 역할을 분리하고, 하나의 요소에 여러 이벤트를 관리하기 쉽도록 하기 위해서입니다.

### `innerHTML`과 `textContent`의 차이는 무엇인가요?

`textContent`는 텍스트를 그대로 넣고, `innerHTML`은 HTML 문자열을 해석합니다. 프로젝트 카드처럼 여러 태그를 포함한 동적 마크업을 만들 때 `innerHTML`을 사용했습니다.

