# 실행, 배포, 접근성 설명 자료

## 1. VS Code와 Live Server

HTML 파일을 직접 더블 클릭하면 `file://` 주소로 열립니다. 이 방식은 브라우저 보안 정책 때문에 외부 API 요청이 제한될 수 있습니다.

Live Server는 프로젝트 폴더를 작은 로컬 웹 서버로 실행해 다음과 같은 HTTP 주소를 만들어 줍니다.

```text
http://127.0.0.1:5500/submissions/4-1/index.html
```

실행 방법:

1. VS Code에서 저장소 루트를 엽니다.
2. `submissions/4-1/index.html`을 엽니다.
3. Live Server 확장 프로그램을 설치합니다.
4. 파일에서 마우스 오른쪽 버튼을 누르고 **Open with Live Server**를 선택합니다.

## 2. 상대 경로

현재 `index.html` 기준으로 CSS, JavaScript, 이미지 경로를 작성했습니다.

```html
<link rel="stylesheet" href="css/style.css" />
<script src="js/main.js" defer></script>
<img src="images/profile.svg" alt="..." />
```

배포 위치가 바뀌어도 같은 폴더 구조를 유지하면 리소스가 올바르게 연결됩니다.

## 3. GitHub Pages

이 프로젝트는 정적 HTML 사이트이므로 GitHub Pages로 배포할 수 있습니다.

현재 결과물은 `submissions/4-1/`에 있습니다. 저장소 루트를 GitHub Pages 배포 대상으로 선택하면 다음처럼 하위 경로에서 접속할 수 있습니다.

```text
https://stevenkim18.github.io/2026_codyssey/submissions/4-1/
```

GitHub에서 설정하는 흐름:

1. 저장소의 **Settings**로 이동합니다.
2. **Pages** 메뉴를 엽니다.
3. 배포 브랜치로 `main`을 선택합니다.
4. 폴더는 저장소 루트(`/`)를 선택합니다.
5. 생성된 URL에서 `/submissions/4-1/` 경로를 추가해 접속합니다.

배포 후에는 CSS, JavaScript, 이미지가 모두 200 응답으로 로드되는지와 GitHub API 요청이 정상인지 확인합니다.

## 4. 접근성 체크

- 모든 이미지에 의미 있는 `alt`를 작성했습니다.
- 폼의 `label`과 입력 요소를 연결했습니다.
- 버튼은 `button` 요소로 작성해 키보드로 조작할 수 있습니다.
- 메뉴 열림 상태를 `aria-expanded`로 표현했습니다.
- 다크 모드 상태를 `aria-pressed`로 표현했습니다.
- API 로딩과 폼 성공 상태를 보조 기술이 알 수 있도록 `role="status"`와 `aria-live`를 사용했습니다.
- `prefers-reduced-motion`을 지원해 애니메이션을 줄일 수 있게 했습니다.
- 외부 링크에 `target="_blank"`를 사용할 때 `rel="noreferrer"`를 추가했습니다.

## 5. 최종 점검표

- [ ] 데스크톱에서 레이아웃 확인
- [ ] 모바일에서 햄버거 메뉴 확인
- [ ] 다크 모드 전환 및 새로고침 유지 확인
- [ ] GitHub 프로젝트 카드 확인
- [ ] API 에러 및 재시도 UI 확인
- [ ] 빈 폼 제출 오류 확인
- [ ] 잘못된 이메일 형식 오류 확인
- [ ] 정상 폼 제출 성공 메시지 확인
- [ ] GitHub Pages URL 확인
- [ ] 배포된 URL에서 이미지·CSS·JavaScript 로드 확인

## 6. 평가 질문

### 왜 GitHub Pages를 사용하나요?

이 프로젝트는 서버에서 별도의 프로그램을 실행하지 않는 정적 웹사이트이므로 GitHub 저장소와 연결해 쉽게 공개할 수 있습니다.

### 배포 후 가장 먼저 확인할 것은 무엇인가요?

상대 경로가 맞는지, CSS와 JavaScript가 로드되는지, GitHub API가 호출되는지, 모바일 레이아웃이 유지되는지를 확인합니다.

### 접근성을 고려한 부분은 무엇인가요?

시맨틱 태그, 이미지 대체 텍스트, 폼 라벨, 키보드 조작 가능한 버튼, ARIA 상태 속성, 동작 감소 설정을 적용했습니다.

