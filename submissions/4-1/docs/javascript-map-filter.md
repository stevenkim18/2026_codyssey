# JavaScript 배열 메서드: map과 filter

## 1. 문서의 목표

이 문서는 JavaScript 배열의 대표적인 메서드인 map과 filter를 입문자 눈높이에서 설명합니다.

- 배열과 배열 메서드의 기본 개념
- map과 filter를 사용하는 이유
- map과 filter의 문법과 반환값
- 원본 배열이 어떻게 되는지
- for문, forEach와의 차이
- map과 filter를 함께 사용하는 방법
- GitHub API 데이터와 DOM 렌더링에 적용하는 방법
- 자주 하는 실수

핵심 문장은 다음과 같습니다.

> map은 배열의 각 요소를 다른 값으로 바꾸고, filter는 조건에 맞는 요소만 남깁니다.

---

## 2. 배열이란 무엇인가요?

배열은 여러 값을 순서대로 묶어 저장하는 자료구조입니다.

~~~javascript
const numbers = [1, 2, 3, 4];
const fruits = ["사과", "바나나", "포도"];
~~~

각 값은 인덱스(index)라는 번호로 찾을 수 있습니다. 인덱스는 0부터 시작합니다.

~~~javascript
const fruits = ["사과", "바나나", "포도"];

console.log(fruits[0]); // "사과"
console.log(fruits[1]); // "바나나"
~~~

배열에는 값이 여러 개 들어 있기 때문에, 모든 값을 하나씩 확인하거나 변환하거나 일부만 골라내는 일이 자주 필요합니다. 이때 배열 메서드를 사용합니다.

---

## 3. 왜 map과 filter를 사용하나요?

배열을 직접 반복하려면 for문을 사용할 수 있습니다.

~~~javascript
const numbers = [1, 2, 3];
const doubled = [];

for (let index = 0; index < numbers.length; index += 1) {
  doubled.push(numbers[index] * 2);
}

console.log(doubled); // [2, 4, 6]
~~~

동작하지만, 반복문 안에서 다음 내용을 직접 관리해야 합니다.

- 현재 위치를 나타내는 인덱스
- 배열의 길이
- 결과를 저장할 빈 배열
- 값을 추가하는 push

map과 filter는 반복에서 자주 사용하는 목적을 메서드 이름으로 표현합니다.

~~~javascript
const doubled = numbers.map((number) => number * 2);
const evenNumbers = numbers.filter((number) => number % 2 === 0);
~~~

코드만 읽어도 다음 의도를 알 수 있습니다.

- map: 모든 요소를 변환한다.
- filter: 조건에 맞는 요소를 걸러낸다.

### 사용하면 좋은 이유

1. 코드의 목적이 명확합니다.
2. 반복에 필요한 세부 작업을 줄일 수 있습니다.
3. 원본 배열을 보존하면서 새 배열을 만들기 쉽습니다.
4. API 응답처럼 배열로 받은 데이터를 UI에 맞게 가공하기 좋습니다.
5. filter, map, slice 등을 연결해 읽기 쉬운 데이터 처리 흐름을 만들 수 있습니다.

---

## 4. 간단한 역사

JavaScript 초기에는 배열을 반복할 때 for문을 주로 사용했습니다. 이후 ECMAScript 5 표준이 2009년에 발표되면서 map과 filter를 포함한 여러 배열 메서드가 표준 기능으로 널리 사용되기 시작했습니다.

이 메서드들은 함수형 프로그래밍의 영향을 받았습니다. 핵심은 데이터를 직접 바꾸기보다, 기존 배열을 바탕으로 새로운 결과를 만드는 방식입니다.

물론 for문이 사라진 것은 아닙니다.

- 복잡한 반복 제어가 필요하면 for문이 적합합니다.
- 모든 요소를 변환하면 map이 적합합니다.
- 조건에 맞는 요소만 선택하면 filter가 적합합니다.

---

## 5. 콜백 함수 이해하기

map과 filter에는 함수를 전달합니다. 이 함수를 콜백 함수(callback function)라고 합니다.

~~~javascript
const numbers = [1, 2, 3];

const doubled = numbers.map((number) => {
  return number * 2;
});
~~~

배열의 각 요소마다 콜백 함수가 한 번씩 실행됩니다.

처음에는 다음처럼 이해하면 됩니다.

~~~text
numbers의 첫 번째 값 → 콜백 함수 실행
numbers의 두 번째 값 → 콜백 함수 실행
numbers의 세 번째 값 → 콜백 함수 실행
결과를 새 배열에 저장
~~~

콜백 함수는 보통 세 가지 인자를 받을 수 있습니다.

~~~javascript
const fruits = ["사과", "바나나"];

fruits.map((fruit, index, array) => {
  console.log(fruit); // 현재 요소
  console.log(index); // 현재 인덱스
  console.log(array); // 원본 배열
});
~~~

대부분의 경우에는 첫 번째 인자인 현재 요소만 사용합니다.

---

## 6. map

### 6.1 map이란?

map은 배열의 모든 요소를 순서대로 변환하여 새로운 배열을 만드는 메서드입니다.

~~~javascript
const numbers = [1, 2, 3, 4];

const doubled = numbers.map((number) => {
  return number * 2;
});

console.log(doubled); // [2, 4, 6]
~~~

처리 흐름은 다음과 같습니다.

~~~text
[1, 2, 3, 4]
 ↓  ↓  ↓  ↓
[2, 4, 6, 8]
~~~

원본 배열은 그대로 유지됩니다.

~~~javascript
const numbers = [1, 2, 3, 4];
const doubled = numbers.map((number) => number * 2);

console.log(numbers); // [1, 2, 3, 4]
console.log(doubled); // [2, 4, 6, 8]
~~~

### 6.2 기본 문법

~~~javascript
const newArray = array.map((currentValue, index, array) => {
  return transformedValue;
});
~~~

- currentValue: 현재 처리 중인 요소
- index: 현재 요소의 인덱스
- array: map을 실행한 원본 배열
- return: 새 배열에 들어갈 값

map은 원본 배열과 같은 개수의 결과를 만듭니다.

~~~javascript
const numbers = [10, 20, 30];
const labels = numbers.map((number) => number + "점");

console.log(labels); // ["10점", "20점", "30점"]
~~~

### 6.3 객체 배열 변환하기

API에서는 객체가 들어 있는 배열을 자주 받습니다.

~~~javascript
const users = [
  { name: "민수", age: 20 },
  { name: "지영", age: 25 }
];

const names = users.map((user) => user.name);

console.log(names); // ["민수", "지영"]
~~~

객체를 다른 모양의 객체로 변환할 수도 있습니다.

~~~javascript
const cards = users.map((user) => ({
  title: user.name,
  description: user.age + "세"
}));

console.log(cards);
~~~

이처럼 map은 데이터 구조를 화면이나 다른 함수에 맞게 바꿀 때 유용합니다.

### 6.4 문자열 HTML로 변환하기

프로젝트 카드 데이터가 있다고 가정해 보겠습니다.

~~~javascript
const projects = [
  { name: "Portfolio", language: "JavaScript" },
  { name: "Todo App", language: "HTML" }
];

const cardMarkup = projects.map((project) => {
  return (
    "<article class=\"project-card\">" +
      "<h3>" + project.name + "</h3>" +
      "<p>" + project.language + "</p>" +
    "</article>"
  );
});

console.log(cardMarkup);
~~~

map의 결과는 HTML 문자열 배열입니다.

~~~text
[
  "<article>Portfolio ...</article>",
  "<article>Todo App ...</article>"
]
~~~

문자열을 하나로 합쳐 DOM에 넣으려면 join을 사용할 수 있습니다.

~~~javascript
const html = projects
  .map((project) => {
    return "<article>" + project.name + "</article>";
  })
  .join("");

projectsGrid.innerHTML = html;
~~~

현재 프로젝트의 GitHub 저장소 카드 렌더링도 같은 흐름을 사용합니다.

### 6.5 map에서 return을 빼먹는 실수

중괄호를 사용하는 화살표 함수에서는 return을 직접 작성해야 합니다.

~~~javascript
const doubled = numbers.map((number) => {
  number * 2;
});

console.log(doubled); // [undefined, undefined, undefined, undefined]
~~~

올바른 방법은 두 가지입니다.

~~~javascript
/* return을 작성 */
const doubledA = numbers.map((number) => {
  return number * 2;
});

/* 중괄호를 생략하고 바로 반환 */
const doubledB = numbers.map((number) => number * 2);
~~~

---

## 7. filter

### 7.1 filter란?

filter는 배열의 요소를 조건에 따라 검사하고, 조건 결과가 true인 요소만 모아 새로운 배열을 만드는 메서드입니다.

~~~javascript
const numbers = [1, 2, 3, 4, 5];

const evenNumbers = numbers.filter((number) => {
  return number % 2 === 0;
});

console.log(evenNumbers); // [2, 4]
~~~

처리 흐름은 다음과 같습니다.

~~~text
1 → false → 제외
2 → true  → 남김
3 → false → 제외
4 → true  → 남김
5 → false → 제외

결과: [2, 4]
~~~

filter도 원본 배열을 바꾸지 않습니다.

~~~javascript
const numbers = [1, 2, 3, 4, 5];
const evenNumbers = numbers.filter((number) => number % 2 === 0);

console.log(numbers);      // [1, 2, 3, 4, 5]
console.log(evenNumbers);  // [2, 4]
~~~

### 7.2 기본 문법

~~~javascript
const newArray = array.filter((currentValue, index, array) => {
  return condition;
});
~~~

- 조건이 true이면 현재 요소를 새 배열에 추가합니다.
- 조건이 false이면 현재 요소를 제외합니다.
- 모든 조건이 false이면 빈 배열을 반환합니다.
- 결과 배열의 개수는 원본보다 같거나 작습니다.

~~~javascript
const scores = [45, 80, 92, 60];

const passedScores = scores.filter((score) => score >= 60);

console.log(passedScores); // [80, 92, 60]
~~~

### 7.3 객체 배열 필터링하기

객체 배열에서 특정 조건에 맞는 데이터만 선택할 수 있습니다.

~~~javascript
const repositories = [
  { name: "portfolio", fork: false, archived: false },
  { name: "example", fork: true, archived: false },
  { name: "old-project", fork: false, archived: true }
];

const visibleRepositories = repositories.filter(
  ({ fork, archived }) => !fork && !archived
);

console.log(visibleRepositories);
// [{ name: "portfolio", fork: false, archived: false }]
~~~

위 코드는 다음 뜻입니다.

- fork가 false인 저장소
- archived가 false인 저장소
- 두 조건을 모두 만족하는 저장소만 남김

현재 프로젝트에서는 GitHub 저장소 중 포크와 보관된 저장소를 제외할 때 filter를 사용합니다.

### 7.4 여러 조건 사용하기

논리 연산자를 사용해 조건을 여러 개 조합할 수 있습니다.

~~~javascript
const products = [
  { name: "키보드", price: 50000, inStock: true },
  { name: "마우스", price: 30000, inStock: false },
  { name: "모니터", price: 200000, inStock: true }
];

const affordableProducts = products.filter(
  (product) => product.price < 100000 && product.inStock
);

console.log(affordableProducts);
// [{ name: "키보드", price: 50000, inStock: true }]
~~~

- &&: 모든 조건이 true여야 합니다.
- ||: 조건 중 하나라도 true이면 됩니다.
- !: true와 false를 반대로 바꿉니다.

---

## 8. map과 filter 비교

| 구분 | map | filter |
| --- | --- | --- |
| 목적 | 모든 요소를 변환 | 조건에 맞는 요소만 선택 |
| 결과 개수 | 원본과 같음 | 원본과 같거나 적음 |
| 콜백의 return | 새 배열에 넣을 값 | 남길지 결정하는 true/false |
| 예시 | 객체를 HTML로 변환 | 공개 저장소만 선택 |
| 질문 | “각 요소를 무엇으로 바꿀까?” | “어떤 요소를 남길까?” |

같은 배열에 적용해 보면 차이가 더 분명합니다.

~~~javascript
const numbers = [1, 2, 3, 4];

/* 모든 값을 2배로 변환 */
const mapped = numbers.map((number) => number * 2);
// [2, 4, 6, 8]

/* 짝수만 선택 */
const filtered = numbers.filter((number) => number % 2 === 0);
// [2, 4]
~~~

map은 요소의 값을 바꾸고, filter는 요소의 개수를 줄일 수 있습니다.

---

## 9. map과 filter 함께 사용하기

실제 데이터 처리에서는 filter로 필요한 데이터를 고른 다음 map으로 화면에 맞게 변환하는 경우가 많습니다.

~~~javascript
const numbers = [1, 2, 3, 4, 5, 6];

const result = numbers
  .filter((number) => number % 2 === 0)
  .map((number) => number * 10);

console.log(result); // [20, 40, 60]
~~~

처리 순서는 다음과 같습니다.

~~~text
원본 [1, 2, 3, 4, 5, 6]
  ↓ filter: 짝수만 선택
[2, 4, 6]
  ↓ map: 10을 곱함
[20, 40, 60]
~~~

API 데이터를 화면에 표시하는 대표적인 흐름은 다음과 같습니다.

~~~javascript
const visibleRepositories = repositories
  .filter(({ fork, archived }) => !fork && !archived)
  .slice(0, 6)
  .map(createProjectCard)
  .join("");

projectsGrid.innerHTML = visibleRepositories;
~~~

각 단계의 역할은 다음과 같습니다.

1. filter: 표시하지 않을 데이터를 제외합니다.
2. slice: 최대 개수만 선택합니다.
3. map: 각 데이터를 카드 HTML로 변환합니다.
4. join: 문자열 배열을 하나의 HTML 문자열로 합칩니다.
5. innerHTML: 완성한 문자열을 화면에 표시합니다.

이처럼 메서드를 줄로 연결하는 것을 메서드 체이닝(method chaining)이라고 합니다.

---

## 10. map, filter, forEach의 차이

forEach도 배열의 모든 요소를 반복하지만, map과 목적이 다릅니다.

~~~javascript
const numbers = [1, 2, 3];

const mapResult = numbers.map((number) => number * 2);
const forEachResult = numbers.forEach((number) => number * 2);

console.log(mapResult);     // [2, 4, 6]
console.log(forEachResult); // undefined
~~~

| 메서드 | 용도 | 반환값 |
| --- | --- | --- |
| map | 모든 요소를 변환 | 새로운 배열 |
| filter | 조건에 맞는 요소를 선택 | 새로운 배열 |
| forEach | 각 요소에 작업 실행 | 기본적으로 undefined |

### forEach를 사용하는 상황

화면의 요소에 이벤트를 등록하거나, 결과 배열이 필요 없는 작업에는 forEach가 적합합니다.

~~~javascript
buttons.forEach((button) => {
  button.addEventListener("click", handleClick);
});
~~~

### map을 사용하는 상황

각 요소를 새로운 값으로 변환해 결과 배열이 필요할 때 사용합니다.

~~~javascript
const names = users.map((user) => user.name);
~~~

### filter를 사용하는 상황

조건에 맞는 데이터만 모아 새로운 배열이 필요할 때 사용합니다.

~~~javascript
const activeUsers = users.filter((user) => user.active);
~~~

---

## 11. 원본 배열과 얕은 복사

map과 filter는 새 배열을 반환하므로 원본 배열의 요소 개수나 배열 구조는 바꾸지 않습니다.

~~~javascript
const numbers = [1, 2, 3];
const doubled = numbers.map((number) => number * 2);

console.log(numbers); // [1, 2, 3]
~~~

다만 객체 배열에서는 객체 자체가 깊이 복사되는 것은 아닙니다.

~~~javascript
const users = [{ name: "민수" }];
const copiedUsers = users.map((user) => user);

copiedUsers[0].name = "지영";

console.log(users[0].name); // "지영"
~~~

배열은 새로 만들어졌지만, 내부 객체는 같은 객체를 가리키고 있기 때문입니다. 이 내용을 얕은 복사라고 합니다.

객체를 수정하지 않고 새로운 객체를 만들려면 다음처럼 작성합니다.

~~~javascript
const renamedUsers = users.map((user) => ({
  ...user,
  name: "지영"
}));
~~~

초보 단계에서는 다음 원칙을 기억하면 충분합니다.

- 숫자나 문자열을 변환하는 map은 원본에 영향을 주지 않습니다.
- 객체의 속성을 직접 수정하면 원본 객체에도 영향을 줄 수 있습니다.
- 기존 객체를 유지하면서 일부 값만 바꾸려면 전개 연산자(...)로 새 객체를 만듭니다.

---

## 12. 자주 하는 실수

### 12.1 map에서 조건에 따라 요소를 빼려고 하기

map은 모든 요소에 대해 결과를 만들어야 합니다.

~~~javascript
const numbers = [1, 2, 3, 4];

const result = numbers.map((number) => {
  if (number % 2 === 0) {
    return number;
  }
});

console.log(result); // [undefined, 2, undefined, 4]
~~~

일부 요소만 남기려면 filter를 먼저 사용합니다.

~~~javascript
const result = numbers
  .filter((number) => number % 2 === 0)
  .map((number) => number * 10);

console.log(result); // [20, 40]
~~~

### 12.2 filter에서 변환된 값을 반환하기

filter의 return 값은 새 값이 아니라 true 또는 false로 해석되는 조건이어야 합니다.

~~~javascript
const numbers = [1, 2, 3];

const result = numbers.filter((number) => number * 2);
// 모든 값이 0이 아니므로 모두 남을 수 있음
~~~

변환이 목적이면 map을 사용합니다.

~~~javascript
const result = numbers.map((number) => number * 2);
~~~

### 12.3 filter 결과가 항상 하나라고 생각하기

filter는 조건에 맞는 모든 요소를 배열로 반환합니다. 하나만 찾고 싶다면 find를 고려할 수 있습니다.

~~~javascript
const users = [
  { id: 1, name: "민수" },
  { id: 2, name: "지영" }
];

const user = users.find((item) => item.id === 2);

console.log(user); // { id: 2, name: "지영" }
~~~

### 12.4 원본 배열이 바뀐다고 생각하기

map과 filter는 원본 배열을 바꾸지 않습니다. 결과를 변수에 저장해야 합니다.

~~~javascript
const numbers = [1, 2, 3];

numbers.map((number) => number * 2);
console.log(numbers); // [1, 2, 3]
~~~

### 12.5 너무 긴 체이닝 만들기

메서드 체이닝은 편리하지만, 한 줄이 지나치게 길면 각 단계를 의미 있는 변수로 나누는 편이 읽기 쉽습니다.

~~~javascript
const visibleRepositories = repositories.filter(
  ({ fork, archived }) => !fork && !archived
);

const recentRepositories = visibleRepositories.slice(0, 6);
const cards = recentRepositories.map(createProjectCard);
const html = cards.join("");
~~~

---

## 13. 현재 프로젝트에서의 활용

현재 프로젝트는 GitHub API에서 받은 저장소 배열을 다음 순서로 처리합니다.

~~~javascript
const visibleRepositories = repositories
  .filter(({ fork, archived }) => !fork && !archived)
  .slice(0, 6);

projectsGrid.innerHTML = visibleRepositories
  .map(createProjectCard)
  .join("");
~~~

### filter 단계

~~~javascript
.filter(({ fork, archived }) => !fork && !archived)
~~~

포크 저장소와 보관된 저장소를 제외합니다. 조건에 맞는 저장소만 다음 단계로 전달합니다.

### slice 단계

~~~javascript
.slice(0, 6)
~~~

앞에서부터 최대 6개의 저장소만 선택합니다. slice 역시 원본 배열을 바꾸지 않고 일부를 담은 새 배열을 반환합니다.

### map 단계

~~~javascript
.map(createProjectCard)
~~~

각 저장소 객체를 프로젝트 카드 HTML 문자열로 변환합니다.

### join 단계

~~~javascript
.join("")
~~~

map의 결과인 문자열 배열을 하나의 문자열로 합칩니다.

이 흐름은 다음과 같습니다.

~~~text
GitHub 저장소 배열
  ↓ filter
포크·보관 저장소 제외
  ↓ slice
최대 6개 선택
  ↓ map
카드 HTML로 변환
  ↓ join
하나의 문자열로 결합
  ↓ innerHTML
브라우저 화면에 표시
~~~

---

## 14. 실전 판단 기준

다음 질문으로 메서드를 선택할 수 있습니다.

### 모든 요소를 다른 값으로 바꾸고 싶은가?

map을 사용합니다.

~~~javascript
const prices = [1000, 2000, 3000];
const discountedPrices = prices.map((price) => price * 0.9);
~~~

### 조건에 맞는 요소만 남기고 싶은가?

filter를 사용합니다.

~~~javascript
const prices = [1000, 2000, 3000];
const expensivePrices = prices.filter((price) => price >= 2000);
~~~

### 각 요소에 작업만 실행하고 결과 배열은 필요 없는가?

forEach를 사용합니다.

~~~javascript
prices.forEach((price) => {
  console.log(price);
});
~~~

### 조건에 맞는 첫 번째 요소 하나만 찾고 싶은가?

find를 사용합니다.

~~~javascript
const price = prices.find((price) => price >= 2000);
~~~

---

## 15. 최종 요약

### map

~~~javascript
const result = array.map((item) => {
  return newValue;
});
~~~

배열의 모든 요소를 변환해 원본과 같은 개수의 새 배열을 만듭니다.

### filter

~~~javascript
const result = array.filter((item) => {
  return condition;
});
~~~

조건이 true인 요소만 모아 새 배열을 만듭니다.

### 기억할 기준

> map은 “모든 요소를 무엇으로 바꿀까?”  
> filter는 “어떤 요소를 남길까?”  
> forEach는 “각 요소에 어떤 작업을 실행할까?”

API 데이터를 화면에 표시할 때는 보통 다음 흐름을 사용합니다.

~~~text
filter로 필요한 데이터 선택
→ slice로 개수 제한
→ map으로 화면 형태로 변환
→ join으로 결합
→ DOM에 렌더링
~~~

