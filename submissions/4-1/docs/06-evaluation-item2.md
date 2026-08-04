# 항목 2 평가 대비: 파일 분리, 시맨틱 HTML, CSS 변수, 이벤트 연결

이 문서는 평가 항목 2의 질문에 답하기 위한 설명 자료입니다. 단순히 개념을 외우기보다, 현재 프로젝트의 실제 파일과 코드를 기준으로 “왜 이렇게 작성했는가?”를 설명하는 것을 목표로 합니다.

## 평가 항목 2에서 확인하는 것

평가자는 다음 네 가지를 확인합니다.

1. HTML, CSS, JavaScript를 왜 파일로 나누었고, 각 파일이 어떤 역할을 하는지 설명할 수 있는가?
2. `header`, `nav`, `main`, `section`, `footer` 같은 시맨틱 태그를 어떤 기준으로 선택했는지 설명할 수 있는가?
3. `:root`의 CSS 변수는 무엇이며, 변수로 관리했을 때 어떤 장점이 있는지 설명할 수 있는가?
4. HTML의 `onclick` 대신 JavaScript의 `addEventListener`를 사용한 이유를 두 방식의 차이와 함께 설명할 수 있는가?

---

## 1. HTML, CSS, JavaScript를 파일로 분리한 이유

### 1-1. 세 파일의 역할

웹페이지를 만들 때 세 기술은 서로 다른 일을 담당합니다.

| 파일 | 담당하는 일 | 현재 프로젝트의 예시 |
| --- | --- | --- |
| `index.html` | 콘텐츠의 구조와 의미 | 제목, 메뉴, 섹션, 카드 영역, 폼 |
| `css/style.css` | 색상, 글꼴, 크기, 배치, 반응형 디자인 | 다크 모드 색상, Grid, 모바일 메뉴 스타일 |
| `js/main.js` | 사용자 행동과 동적인 변화 | 버튼 클릭, API 요청, 폼 검증, 스크롤 처리 |

쉽게 비유하면 다음과 같습니다.

```text
HTML = 건물의 뼈대와 방의 용도
CSS  = 벽지, 가구 배치, 조명 같은 외관
JS   = 스위치를 눌렀을 때 불이 켜지는 동작
```

`index.html`에 페이지 구조를 작성하고, CSS와 JavaScript 파일을 연결합니다.

```html
<link rel="stylesheet" href="css/style.css" />
<script src="js/main.js" defer></script>
```

이 코드는 다음과 같은 의미입니다.

- `link`: `css/style.css`의 스타일을 현재 HTML에 적용합니다.
- `script`: `js/main.js`의 JavaScript를 현재 HTML에서 실행합니다.
- `defer`: HTML을 먼저 분석한 뒤 JavaScript를 실행합니다. 따라서 JavaScript가 HTML 요소를 찾을 때 요소가 이미 준비되어 있습니다.

### 1-2. 현재 프로젝트의 파일별 구현

#### `index.html`

페이지에 어떤 내용이 있는지를 작성합니다.

```html
<h1>작은 디테일로 더 나은 경험을 만듭니다.</h1>
<section id="projects">
  <h2>만들면서 배운 것들.</h2>
  <div id="projects-grid"></div>
</section>
```

여기에는 “프로젝트 영역이 존재한다”는 구조가 들어 있습니다. 프로젝트 카드의 실제 내용은 나중에 JavaScript가 GitHub API 응답을 이용해 채웁니다.

#### `css/style.css`

HTML 요소가 어떻게 보일지를 작성합니다.

```css
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}
```

이 규칙은 프로젝트 카드 영역을 화면 너비에 맞춰 여러 열로 배치합니다. CSS 파일에 스타일을 모아두었기 때문에 HTML의 구조를 읽을 때 색상이나 여백 코드가 섞이지 않습니다.

#### `js/main.js`

사용자 행동에 따라 페이지가 바뀌는 동작을 작성합니다.

```javascript
themeToggle.addEventListener("click", () => {
  const nextTheme = body.dataset.theme === "dark" ? "light" : "dark";
  setTheme(nextTheme);
});
```

이 코드는 테마 버튼을 클릭했을 때 현재 테마의 반대 테마를 적용합니다. HTML에는 버튼이 있다는 사실만 작성하고, 버튼을 눌렀을 때 무엇을 할지는 JavaScript가 담당합니다.

### 1-3. 분리했을 때의 장점

#### 역할을 구분할 수 있습니다

화면 구조를 바꾸려면 HTML, 디자인을 바꾸려면 CSS, 동작을 바꾸려면 JavaScript를 우선 확인하면 됩니다. 파일 하나에 모든 코드가 섞여 있을 때보다 문제를 찾기 쉽습니다.

#### 유지보수가 쉬워집니다

예를 들어 프로젝트 카드의 색상만 바꾸고 싶다면 `index.html`이나 `main.js`를 수정할 필요 없이 `style.css`의 관련 규칙을 수정하면 됩니다.

#### 코드 재사용이 쉬워집니다

하나의 CSS 파일을 여러 HTML 페이지에 연결할 수 있고, 하나의 JavaScript 함수도 여러 요소에 재사용할 수 있습니다.

#### 협업하기 좋습니다

HTML을 담당하는 사람, 스타일을 담당하는 사람, 기능을 담당하는 사람이 서로의 영역을 덜 침범하면서 작업할 수 있습니다. 한 파일의 같은 줄을 동시에 수정할 가능성도 줄어듭니다.

### 1-4. 평가에서 말할 수 있는 답변

> `index.html`은 페이지의 구조와 콘텐츠, `css/style.css`는 색상·배치·반응형 스타일, `js/main.js`는 이벤트와 동적인 화면 변경을 담당하도록 분리했습니다. 이렇게 역할을 나누면 각 파일의 책임이 명확해지고, 디자인이나 기능을 수정할 때 관련 파일만 찾으면 되므로 유지보수와 협업이 쉬워집니다. 또한 HTML에 `defer`로 JavaScript를 연결해 문서가 준비된 뒤 스크립트가 실행되도록 했습니다.

---

## 2. 시맨틱 태그를 선택한 기준

### 2-1. 시맨틱 HTML이란?

시맨틱(semantic)은 “의미가 있는”이라는 뜻입니다. 시맨틱 HTML은 단순히 화면을 배치하는 것이 아니라, 각 영역의 역할이 태그 이름에 드러나도록 작성하는 방법입니다.

`div`는 의미가 없는 일반 컨테이너입니다. 반면 `header`, `nav`, `main`, `section`, `article`, `footer`는 콘텐츠의 역할을 설명합니다.

```html
<!-- 의미를 알기 어려운 구조 -->
<div class="top">...</div>
<div class="menu">...</div>
<div class="content">...</div>

<!-- 영역의 역할이 드러나는 구조 -->
<header>...</header>
<nav>...</nav>
<main>...</main>
```

시맨틱 태그는 화면을 예쁘게 만드는 태그가 아닙니다. 브라우저, 검색 엔진, 스크린 리더 같은 보조 기술이 문서의 구조와 콘텐츠의 역할을 이해하도록 돕는 태그입니다.

### 2-2. 태그를 고르는 기준

태그를 선택할 때 “어떤 모양으로 보이는가?”보다 “이 콘텐츠의 역할은 무엇인가?”를 먼저 생각합니다.

| 태그 | 선택 기준 | 현재 프로젝트 |
| --- | --- | --- |
| `header` | 페이지 또는 특정 영역의 머리말 | 고정된 사이트 헤더 |
| `nav` | 다른 페이지나 섹션으로 이동하는 주요 메뉴 | About, Skills, Projects, Contact 메뉴 |
| `main` | 페이지에서 가장 중요한 하나의 콘텐츠 영역 | Hero부터 Contact까지 |
| `section` | 하나의 주제를 가진 콘텐츠 묶음 | About, Skills, Projects, Contact |
| `article` | 다른 곳에 옮겨도 독립적인 의미가 있는 콘텐츠 | 각각의 Skills 카드, 프로젝트 카드 |
| `footer` | 페이지 하단의 저작권, 링크, 추가 정보 | 저작권과 GitHub·Contact 링크 |
| `div` | 별도의 의미가 없는 단순한 스타일·배치용 묶음 | 카드 내부 레이아웃, 버튼 묶음 |

### 2-3. 현재 HTML의 구조

현재 `index.html`은 다음과 같은 문서 구조를 가지고 있습니다.

```text
body
├── header.site-header
│   └── nav.nav
│       ├── 로고
│       ├── 모바일 메뉴 버튼
│       └── 메뉴 링크와 테마 버튼
├── main#main-content
│   ├── section#hero
│   ├── section#about
│   ├── section#skills
│   │   └── article.skill-card × 3
│   ├── section#projects
│   │   └── article.project-card × 여러 개
│   └── section#contact
└── footer.site-footer
```

예를 들어 프로젝트 영역은 다음처럼 작성되어 있습니다.

```html
<section class="section section-muted" id="projects" aria-labelledby="projects-title">
  <h2 id="projects-title">만들면서 배운 것들.</h2>
  <div class="projects-grid" id="projects-grid"></div>
</section>
```

이때 `section`을 선택한 이유는 Projects가 페이지 안에서 “프로젝트”라는 하나의 주제를 가진 독립적인 영역이기 때문입니다. `aria-labelledby="projects-title"`를 사용해 이 영역의 제목이 `id="projects-title"`인 `h2`임도 명확하게 연결했습니다.

JavaScript가 만드는 각각의 프로젝트 카드는 독립적으로 제목, 설명, GitHub 링크를 가지므로 `article`을 사용합니다.

```javascript
const createProjectCard = ({ name, description, html_url: htmlUrl }, index) => `
  <article class="project-card">
    <h3>${name}</h3>
    <p>${description || "설명이 등록되지 않은 프로젝트입니다."}</p>
    <a href="${htmlUrl}">저장소 열기</a>
  </article>`;
```

### 2-4. 시맨틱 태그의 장점

#### 코드를 읽기 쉽습니다

클래스 이름을 모두 확인하지 않아도 `<nav>`를 보면 메뉴 영역이라는 것을 알 수 있습니다. 나중에 코드를 다시 보거나 다른 사람이 코드를 평가할 때 구조를 빠르게 파악할 수 있습니다.

#### 접근성이 좋아집니다

스크린 리더는 랜드마크 역할을 가진 `nav`, `main`, `footer` 등을 사용자가 이동할 수 있는 영역으로 안내할 수 있습니다. 키보드나 스크린 리더 사용자가 페이지를 탐색하기 쉬워집니다.

#### 검색 엔진이 구조를 이해하기 쉽습니다

콘텐츠의 제목과 본문, 주요 영역이 분명하므로 검색 엔진이 페이지 내용을 해석하는 데 도움이 됩니다. 단, 시맨틱 태그를 사용한다고 검색 순위가 자동으로 올라가는 것은 아니며, 구조와 콘텐츠를 올바르게 작성하는 것이 중요합니다.

### 2-5. 시맨틱 태그를 사용할 때 주의할 점

- 모든 것을 `div`로 작성하지 않습니다.
- 반대로 의미가 맞지 않는데도 시맨틱 태그를 억지로 사용하지 않습니다.
- `section`에는 보통 해당 영역을 설명하는 제목을 둡니다.
- 클릭 동작이 필요한 요소는 `div`보다 `button`이나 `a`를 사용합니다.
- 페이지의 최상위 `main`은 일반적으로 하나만 둡니다.

### 2-6. 평가에서 말할 수 있는 답변

> 태그의 모양이 아니라 콘텐츠의 역할을 기준으로 선택했습니다. 전체 상단 메뉴는 `header` 안의 `nav`, 페이지의 핵심 콘텐츠는 `main`, About·Skills·Projects·Contact처럼 주제가 나뉘는 영역은 `section`, 독립적으로 읽을 수 있는 각각의 기술 카드와 프로젝트 카드는 `article`, 하단 정보는 `footer`로 작성했습니다. 이렇게 하면 코드의 의도가 명확해지고 검색 엔진과 스크린 리더도 페이지 구조를 이해하기 쉬워집니다.

---

## 3. CSS 변수(`:root`) 사용 방법

### 3-1. CSS 변수란?

CSS 변수는 자주 사용하는 값을 이름으로 저장해두고 다시 사용하는 기능입니다. 정확한 이름은 CSS 사용자 지정 속성(custom property)이며, 보통 `--`로 시작합니다.

```css
:root {
  --accent: #c6ed63;
  --text: #18211d;
}

button {
  color: var(--text);
  background: var(--accent);
}
```

위 코드에서 `--accent`와 `--text`가 변수 선언이고, `var(--accent)`와 `var(--text)`가 변수 사용입니다.

### 3-2. `:root`에 작성한 이유

`:root`는 문서의 가장 바깥 요소를 선택하는 의사 클래스입니다. HTML 문서에서는 보통 `html` 요소를 가리킵니다. 여기에 변수를 선언하면 페이지 전체에서 사용할 수 있습니다.

현재 프로젝트의 `:root`에는 색상, 그림자, 모서리 반지름, 컨테이너 최대 너비 같은 공통 값이 있습니다.

```css
:root {
  --bg: #f4f1eb;
  --surface: #fbfaf7;
  --text: #18211d;
  --muted: #66716b;
  --line: #d8d5ce;
  --accent: #c6ed63;
  --shadow: 0 18px 50px rgba(24, 33, 29, 0.09);
  --radius: 20px;
  --container: 1160px;
}
```

예를 들어 페이지 배경은 `background: var(--bg)`, 기본 글자색은 `color: var(--text)`, 카드의 모서리는 `border-radius: var(--radius)`처럼 사용합니다.

### 3-3. 다크 모드와 CSS 변수

다크 모드에서는 변수 이름은 그대로 두고 값만 바꿉니다.

```css
[data-theme="dark"] {
  --bg: #101613;
  --surface: #18211d;
  --text: #eef4ec;
  --muted: #a4b0a8;
  --line: #35423a;
}
```

JavaScript가 `body`에 `data-theme="dark"`를 설정하면, `[data-theme="dark"]` 규칙이 적용됩니다. 그러면 여러 요소가 직접 다크 모드를 판단하지 않아도 같은 변수 값을 사용하면서 전체 색상이 바뀝니다.

```javascript
body.dataset.theme = "dark";
```

```css
body {
  background: var(--bg);
  color: var(--text);
}
```

`body`의 테마 속성 하나가 바뀌고, `var(--bg)`와 `var(--text)`의 실제 값이 달라지면서 페이지 전체 색상이 바뀌는 구조입니다.

현재 프로젝트의 글꼴은 `body`와 일부 텍스트 요소에서 `font-family`를 직접 지정하고 있습니다. 즉, 색상과 그림자 등은 CSS 변수로 관리하고 있지만 글꼴까지 CSS 변수로 만든 것은 아닙니다. 글꼴도 변수로 관리하고 싶다면 다음처럼 확장할 수 있습니다.

```css
:root {
  --font-sans: "Manrope", sans-serif;
  --font-mono: "DM Mono", monospace;
}

body {
  font-family: var(--font-sans);
}
```

이처럼 현재 구현된 부분과 앞으로 개선할 수 있는 부분을 구분해서 설명하면 코드에 근거한 답변이 됩니다.

### 3-5. CSS 변수를 사용했을 때의 장점

#### 값을 한 곳에서 바꿀 수 있습니다

accent 색상을 여러 곳에서 사용하더라도 `--accent`의 값만 수정하면 관련 요소가 함께 바뀝니다.

```css
/* 변수 없이 작성하면 같은 색상 코드를 여러 곳에 반복해야 합니다. */
color: #c6ed63;
border-color: #c6ed63;
background: #c6ed63;

/* 변수로 작성하면 이름으로 의도를 알 수 있습니다. */
color: var(--accent);
border-color: var(--accent);
background: var(--accent);
```

#### 디자인의 일관성을 유지할 수 있습니다

버튼마다 서로 다른 녹색을 직접 입력하면 작은 차이가 생기기 쉽습니다. 공통 변수 하나를 사용하면 같은 역할의 요소가 같은 값을 사용합니다.

#### 테마를 쉽게 만들 수 있습니다

라이트 테마와 다크 테마가 같은 변수 이름을 공유하므로, 각 선택자마다 모든 색상 규칙을 새로 작성할 필요가 없습니다.

#### 코드의 의도가 읽힙니다

`#c6ed63`보다 `var(--accent)`가 “강조 색상”이라는 뜻을 더 잘 전달합니다. 숫자 값을 외우지 않아도 변수 이름으로 역할을 알 수 있습니다.

#### 유지보수 범위를 줄입니다

브랜드 색상이나 카드 모서리 값을 바꿀 때 여러 파일과 여러 선택자를 찾아다닐 필요가 줄어듭니다.

### 3-6. CSS 변수와 JavaScript 변수는 다릅니다

둘 다 값을 이름으로 관리하지만 동작하는 곳이 다릅니다.

| 구분 | CSS 변수 | JavaScript 변수 |
| --- | --- | --- |
| 사용 목적 | 스타일 값 관리 | 데이터와 로직 관리 |
| 선언 예시 | `--accent: #c6ed63` | `const nextTheme = "dark"` |
| 사용 위치 | CSS 속성의 `var(...)` | JavaScript 표현식 |
| 현재 프로젝트 | 색상, 그림자, 간격, 반지름 | 테마, API 데이터, 폼 검증 결과 |

### 3-7. 평가에서 말할 수 있는 답변

> `:root`에 색상, 그림자, 모서리 반지름, 컨테이너 너비를 CSS 변수로 정의했습니다. 여러 선택자에서 같은 값을 재사용할 수 있어 디자인의 일관성을 유지하고, 나중에 값을 바꿀 때 한 곳만 수정하면 됩니다. 현재 글꼴은 `font-family`로 직접 지정했지만, 글꼴도 `--font-sans` 같은 변수로 관리할 수 있습니다. 특히 `[data-theme="dark"]`에서 같은 변수 이름에 다크 테마용 값을 다시 지정해, JavaScript가 `body`의 테마 속성만 바꾸면 전체 페이지 색상이 전환되도록 구현했습니다.

---

## 4. `onclick`과 `addEventListener` 비교

### 4-1. `onclick` 방식

`onclick`은 HTML 태그에 클릭할 때 실행할 코드를 직접 적는 방식입니다.

```html
<button onclick="toggleTheme()">테마 변경</button>
```

간단한 실습에서는 빠르게 사용할 수 있지만, HTML 구조 안에 JavaScript 동작이 들어갑니다.

### 4-2. `addEventListener` 방식

`addEventListener`는 JavaScript에서 HTML 요소를 선택한 후 이벤트를 연결하는 방식입니다.

```html
<button class="theme-toggle" type="button">테마 변경</button>
```

```javascript
const themeToggle = document.querySelector(".theme-toggle");

themeToggle.addEventListener("click", () => {
  setTheme("dark");
});
```

HTML은 “테마 버튼이 있다”는 구조만 표현하고, 클릭 후 동작은 JavaScript에 모아둡니다.

### 4-3. 두 방식의 차이

| 비교 기준 | `onclick` 인라인 속성 | `addEventListener` |
| --- | --- | --- |
| 코드 위치 | HTML 태그 안 | JavaScript 파일 |
| 역할 분리 | 구조와 동작이 섞임 | HTML과 JavaScript가 분리됨 |
| 여러 이벤트 | 같은 속성에 관리하기 어려움 | 여러 리스너를 추가할 수 있음 |
| 재사용 | 전역 함수 이름에 의존하기 쉬움 | 함수와 요소를 조합해 재사용하기 쉬움 |
| 이벤트 옵션 | 사용이 제한적임 | `passive`, `once` 같은 옵션 사용 가능 |
| 유지보수 | HTML이 복잡해질 수 있음 | 동작을 한 파일에서 찾기 쉬움 |

### 4-4. 왜 이 프로젝트에서는 `addEventListener`를 사용했나요?

#### HTML과 JavaScript의 책임을 분리하기 위해서입니다

HTML에는 콘텐츠와 구조를 작성하고, 동작은 `main.js`에 모았습니다. 이렇게 하면 디자이너가 HTML 구조를 읽을 때 JavaScript 코드를 함께 해석하지 않아도 됩니다.

#### 전역 함수에 의존하지 않기 위해서입니다

`onclick="toggleTheme()"`을 사용하려면 브라우저가 찾을 수 있는 전역 함수가 필요합니다. JavaScript 파일의 함수 구조가 바뀌거나 모듈을 사용하게 되면 연결이 깨질 가능성이 있습니다. `addEventListener`는 선택한 요소와 함수의 연결을 JavaScript 안에서 관리합니다.

#### 하나의 요소에 여러 동작을 연결할 수 있기 때문입니다

```javascript
button.addEventListener("click", logClick);
button.addEventListener("click", updateAnalytics);
```

`addEventListener`는 서로 다른 리스너를 추가할 수 있습니다. 반면 `element.onclick = ...`처럼 이벤트 속성에 함수를 대입하는 방식은 새 대입으로 기존 함수를 덮어쓸 수 있습니다.

#### 여러 요소에 같은 동작을 적용하기 쉽기 때문입니다

현재 프로젝트에서는 여러 내비게이션 링크에 메뉴 닫기 동작을 연결합니다.

```javascript
document.querySelectorAll(".nav-link, .logo, .scroll-cue").forEach((link) => {
  link.addEventListener("click", () => closeMobileMenu());
});
```

이렇게 하면 각 링크의 HTML에 `onclick`을 반복해서 작성하지 않아도 됩니다.

#### 이벤트 옵션을 사용할 수 있기 때문입니다

스크롤 이벤트에는 다음처럼 `passive` 옵션을 사용했습니다.

```javascript
window.addEventListener("scroll", updateScrollUI, { passive: true });
```

이 리스너에서는 스크롤의 기본 동작을 막지 않겠다는 의도를 브라우저에 알려 스크롤 처리를 효율적으로 할 수 있습니다.

### 4-5. 현재 프로젝트의 이벤트 연결 예시

테마 버튼의 실제 흐름은 다음과 같습니다.

```text
1. JavaScript가 .theme-toggle 버튼을 선택한다.
2. addEventListener로 click 이벤트를 연결한다.
3. 사용자가 버튼을 클릭한다.
4. 현재 body.dataset.theme을 확인한다.
5. 다음 테마를 결정한다.
6. setTheme()이 data-theme, 버튼 글자, aria 속성, localStorage를 갱신한다.
7. CSS 변수가 새 값으로 적용되어 화면이 바뀐다.
```

코드로 보면 다음 두 부분이 연결되어 있습니다.

```javascript
themeToggle.addEventListener("click", () => {
  const nextTheme = body.dataset.theme === "dark" ? "light" : "dark";
  setTheme(nextTheme);
});
```

```javascript
const setTheme = (theme) => {
  const isDark = theme === "dark";
  body.dataset.theme = isDark ? "dark" : "light";
  themeToggle.setAttribute("aria-pressed", String(isDark));
  themeLabel.textContent = isDark ? "Dark" : "Light";
  localStorage.setItem("portfolio-theme", isDark ? "dark" : "light");
};
```

버튼 클릭 코드가 직접 모든 화면을 수정하는 것이 아니라, `setTheme`이라는 하나의 함수에 테마 변경 작업을 모아둔 점도 중요한 부분입니다.

### 4-6. 평가에서 말할 수 있는 답변

> `onclick`을 사용하면 HTML 안에 JavaScript 동작이 들어가 구조와 동작이 섞입니다. 또한 같은 요소의 이벤트를 관리하거나 여러 요소에 같은 동작을 재사용하기가 불편할 수 있습니다. 그래서 HTML에는 버튼과 링크의 구조만 작성하고, `main.js`에서 `querySelector`로 요소를 선택해 `addEventListener`로 이벤트를 연결했습니다. 이렇게 하면 역할이 분리되고, 여러 이벤트 리스너와 옵션을 관리하기 쉬우며, 유지보수와 재사용에도 유리합니다.

---

## 5. 평가 직전 1분 답변 요약

다음처럼 이어서 설명하면 네 가지 질문을 한 번에 답할 수 있습니다.

> 이 프로젝트는 `index.html`, `css/style.css`, `js/main.js`로 역할을 분리했습니다. HTML은 구조와 콘텐츠, CSS는 디자인과 반응형 레이아웃, JavaScript는 이벤트와 동작을 담당합니다. HTML 구조는 화면 모양이 아니라 콘텐츠의 역할을 기준으로 정해서, 메뉴는 `header` 안의 `nav`, 핵심 내용은 `main`, 주제별 영역은 `section`, 독립적인 카드는 `article`, 하단 정보는 `footer`를 사용했습니다. CSS에서는 `:root`에 공통 색상과 간격을 변수로 저장해 재사용하고, 다크 모드에서는 같은 변수 이름의 값만 바꿨습니다. 마지막으로 `onclick` 대신 `addEventListener`를 사용해 HTML과 JavaScript를 분리하고, 여러 요소와 이벤트를 관리하기 쉽게 했습니다.

## 6. 직접 확인할 파일

- HTML 구조: [`index.html`](../index.html)
- CSS 변수와 시맨틱 영역 스타일: [`css/style.css`](../css/style.css)
- 이벤트 연결과 DOM 변경: [`js/main.js`](../js/main.js)
- 기존 HTML/CSS 설명: [`01-html-css.md`](./01-html-css.md)
- 기존 JavaScript 설명: [`02-javascript-dom-event.md`](./02-javascript-dom-event.md)
