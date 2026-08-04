# 항목 4 평가 대비: 상태 객체와 모바일 퍼스트

항목 4는 상태를 어떻게 관리하는지, 그리고 반응형 CSS를 어떤 순서와 기준으로 작성하는지를 확인합니다.

## 평가 질문

- 상태(STATE) 객체를 따로 관리하는 이유와, 단순 변수만 사용할 때의 차이를 설명할 수 있는가?
- 반응형 디자인을 모바일 퍼스트로 작성한 이유를 설명할 수 있는가?

---

## 1. 상태(State)란 무엇인가요?

상태는 현재 화면과 기능의 상황을 나타내는 값입니다. 상태가 바뀌면 사용자에게 보여주는 화면도 달라질 수 있습니다.

| 상태 | 가능한 값 | 화면 변화 |
| --- | --- | --- |
| 테마 | light, dark | 배경과 글자 색상 변화 |
| 모바일 메뉴 | 열림, 닫힘 | 메뉴 표시 여부 변화 |
| API 요청 | loading, success, error, empty | 로딩·카드·오류 문구 변화 |
| 폼 필드 | 유효, 오류 | 오류 스타일과 안내 문구 변화 |

상태를 이해할 때는 다음 두 질문을 합니다.

~~~
지금 무엇이 바뀌었는가?
그 값이 바뀌면 화면의 어느 부분이 달라지는가?
~~~

---

## 2. STATE 객체란 무엇인가요?

관련된 상태를 하나의 객체 안에서 관리하는 방법입니다.

~~~javascript
const STATE = {
  theme: "light",
  menuOpen: false,
  projects: {
    status: "loading",
    data: [],
    error: null,
  },
};
~~~

이 객체는 애플리케이션의 현재 상황을 한곳에 모아 보여줍니다.

~~~
STATE.theme           → 현재 테마
STATE.menuOpen        → 모바일 메뉴 열림 여부
STATE.projects.status → API 상태
STATE.projects.data   → 프로젝트 데이터
STATE.projects.error  → API 오류 정보
~~~

### 2-1. 왜 상태를 객체로 묶나요?

- 관련된 값을 한곳에서 볼 수 있습니다.
- 같은 상태를 여러 곳에서 따로 저장해 값이 어긋나는 문제를 줄입니다.
- 어떤 이벤트가 어떤 값을 바꾸었는지 추적하기 쉽습니다.
- 필터, 정렬, 로그인 사용자처럼 기능이 늘어날 때 구조적으로 확장할 수 있습니다.

예를 들어 상태를 바꾸는 흐름을 명시적으로 표현할 수 있습니다.

~~~javascript
STATE.theme = "dark";
STATE.projects.status = "success";
~~~

### 2-2. 단순 변수만 사용하면 안 되나요?

작은 기능에서는 단순 변수로도 충분합니다.

~~~javascript
let currentTheme = "light";
let isMenuOpen = false;
let projectStatus = "loading";
~~~

문제는 기능이 커질 때 생깁니다.

- 상태 변수가 여러 함수와 파일에 흩어질 수 있습니다.
- 같은 의미의 값이 여러 개 생길 수 있습니다.
- 변수만 바꾸고 화면 업데이트를 빠뜨릴 수 있습니다.
- 어떤 이벤트가 어떤 값을 바꾸었는지 추적하기 어려워집니다.

따라서 STATE 객체는 “변수로 처리하면 절대 안 된다”는 규칙이 아닙니다. 관련 상태가 많아질 때 일관되게 관리하기 위한 구조입니다.

---

## 3. 현재 프로젝트의 상태 관리 방식

현재 <code>js/main.js</code>에는 이름이 <code>STATE</code>인 중앙 객체가 직접 정의되어 있지 않습니다. 대신 기능별 값과 DOM 속성을 상태 저장소처럼 사용합니다. 평가에서는 이 점을 실제 코드에 근거해 설명해야 합니다.

### 3-1. 테마 상태

현재 테마는 <code>body.dataset.theme</code>에 저장합니다.

~~~javascript
const isDark = theme === "dark";
body.dataset.theme = isDark ? "dark" : "light";
~~~

새로고침 후에도 유지하기 위해 <code>localStorage</code>에도 저장합니다.

~~~javascript
localStorage.setItem("portfolio-theme", isDark ? "dark" : "light");
~~~

~~~
현재 페이지에서 사용할 테마 → body.dataset.theme
새로고침 후 불러올 테마 → localStorage
~~~

### 3-2. 모바일 메뉴 상태

메뉴가 열렸는지는 <code>navMenu</code>의 <code>active</code> 클래스와 버튼의 <code>aria-expanded</code> 속성으로 표현합니다.

~~~javascript
const isOpen = navMenu.classList.toggle("active");
navToggle.setAttribute("aria-expanded", String(isOpen));
~~~

CSS는 <code>active</code> 클래스가 있을 때 메뉴를 보여줍니다.

~~~css
.nav-menu {
  display: none;
}

.nav-menu.active {
  display: flex;
}
~~~

별도의 <code>isMenuOpen</code> 변수 대신 DOM의 클래스와 ARIA 속성이 현재 메뉴 상태를 표시합니다.

### 3-3. API 상태

API 상태는 문자열 변수 하나로 저장하기보다 <code>showProjectState</code>가 DOM의 <code>hidden</code> 상태를 바꾸는 방식으로 표현합니다.

~~~javascript
const showProjectState = (state) => {
  projectStatus.hidden = state !== "loading";
  projectError.hidden = state !== "error";
  projectsGrid.hidden = state !== "success";
};
~~~

~~~
loading → projectStatus 표시
success → projectsGrid 표시
error   → projectError 표시
empty   → projectStatus에 빈 상태 문구 표시
~~~

### 3-4. 현재 구현을 평가에서 설명하는 방법

> 현재 코드는 중앙 STATE 객체를 사용하기보다 body.dataset.theme, localStorage, DOM의 active·hidden·aria-expanded 속성, API 응답 배열 등에 기능별 상태를 나누어 관리합니다. 작은 프로젝트에서는 각 기능의 상태와 화면이 가까이 있어 이해하기 쉽습니다. 다만 기능이 더 많아지면 상태가 여러 곳에 흩어질 수 있으므로, 테마·메뉴·API 상태를 하나의 STATE 객체로 모으면 변경 흐름과 기준값을 더 명확하게 만들 수 있습니다.

---

## 4. STATE 객체를 적용한다면

다음은 상태 객체를 활용하는 개념적인 예시입니다. 현재 프로젝트에 그대로 적용되어 있다는 뜻이 아니라, 상태를 중앙화하는 방법을 보여주는 예시입니다.

~~~javascript
const STATE = {
  theme: "light",
  projects: {
    status: "loading",
    items: [],
    error: null,
  },
};

const setTheme = (theme) => {
  STATE.theme = theme;
  renderTheme();
};

const renderTheme = () => {
  const isDark = STATE.theme === "dark";
  body.dataset.theme = STATE.theme;
  themeLabel.textContent = isDark ? "Dark" : "Light";
};
~~~

이 구조에서는 값을 바꾸는 함수와 화면을 반영하는 함수를 구분할 수 있습니다.

~~~
setTheme("dark")
→ STATE.theme 변경
→ renderTheme() 호출
→ DOM과 CSS 업데이트
~~~

상태 객체를 도입할 때는 객체만 만드는 것으로 끝나지 않습니다. 상태를 변경한 뒤 항상 관련 화면을 다시 렌더링하는 규칙도 함께 정해야 합니다.

---

## 5. 모바일 퍼스트란 무엇인가요?

모바일 퍼스트는 작은 화면을 기본으로 작성한 뒤, 화면이 넓어질수록 <code>min-width</code> 미디어 쿼리로 레이아웃을 확장하는 방식입니다.

~~~css
/* 기본: 모바일 */
.layout {
  display: grid;
  grid-template-columns: 1fr;
}

/* 태블릿 이상 */
@media (min-width: 768px) {
  .layout {
    grid-template-columns: 1fr 1fr;
  }
}
~~~

### 5-1. 모바일부터 작성하는 이유

- 모바일은 화면이 좁아 모든 요소를 동시에 보여주기 어렵기 때문에 콘텐츠 우선순위를 먼저 정할 수 있습니다.
- 기본 스타일을 단순하게 작성하고, 넓은 화면에서 필요한 규칙만 추가할 수 있습니다.
- 터치 영역, 글자 크기, 줄바꿈, 가로 스크롤 방지 같은 사용성을 먼저 확인할 수 있습니다.
- 데스크톱 스타일을 먼저 만든 뒤 모바일에서 많은 규칙을 덮어쓰는 것보다 예외 규칙이 줄어들 수 있습니다.

---

## 6. 현재 프로젝트의 반응형 규칙

현재 프로젝트는 다음 화면 구간을 사용합니다.

~~~
767px 이하  → 모바일 메뉴, 한 열 레이아웃
768~1023px  → 태블릿 레이아웃
1024px 이상 → 데스크톱 간격과 섹션 크기
~~~

모바일에서 메뉴를 숨기고 햄버거 버튼을 표시합니다.

~~~css
@media (max-width: 767px) {
  .nav-toggle {
    display: block;
  }

  .nav-menu {
    display: none;
  }

  .nav-menu.active {
    display: flex;
  }
}
~~~

여러 열을 모바일에서 한 열로 변경합니다.

~~~css
@media (max-width: 767px) {
  .hero-grid,
  .split-layout,
  .contact-layout {
    grid-template-columns: 1fr;
  }

  .skills-grid {
    grid-template-columns: 1fr;
  }
}
~~~

### 6-1. 현재 코드에 대한 정확한 설명

현재 CSS는 기본 규칙에 데스크톱용 두 열·세 열 레이아웃을 먼저 작성하고, <code>@media (max-width: 767px)</code>에서 모바일 스타일로 덮어쓰는 부분이 있습니다.

예를 들어 기본 규칙은 다음과 같습니다.

~~~css
.hero-grid {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
~~~

화면 동작 자체는 반응형이지만, 작성 순서만 놓고 보면 엄밀한 의미의 모바일 퍼스트라기보다 “데스크톱 기본 + 모바일 덮어쓰기”에 가깝습니다.

평가에서는 다음처럼 정확하게 설명할 수 있습니다.

> 모바일 구간에서는 한 열 레이아웃과 햄버거 메뉴를 적용하고, 768px 이상에서 태블릿·데스크톱 레이아웃으로 확장하도록 브레이크포인트를 나누었습니다. 현재 CSS는 일부 기본 규칙이 데스크톱 기준이고 모바일 미디어 쿼리에서 덮어쓰는 구조이므로, 요구사항의 모바일 퍼스트 원칙을 더 엄밀히 맞추려면 모바일 스타일을 기본 규칙으로 옮긴 뒤 min-width 미디어 쿼리에서 넓은 화면 스타일을 추가할 수 있습니다.

---

## 7. 모바일 퍼스트로 개선하는 방향

모바일 퍼스트로 바꾸려면 기본 규칙을 모바일로 작성하고 넓은 화면의 변화만 <code>min-width</code>에 둡니다.

~~~css
/* 기본: 모바일 */
.hero-grid,
.split-layout,
.contact-layout,
.skills-grid {
  grid-template-columns: 1fr;
}

.nav-toggle {
  display: block;
}

.nav-menu {
  display: none;
}

/* 태블릿 */
@media (min-width: 768px) {
  .hero-grid,
  .split-layout,
  .contact-layout {
    grid-template-columns: 1fr 1fr;
  }

  .skills-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 데스크톱 */
@media (min-width: 1024px) {
  .hero-grid {
    grid-template-columns: 1.1fr 0.9fr;
  }

  .skills-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .nav-toggle {
    display: none;
  }

  .nav-menu {
    display: flex;
  }
}
~~~

실제 리팩터링을 할 때는 기존의 <code>max-width</code> 규칙과 중복되지 않도록 정리해야 합니다. 위 코드는 작성 방향을 이해하기 위한 예시입니다.

---

## 8. 평가 직전 답변 요약

### 상태 객체

> 상태는 테마, 메뉴 열림 여부, API 요청 상태처럼 현재 화면의 상황을 나타내는 값입니다. 관련 상태를 STATE 객체에 모으면 기준값이 한곳에 모이고, 어떤 이벤트가 어떤 값을 바꾸는지 추적하기 쉽습니다. 현재 프로젝트는 중앙 STATE 객체 대신 data-theme, localStorage, DOM 클래스와 hidden 속성으로 기능별 상태를 관리하고 있습니다. 프로젝트가 커지면 이를 하나의 객체로 통합하는 것이 더 명확합니다.

### 모바일 퍼스트

> 모바일 퍼스트는 작은 화면의 기본 스타일을 먼저 작성하고 min-width 미디어 쿼리로 태블릿과 데스크톱 레이아웃을 확장하는 방식입니다. 모바일의 좁은 공간에서 콘텐츠 우선순위와 사용성을 먼저 정할 수 있고, 넓은 화면에서 필요한 스타일만 추가할 수 있습니다. 현재 프로젝트는 반응형 레이아웃을 구현했지만 일부 기본 규칙은 데스크톱 기준이라, 엄밀한 모바일 퍼스트를 위해서는 모바일 스타일을 기본 규칙으로 옮기는 개선이 가능합니다.

## 9. 직접 확인할 파일

- 상태·이벤트·API 흐름: [js/main.js](../js/main.js)
- 시맨틱 구조: [index.html](../index.html)
- Flexbox/Grid와 반응형 규칙: [css/style.css](../css/style.css)
- 항목 2 설명: [06-evaluation-item2.md](./06-evaluation-item2.md)
