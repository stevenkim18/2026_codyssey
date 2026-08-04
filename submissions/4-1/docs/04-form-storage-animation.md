# 폼, localStorage, 스크롤 애니메이션 설명 자료

## 1. 문의 폼 검증

문의 폼은 이름, 이메일, 메시지를 입력받습니다. 모든 필드는 필수이고 이메일은 정규 표현식으로 기본적인 형식을 확인합니다.

```javascript
const validationRules = {
  name: (value) => value.trim() ? "" : "이름을 입력해주세요.",
  email: (value) => {
    if (!value.trim()) return "이메일을 입력해주세요.";
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
      ? ""
      : "올바른 이메일 형식을 입력해주세요.";
  },
};
```

검증 함수는 오류가 없으면 빈 문자열을, 오류가 있으면 사용자에게 보여줄 메시지를 반환합니다.

### 제출 흐름

```text
submit 이벤트 발생
→ event.preventDefault()
→ 모든 필드 검증
→ 하나라도 실패하면 오류 메시지 표시
→ 모두 성공하면 폼 초기화 및 성공 메시지 표시
```

`event.preventDefault()`는 실제 서버로 폼을 전송하고 페이지가 새로고침되는 기본 동작을 막습니다. 현재 과제는 실제 이메일 전송이 보너스 범위이므로, 성공 메시지만 표시합니다.

## 2. `localStorage`

`localStorage`는 브라우저에 문자열 형태의 데이터를 저장하는 기능입니다. 페이지를 새로고침해도 같은 도메인에서는 값이 남아 있습니다.

```javascript
localStorage.setItem("portfolio-theme", "dark");
const storedTheme = localStorage.getItem("portfolio-theme");
```

이 프로젝트에서는 테마 상태를 `portfolio-theme`라는 키로 저장합니다.

```text
페이지 실행
→ localStorage에서 기존 테마 읽기
→ body의 data-theme 설정
→ CSS 변수로 색상 적용
→ 버튼을 누르면 반대 테마 저장
```

## 3. Intersection Observer

Intersection Observer는 요소가 화면에 들어왔는지 감지하는 브라우저 API입니다. 스크롤 이벤트에서 매번 위치를 계산하는 것보다 특정 요소의 화면 진입을 관찰하는 목적에 적합합니다.

```javascript
const observer = new IntersectionObserver(callback, {
  threshold: 0.2,
});
```

`threshold: 0.2`는 관찰 대상의 약 20%가 화면에 들어왔을 때 콜백을 실행한다는 의미입니다. 콜백에서 `is-visible` 클래스를 추가하고, CSS가 투명도와 이동 거리를 바꿔 애니메이션을 보여줍니다.

## 4. 스크롤 기반 UI

`window.scrollY`로 현재 스크롤 위치를 읽습니다.

- 60px 이상: 헤더에 `scrolled` 클래스 추가
- 300px 이상: 맨 위로 버튼 표시
- 맨 위로 버튼 클릭: `window.scrollTo({ top: 0, behavior: "smooth" })`

스크롤 이벤트에는 `{ passive: true }`를 사용해 브라우저가 스크롤을 더 효율적으로 처리할 수 있게 했습니다.

## 5. 평가 질문

### `localStorage`와 일반 변수의 차이는 무엇인가요?

일반 변수는 페이지가 새로고침되면 사라지지만 `localStorage`는 브라우저에 저장되어 새로고침 후에도 값을 읽을 수 있습니다.

### Intersection Observer를 사용한 이유는 무엇인가요?

요소가 화면에 들어오는 순간을 감지하기에 적합하고, 모든 스크롤 이벤트마다 요소 위치를 직접 계산하는 방식보다 목적이 명확합니다.

### `preventDefault()`는 왜 사용했나요?

문의 폼이 제출될 때 브라우저의 기본 페이지 이동과 새로고침을 막고, JavaScript로 직접 검증과 성공 메시지 표시를 처리하기 위해 사용했습니다.

