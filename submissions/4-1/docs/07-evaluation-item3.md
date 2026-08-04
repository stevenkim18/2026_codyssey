# 항목 3 평가 대비: 상태 흐름, API, 배열 메서드, 레이아웃

항목 3은 기능을 실행하는 것뿐 아니라, 코드가 **이벤트 → 상태 변경 → 화면 업데이트** 순서로 어떻게 이어지는지 설명할 수 있는지를 확인합니다.

## 평가 질문

- 다크 모드, API 호출, 폼 검증 중 하나를 예로 들어 이벤트 → 상태 변경 → 화면 업데이트 흐름을 설명할 수 있는가?
- <code>async/await</code>와 <code>try/catch</code>로 API 성공과 실패를 어떻게 나누었는가?
- <code>map</code>, <code>filter</code>로 GitHub 데이터를 카드 UI로 어떻게 변환하는가?
- Flexbox와 Grid를 각각 어디에 사용했고, 왜 선택했는가?

---

## 1. 이벤트 → 상태 변경 → 화면 업데이트

| 단계 | 뜻 | 이 프로젝트의 예시 |
| --- | --- | --- |
| 이벤트 | 사용자 행동이나 브라우저의 변화 | 버튼 클릭, 입력, 제출, 스크롤, 페이지 로드 |
| 상태 변경 | 현재 상황을 나타내는 값을 변경 | 테마, 메뉴 열림 여부, API 상태, 폼 유효성 |
| 화면 업데이트 | 변경 결과를 DOM·CSS에 반영 | 클래스, <code>hidden</code>, <code>textContent</code>, CSS 변수 변경 |

### 1-1. 다크 모드의 전체 흐름

다크 모드는 이벤트부터 화면 변화까지 연결해서 설명하기 좋은 예시입니다.

~~~
테마 버튼 클릭
→ 현재 body.dataset.theme 확인
→ light 또는 dark 결정
→ body의 data-theme과 localStorage 변경
→ 버튼 글자·ARIA 속성 변경
→ CSS 변수 변경
→ 전체 화면 색상 변경
~~~

HTML에는 버튼의 구조만 있습니다.

~~~html
<button class="theme-toggle" type="button" aria-pressed="false">
  <span class="theme-icon" aria-hidden="true">☼</span>
  <span class="theme-label">Light</span>
</button>
~~~

JavaScript가 <code>click</code> 이벤트를 연결하고 다음 테마를 계산합니다.

~~~javascript
themeToggle.addEventListener("click", () => {
  const nextTheme = body.dataset.theme === "dark" ? "light" : "dark";
  setTheme(nextTheme);
});
~~~

<code>setTheme</code>은 테마 상태와 화면에 필요한 값을 함께 갱신합니다.

~~~javascript
const setTheme = (theme) => {
  const isDark = theme === "dark";
  body.dataset.theme = isDark ? "dark" : "light";
  themeToggle.setAttribute("aria-pressed", String(isDark));
  themeIcon.textContent = isDark ? "☾" : "☼";
  themeLabel.textContent = isDark ? "Dark" : "Light";
  localStorage.setItem("portfolio-theme", isDark ? "dark" : "light");
};
~~~

CSS는 <code>data-theme</code>에 따라 같은 변수의 값을 다르게 사용합니다.

~~~css
body {
  background: var(--bg);
  color: var(--text);
}

[data-theme="dark"] {
  --bg: #101613;
  --text: #eef4ec;
}
~~~

따라서 버튼 클릭 코드가 모든 스타일을 직접 바꾸는 것이 아니라, 테마 속성과 CSS 변수를 연결해 전체 화면이 바뀝니다.

### 1-2. API와 폼도 같은 구조입니다

API에서는 페이지 로드가 이벤트 역할을 합니다.

~~~
페이지 로드
→ loading 상태 표시
→ GitHub API 요청
→ 성공이면 카드 렌더링
→ 데이터가 없으면 empty 표시
→ 요청 실패면 error와 재시도 버튼 표시
~~~

폼에서는 <code>input</code> 이벤트가 발생할 때 값을 검사하고 DOM을 갱신합니다.

~~~javascript
field.addEventListener("input", () => {
  validateField(field);
  formSuccess.hidden = true;
});
~~~

<code>validateField</code>는 오류가 있으면 <code>invalid</code> 클래스와 <code>aria-invalid</code>를 설정하고, 오류 문구를 <code>textContent</code>에 넣습니다.

### 1-3. 평가 답변 예시

> 다크 모드를 예로 들면, 먼저 테마 버튼의 click 이벤트를 받습니다. 현재 body.dataset.theme을 확인해 다음 테마를 정하고, setTheme에서 data-theme과 localStorage를 변경합니다. 버튼의 글자와 aria-pressed도 갱신하고, CSS는 새 테마의 변수를 적용합니다. 따라서 이벤트 → 테마 상태 변경 → DOM과 CSS 업데이트 순서로 동작합니다.

---

## 2. async/await와 try/catch로 API 처리하기

네트워크 요청은 언제 끝날지 알 수 없으므로 비동기로 처리합니다. 요청을 기다리는 동안 브라우저가 멈추지 않게 하기 위해서입니다.

현재 <code>loadProjects</code>의 핵심 구조는 다음과 같습니다.

~~~javascript
const loadProjects = async () => {
  showProjectState("loading");

  try {
    const response = await fetch(apiUrl);
    if (!response.ok) throw new Error("GitHub API 요청 실패");

    const repositories = await response.json();
    // 데이터 가공과 카드 렌더링
  } catch (error) {
    console.error("프로젝트를 불러오지 못했습니다.", error);
    showProjectState("error");
  }
};
~~~

### 코드별 의미

- <code>async</code>: 함수 안에서 <code>await</code>를 사용할 수 있게 합니다.
- <code>await fetch(...)</code>: API 응답이 올 때까지 다음 줄을 기다립니다.
- <code>response.ok</code>: HTTP 응답이 성공 범위인지 직접 확인합니다.
- <code>throw</code>: <code>response.ok</code>가 false일 때 실패 흐름으로 보냅니다.
- <code>response.json()</code>: 응답 본문을 JavaScript 배열·객체로 변환합니다.
- <code>try/catch</code>: 성공 흐름과 오류 흐름을 분리합니다.

<code>fetch</code>는 403, 404 같은 HTTP 오류에서 Promise 자체가 실패하지 않을 수 있습니다. 그래서 <code>response.ok</code>를 확인하고, 실패하면 직접 <code>throw</code>해야 합니다.

### 성공·빈 상태·실패는 다릅니다

| 상황 | 의미 | UI |
| --- | --- | --- |
| 성공 | 요청 성공 + 저장소 존재 | 프로젝트 카드 |
| 빈 상태 | 요청 성공 + 배열이 비어 있음 | “표시할 프로젝트가 없습니다” |
| 실패 | 네트워크 오류 또는 403·404 | 오류 문구 + 다시 시도 |

빈 배열은 오류가 아니므로 <code>catch</code>가 아니라 별도로 처리합니다.

~~~javascript
if (visibleRepositories.length === 0) {
  showProjectState("empty");
  projectStatus.hidden = false;
  projectStatus.innerHTML = "<span>표시할 프로젝트가 없습니다.</span>";
  return;
}
~~~

재시도 버튼은 같은 함수를 다시 사용합니다.

~~~javascript
retryProjects.addEventListener("click", loadProjects);
~~~

### 평가 답변 예시

> loadProjects를 async 함수로 만들고 fetch와 response.json() 앞에 await를 사용했습니다. 요청 전에는 로딩 상태를 표시하고, response.ok를 확인해 HTTP 실패도 처리합니다. 성공하면 데이터를 카드로 변환하고, 배열이 비어 있으면 빈 상태를 표시합니다. 네트워크 오류나 throw된 오류는 catch에서 처리해 오류 문구와 재시도 버튼을 보여줍니다.

---

## 3. filter와 map으로 GitHub 데이터를 카드로 변환하기

GitHub API가 반환하는 것은 카드 HTML이 아니라 저장소 객체 배열입니다. 화면에 표시하기 전에 다음 순서로 가공합니다.

~~~
전체 저장소 배열
→ filter: 제외할 저장소 제거
→ slice: 최대 개수 제한
→ map: 저장소 객체를 카드 HTML로 변환
→ join: 문자열 배열을 하나로 결합
→ innerHTML: 화면에 삽입
~~~

### 3-1. filter

~~~javascript
const visibleRepositories = repositories
  .filter(({ fork, archived }) => !fork && !archived);
~~~

<code>filter</code>는 조건이 true인 항목만 새 배열로 반환합니다. 이 코드는 포크 저장소와 아카이브 저장소를 제외합니다.

~~~
fork=false, archived=false → 표시
fork=true                  → 제외
archived=true              → 제외
~~~

### 3-2. slice

~~~javascript
.slice(0, portfolioConfig.projectLimit);
~~~

현재 <code>projectLimit</code>은 6입니다. <code>slice</code>는 원본 배열을 훼손하지 않고 처음부터 최대 6개를 선택합니다.

### 3-3. map

현재 코드의 <code>createProjectCard</code>는 저장소 객체 하나를 카드 HTML 문자열 하나로 변환합니다. 개념을 단순화하면 다음과 같습니다.

~~~javascript
const createProjectCard = (repository) => {
  const title = repository.name;
  const description = repository.description || "설명이 없습니다.";
  return "<article><h3>" + title + "</h3><p>" + description + "</p></article>";
};
~~~

실제 코드에서는 구조분해 할당과 템플릿 리터럴을 사용해 같은 작업을 더 읽기 쉽게 작성합니다. GitHub의 <code>html_url</code>은 <code>htmlUrl</code>이라는 이름으로 바꾸어 사용합니다.

### 3-4. join과 innerHTML

~~~javascript
projectsGrid.innerHTML = visibleRepositories
  .map(createProjectCard)
  .join("");
~~~

<code>map</code>의 결과는 카드 문자열 배열입니다. <code>join("")</code>으로 하나의 HTML 문자열로 합친 뒤 <code>innerHTML</code>에 넣어 화면에 표시합니다.

<code>map</code>은 값을 변환해 새 배열을 만들 때 사용하고, <code>forEach</code>는 새 배열이 필요하지 않고 각 항목에 작업만 실행할 때 사용합니다.

### 평가 답변 예시

> 먼저 filter로 포크와 아카이브 저장소를 제외하고, slice로 최대 6개를 선택합니다. map에 createProjectCard를 전달해 저장소 객체를 article 카드 HTML로 바꾸고, join("")으로 합친 뒤 projectsGrid.innerHTML에 삽입합니다. 즉, API 데이터 배열을 필터링하고 변환해 화면용 UI 목록으로 만든 과정입니다.

---

## 4. Flexbox와 Grid의 적용 위치와 선택 이유

| 구분 | Flexbox | Grid |
| --- | --- | --- |
| 방향 | 한 방향 배치 | 행과 열을 함께 배치 |
| 적합한 상황 | 메뉴, 버튼, 정렬 | 카드 목록, 큰 영역 나누기 |
| 현재 사용 위치 | 네비게이션, 카드 내부 | 프로젝트·스킬 카드, Hero·Contact 영역 |

### 4-1. 네비게이션은 Flexbox

~~~css
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 30px;
}
~~~

로고와 메뉴를 한 줄에서 양끝에 배치하고 간격을 조절해야 하므로 Flexbox를 사용했습니다. 버튼 묶음과 Footer 링크도 한 방향 정렬이므로 Flexbox가 적합합니다.

### 4-2. 프로젝트·스킬 카드는 Grid

~~~css
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 18px;
}
~~~

카드 목록은 화면 폭에 따라 열 개수가 달라져야 합니다. <code>auto-fit</code>과 <code>minmax</code>를 사용하면 카드가 너무 작아지지 않는 범위에서 3열·2열·1열로 자동 조정됩니다. 행과 열을 함께 다루므로 Grid를 선택했습니다.

### 4-3. 큰 영역과 카드 내부

Hero, About, Contact는 콘텐츠를 좌우 영역으로 나누므로 Grid를 사용합니다.

~~~css
.hero-grid,
.split-layout,
.contact-layout {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
}
~~~

반대로 카드 내부는 위에서 아래로 흐르게 하고 Footer를 아래에 붙여야 하므로 Flexbox를 사용합니다.

~~~css
.project-card {
  display: flex;
  flex-direction: column;
}

.project-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
}
~~~

### 평가 답변 예시

> 네비게이션은 로고와 메뉴를 한 방향으로 정렬하므로 Flexbox를 사용했습니다. 프로젝트와 스킬 카드는 행과 열의 개수가 화면 폭에 따라 달라지는 목록이므로 Grid를 사용했고, auto-fit과 minmax로 반응형 열을 만들었습니다. 카드 내부처럼 한 방향의 세로 정렬이 필요한 곳에는 Flexbox를 다시 사용했습니다.

## 5. 코드 설명 순서

1. 이벤트가 어디에서 발생하는지 말합니다.
2. 이벤트 핸들러가 무엇을 변경하는지 말합니다.
3. 변경 결과를 DOM·클래스·속성·CSS 중 무엇으로 반영하는지 설명합니다.
4. API라면 성공·빈 상태·실패를 구분합니다.
5. 배열이라면 filter → slice → map → join 순서를 짚습니다.
6. 레이아웃이라면 한 방향은 Flexbox, 행·열은 Grid라고 비교합니다.
