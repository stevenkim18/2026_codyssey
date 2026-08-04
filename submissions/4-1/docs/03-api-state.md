# GitHub API와 상태 관리 설명 자료

## 1. API란 무엇인가요?

API는 다른 프로그램의 기능이나 데이터를 사용할 수 있도록 정해 둔 약속입니다. 이 프로젝트는 GitHub REST API를 사용해 GitHub 저장소 목록을 가져옵니다.

사용한 엔드포인트는 다음과 같습니다.

```text
https://api.github.com/users/{사용자ID}/repos
```

현재 프로젝트에서는 `js/main.js`의 설정값을 바탕으로 다음 URL을 요청합니다.

```text
https://api.github.com/users/stevenkim18/repos?sort=updated&per_page=100
```

## 2. `fetch`와 `async/await`

네트워크 요청은 시간이 걸릴 수 있으므로 비동기 방식으로 처리합니다.

```javascript
const loadProjects = async () => {
  showProjectState("loading");

  try {
    const response = await fetch(apiUrl);
    if (!response.ok) throw new Error("API 요청 실패");
    const repositories = await response.json();
  } catch (error) {
    showProjectState("error");
  }
};
```

- `async`: 함수 안에서 `await`를 사용할 수 있게 합니다.
- `await`: Promise가 완료될 때까지 해당 함수의 다음 작업을 기다립니다.
- `fetch`: 서버에 네트워크 요청을 보냅니다.
- `response.ok`: HTTP 응답이 성공 범위인지 확인합니다.
- `response.json()`: 응답 본문을 JavaScript 객체나 배열로 변환합니다.
- `try/catch`: 요청 성공과 실패를 나누어 처리합니다.

## 3. API 상태

API는 요청 결과만 있는 것이 아니라 요청 중인 상태도 있습니다. 이 프로젝트는 네 가지 상태를 화면에 표시합니다.

| 상태 | 화면 | 조건 |
| --- | --- | --- |
| loading | 로딩 문구와 스피너 | 요청을 시작한 직후 |
| success | 프로젝트 카드 목록 | 응답 성공 및 데이터 존재 |
| error | 에러 문구와 다시 시도 버튼 | 네트워크 오류 또는 실패 응답 |
| empty | 표시할 프로젝트가 없다는 문구 | 성공했지만 배열이 비어 있음 |

`showProjectState`는 각 상태에 따라 `hidden` 속성을 바꾸고, 필요한 영역만 보이게 합니다.

## 4. 데이터 가공

GitHub에서 받은 모든 저장소를 그대로 보여주지 않고 다음 조건으로 가공합니다.

1. `filter`로 fork와 archived 저장소를 제외합니다.
2. `slice`로 최신 저장소 중 최대 6개를 선택합니다.
3. `map`으로 저장소 객체를 카드 HTML로 변환합니다.
4. `innerHTML`로 Projects 영역에 삽입합니다.

이 과정은 “데이터 상태 변경 → DOM 렌더링”의 대표적인 예입니다.

## 5. 오류 처리

GitHub API는 인증 없이 호출하면 시간당 요청 횟수 제한이 있습니다. 제한에 걸리거나 네트워크가 끊기면 `response.ok`가 `false`가 될 수 있습니다. 이때 `throw`로 오류를 `catch`에 전달하고, 사용자가 상황을 이해할 수 있는 메시지와 재시도 버튼을 보여줍니다.

## 6. 평가 질문

### `fetch`는 왜 비동기로 사용하나요?

서버 응답을 기다리는 동안 브라우저 화면이 멈추지 않아야 하기 때문입니다. `async/await`를 사용하면 비동기 코드를 순서가 읽히는 형태로 작성할 수 있습니다.

### `response.ok`를 확인하는 이유는 무엇인가요?

`fetch`는 서버가 404나 403을 반환해도 Promise 자체가 해결될 수 있습니다. 따라서 실제 HTTP 응답이 성공인지 직접 확인해야 합니다.

### 로딩·에러·빈 상태가 왜 필요한가요?

사용자는 데이터가 없는 것인지, 아직 불러오는 중인지, 요청에 실패한 것인지 구분할 수 있어야 합니다. 상태별 UI는 사용자에게 현재 상황과 다음 행동을 알려줍니다.

