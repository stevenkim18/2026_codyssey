# JavaScript 이벤트 처리: onclick과 addEventListener

## 1. 문서의 목표

이 문서는 HTML의 onclick 인라인 이벤트와 JavaScript의 addEventListener를 비교합니다.

특히 다음 평가 질문에 답할 수 있도록 정리합니다.

> onclick 인라인 속성 대신 addEventListener를 사용한 이유를 두 방식의 차이와 함께 설명할 수 있는가?

다룰 내용은 다음과 같습니다.

- 이벤트와 이벤트 핸들러의 기본 개념
- onclick 인라인 방식의 동작
- addEventListener 방식의 동작
- 두 방식의 차이와 장단점
- 여러 이벤트와 여러 요소를 관리하는 방법
- 이벤트 옵션과 이벤트 객체
- HTML, CSS, JavaScript를 분리하는 이유
- 현재 프로젝트에서 addEventListener를 사용한 이유
- 평가에서 말할 수 있는 답변

---

## 2. 이벤트란 무엇인가요?

이벤트(event)는 브라우저에서 발생한 사건입니다.

사용자가 직접 일으키는 사건도 있고, 브라우저가 자동으로 발생시키는 사건도 있습니다.

| 이벤트 | 발생하는 상황 |
| --- | --- |
| click | 버튼이나 링크를 클릭했을 때 |
| input | 입력창의 값이 바뀔 때 |
| submit | 폼을 제출할 때 |
| keydown | 키보드 키를 눌렀을 때 |
| mouseenter | 마우스가 요소 위에 들어왔을 때 |
| scroll | 페이지를 스크롤할 때 |
| load | 문서나 리소스가 로드되었을 때 |

이벤트가 발생했을 때 실행할 함수를 이벤트 핸들러(event handler)라고 합니다.

~~~text
사용자 행동
  ↓
이벤트 발생(click)
  ↓
이벤트 핸들러 실행
  ↓
상태 변경
  ↓
화면 갱신
~~~

예를 들어 다크 모드 버튼에서는 다음 흐름이 일어납니다.

~~~text
테마 버튼 클릭
  ↓
click 이벤트 발생
  ↓
테마 변경 함수 실행
  ↓
body의 data-theme 변경
  ↓
CSS 변수 변경
  ↓
화면이 다크 모드로 변경
~~~

---

## 3. onclick 인라인 방식

### 3.1 기본 문법

onclick 인라인 방식은 HTML 태그의 속성에 클릭 동작을 직접 작성합니다.

~~~html
<button onclick="toggleTheme()">테마 변경</button>
~~~

사용자가 버튼을 클릭하면 브라우저가 toggleTheme 함수를 찾아 실행합니다.

~~~html
<button onclick="alert('클릭했습니다')">
  클릭
</button>
~~~

간단한 예제를 빠르게 만들 수 있다는 장점이 있습니다.

### 3.2 함수 호출 방식

보통 HTML에서는 함수를 호출하고, 함수의 실제 내용은 JavaScript에 작성합니다.

~~~html
<button onclick="showMessage()">메시지 표시</button>
~~~

~~~javascript
function showMessage() {
  alert("안녕하세요");
}
~~~

하지만 일반적인 script 환경에서는 HTML의 onclick 코드가 전역에서 접근할 수 있는 함수에 의존하게 됩니다.

### 3.3 HTML에 동작이 섞이는 문제

다음 HTML은 버튼의 구조와 JavaScript 동작이 함께 들어 있습니다.

~~~html
<button
  class="theme-toggle"
  type="button"
  onclick="toggleTheme()"
>
  테마 변경
</button>
~~~

HTML을 읽는 사람은 버튼의 역할뿐 아니라 클릭 시 실행될 함수 이름도 함께 확인해야 합니다. 페이지에 버튼이 많아지면 HTML에 동작 코드가 반복될 수 있습니다.

~~~html
<button onclick="openMenu()">메뉴</button>
<button onclick="closeMenu()">닫기</button>
<button onclick="saveForm()">저장</button>
~~~

---

## 4. addEventListener 방식

### 4.1 기본 문법

addEventListener는 JavaScript에서 요소를 선택한 다음 이벤트와 함수를 연결하는 방식입니다.

~~~html
<button class="theme-toggle" type="button">
  테마 변경
</button>
~~~

~~~javascript
const themeToggle = document.querySelector(".theme-toggle");

themeToggle.addEventListener("click", () => {
  toggleTheme();
});
~~~

HTML에는 버튼의 구조와 콘텐츠만 남고, JavaScript 파일에서 클릭 후 동작을 관리합니다.

### 4.2 함수 이름을 직접 전달하기

실행할 함수가 이벤트 객체를 사용하지 않는다면 함수를 호출하지 않고 전달할 수 있습니다.

~~~javascript
const button = document.querySelector(".button");

button.addEventListener("click", handleClick);

function handleClick() {
  console.log("버튼이 클릭되었습니다.");
}
~~~

다음처럼 작성하면 안 됩니다.

~~~javascript
button.addEventListener("click", handleClick());
~~~

handleClick()은 이벤트가 발생하기 전에 즉시 실행됩니다. addEventListener에는 실행 결과가 아니라 나중에 실행할 함수 자체를 전달해야 합니다.

### 4.3 화살표 함수로 작성하기

짧은 동작은 화살표 함수로 바로 작성할 수 있습니다.

~~~javascript
button.addEventListener("click", () => {
  console.log("버튼이 클릭되었습니다.");
});
~~~

실행할 내용이 한 줄이면 다음처럼 줄일 수도 있습니다.

~~~javascript
button.addEventListener("click", () => console.log("클릭"));
~~~

동작이 길어지면 이름 있는 함수를 분리하는 편이 읽기 쉽습니다.

---

## 5. onclick과 addEventListener 비교

### 5.1 기본 비교

| 비교 기준 | onclick 인라인 속성 | addEventListener |
| --- | --- | --- |
| 코드 위치 | HTML 태그 안 | JavaScript 파일 |
| 역할 분리 | 구조와 동작이 섞임 | HTML과 JavaScript가 분리됨 |
| 여러 요소에 적용 | HTML마다 반복하기 쉬움 | 선택한 여러 요소에 반복 적용 가능 |
| 여러 핸들러 | 관리가 불편함 | 여러 리스너를 추가할 수 있음 |
| 재사용 | 전역 함수에 의존하기 쉬움 | 함수와 요소를 조합하기 쉬움 |
| 이벤트 옵션 | 사용할 수 있는 범위가 제한적임 | once, passive, capture 등을 사용할 수 있음 |
| 유지보수 | HTML이 복잡해질 수 있음 | 동작을 JavaScript에서 찾기 쉬움 |
| 적합한 상황 | 아주 간단한 실습이나 테스트 | 실제 프로젝트와 규모 있는 코드 |

### 5.2 역할 분리

onclick 방식:

~~~html
<button onclick="toggleTheme()">테마 변경</button>
~~~

addEventListener 방식:

~~~html
<button class="theme-toggle" type="button">
  테마 변경
</button>
~~~

~~~javascript
const themeToggle = document.querySelector(".theme-toggle");

themeToggle.addEventListener("click", toggleTheme);
~~~

addEventListener 방식에서는 다음처럼 역할이 나뉩니다.

- HTML: 버튼이라는 구조와 텍스트
- CSS: 버튼의 모양과 상태 스타일
- JavaScript: 클릭 후 실행할 동작

이 분리는 코드의 책임을 명확하게 하고, 파일별로 수정할 위치를 쉽게 찾도록 합니다.

### 5.3 여러 이벤트 핸들러 연결

addEventListener는 같은 요소에 여러 이벤트 리스너를 추가할 수 있습니다.

~~~javascript
button.addEventListener("click", logClick);
button.addEventListener("click", updateCounter);
~~~

버튼을 클릭하면 두 함수가 모두 실행됩니다.

반면 onclick 속성에 동작을 하나만 작성하는 방식은 여러 동작을 관리하기 불편합니다.

또한 JavaScript에서 onclick 프로퍼티에 함수를 대입하는 방식도 주의해야 합니다.

~~~javascript
button.onclick = logClick;
button.onclick = updateCounter;
~~~

두 번째 대입이 첫 번째 함수를 덮어쓸 수 있습니다. addEventListener는 서로 다른 리스너를 별도로 등록합니다.

### 5.4 여러 요소에 같은 이벤트 연결

메뉴 링크 여러 개에 같은 동작을 적용해야 한다고 가정해 보겠습니다.

onclick 방식은 각 HTML 요소에 속성을 반복해서 작성할 수 있습니다.

~~~html
<a href="#about" onclick="closeMenu()">소개</a>
<a href="#projects" onclick="closeMenu()">프로젝트</a>
<a href="#contact" onclick="closeMenu()">연락처</a>
~~~

addEventListener 방식은 JavaScript에서 여러 요소를 선택한 뒤 반복해서 연결할 수 있습니다.

~~~javascript
const links = document.querySelectorAll(".nav-link");

links.forEach((link) => {
  link.addEventListener("click", closeMenu);
});
~~~

동작의 이름이 HTML에 반복되지 않고, 연결 규칙이 JavaScript에 한 곳에 모입니다.

### 5.5 이벤트 옵션

addEventListener는 이벤트 동작을 조정하는 옵션을 사용할 수 있습니다.

~~~javascript
window.addEventListener("scroll", updateScrollUI, {
  passive: true
});
~~~

자주 사용하는 옵션은 다음과 같습니다.

| 옵션 | 의미 |
| --- | --- |
| once | 이벤트를 한 번만 실행한 뒤 리스너 제거 |
| passive | 핸들러가 기본 동작을 막지 않는다고 알림 |
| capture | 이벤트 전파의 캡처 단계에서 처리 |

한 번만 실행해야 하는 이벤트에는 once를 사용할 수 있습니다.

~~~javascript
window.addEventListener("load", initialize, {
  once: true
});
~~~

스크롤 이벤트처럼 기본 동작을 막지 않는 리스너에는 passive를 사용할 수 있습니다.

---

## 6. 이벤트 객체

addEventListener의 핸들러는 이벤트 객체를 받을 수 있습니다.

~~~javascript
button.addEventListener("click", (event) => {
  console.log(event.type);   // "click"
  console.log(event.target); // 실제 클릭된 요소
});
~~~

이벤트 객체에는 이벤트와 관련된 정보가 들어 있습니다.

### 6.1 기본 동작 막기

폼 제출이나 링크 이동처럼 브라우저의 기본 동작을 막아야 할 때 preventDefault를 사용합니다.

~~~javascript
form.addEventListener("submit", (event) => {
  event.preventDefault();
  console.log("기본 제출 대신 JavaScript로 처리합니다.");
});
~~~

현재 프로젝트에서는 문의 폼을 실제 서버로 제출하지 않고, JavaScript에서 검증 결과와 성공 메시지를 표시하므로 preventDefault를 사용합니다.

### 6.2 이벤트 대상 구분하기

target은 실제로 이벤트가 발생한 요소입니다.

~~~javascript
button.addEventListener("click", (event) => {
  event.target.classList.toggle("active");
});
~~~

여러 요소에 같은 리스너를 연결할 때 target을 활용할 수 있습니다.

---

## 7. 이벤트 전파와 addEventListener

브라우저 이벤트는 요소 하나에서만 끝나지 않고 부모 방향으로 전달될 수 있습니다. 이를 이벤트 버블링이라고 합니다.

~~~html
<div class="card">
  <button class="delete-button">삭제</button>
</div>
~~~

~~~javascript
card.addEventListener("click", () => {
  console.log("카드 클릭");
});

deleteButton.addEventListener("click", (event) => {
  event.stopPropagation();
  console.log("삭제 버튼 클릭");
});
~~~

삭제 버튼을 클릭했을 때 카드의 click까지 실행되지 않게 하려면 stopPropagation을 사용할 수 있습니다.

이벤트 전파를 활용하면 부모 하나에 리스너를 연결해 여러 자식 요소를 처리하는 이벤트 위임(event delegation)도 구현할 수 있습니다.

~~~javascript
list.addEventListener("click", (event) => {
  if (event.target.matches(".delete-button")) {
    removeItem(event.target);
  }
});
~~~

동적으로 추가되는 자식 요소까지 처리해야 할 때 유용합니다.

---

## 8. HTML과 JavaScript를 분리하는 이유

### 8.1 책임이 명확해집니다

프로젝트의 파일을 다음처럼 나눌 수 있습니다.

~~~text
index.html       → 문서 구조와 콘텐츠
css/style.css    → 색상, 간격, 배치, 반응형
js/main.js       → 이벤트, 상태 변경, DOM 갱신
~~~

onclick을 사용하면 HTML에 JavaScript 동작이 들어가 역할이 섞입니다.

addEventListener를 사용하면 HTML에는 구조만 남기고, 동작은 JavaScript 파일에 모을 수 있습니다.

### 8.2 유지보수가 쉬워집니다

테마 변경 방식을 수정한다고 가정해 보겠습니다.

onclick 방식에서는 여러 HTML 요소의 onclick 속성과 연결된 함수 이름을 확인해야 할 수 있습니다.

addEventListener 방식에서는 JavaScript에서 이벤트 연결 부분과 핸들러를 찾으면 됩니다.

### 8.3 재사용이 쉬워집니다

같은 closeMenu 함수를 여러 내비게이션 링크에 연결할 수 있습니다.

~~~javascript
document
  .querySelectorAll(".nav-link, .logo, .scroll-cue")
  .forEach((link) => {
    link.addEventListener("click", closeMobileMenu);
  });
~~~

HTML에 같은 onclick 코드를 반복할 필요가 없습니다.

### 8.4 전역 함수 의존성을 줄입니다

onclick="toggleTheme()" 방식은 HTML이 toggleTheme이라는 함수를 찾을 수 있어야 합니다. 함수가 전역에 노출되지 않거나 JavaScript가 모듈 방식으로 변경되면 연결이 깨질 수 있습니다.

addEventListener는 JavaScript 안에서 요소와 함수를 직접 연결하므로 이러한 전역 이름 의존성을 줄일 수 있습니다.

### 8.5 콘텐츠 보안 정책과의 충돌을 줄일 수 있습니다

웹사이트에서 엄격한 Content Security Policy(CSP)를 사용하는 경우 인라인 JavaScript 실행을 제한할 수 있습니다. onclick 인라인 코드는 정책에 따라 차단될 수 있지만, 외부 JavaScript 파일에서 addEventListener로 연결하는 방식은 분리된 스크립트 정책에 맞추기 쉽습니다.

---

## 9. 접근성과 이벤트 처리

이벤트 처리 방식과 함께 HTML 요소의 의미도 중요합니다.

클릭 동작이 필요한 요소는 가능하면 div보다 button이나 a를 사용합니다.

~~~html
<!-- 버튼 동작에는 button 사용 -->
<button class="theme-toggle" type="button">
  테마 변경
</button>

<!-- 다른 위치로 이동에는 a 사용 -->
<a href="#projects">프로젝트로 이동</a>
~~~

button은 키보드로도 사용할 수 있고, 스크린 리더가 버튼으로 이해할 수 있습니다.

다음처럼 div에 onclick을 붙이는 것은 피하는 편이 좋습니다.

~~~html
<div onclick="toggleMenu()">메뉴</div>
~~~

div는 기본적으로 버튼처럼 키보드로 조작되지 않습니다. 꼭 사용자 동작을 받는 요소라면 의미에 맞는 HTML 요소를 사용합니다.

---

## 10. 현재 프로젝트에서의 적용

현재 프로젝트는 HTML의 onclick 인라인 속성을 사용하지 않고 JavaScript에서 addEventListener로 이벤트를 연결합니다.

### 10.1 테마 버튼

~~~javascript
themeToggle.addEventListener("click", () => {
  const nextTheme = body.dataset.theme === "dark" ? "light" : "dark";
  setTheme(nextTheme);
});
~~~

동작 순서는 다음과 같습니다.

~~~text
1. .theme-toggle 요소를 선택
2. click 이벤트 연결
3. 사용자가 버튼 클릭
4. 현재 테마 확인
5. 다음 테마 결정
6. setTheme 실행
7. data-theme, aria 속성, localStorage 갱신
8. CSS 변수 적용
~~~

### 10.2 모바일 메뉴

~~~javascript
navToggle.addEventListener("click", () => {
  const isOpen = navMenu.classList.toggle("active");
  navToggle.setAttribute("aria-expanded", String(isOpen));
});
~~~

클릭 이벤트가 발생하면 메뉴의 active 클래스와 aria-expanded 속성이 함께 바뀝니다.

### 10.3 여러 내비게이션 링크

~~~javascript
document
  .querySelectorAll(".nav-link, .logo, .scroll-cue")
  .forEach((link) => {
    link.addEventListener("click", () => closeMobileMenu());
  });
~~~

여러 요소에 같은 모바일 메뉴 닫기 동작을 반복해서 연결합니다.

### 10.4 스크롤 이벤트

~~~javascript
window.addEventListener("scroll", updateScrollUI, {
  passive: true
});
~~~

스크롤이 일어날 때 네비게이션 스타일과 맨 위로 버튼 표시 상태를 갱신합니다. passive 옵션은 이 리스너가 스크롤의 기본 동작을 막지 않는다는 것을 브라우저에 알려줍니다.

### 10.5 문의 폼

~~~javascript
contactForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const isValid = fields.map(validateField).every(Boolean);

  if (isValid) {
    showFormSuccess();
  }
});
~~~

폼 제출 이벤트에서 기본 페이지 이동을 막고, 각 필드의 유효성을 검사한 뒤 결과에 따라 화면을 갱신합니다.

---

## 11. 언제 onclick을 사용할 수 있나요?

onclick이 항상 잘못된 것은 아닙니다.

다음과 같은 상황에서는 간단한 onclick이 이해하기 쉬울 수 있습니다.

- 짧은 HTML 실습
- 이벤트 처리 방법을 처음 테스트하는 작은 예제
- 하나의 파일 안에서 동작을 빠르게 확인하는 프로토타입

~~~html
<button onclick="alert('테스트')">테스트</button>
~~~

하지만 페이지가 커지거나 여러 요소와 상태를 관리해야 한다면 addEventListener가 더 적합합니다.

선택의 핵심은 “onclick을 절대 쓰면 안 된다”가 아니라, 프로젝트 규모와 유지보수 필요성입니다.

---

## 12. 평가 답변 예시

### 짧은 답변

> onclick은 HTML에 JavaScript 동작을 직접 작성하는 인라인 방식이라 HTML 구조와 동작이 섞입니다. 반면 addEventListener는 JavaScript에서 요소와 이벤트 핸들러를 연결하므로 역할을 분리할 수 있습니다. 또한 여러 요소에 같은 동작을 적용하거나 여러 이벤트 리스너와 once, passive 같은 옵션을 관리하기 쉽습니다. 그래서 이 프로젝트에서는 HTML에는 구조만 작성하고 JavaScript의 addEventListener로 이벤트를 연결했습니다.

### 조금 더 자세한 답변

> onclick 방식은 버튼 태그 안에 onclick="함수()"를 작성하는 방식입니다. 간단하지만 HTML에 JavaScript 코드가 들어가 구조와 동작이 섞이고, 여러 요소에 같은 이벤트를 적용할 때 코드가 반복될 수 있습니다. addEventListener는 JavaScript에서 요소를 선택한 뒤 click, input, submit 같은 이벤트를 연결합니다. 따라서 HTML, CSS, JavaScript의 역할을 분리할 수 있고, 여러 요소에 같은 함수를 재사용하거나 하나의 요소에 여러 리스너를 추가할 수 있습니다. 또한 현재 프로젝트의 스크롤 이벤트처럼 passive 옵션도 사용할 수 있습니다. 이런 유지보수성과 확장성 때문에 addEventListener를 선택했습니다.

### 현재 프로젝트를 포함한 답변

> 이 프로젝트는 index.html은 구조, style.css는 디자인과 반응형, main.js는 이벤트와 동작을 담당하도록 역할을 분리했습니다. 그래서 HTML의 onclick 인라인 속성 대신 main.js에서 querySelector로 요소를 선택하고 addEventListener로 이벤트를 연결했습니다. 예를 들어 테마 버튼의 click 이벤트가 발생하면 현재 테마를 확인하고 setTheme을 실행해 data-theme, aria 속성, localStorage를 갱신합니다. addEventListener를 사용하면 여러 내비게이션 링크에 같은 닫기 동작을 연결할 수 있고, 스크롤 이벤트에는 passive 옵션도 적용할 수 있어 유지보수와 확장에 유리합니다.

---

## 13. 최종 요약

### onclick

~~~html
<button onclick="toggleTheme()">테마 변경</button>
~~~

- HTML에서 바로 동작을 연결합니다.
- 짧은 실습에는 편리합니다.
- HTML과 JavaScript의 역할이 섞일 수 있습니다.
- 여러 이벤트와 요소를 관리하기에는 불편할 수 있습니다.

### addEventListener

~~~javascript
const button = document.querySelector(".theme-toggle");

button.addEventListener("click", toggleTheme);
~~~

- JavaScript에서 이벤트를 연결합니다.
- HTML과 JavaScript를 분리할 수 있습니다.
- 여러 요소와 이벤트를 관리하기 쉽습니다.
- 이벤트 옵션과 이벤트 객체를 활용할 수 있습니다.

### 기억할 기준

> 작은 테스트에는 onclick도 가능하지만, 실제 프로젝트에서는 역할 분리와 유지보수를 위해 addEventListener를 사용하는 것이 적합합니다.

현재 프로젝트의 핵심 흐름은 다음과 같습니다.

~~~text
HTML 요소 선택
→ addEventListener로 이벤트 연결
→ 사용자 행동
→ 이벤트 핸들러 실행
→ 상태 변경
→ DOM과 CSS 갱신
~~~

