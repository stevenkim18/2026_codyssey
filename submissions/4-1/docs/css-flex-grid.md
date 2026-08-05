# CSS 레이아웃: Flexbox와 Grid

## 1. 문서의 목표

이 문서는 웹페이지의 요소를 배치하는 CSS 레이아웃을 입문자 눈높이에서 설명합니다.

- 왜 레이아웃 기술이 필요한가
- Flexbox와 Grid가 등장하기 전에는 어떻게 배치했는가
- Flexbox와 Grid의 기본 개념과 주요 속성
- 어떤 상황에서 무엇을 선택하는가
- 반응형 화면에서 어떻게 활용하는가

> Flexbox는 한 방향으로 정렬할 때 사용하고, Grid는 행과 열을 함께 배치할 때 사용합니다.

---

## 2. 레이아웃이란 무엇인가요?

HTML은 콘텐츠의 구조를 만들고, CSS는 콘텐츠가 화면에 어떻게 보일지 정합니다.

~~~html
<header>사이트 제목</header>
<main>본문</main>
<aside>사이드 메뉴</aside>
~~~

HTML만 작성하면 요소는 기본적으로 위에서 아래 방향으로 배치됩니다.

~~~text
사이트 제목
본문
사이드 메뉴
~~~

하지만 실제 웹사이트에서는 헤더, 사이드바, 본문, 푸터를 나누고, 메뉴와 버튼을 가로로 정렬해야 합니다.

~~~text
┌─────────────────────────────┐
│            헤더             │
├──────────┬──────────────────┤
│ 사이드바 │       본문       │
└──────────┴──────────────────┘
~~~

이처럼 화면 안에서 요소의 위치, 크기, 간격, 정렬 방식을 정하는 작업을 레이아웃이라고 합니다.

---

## 3. 왜 Flexbox와 Grid를 사용하나요?

웹페이지는 화면 크기와 콘텐츠에 따라 변합니다.

- 데스크톱에서는 카드 3개를 한 줄에 보여줄 수 있습니다.
- 모바일에서는 카드 1개씩 보여주는 편이 읽기 쉽습니다.
- 글자 수가 달라도 메뉴 사이의 간격을 일정하게 유지해야 합니다.
- 로고와 버튼을 세로 가운데에 맞춰야 합니다.

예전에는 이런 배치를 table, float, position 등으로 직접 계산하는 경우가 많았습니다. 이 방식은 화면 크기나 콘텐츠 길이가 바뀌면 레이아웃이 쉽게 깨졌습니다.

Flexbox와 Grid는 브라우저에 배치 규칙을 알려주는 방식입니다.

~~~css
/* 요소를 한 방향으로 배치 */
display: flex;

/* 3개의 열을 생성 */
display: grid;
grid-template-columns: repeat(3, 1fr);
~~~

브라우저가 남은 공간, 요소의 크기, 줄바꿈 등을 계산하므로 직접 좌표를 계산할 필요가 줄어듭니다.

### 주요 장점

1. 정렬이 간단합니다. 가로·세로 가운데 정렬을 몇 줄로 작성할 수 있습니다.
2. 콘텐츠 변화에 강합니다. 글자 수나 카드 개수가 바뀌어도 덜 깨집니다.
3. 반응형 구현이 쉽습니다. 화면 폭에 따라 방향이나 열 개수를 바꿀 수 있습니다.
4. 코드 의도가 분명합니다. flex는 한 방향 정렬, grid는 행과 열 배치라는 의미가 드러납니다.
5. 유지보수가 쉽습니다. 위치를 일일이 고치는 대신 컨테이너의 규칙을 수정하면 됩니다.

---

## 4. 레이아웃 기술의 발전

### 4.1 table 레이아웃

초기 웹에서는 표를 표현하는 HTML의 table 요소를 페이지 레이아웃에도 사용했습니다.

~~~html
<table>
  <tr>
    <td>메뉴</td>
    <td>본문</td>
  </tr>
</table>
~~~

행과 열을 만들 수 있다는 장점은 있었지만, 페이지가 데이터 표가 아닌데도 표 요소를 사용한다는 문제가 있었습니다.

- 콘텐츠의 의미보다 배치 방법이 HTML에 드러납니다.
- 구조가 복잡해지고 수정하기 어렵습니다.
- 모바일 화면에 맞게 바꾸기 어렵습니다.
- 스크린 리더가 페이지를 표로 이해할 수 있습니다.

### 4.2 float 레이아웃

이후에는 float으로 요소를 왼쪽이나 오른쪽에 띄우는 방법이 널리 사용되었습니다.

~~~css
.sidebar {
  float: left;
  width: 240px;
}

.content {
  float: left;
  width: calc(100% - 240px);
}
~~~

float은 원래 이미지 옆으로 글자가 흐르게 하는 기능입니다.

~~~css
img {
  float: left;
  margin-right: 16px;
}
~~~

레이아웃에 사용하면 부모 요소가 자식의 높이를 제대로 감지하지 못하거나, 다음 요소에 영향을 주지 않도록 clear를 추가해야 하는 등 관리가 복잡했습니다.

### 4.3 position을 이용한 직접 배치

position: absolute와 top, left로 요소의 좌표를 직접 지정할 수도 있습니다.

~~~css
.badge {
  position: absolute;
  top: 12px;
  right: 12px;
}
~~~

카드 모서리의 배지처럼 특정 부모를 기준으로 겹쳐 배치할 때는 유용합니다. 하지만 모든 요소를 좌표로 배치하면 화면 크기나 콘텐츠 변화에 취약합니다.

### 4.4 Flexbox와 Grid

이런 문제를 줄이기 위해 CSS에는 목적에 맞는 레이아웃 시스템이 추가되었습니다.

- Flexbox: 한 축을 중심으로 요소를 정렬
- Grid: 두 축, 즉 행과 열을 기준으로 영역을 배치

두 기술은 과거 기술을 전부 대체해야 한다는 뜻이 아니라, 일반적인 페이지 레이아웃을 더 예측 가능하게 작성하도록 도와주는 현대적인 도구입니다.

---

## 5. Flexbox

### 5.1 기본 구조

Flexbox는 부모 요소에 display: flex를 지정하면서 시작합니다.

~~~html
<nav class="menu">
  <a href="#home">홈</a>
  <a href="#about">소개</a>
  <a href="#contact">연락처</a>
</nav>
~~~

~~~css
.menu {
  display: flex;
  gap: 20px;
}
~~~

결과:

~~~text
홈  소개  연락처
~~~

menu는 flex container이고, 안의 a 요소들은 flex item입니다.

Flex의 핵심은 부모에게 규칙을 작성한다는 점입니다. 자식마다 left나 top을 지정하기보다 부모가 자식들을 어떻게 정렬할지 선언합니다.

### 5.2 주축과 교차축

Flexbox에는 두 방향의 축이 있습니다.

~~~text
flex-direction: row

주축 ───────────────────────→
     [아이템] [아이템] [아이템]
교차축은 위아래 방향
~~~

- 주축(main axis): 아이템이 주로 이동하는 방향
- 교차축(cross axis): 주축과 직각인 방향

기본값인 flex-direction: row에서는 주축이 가로이고, flex-direction: column에서는 주축이 세로가 됩니다.

### 5.3 자주 사용하는 속성

#### flex-direction

아이템이 배치될 방향을 정합니다.

~~~css
.container {
  display: flex;
  flex-direction: row; /* 기본값: 가로 */
}

.column {
  flex-direction: column; /* 세로 */
}
~~~

#### justify-content

주축 방향으로 아이템을 정렬합니다.

~~~css
.container {
  display: flex;
  justify-content: center;
}
~~~

주요 값:

~~~css
justify-content: flex-start;    /* 시작점 */
justify-content: center;        /* 가운데 */
justify-content: flex-end;      /* 끝점 */
justify-content: space-between; /* 양끝 배치, 사이 간격 균등 */
justify-content: space-around;  /* 주변 간격 균등 */
justify-content: space-evenly;  /* 모든 간격 동일 */
~~~

#### align-items

교차축 방향으로 아이템을 정렬합니다.

~~~css
.header {
  display: flex;
  align-items: center;
  height: 80px;
}
~~~

가로 방향 Flex에서 로고와 메뉴를 양끝에 배치하는 대표적인 조합은 다음과 같습니다.

~~~css
.header {
  display: flex;
  justify-content: space-between; /* 가로: 양끝 */
  align-items: center;             /* 세로: 가운데 */
}
~~~

#### gap

아이템 사이의 간격을 정합니다.

~~~css
.menu {
  display: flex;
  gap: 16px;
}
~~~

각 아이템에 margin을 일일이 지정하는 것보다 의도가 분명하고, 첫 번째나 마지막 아이템에 불필요한 바깥 여백이 생기지 않습니다.

#### flex-wrap

공간이 부족할 때 다음 줄로 넘어갈지 정합니다.

~~~css
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
~~~

태그나 버튼 목록처럼 개수가 많아질 수 있는 요소에 유용합니다.

### 5.4 Flex를 사용하는 상황

- 상단 헤더의 로고와 메뉴
- 가로 내비게이션
- 버튼 여러 개의 정렬
- 아이콘과 텍스트를 한 줄에 배치
- 요소를 가로 또는 세로 가운데 정렬
- 간단한 카드 내부 구성

---

## 6. Grid

### 6.1 기본 구조

Grid도 부모 요소에 display: grid를 지정하면서 시작합니다.

~~~html
<section class="cards">
  <article>카드 1</article>
  <article>카드 2</article>
  <article>카드 3</article>
  <article>카드 4</article>
</section>
~~~

~~~css
.cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}
~~~

결과:

~~~text
┌────────┐ ┌────────┐
│ 카드 1 │ │ 카드 2 │
└────────┘ └────────┘
┌────────┐ ┌────────┐
│ 카드 3 │ │ 카드 4 │
└────────┘ └────────┘
~~~

Grid에서는 부모가 전체 격자의 열과 행을 정하고, 자식 요소가 그 칸에 자동으로 배치됩니다.

### 6.2 grid-template-columns

열의 개수와 크기를 정합니다.

~~~css
/* 3개의 열을 같은 크기로 나눔 */
.cards {
  grid-template-columns: 1fr 1fr 1fr;
}

/* 위와 같은 의미 */
.cards {
  grid-template-columns: repeat(3, 1fr);
}
~~~

fr은 사용 가능한 공간을 나누는 단위입니다.

~~~css
.layout {
  grid-template-columns: 240px 1fr;
}
~~~

첫 번째 열은 240px이 되고, 두 번째 열은 남은 공간을 사용합니다. 따라서 사이드바와 본문을 나눌 때 적합합니다.

### 6.3 grid-template-rows

행의 크기를 지정합니다.

~~~css
.layout {
  display: grid;
  grid-template-rows: 80px 1fr 60px;
}
~~~

헤더 80px, 본문은 남은 공간, 푸터 60px인 페이지 구조를 만들 수 있습니다.

### 6.4 gap

행과 열 사이의 간격을 지정합니다.

~~~css
.cards {
  display: grid;
  gap: 24px;
}
~~~

가로와 세로 간격을 다르게 지정할 수도 있습니다.

~~~css
.cards {
  column-gap: 24px;
  row-gap: 16px;
}
~~~

### 6.5 반응형 Grid

화면 폭에 따라 열의 수를 바꿀 수 있습니다.

~~~css
.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 700px) {
  .cards {
    grid-template-columns: 1fr;
  }
}
~~~

더 유연하게 만들려면 auto-fit과 minmax()를 사용할 수 있습니다.

~~~css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}
~~~

이 규칙은 다음과 같이 동작합니다.

- 카드 하나의 최소 너비는 240px입니다.
- 화면에 들어갈 수 있는 만큼 열을 만듭니다.
- 공간이 부족하면 열의 수를 자동으로 줄입니다.
- 각 열은 남은 공간을 균등하게 나눠 가집니다.

따라서 카드 목록, 상품 목록, 사진 갤러리에 자주 사용합니다.

### 6.6 영역 이름으로 페이지 구성하기

Grid는 페이지 전체 구조를 표현할 때도 사용할 수 있습니다.

~~~html
<div class="page">
  <header class="header">헤더</header>
  <aside class="sidebar">사이드바</aside>
  <main class="main">본문</main>
  <footer class="footer">푸터</footer>
</div>
~~~

~~~css
.page {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: 80px 1fr 60px;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
~~~

grid-template-areas를 사용하면 숫자 좌표보다 페이지의 구조를 읽기 쉽게 표현할 수 있습니다.

### 6.7 Grid를 사용하는 상황

- 상품이나 프로젝트 카드 목록
- 사진 갤러리
- 대시보드
- 사이드바와 본문이 있는 페이지
- 헤더·본문·푸터 구조
- 행과 열의 위치를 함께 관리해야 하는 레이아웃

---

## 7. Flexbox와 Grid 비교

| 기준 | Flexbox | Grid |
| --- | --- | --- |
| 방향 | 한 방향 중심 | 가로와 세로를 함께 관리 |
| 기준 | 콘텐츠의 흐름과 정렬 | 미리 정한 행과 열 |
| 적합한 예 | 메뉴, 버튼, 헤더 내부 | 카드, 갤러리, 페이지 전체 |
| 대표 질문 | “이 요소들을 어떻게 정렬할까?” | “이 영역을 어떻게 나눌까?” |
| 주요 속성 | justify-content, align-items, gap | grid-template-columns, grid-template-areas, gap |

다음처럼 선택하면 됩니다.

~~~text
한 줄 또는 한 열로 정렬한다       → Flexbox
행과 열을 기준으로 배치한다        → Grid
요소의 내용 크기가 중심이다        → Flexbox
페이지의 전체 구조가 중심이다      → Grid
~~~

둘 중 하나만 사용해야 하는 것은 아닙니다. 하나의 웹페이지 안에서 용도에 따라 함께 사용하는 것이 일반적입니다.

~~~css
/* 전체 페이지 구조는 Grid */
.page {
  display: grid;
  grid-template-columns: 240px 1fr;
}

/* 헤더 안 요소의 정렬은 Flexbox */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
~~~

---

## 8. 가운데 정렬 예제

Flexbox는 가운데 정렬에 특히 편리합니다.

~~~html
<div class="center-box">
  <p>가운데에 있는 내용</p>
</div>
~~~

~~~css
.center-box {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}
~~~

- justify-content: center: 주축 방향 가운데 정렬
- align-items: center: 교차축 방향 가운데 정렬

기본 방향인 가로 Flex에서는 결과적으로 가로와 세로 모두 가운데에 배치됩니다.

Grid에서는 다음처럼 작성할 수 있습니다.

~~~css
.center-box {
  display: grid;
  place-items: center;
  min-height: 200px;
}
~~~

place-items: center는 아이템을 가로와 세로 모두 가운데에 배치하는 편의 속성입니다.

---

## 9. 자주 하는 실수

### 9.1 display: flex를 자식에게 지정하는 실수

정렬 규칙은 보통 정렬 대상의 부모에게 지정합니다.

~~~css
/* 올바른 예 */
.menu {
  display: flex;
}
~~~

menu 안에 있는 자식들이 Flex item이 됩니다.

### 9.2 justify-content와 align-items를 방향 없이 외우기

두 속성의 방향은 flex-direction에 따라 달라집니다. 먼저 주축이 가로인지 세로인지 확인해야 합니다.

### 9.3 Grid 열의 합이 컨테이너보다 커지는 경우

~~~css
.cards {
  grid-template-columns: 300px 300px 300px;
  padding: 20px;
}
~~~

컨테이너가 800px인데 열만 900px이면 가로 스크롤이 생길 수 있습니다. 유동적인 레이아웃에서는 fr, %, minmax()를 함께 고려합니다.

### 9.4 모든 것을 position: absolute로 배치하기

겹침이나 장식 요소에는 유용하지만, 일반적인 문서 흐름을 유지해야 하는 레이아웃에는 Flexbox나 Grid가 더 적합합니다.

### 9.5 margin으로 간격을 모두 직접 계산하기

아이템 사이 간격을 일정하게 만들 때는 gap을 우선 고려합니다.

---

## 10. 이 프로젝트에서의 활용

개인 포트폴리오와 같은 페이지에서는 두 기술을 다음처럼 나눠 사용할 수 있습니다.

~~~css
/* 로고와 메뉴를 한 줄에 정렬 */
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* 프로젝트 카드를 화면 폭에 맞게 배치 */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}
~~~

- 네비게이션은 로고와 메뉴를 한 방향으로 배치하므로 Flexbox가 적합합니다.
- 프로젝트 카드는 행과 열로 배치하고 화면 폭에 따라 열 수가 달라지므로 Grid가 적합합니다.

레이아웃의 목적에 따라 도구를 선택하면 CSS를 읽는 사람도 구현 의도를 쉽게 이해할 수 있습니다.

---

## 11. 최종 요약

### Flexbox

~~~css
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}
~~~

요소를 한 방향으로 정렬하고, 간격을 조정하고, 가운데에 배치할 때 사용합니다.

### Grid

~~~css
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
~~~

요소를 행과 열로 나누고, 카드나 페이지 영역을 구조적으로 배치할 때 사용합니다.

### 기억할 기준

> 메뉴와 내부 정렬은 Flexbox, 카드 목록과 전체 영역 구성은 Grid.

처음에는 이 기준으로 시작하고, 실제 레이아웃의 방향과 화면 변화에 따라 세부 속성을 추가하면 됩니다.

