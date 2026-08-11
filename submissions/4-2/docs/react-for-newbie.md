# 정말 처음 시작하는 React

이 문서는 React를 처음 접하는 사람이 React의 기본 개념과 화면이 바뀌는 원리를 이해할 수 있도록 작성한 입문 자료입니다.

React 문법을 외우는 것이 목적이 아닙니다. 다음 흐름을 이해하는 것이 가장 중요합니다.

```text
사용자가 행동한다
    ↓
이벤트 함수가 실행된다
    ↓
State가 변경된다
    ↓
React가 컴포넌트를 다시 실행한다
    ↓
새로운 데이터에 맞는 화면이 표시된다
```

## 1. React를 한 문장으로 이해하기

React는 사용자 인터페이스(UI)를 만들기 위한 JavaScript 라이브러리입니다.

쉽게 말하면 다음과 같습니다.

> React는 화면을 작은 부품으로 나누어 만들고, 데이터가 바뀌면 데이터에 맞는 화면을 다시 보여주는 도구입니다.

### React가 없을 때는 어떻게 만들었을까?

React가 나오기 전에도 웹사이트는 있었습니다. 다만 화면과 데이터를 바꾸는 방법이 지금과 달랐습니다. 주로 다음 두 가지 방식이 사용되었습니다.

#### 1. 서버가 HTML을 만들어 다시 보내는 방식

가장 전통적인 웹사이트는 사용자가 주소를 요청하면 서버가 HTML을 만들고, 브라우저가 그 HTML을 받는 방식으로 동작했습니다.

```text
사용자가 /products를 요청
    ↓
서버가 데이터베이스에서 상품 조회
    ↓
서버가 상품 목록이 포함된 HTML 생성
    ↓
브라우저가 새로운 HTML을 받아 화면 전체 표시
```

예를 들어 상품 목록에서 상품 하나를 삭제하면 다음과 같은 일이 일어날 수 있습니다.

```text
삭제 버튼 클릭
    ↓
서버에 삭제 요청
    ↓
서버가 삭제된 상품 목록으로 HTML을 다시 생성
    ↓
브라우저가 페이지 전체를 새로고침
```

이 방식은 구조가 단순하고 검색 엔진이 읽기 쉬운 장점이 있습니다. 하지만 작은 내용 하나만 바뀌어도 페이지 전체를 다시 받아야 하므로 화면이 깜빡이거나, 입력 중인 값이 사라질 수 있습니다.

#### 2. JavaScript로 DOM을 직접 바꾸는 방식

페이지를 새로고침하지 않고 화면을 바꾸기 위해 JavaScript의 DOM API를 직접 사용하기도 했습니다. DOM은 브라우저가 HTML을 화면 요소로 표현한 구조입니다.

다음은 React 없이 만든 간단한 카운터입니다.

```html
<p id="count">현재 숫자: 0</p>
<button id="increase-button">증가</button>

<script>
  let count = 0
  const countElement = document.querySelector("#count")
  const increaseButton = document.querySelector("#increase-button")

  increaseButton.addEventListener("click", () => {
    count += 1
    countElement.textContent = `현재 숫자: ${count}`
  })
</script>
```

이 코드는 잘 동작합니다. 버튼을 클릭하면 `count`를 직접 바꾸고, 그 값을 다시 `p` 요소의 `textContent`에 직접 써 넣습니다.

#### 구체적인 사례: 장바구니 수량 변경

온라인 쇼핑몰의 장바구니에 다음 데이터가 있다고 가정해 보겠습니다.

```js
const cartItem = {
  name: "키보드",
  price: 50000,
  quantity: 1,
}
```

수량을 1개에서 2개로 바꾸면 다음 화면이 함께 변경되어야 합니다.

- 상품 수량
- 상품의 소계 금액
- 장바구니 상품 개수
- 전체 결제 금액
- 수량 감소 버튼의 비활성화 여부

DOM을 직접 조작하는 방식에서는 개발자가 바뀐 요소를 하나씩 찾아서 모두 수정해야 합니다.

```js
cartItem.quantity += 1

document.querySelector("#quantity").textContent = cartItem.quantity
document.querySelector("#item-total").textContent =
  cartItem.price * cartItem.quantity
document.querySelector("#cart-count").textContent = cartItem.quantity
document.querySelector("#payment-total").textContent =
  cartItem.price * cartItem.quantity
```

화면이 작을 때는 괜찮지만, 상품이 여러 개이고 할인·배송비·재고·선택 상태까지 추가되면 “어떤 데이터가 바뀌었을 때 어떤 DOM을 수정해야 하는가?”를 개발자가 계속 추적해야 합니다. 한 곳을 빠뜨리면 화면 일부만 이전 값으로 남는 문제가 생깁니다.

React에서는 데이터와 화면의 관계를 컴포넌트로 표현하고, State만 변경합니다.

```tsx
import { useState } from "react"

function CartItem() {
  const [quantity, setQuantity] = useState(1)
  const price = 50000

  return (
    <article>
      <h2>키보드</h2>
      <p>수량: {quantity}</p>
      <p>소계: {price * quantity}원</p>
      <button type="button" onClick={() => setQuantity(quantity + 1)}>
        수량 증가
      </button>
    </article>
  )
}
```

React에서는 `quantity`가 바뀌면 JSX 안의 수량과 소계가 모두 새로운 State에 맞춰 다시 계산됩니다. 개발자가 각각의 DOM 요소를 찾아 직접 수정하지 않아도 됩니다.

#### jQuery를 사용하던 시기도 있었다

DOM을 직접 다루는 코드를 조금 편하게 작성하기 위해 jQuery 같은 라이브러리도 널리 사용되었습니다.

```js
let count = 0

$("#increase-button").on("click", () => {
  count += 1
  $("#count").text(`현재 숫자: ${count}`)
})
```

jQuery는 DOM 선택과 이벤트 처리를 편하게 해 주었지만, 화면이 복잡해질수록 데이터와 DOM을 개발자가 직접 동기화해야 한다는 문제는 남아 있었습니다.

#### React가 해결하려고 한 문제

React는 기존 기술을 없앤 것이 아니라, 복잡해지는 화면을 관리하는 방법을 바꾸었습니다.

| 구분 | DOM 직접 조작 방식 | React 방식 |
| --- | --- | --- |
| 화면 변경 | 개발자가 DOM 요소를 찾아 직접 수정 | State와 Props에 맞춰 JSX를 다시 계산 |
| 데이터와 화면의 관계 | 여러 이벤트 함수에 흩어지기 쉬움 | 컴포넌트 코드에 함께 표현 |
| 재사용 | HTML과 이벤트 코드를 복사하기 쉬움 | 컴포넌트를 여러 곳에서 재사용 |
| 데이터 변경 결과 | 수정해야 할 DOM을 개발자가 모두 관리 | React가 변경된 화면을 반영 |
| 페이지가 복잡해질 때 | 화면 상태 추적이 어려워짐 | 역할별 컴포넌트와 State로 분리 |

다만 DOM을 직접 조작하는 방식이 항상 잘못된 것은 아닙니다. 간단한 페이지나 특정 브라우저 API를 사용할 때는 여전히 필요할 수 있습니다. React의 핵심은 “DOM을 절대 직접 만지지 않는다”가 아니라, 일반적인 화면 변경은 데이터 중심으로 관리해 복잡도를 줄이는 것입니다.

예를 들어 목록 화면에는 다음과 같은 화면 부품이 있을 수 있습니다.

```text
App
 ├─ Header
 ├─ ItemList
 │   └─ ItemCard
 └─ Footer
```

HTML로 모든 화면을 한 파일에 작성하는 대신, 역할이 분명한 부품을 만들고 조합합니다.

## 2. React를 배우기 전에 알아야 할 것

React를 시작하기 위해 JavaScript의 모든 내용을 미리 공부할 필요는 없습니다. 변수, 함수, 조건문, 배열, 객체처럼 기본적인 프로그래밍 개념은 알고 있다고 가정합니다.

그 대신 React를 이해하려면 “코드가 브라우저 화면이 되는 과정”과 “웹 화면이 데이터를 다루는 방식”을 알아야 합니다.

### 2.1 브라우저와 DOM

브라우저는 HTML 문자열을 읽어 DOM이라는 트리 구조를 만듭니다. DOM은 화면에 있는 요소를 JavaScript가 찾아서 읽거나 바꿀 수 있도록 만든 객체 구조입니다.

```text
HTML 파일
    ↓ 브라우저가 해석
DOM 트리
    ↓ CSS와 함께 계산
브라우저 화면
```

HTML이 다음과 같다면:

```html
<main>
  <h1>안녕하세요</h1>
</main>
```

브라우저는 대략 다음과 같은 관계로 이해합니다.

```text
main
 └─ h1
```

JavaScript로 DOM을 직접 바꾸는 코드는 다음과 같습니다.

```js
const heading = document.querySelector("h1")
heading.textContent = "반갑습니다"
```

이전 절에서 살펴본 React 이전의 방식이 바로 DOM을 직접 선택하고 수정하는 방식입니다. React를 이해하려면 React가 화면을 직접 조작하는 코드를 매번 작성하게 하는 대신, State와 Props를 바탕으로 화면을 계산한다는 차이를 이해해야 합니다.

여기서 Virtual DOM의 내부 구현을 먼저 외울 필요는 없습니다. 입문 단계에서는 다음 정도로 충분합니다.

> 개발자는 현재 데이터에 맞는 UI를 표현하고, React가 실제 DOM에 필요한 변경을 반영한다.

### 2.2 브라우저 이벤트

브라우저 이벤트는 사용자의 행동이나 브라우저에서 일어난 일을 의미합니다.

- 버튼을 클릭함: `click`
- 입력창의 값이 바뀜: `input`, `change`
- 폼을 제출함: `submit`
- 마우스를 올림: `mouseenter`
- 키보드를 누름: `keydown`

React에 오기 전에는 다음처럼 DOM 요소에 이벤트 함수를 연결했습니다.

```js
const button = document.querySelector("button")

button.addEventListener("click", () => {
  console.log("클릭했습니다.")
})
```

React에서는 JSX의 속성처럼 이벤트를 연결합니다.

```tsx
function SaveButton() {
  function handleClick() {
    console.log("클릭했습니다.")
  }

  return <button onClick={handleClick}>저장</button>
}
```

React를 배우기 전에는 이벤트가 “사용자의 행동을 감지하고 함수를 실행하는 장치”라는 점과 이벤트가 발생한 요소의 값을 `event.target.value`로 읽을 수 있다는 점을 알면 좋습니다.

### 2.3 명령형 UI와 선언형 UI

React를 이해하는 데 가장 도움이 되는 준비 개념은 “화면을 어떻게 바꿀지 직접 지시하는 방식”과 “어떤 상태일 때 어떤 화면인지 표현하는 방식”의 차이입니다.

DOM을 직접 조작하는 명령형 방식에서는 화면을 바꾸는 순서를 작성합니다.

```js
if (isLoggedIn) {
  loginButton.hidden = true
  profileButton.hidden = false
} else {
  loginButton.hidden = false
  profileButton.hidden = true
}
```

개발자가 “어떤 요소를 숨기고, 어떤 요소를 보여줄지”를 직접 지시합니다.

React에서는 현재 상태에 따른 화면의 모습을 표현합니다.

```tsx
function Navigation({ isLoggedIn }: { isLoggedIn: boolean }) {
  return isLoggedIn ? (
    <button type="button">마이페이지</button>
  ) : (
    <button type="button">로그인</button>
  )
}
```

React 코드에서는 DOM 요소를 찾아 숨기거나 보여주는 순서보다, `isLoggedIn` 값이 참일 때 어떤 UI를 보여줄지를 작성합니다. 이 방식을 선언형 UI라고 합니다.

```text
명령형: 버튼을 숨기고 다른 버튼을 보여줘
선언형: 로그인 상태라면 마이페이지 버튼을 보여줘
```

React의 컴포넌트, Props, State는 이 선언형 방식으로 화면을 표현하기 위한 개념입니다. 따라서 이 차이를 이해하면 “왜 React는 DOM을 직접 조작하지 않고 State를 바꾸는가?”라는 질문에도 답하기 쉬워집니다.

### 2.4 React 시작 전 체크리스트

기본적인 프로그래밍 개념을 제외하고 다음 질문에 답할 수 있으면 React를 시작하기에 충분합니다.

- 브라우저가 HTML을 DOM으로 만든다는 것을 아는가?
- JavaScript로 DOM을 선택하고 바꿀 수 있다는 것을 아는가?
- 클릭과 입력 같은 브라우저 이벤트를 아는가?
- 상태에 따라 다른 화면을 보여줄 수 있다는 뜻을 이해하는가?

반대로 다음 내용은 React 기초를 시작한 뒤 배우는 편이 좋습니다.

- Virtual DOM의 구체적인 내부 구현
- 서버 통신과 `fetch`, JSON
- npm과 빌드 도구
- TypeScript와 TSX의 타입 문법
- Redux 같은 전역 상태 관리 라이브러리
- `useMemo`, `useCallback` 같은 최적화 Hook
- 서버 컴포넌트와 렌더링 최적화
- 복잡한 인증·권한·캐시 설계

처음부터 모든 웹 기술을 공부할 필요는 없습니다. DOM과 이벤트를 이해하고, 명령형 방식과 선언형 방식의 차이를 간단히 경험한 뒤 React의 컴포넌트와 State로 넘어가면 충분합니다.

## 3. 컴포넌트: 화면을 나누는 부품

컴포넌트는 화면의 일부를 담당하는 함수입니다. 컴포넌트 함수는 화면에 표시할 JSX를 반환합니다.

```tsx
function Welcome() {
  return <h1>안녕하세요!</h1>
}
```

다른 컴포넌트 안에서 HTML 태그처럼 사용할 수 있습니다.

```tsx
function App() {
  return (
    <main>
      <Welcome />
    </main>
  )
}
```

컴포넌트 이름은 대문자로 시작해야 합니다. 대문자로 시작하면 React는 일반 HTML 태그가 아니라 직접 만든 컴포넌트로 인식합니다.

```tsx
<Welcome /> // 직접 만든 컴포넌트
<h1>제목</h1> // HTML 요소
```

컴포넌트를 나누는 기준은 다음과 같습니다.

- 하나의 분명한 역할이 있는가?
- 여러 곳에서 재사용할 수 있는가?
- 코드가 너무 길어져 별도로 읽는 것이 쉬운가?
- 별도로 상태나 이벤트를 관리해야 하는가?

컴포넌트는 무조건 작게 쪼개는 것이 목표가 아닙니다. 읽기 쉽고 재사용하기 좋은 단위로 나누는 것이 목표입니다.

## 4. JSX: JavaScript 안에서 화면 작성하기

JSX는 JavaScript 코드 안에서 HTML과 비슷한 모양으로 화면을 작성하는 문법입니다.

### JSX를 사용하는 이유

JSX는 React에서 반드시 사용해야 하는 문법은 아닙니다. JSX 없이도 `createElement`를 사용해 화면을 만들 수 있습니다.

```tsx
import { createElement } from "react"

function SaveButton() {
  return createElement("button", { type: "button" }, "저장")
}
```

하지만 화면 구조가 복잡해지면 `createElement`를 계속 중첩해서 작성해야 하므로 읽기 어렵습니다. JSX를 사용하면 같은 화면을 HTML과 비슷한 형태로 표현할 수 있습니다.

```tsx
function SaveButton() {
  return <button type="button">저장</button>
}
```

JSX를 사용하는 이유는 다음과 같습니다.

- 화면 구조를 한눈에 읽을 수 있습니다.
- JavaScript 값과 화면 구조를 가까운 곳에서 함께 사용할 수 있습니다.
- 컴포넌트를 HTML 요소처럼 조합하기 쉽습니다.
- 현재 데이터에 어떤 화면을 보여줄지 선언적으로 표현할 수 있습니다.

```tsx
function ItemSummary({ name, itemCount }: { name: string; itemCount: number }) {
  return <p>{name}님의 항목은 {itemCount}개입니다.</p>
}
```

위 코드에서 `{name}`과 `{taskCount}`는 JavaScript 값입니다. JSX는 화면 구조를 표현하면서도 중괄호 안에서 JavaScript 표현식을 사용할 수 있게 해 줍니다.

즉, JSX는 새로운 HTML이 아니라 React 화면을 사람이 읽고 관리하기 쉽게 작성하기 위한 JavaScript 문법입니다.

```tsx
function Profile() {
  const name = "민수"

  return <h1>{name}님의 프로필</h1>
}
```

중괄호 `{}` 안에는 JavaScript 표현식을 작성할 수 있습니다.

```tsx
function Greeting() {
  const isMorning = true
  const name = "민수"

  return (
    <div>
      <h1>{name}님</h1>
      <p>{isMorning ? "좋은 아침입니다." : "좋은 하루 보내세요."}</p>
    </div>
  )
}
```

JSX에서 자주 만나는 규칙은 다음과 같습니다.

- `class` 대신 `className`을 사용합니다.
- JSX에서는 여러 요소를 하나의 부모 요소로 감싸야 합니다.
- 태그는 반드시 닫아야 합니다. 예: `<input />`
- JavaScript 값은 `{}` 안에 작성합니다.
- HTML의 `for` 대신 `htmlFor`를 사용합니다.
- 이벤트 이름은 `onClick`, `onChange`, `onSubmit`처럼 작성합니다.

JSX는 실제 HTML 파일 자체가 아닙니다. 빌드 도구가 React가 이해할 수 있는 JavaScript 코드로 변환합니다.

## 5. Props: 부모가 자식에게 전달하는 값

Props는 부모 컴포넌트가 자식 컴포넌트에 전달하는 값입니다. 컴포넌트에 전달하는 매개변수라고 생각하면 됩니다.

### Props가 필요한 이유

Props가 없으면 컴포넌트 안에 데이터가 고정됩니다.

```tsx
function Greeting() {
  return <h1>민수님 안녕하세요.</h1>
}
```

이 컴포넌트는 항상 민수에게만 사용할 수 있습니다. Props를 사용하면 같은 컴포넌트에 다른 값을 전달할 수 있습니다.

```tsx
function Greeting({ name }: { name: string }) {
  return <h1>{name}님 안녕하세요.</h1>
}

function App() {
  return (
    <>
      <Greeting name="민수" />
      <Greeting name="지수" />
    </>
  )
}
```

Props를 사용하는 핵심 이유는 다음과 같습니다.

- 같은 컴포넌트를 여러 데이터에 재사용할 수 있습니다.
- 부모는 데이터를 관리하고, 자식은 화면 표시를 담당할 수 있습니다.
- 컴포넌트 내부에 데이터가 고정되지 않습니다.
- 부모에서 자식으로 데이터가 흐르는 구조를 만들 수 있습니다.
- 함수를 Props로 전달하면 자식의 행동을 부모에게 알릴 수 있습니다.

즉, Props는 컴포넌트의 매개변수입니다. 함수가 매개변수를 받아 다양한 결과를 만들듯이, 컴포넌트는 Props를 받아 다양한 화면을 만듭니다.

Props의 핵심 규칙은 다음과 같습니다.

- Props는 부모에서 자식 방향으로 전달됩니다.
- 자식은 Props를 읽어서 사용합니다.
- 자식이 Props 값을 직접 변경하면 안 됩니다.
- Props에는 문자열뿐 아니라 숫자, 배열, 객체, 함수도 전달할 수 있습니다.

```tsx
type ItemCardProps = {
  title: string
  description: string
}

function ItemCard({ title, description }: ItemCardProps) {
  return (
    <article>
      <h2>{title}</h2>
      <p>{description}</p>
    </article>
  )
}
```

## 6. State: 컴포넌트가 기억하는 값

State는 시간이 지나거나 사용자의 행동에 따라 바뀌며, 화면에도 영향을 주는 값입니다.

예시는 다음과 같습니다.

- 현재 숫자
- 입력창의 내용
- 로그인 여부
- 목록 데이터
- 로딩 중인지 여부
- 에러 메시지

### State가 필요한 이유

일반 변수는 값을 저장할 수 있지만, 값이 바뀌었을 때 React에게 화면을 다시 그려 달라고 알리지는 못합니다.

```tsx
function Counter() {
  let count = 0

  function handleClick() {
    count += 1
  }

  return (
    <button type="button" onClick={handleClick}>
      {count}
    </button>
  )
}
```

위 코드에서 `count` 값은 바뀔 수 있지만 화면은 자동으로 갱신되지 않습니다. 컴포넌트가 다시 실행되면 `count`가 다시 `0`으로 만들어질 수도 있습니다.

State를 사용하면 값이 바뀌었을 때 React가 변경 사실을 알고 화면을 다시 계산합니다.

```text
State 변경 함수 호출
    ↓
State 값 변경
    ↓
컴포넌트 다시 렌더링
    ↓
새로운 State 값이 화면에 표시
```

따라서 화면에 영향을 주고, 사용자 행동이나 시간에 따라 바뀌며, 그 값을 계속 기억해야 하는 값은 State로 관리합니다. State는 단순한 저장 공간이 아니라 “값을 기억하면서 화면도 갱신하는 장치”입니다.

### Hook이란 무엇인가

Hook은 함수형 컴포넌트에서 State나 Effect 같은 React 기능을 사용할 수 있게 해주는 함수입니다. 이름이 보통 `use`로 시작합니다.

```tsx
const [count, setCount] = useState(0)
useEffect(() => {
  // 렌더링 외부의 작업
}, [])
```

대표적인 기본 Hook은 다음과 같습니다.

- `useState`: 컴포넌트의 State를 관리합니다.
- `useEffect`: 렌더링 외부의 작업을 처리합니다.
- `useContext`: Context로 공유한 값을 읽습니다.

Hook은 다음 규칙을 지켜야 합니다.

- 컴포넌트 함수나 커스텀 Hook의 최상위에서 호출합니다.
- 조건문, 반복문, 중첩 함수 안에서 호출하지 않습니다.
- 일반 함수에서 임의로 호출하지 않고, Hook의 규칙에 맞게 사용합니다.

```tsx
function Counter() {
  // 올바른 사용: 컴포넌트 최상위에서 호출
  const [count, setCount] = useState(0)

  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

Hook은 호출 순서를 기준으로 State를 관리하기 때문에, 조건에 따라 호출 여부가 달라지면 안 됩니다.

State는 `useState`라는 Hook으로 만들 수 있습니다.

```tsx
import { useState } from "react"

function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>현재 숫자: {count}</p>
      <button type="button" onClick={() => setCount(count + 1)}>
        증가
      </button>
    </div>
  )
}
```

다음처럼 이해하면 됩니다.

- `count`: 현재 State 값
- `setCount`: State를 변경하는 함수
- `useState(0)`: 초기값이 `0`이라는 의미

일반 변수와 State는 다릅니다.

```tsx
// 일반 변수: 값은 바뀌지만 화면이 자동으로 갱신되지 않습니다.
let count = 0
count += 1

// State: 변경 함수가 호출되면 React가 화면을 다시 계산합니다.
const [count, setCount] = useState(0)
setCount(count + 1)
```

State 값을 직접 변경하지 말고 반드시 State 변경 함수를 사용해야 합니다.

```tsx
// 잘못된 방법
count = count + 1

// 올바른 방법
setCount(count + 1)
```

### 배열과 객체 State 변경하기

배열이나 객체를 State로 사용할 때도 기존 값을 직접 수정하지 않고, 새로운 배열이나 객체를 만들어 변경 함수에 전달합니다. 이 원칙을 불변성이라고 합니다.

```tsx
const [tasks, setTasks] = useState<Task[]>([])
const newTask = { id: 1, title: "React 공부하기" }

// 잘못된 방법: 기존 배열을 직접 수정
tasks.push(newTask)
setTasks(tasks)

// 올바른 방법: 새로운 배열 생성
setTasks([...tasks, newTask])
```

기존 배열의 특정 항목을 수정할 때는 `map`으로 새로운 배열을 만듭니다.

```tsx
setTasks(
  tasks.map((task) =>
    task.id === targetId
      ? { ...task, completed: true }
      : task,
  ),
)
```

객체도 같은 방식으로 필요한 속성만 복사해 새로운 객체를 만듭니다.

```tsx
setUser({ ...user, name: "새 이름" })
```

기존 배열이나 객체를 직접 수정하면 React가 변경을 제대로 감지하지 못하거나, 이전 State와 현재 State를 비교하기 어려워질 수 있습니다.

## 7. 이벤트: 사용자의 행동 처리하기

사용자가 버튼을 클릭하거나 입력창에 글자를 입력하면 이벤트가 발생합니다. React에서는 이벤트에 함수를 연결합니다.

```tsx
function SaveButton() {
  function handleClick() {
    alert("저장했습니다.")
  }

  return (
    <button type="button" onClick={handleClick}>
      저장
    </button>
  )
}
```

함수를 호출하는 것이 아니라 함수 자체를 전달해야 합니다.

```tsx
onClick={handleClick} // 클릭했을 때 실행
onClick={handleClick()} // 렌더링하는 순간 실행될 수 있음
```

매개변수를 전달해야 한다면 화살표 함수로 감쌉니다.

```tsx
function DeleteButton() {
  function handleDelete(id: number) {
    console.log(`삭제할 항목: ${id}`)
  }

  return (
    <button type="button" onClick={() => handleDelete(10)}>
      삭제
    </button>
  )
}
```

## 8. State와 이벤트를 연결하기

React의 가장 기본적인 흐름은 이벤트와 State를 연결하는 것입니다.

```tsx
import { useState } from "react"

function Toggle() {
  const [isOpen, setIsOpen] = useState(false)

  function handleToggle() {
    setIsOpen(!isOpen)
  }

  return (
    <div>
      <button type="button" onClick={handleToggle}>
        {isOpen ? "닫기" : "열기"}
      </button>

      {isOpen && <p>상세 내용이 열려 있습니다.</p>}
    </div>
  )
}
```

버튼을 클릭하면 다음 순서로 동작합니다.

1. `handleToggle` 함수가 실행됩니다.
2. `setIsOpen`이 State를 변경합니다.
3. React가 `Toggle` 컴포넌트를 다시 실행합니다.
4. `isOpen` 값에 따라 버튼 글자와 상세 내용이 바뀝니다.

## 9. 조건부 렌더링

조건부 렌더링은 State나 Props에 따라 다른 화면을 보여주는 것입니다.

삼항 연산자를 사용하면 조건에 따라 둘 중 하나를 표시할 수 있습니다.

```tsx
function LoginStatus({ isLoggedIn }: { isLoggedIn: boolean }) {
  return (
    <p>{isLoggedIn ? "로그인 상태입니다." : "로그아웃 상태입니다."}</p>
  )
}
```

조건이 참일 때만 화면을 보여주려면 `&&`를 사용할 수 있습니다.

```tsx
{isLoggedIn && <button type="button">마이페이지</button>}
```

로딩, 에러, 빈 목록도 조건부 렌더링으로 표현합니다.

```tsx
function TaskList({ tasks, isLoading }: { tasks: string[]; isLoading: boolean }) {
  if (isLoading) {
    return <p>불러오는 중입니다...</p>
  }

  if (tasks.length === 0) {
    return <p>등록된 항목이 없습니다.</p>
  }

  return <ul>{tasks.map((task) => <li key={task}>{task}</li>)}</ul>
}
```

실제 서비스에서는 다음 상태를 서로 구분하는 것이 좋습니다.

- 로딩 중: 아직 요청이 끝나지 않음
- 빈 상태: 요청은 성공했지만 데이터가 없음
- 에러 상태: 요청에 실패함
- 성공 상태: 표시할 데이터가 있음

## 10. 배열 렌더링과 `key`

배열의 데이터를 여러 화면 요소로 바꿀 때 `map`을 사용합니다.

```tsx
type Task = {
  id: number
  title: string
}

function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul>
      {tasks.map((task) => (
        <li key={task.id}>{task.title}</li>
      ))}
    </ul>
  )
}
```

`key`는 React가 목록의 각 항목을 구분하기 위한 식별자입니다. 데이터가 추가되거나 삭제될 때 어떤 항목이 바뀌었는지 판단하는 데 사용됩니다.

가능하면 데이터의 고유한 ID를 사용합니다.

```tsx
key={task.id} // 권장
```

배열의 순번을 `key`로 사용하는 것은 항목이 추가·삭제·정렬되는 목록에서는 피하는 것이 좋습니다.

## 11. 폼과 Controlled Component

React에서 State가 input의 값을 관리하는 방식을 Controlled Component라고 합니다.

```tsx
import { useState } from "react"

function NameForm() {
  const [name, setName] = useState("")

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    alert(`${name}님, 환영합니다.`)
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="name">이름</label>
      <input
        id="name"
        value={name}
        onChange={(event) => setName(event.target.value)}
      />
      <button type="submit">제출</button>
    </form>
  )
}
```

입력 흐름은 다음과 같습니다.

```text
사용자가 입력한다
    ↓
onChange가 실행된다
    ↓
event.target.value를 읽는다
    ↓
setName으로 State를 변경한다
    ↓
input에 새로운 값이 표시된다
```

폼을 제출할 때 `event.preventDefault()`를 호출하는 이유는 브라우저가 기본적으로 페이지를 새로고침하기 때문입니다. React에서는 새로고침하지 않고 JavaScript로 검증과 저장을 처리하는 경우가 많습니다.

## 12. 부모와 자식의 데이터 흐름

React의 기본 데이터 흐름은 부모에서 자식으로 내려가는 방향입니다.

```text
부모 컴포넌트
    ↓ Props로 데이터 전달
자식 컴포넌트
```

자식이 부모의 State를 직접 바꾸는 대신, 부모가 함수를 Props로 전달할 수 있습니다.

```tsx
type ChildProps = {
  onSelect: (message: string) => void
}

function Child({ onSelect }: ChildProps) {
  return (
    <button type="button" onClick={() => onSelect("자식이 선택되었습니다.")}>
      선택
    </button>
  )
}

function Parent() {
  const [message, setMessage] = useState("아직 선택하지 않았습니다.")

  return (
    <div>
      <p>{message}</p>
      <Child onSelect={setMessage} />
    </div>
  )
}
```

이 흐름을 흔히 “데이터는 아래로, 이벤트는 위로”라고 표현합니다.

```text
부모 State ─────Props─────→ 자식 화면
부모 함수 ←──이벤트 호출─── 자식 행동
```

여러 컴포넌트가 같은 값을 사용한다면, 공통 부모가 그 State를 관리하도록 옮기는 것을 상태 끌어올리기라고 합니다.

## 13. State를 어디에 둘 것인가

State는 그 값을 사용하는 컴포넌트 중 가장 가까운 공통 부모에 두는 것이 일반적입니다.

예를 들어 검색어를 입력하는 컴포넌트와 검색 결과를 표시하는 컴포넌트가 있다면, 두 컴포넌트의 공통 부모가 검색어 State를 관리할 수 있습니다.

```text
SearchPage
 ├─ SearchInput     ← 검색어 변경 함수 사용
 └─ SearchResults   ← 검색어와 결과 사용
```

반대로 특정 컴포넌트에서만 사용하는 값은 그 컴포넌트 안에 두는 것이 좋습니다. 모든 State를 App 컴포넌트에 모으면 데이터 흐름이 복잡해질 수 있습니다.

### Context: 여러 컴포넌트에서 공통 데이터 사용하기

Props는 부모에서 자식으로 데이터를 전달하는 기본 방법입니다. 하지만 로그인 사용자처럼 앱의 여러 곳에서 사용하는 값을 여러 단계의 컴포넌트에 계속 Props로 전달하면 코드가 복잡해질 수 있습니다.

이렇게 중간 컴포넌트가 사용하지 않는 값을 전달해야 하는 상황을 Props drilling이라고 합니다.

Context는 특정 데이터를 여러 컴포넌트가 공유할 수 있도록 하는 React 기능입니다.

```jsx
import { createContext, useContext, useState } from "react"

const AuthContext = createContext(null)

function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}

function Header() {
  const { user } = useContext(AuthContext)

  return <header>{user ? `${user.name}님` : "로그인해주세요."}</header>
}
```

`AuthProvider` 안에 있는 컴포넌트는 중간 부모를 거치지 않고 Context의 값을 읽을 수 있습니다. 로그인 사용자나 테마처럼 여러 화면에서 사용하는 공통 데이터를 공유할 때 활용할 수 있습니다.

Context는 모든 State를 넣는 전역 저장소가 아닙니다. 로그인 사용자, 테마, 언어처럼 많은 컴포넌트가 공통으로 사용하는 값에 선택적으로 사용하는 것이 좋습니다.

### 커스텀 Hook: State 로직 재사용하기

커스텀 Hook은 여러 컴포넌트에서 반복되는 State와 관련 로직을 하나의 함수로 분리한 것입니다. 이름은 `use`로 시작해야 합니다.

```tsx
function useToggle(initialValue = false) {
  const [isOpen, setIsOpen] = useState(initialValue)

  function toggle() {
    setIsOpen((currentValue) => !currentValue)
  }

  return { isOpen, toggle }
}

function Panel() {
  const { isOpen, toggle } = useToggle()

  return (
    <div>
      <button type="button" onClick={toggle}>
        {isOpen ? "닫기" : "열기"}
      </button>
      {isOpen && <p>패널 내용</p>}
    </div>
  )
}
```

커스텀 Hook은 State 자체를 모든 컴포넌트와 공유하는 기능이 아닙니다. State를 만들고 변경하는 로직을 재사용하는 기능입니다. 예를 들어 `useTasks`라는 커스텀 Hook으로 목록 조회, 로딩·에러 State, 다시 불러오기 로직을 한 곳에 모을 수 있습니다.

## 14. `useEffect`: 렌더링 외부의 작업

React 컴포넌트는 State와 Props를 바탕으로 화면을 계산합니다. 브라우저 제목 변경, 타이머, 브라우저 이벤트 구독처럼 화면 계산 외부에서 해야 하는 작업은 `useEffect`로 처리할 수 있습니다.

```tsx
import { useEffect, useState } from "react"

function Counter() {
  const [count, setCount] = useState(0)

  useEffect(() => {
    document.title = `현재 숫자: ${count}`
  }, [count])

  return (
    <button type="button" onClick={() => setCount(count + 1)}>
      {count}
    </button>
  )
}
```

이 예제에서 화면의 숫자는 JSX로 표시하고, 브라우저 탭의 제목은 `useEffect`로 동기화합니다. 화면에 표시할 JSX만 계산하는 작업과 브라우저 같은 외부 대상을 변경하는 작업을 구분할 수 있습니다.

### Effect 정리하기

Effect에서 타이머를 만들거나 브라우저 이벤트를 구독했다면, 컴포넌트가 사라질 때 정리해야 합니다. `useEffect` 안에서 반환하는 함수가 정리 함수입니다.

```tsx
useEffect(() => {
  const timerId = window.setInterval(() => {
    console.log("실행 중")
  }, 1000)

  return () => {
    window.clearInterval(timerId)
  }
}, [])
```

정리 함수는 컴포넌트가 화면에서 사라질 때 실행되고, 의존성 값이 바뀌어 Effect를 다시 실행하기 전에도 실행됩니다. 사용하지 않는 타이머나 이벤트 구독을 남겨 두면 메모리 누수나 중복 실행이 발생할 수 있습니다.

로그인 상태나 브라우저 이벤트를 구독하는 경우에도 컴포넌트가 사라질 때 `unsubscribe`를 호출해 정리해야 합니다.

두 번째 인자인 의존성 배열은 effect를 다시 실행할 조건을 나타냅니다.

```tsx
useEffect(() => {
  // 렌더링 후 실행
})
```

의존성 배열을 생략하면 렌더링될 때마다 실행될 수 있습니다.

```tsx
useEffect(() => {
  // 처음 마운트될 때 실행되고, userId가 바뀔 때 다시 실행
}, [userId])
```

빈 배열을 전달하면 컴포넌트가 처음 화면에 나타날 때 실행하는 용도로 사용할 수 있습니다.

```tsx
useEffect(() => {
  // 처음 나타날 때 실행
}, [])
```

`useEffect`는 많이 사용한다고 좋은 것이 아닙니다. State와 Props만으로 화면을 계산할 수 있는 값은 굳이 effect로 만들지 않는 것이 좋습니다.

## 15. React에서 자주 하는 오해

### React는 HTML을 대체하는가?

아닙니다. React는 HTML, CSS, JavaScript를 사용해 UI를 구성하는 방법을 도와주는 도구입니다.

### State가 바뀌면 브라우저 전체가 새로고침되는가?

아닙니다. React는 컴포넌트를 다시 계산하고 필요한 DOM 변경을 적용합니다. 브라우저 페이지 전체가 새로고침되는 것과는 다릅니다.

### Props와 State는 같은가?

다릅니다.

| 구분 | Props | State |
| --- | --- | --- |
| 전달 주체 | 부모가 전달 | 컴포넌트가 관리 |
| 변경 | 자식이 직접 변경하지 않음 | 변경 함수로 변경 |
| 용도 | 외부에서 설정값 전달 | 시간이 지나며 바뀌는 값 저장 |
| 예시 | 카드 제목, 사용자 정보 | 입력값, 모달 열림 여부 |

### 모든 값을 State로 만들어야 하는가?

아닙니다. 화면에 영향을 주지 않는 일반 계산값은 일반 변수로 충분합니다. State는 값이 바뀌었을 때 화면도 바뀌어야 하는 경우에 사용합니다.

```tsx
const total = price * quantity // 단순 계산값
const [quantity, setQuantity] = useState(1) // 화면에 영향을 주는 값
```

### 컴포넌트를 많이 만들수록 좋은가?

아닙니다. 각 컴포넌트가 이해하기 쉬운 역할을 갖도록 나누는 것이 중요합니다.

## 16. 추천 학습 순서와 실습

아래 순서로 작은 기능을 하나씩 추가하면 개념을 자연스럽게 익힐 수 있습니다.

1. `Hello World` 컴포넌트 만들기
2. 이름을 Props로 전달하기
3. 버튼 클릭 이벤트 만들기
4. Counter로 State 변경 확인하기
5. 열기·닫기 Toggle 만들기
6. 배열을 `map`으로 목록에 표시하기
7. Todo 추가·완료·삭제 기능 만들기
8. input을 Controlled Component로 만들기
9. 로딩·에러·빈 상태처럼 조건에 따른 화면 표시하기
10. `useEffect`로 브라우저 제목이나 타이머 다루기
11. Context와 커스텀 Hook 사용해 보기

처음부터 Context, 커스텀 Hook, 복잡한 기능을 모두 사용하기보다 작은 기능 하나에서 다음 질문에 답할 수 있는지 확인하는 것이 좋습니다.

- 어떤 값이 State인가?
- 그 State는 어느 컴포넌트가 관리해야 하는가?
- 사용자의 어떤 행동이 State를 바꾸는가?
- State가 바뀌면 화면의 어느 부분이 달라지는가?
- 자식 컴포넌트에 어떤 Props를 전달하는가?

## 17. 최종 요약

React의 기본 개념은 다음과 같이 정리할 수 있습니다.

- 컴포넌트는 화면을 구성하는 재사용 가능한 부품입니다.
- JSX는 JavaScript 안에서 화면을 작성하는 문법입니다.
- Props는 부모가 자식에게 전달하는 읽기 전용 값입니다.
- State는 컴포넌트가 기억하고 화면에 영향을 주는 값입니다.
- Hook은 함수형 컴포넌트에서 React 기능을 사용할 수 있게 해주는 함수입니다.
- 이벤트는 사용자의 행동을 함수와 연결합니다.
- State가 변경되면 React는 새로운 상태에 맞게 화면을 다시 계산합니다.
- 배열과 객체 State는 기존 값을 직접 수정하지 않고 새로운 값으로 변경합니다.
- `map`과 `key`로 배열 데이터를 목록 화면에 표시합니다.
- 데이터는 기본적으로 부모에서 자식으로 흐릅니다.
- Context는 여러 컴포넌트가 공통 데이터를 사용하게 합니다.
- 커스텀 Hook은 State와 관련된 로직을 재사용하게 합니다.
- `useEffect`는 브라우저 제목이나 타이머처럼 렌더링 외부의 작업에 사용합니다.
- 로딩·에러·빈 상태처럼 State에 따른 화면을 구분해 표현할 수 있습니다.

React를 배운다는 것은 문법을 많이 외우는 것이 아니라, 다음 질문에 답할 수 있게 되는 것입니다.

> 어떤 데이터가 바뀌었고, 그 데이터가 바뀌었을 때 화면의 어느 부분이 다시 표시되어야 하는가?
