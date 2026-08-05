# 4-2 과제 안내: React CRUD 웹 서비스 만들기

이 문서는 [subject4-2 과제 설명](../../../subjects/subject4-2.md)을 처음 읽는 학습자를 위한 학습·구현 안내서입니다.

과제의 핵심은 예쁜 웹사이트를 만드는 것이 아닙니다. 사용자의 행동이 React 상태를 바꾸고, 그 상태에 따라 화면이 다시 그려지는 흐름을 직접 구현하고 설명하는 것입니다.

## 현재 결정된 기술 스택

이번 프로젝트는 다음 조합으로 진행합니다.

| 영역 | 선택 |
| --- | --- |
| 프레임워크 | React + Vite |
| 언어 | TypeScript |
| 라우팅 | React Router |
| 데이터베이스 | Supabase |
| 스타일링 | Tailwind CSS |
| 배포 | Vercel |

TypeScript와 Tailwind CSS는 과제의 필수 조건은 아니지만, 이번 프로젝트에서는 코드의 타입 안정성과 빠른 UI 개발을 위해 사용합니다. 다만 핵심은 여전히 React의 컴포넌트·상태·이벤트·비동기 데이터 흐름입니다.

```text
사용자 행동
  ↓
이벤트 처리
  ↓
React 상태 변경
  ↓
컴포넌트 리렌더링
  ↓
화면 변화
```

## 1. 최종적으로 해야 하는 일

React로 하나의 작은 웹 서비스를 만들고 외부에서 접속할 수 있도록 배포해야 합니다. 서비스의 주제는 직접 정하면 됩니다.

초보자에게 적당한 주제는 다음과 같습니다.

- 할 일 관리
- 독서 기록
- 영화 리뷰
- 맛집 기록
- 여행 일정
- 공부 자료 북마크

처음부터 쇼핑몰, SNS, 중고 거래처럼 기능이 많은 서비스를 만들면 범위가 너무 커집니다. 핵심 데이터 하나만 정하고, 그 데이터를 등록·조회·수정·삭제할 수 있게 만드는 것이 좋습니다.

예를 들어 할 일 관리 서비스를 선택한다면 핵심 데이터는 다음과 같습니다.

```text
할 일
├── 제목
├── 설명
├── 완료 여부
└── 생성일
```

이 데이터를 Supabase 또는 Firebase에 저장하고, React 화면에서 다음 작업이 모두 가능해야 합니다.

| 작업 | 의미 | 할 일 서비스의 예 |
| --- | --- | --- |
| Create | 새 데이터 등록 | 새로운 할 일 저장 |
| Read | 데이터 조회 | 할 일 목록·상세 보기 |
| Update | 기존 데이터 수정 | 제목이나 완료 여부 수정 |
| Delete | 데이터 삭제 | 할 일 삭제 |

## 2. 반드시 만족해야 하는 조건

### 라우팅

- 최소 5개 이상의 페이지 라우트
- 목록 페이지와 상세 페이지
- 잘못된 주소를 위한 Not Found 페이지
- 헤더나 네비게이션을 통한 페이지 이동

예시 라우트는 다음과 같습니다.

| 주소 | 페이지 역할 |
| --- | --- |
| / | 홈 또는 서비스 소개 |
| /items | 핵심 데이터 목록 |
| /items/new | 새 데이터 등록 |
| /items/:id | 특정 데이터 상세 |
| /items/:id/edit | 특정 데이터 수정 |
| * | Not Found |

items/:id의 :id는 실제 데이터 ID가 들어가는 동적 주소입니다. ID가 123이면 /items/123으로 접근합니다.

### CRUD

- 목록에서 원격 데이터 목록을 볼 수 있어야 합니다.
- 목록 항목을 클릭하면 상세 페이지로 이동해야 합니다.
- 등록 폼으로 새 데이터를 저장할 수 있어야 합니다.
- 수정 폼으로 기존 데이터를 변경할 수 있어야 합니다.
- 삭제 후 목록이 갱신되거나 다른 페이지로 이동해야 합니다.

### 폼 UX

- 제목·내용 같은 필수값이 비어 있으면 제출할 수 없어야 합니다.
- 어떤 값이 잘못되었는지 에러 메시지를 보여줘야 합니다.
- 제출 중에는 버튼을 비활성화하거나 스피너를 보여줘야 합니다.
- 네트워크나 권한 오류가 발생하면 실패 사실을 화면에 표시해야 합니다.

### 로딩·성공·빈 상태·에러 상태

핵심 화면에는 다음 네 가지 상태가 있어야 합니다.

| 상태 | 사용자에게 보여줄 내용 |
| --- | --- |
| 로딩 | 데이터를 불러오는 중이라는 표시 |
| 성공 | 목록이나 상세 데이터 |
| 빈 상태 | 데이터가 없다는 안내 |
| 에러 | 요청 실패 안내와 재시도 방법 |

같은 상태 UI를 페이지마다 복사하지 말고 Loading, ErrorState, EmptyState 같은 재사용 컴포넌트로 만듭니다.

### 컴포넌트와 폴더

최소 8개 이상의 재사용 컴포넌트를 만들고, 페이지 컴포넌트와 UI 컴포넌트를 분리합니다.

```text
src/
├── components/       # 여러 페이지에서 재사용하는 UI
├── hooks/            # 데이터 조회·갱신을 담당하는 커스텀 훅
├── lib/              # Supabase/Firebase 설정과 유틸리티
├── pages/            # 라우트와 연결되는 화면
├── App.tsx           # 라우팅과 공통 레이아웃
└── main.tsx          # React 시작점
```

재사용 컴포넌트의 예시는 다음과 같습니다.

- Button
- Input
- Textarea
- Card
- Loading
- ErrorState
- EmptyState
- ItemCard
- ItemList
- ItemForm
- Header
- Layout

컴포넌트 개수만 늘리는 것이 목적은 아닙니다. Button이 variant prop에 따라 기본 버튼·삭제 버튼으로 달라지는 것처럼, props를 받아 실제로 재사용할 수 있어야 합니다.

## 3. 초보자가 공부해야 하는 것

모든 내용을 한 번에 공부할 필요는 없습니다. 아래 순서대로 기초를 익히고 바로 작은 기능을 만들어 보세요.

### 1단계: JavaScript와 TypeScript 기초

React 코드를 이해하려면 다음 문법이 필요합니다.

- const, let
- 함수와 화살표 함수
- 객체와 배열
- 구조분해 할당
- map, filter, find
- 조건문과 삼항 연산자
- import, export
- Promise, async/await, try/catch

TypeScript에서는 여기에 다음 개념을 추가로 공부합니다.

- 기본 타입: string, number, boolean, 배열
- 객체 타입과 type 또는 interface
- 함수 매개변수와 반환값 타입
- 선택적 속성(?)
- React props 타입 작성
- useState 상태 타입 작성

특히 배열의 map은 목록을 화면에 여러 개 그릴 때 자주 사용합니다.

```tsx
items.map((item) => (
  <ItemCard key={item.id} item={item} />
))
```

items 배열의 각 데이터를 ItemCard 컴포넌트로 바꾸어 화면에 표시하는 코드입니다.

### 2단계: React와 Tailwind CSS 기본 개념

#### 컴포넌트와 TSX

컴포넌트는 화면의 일부를 담당하는 함수입니다. 버튼, 카드, 헤더처럼 반복되거나 역할이 분명한 UI를 컴포넌트로 나눕니다. TSX는 TypeScript 안에서 HTML과 비슷한 문법으로 UI를 작성하는 방식입니다.

```tsx
type GreetingProps = {
  name: string
}

function Greeting({ name }: GreetingProps) {
  return <h1>안녕하세요, {name}님</h1>
}
```

#### props

props는 부모 컴포넌트가 자식 컴포넌트에게 전달하는 값입니다. TypeScript에서는 props의 모양과 타입을 먼저 선언하면 잘못된 값을 전달했을 때 개발 도구가 알려줍니다.

```tsx
<ItemCard item={item} onDelete={handleDelete} />
```

#### state

state는 컴포넌트가 기억해야 하는 값입니다. 입력값, 목록 데이터, 로딩 여부처럼 바뀌면 화면도 바뀌어야 하는 값은 state로 관리합니다.

```tsx
const [title, setTitle] = useState<string>("")
```

title을 직접 바꾸지 않고 setTitle을 호출해야 React가 상태 변경을 알고 화면을 다시 렌더링합니다.

#### 이벤트와 조건부 렌더링

사용자의 클릭·입력·제출을 이벤트로 처리합니다. 이벤트 핸들러에서 state를 변경하면 컴포넌트가 다시 렌더링됩니다.

```tsx
<button onClick={handleClick}>삭제</button>
<input value={title} onChange={handleTitleChange} />
```

로딩·에러·빈 상태처럼 조건에 따라 다른 화면을 보여주는 것도 배워야 합니다.

```tsx
if (isLoading) return <Loading />
if (error) return <ErrorState message={error} />
if (items.length === 0) return <EmptyState />

return <ItemList items={items} />
```

#### Tailwind CSS

Tailwind CSS는 미리 준비된 유틸리티 클래스를 JSX 요소에 조합해 스타일을 작성하는 방식입니다. 별도의 CSS 파일에서 긴 선택자를 만들기보다 요소의 className에 레이아웃·간격·색상·반응형 클래스를 작성합니다.

    <button className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 disabled:opacity-50">
      저장
    </button>

먼저 Tailwind에서 자주 사용하는 다음 클래스를 익히면 충분합니다.

- 레이아웃: flex, grid, block, hidden
- 간격: p-*, px-*, py-*, m-*, gap-*
- 크기: w-*, h-*, max-w-*
- 글자: text-*, font-*
- 색상: bg-*, text-*, border-*
- 상태: hover:*, focus:*, disabled:*
- 반응형: sm:*, md:*, lg:*

Tailwind 클래스를 컴포넌트마다 무작정 복사하기보다 Button, Card, Input 같은 컴포넌트 안에 스타일을 모아두면 수정하기 쉽습니다.

### 3단계: useState와 useEffect

useState로 폼 입력값, 목록, 선택된 필터, 제출 중 여부를 관리합니다.

```tsx
const [items, setItems] = useState([])
const [isLoading, setIsLoading] = useState(true)
const [error, setError] = useState(null)
```

useEffect는 컴포넌트가 화면에 나타난 뒤 데이터를 불러오거나, 특정 값이 바뀌었을 때 작업을 실행합니다.

```tsx
useEffect(() => {
  loadItems()
}, [])
```

의존성 배열이 비어 있으면 컴포넌트가 처음 나타날 때 한 번 실행하는 패턴으로 사용합니다. 상세 페이지에서 ID가 바뀔 때 다시 조회하려면 ID를 의존성에 넣습니다.

```tsx
useEffect(() => {
  loadItem(id)
}, [id])
```

useEffect를 사용할 때는 effect 안에서 사용하는 값 중 무엇이 바뀌면 다시 실행해야 하는지 생각해야 합니다.

### 4단계: React Router

라우터는 URL에 따라 어떤 페이지 컴포넌트를 보여줄지 결정합니다.

공부할 내용은 다음과 같습니다.

- BrowserRouter
- Routes와 Route
- Link와 NavLink
- useNavigate
- useParams
- *를 이용한 Not Found 라우트

라우트 파라미터는 상세 데이터 조회에 사용합니다.

```tsx
const { id } = useParams()
```

이 값을 조회 조건에 사용하면 /items/123에서 ID가 123인 데이터를 불러올 수 있습니다.

### 5단계: controlled input과 폼 검증

controlled input은 input의 값을 React state가 관리하는 방식입니다.

```tsx
const [form, setForm] = useState({
  title: "",
  content: "",
})

const handleChange = (event) => {
  const { name, value } = event.target
  setForm((previous) => ({
    ...previous,
    [name]: value,
  }))
}
```

폼 제출은 다음 순서로 처리합니다.

```text
submit 이벤트 발생
  ↓
preventDefault로 브라우저 기본 제출 방지
  ↓
필수값 검사
  ↓
검증 실패 → 에러 메시지 표시
  ↓
검증 성공 → isSubmitting = true
  ↓
원격 데이터 저장
  ↓
성공 → 목록 또는 상세 페이지로 이동
  ↓
실패 → 에러 메시지 표시
  ↓
마지막에 isSubmitting = false
```

### 6단계: 비동기 처리

원격 데이터 요청은 즉시 끝나지 않으므로 요청 상태를 별도로 관리해야 합니다.

```tsx
try {
  setIsLoading(true)
  setError(null)

  const result = await fetchItems()
  setItems(result)
} catch (requestError) {
  setError("데이터를 불러오지 못했습니다.")
} finally {
  setIsLoading(false)
}
```

try/catch/finally를 이용해 성공·실패·종료 시점을 나눕니다. finally는 성공하든 실패하든 실행되므로 로딩 종료 처리에 유용합니다.

### 7단계: Supabase 또는 Firebase

과제에서는 둘 중 하나를 선택해야 합니다. 하나만 선택해서 끝까지 연결하면 됩니다.

| 선택지 | 공부할 내용 |
| --- | --- |
| Supabase | 프로젝트, 테이블, 컬럼, TypeScript용 JavaScript 클라이언트, CRUD 쿼리 |
| Firebase | 프로젝트, Firestore 컬렉션·문서, TypeScript용 JavaScript SDK, CRUD 함수 |

어느 것을 선택하든 다음 작업이 가능해야 합니다.

```text
목록 조회
상세 조회
새 데이터 추가
기존 데이터 수정
데이터 삭제
```

백엔드 고급 기능이나 복잡한 데이터 관계는 필수가 아닙니다. 우선 핵심 데이터 하나를 저장하고 가져오는 흐름에 집중합니다.

### 8단계: 환경변수와 배포

API URL이나 키를 코드에 직접 작성하지 않고 환경변수로 관리하는 방법을 공부합니다.

```text
.env.local
├── VITE_SUPABASE_URL=...
└── VITE_SUPABASE_ANON_KEY=...
```

주의할 점은 다음과 같습니다.

- .env 또는 .env.local을 GitHub에 올리지 않습니다.
- .gitignore에 환경변수 파일을 추가합니다.
- 배포 서비스의 Environment Variables에도 같은 값을 등록합니다.
- 로컬에서는 되는데 배포 후 안 되는 경우 환경변수 등록 여부를 가장 먼저 확인합니다.

## 4. 추천 구현 순서

처음부터 모든 기능을 동시에 만들지 말고, 화면·데이터·상태를 한 단계씩 연결합니다.

### 1단계: 서비스 주제와 데이터 설계

먼저 핵심 데이터의 이름과 필드를 정합니다.

예시: 독서 기록 서비스

```text
Book
├── id
├── title       필수
├── author      필수
├── review      선택 또는 필수
├── rating      선택
└── created_at
```

데이터 종류를 여러 개 만들지 않습니다. Book 하나만으로 목록·상세·등록·수정·삭제가 가능한지 확인합니다.

### 2단계: React 프로젝트 시작

- React + TypeScript 프로젝트를 생성합니다.
- 개발 서버가 실행되는지 확인합니다.
- Git 저장소를 만들고 첫 커밋을 남깁니다.
- 기본 폴더를 pages, components, hooks, lib로 나눕니다.
- Tailwind CSS를 설치하고 기본 스타일이 적용되는지 확인합니다.

### 3단계: 정적 페이지와 공통 레이아웃

먼저 데이터 없이 다음 화면을 만듭니다.

- 헤더와 네비게이션
- 홈 페이지
- 목록 페이지의 제목과 빈 영역
- 등록·수정 폼의 기본 모양
- Not Found 페이지

모든 페이지에 같은 헤더가 보이도록 Layout 컴포넌트를 만듭니다.

### 4단계: 라우팅 연결

최소 라우트를 먼저 연결합니다.

```text
/
/items
/items/new
/items/:id
/items/:id/edit
*
```

각 링크를 눌러 원하는 페이지로 이동하는지 확인합니다. CRUD를 연결하기 전에 주소 이동부터 정상적으로 동작해야 합니다.

### 5단계: 백엔드 연결 전 목록 UI 완성

처음에는 임시 배열로 목록과 상세 화면을 만들면 이해하기 쉽습니다.

```tsx
const sampleItems = [
  { id: "1", title: "첫 번째 항목", content: "내용" },
]
```

이 배열을 이용해 ItemList, ItemCard, ItemDetail이 데이터를 받아 표시하는지 먼저 확인합니다. 화면 구조가 완성된 뒤 원격 데이터로 교체하면 문제를 나누어 해결할 수 있습니다.

### 6단계: 원격 데이터의 조회 연결

- 목록 페이지에서 전체 데이터를 조회합니다.
- 상세 페이지에서 useParams의 ID를 이용해 한 건을 조회합니다.
- 조회 중에는 Loading을 표시합니다.
- 데이터가 없으면 EmptyState를 표시합니다.
- 실패하면 ErrorState와 재시도 버튼을 표시합니다.

### 7단계: 등록과 수정 연결

- ItemForm에 controlled input을 적용합니다.
- 필수값 검증을 추가합니다.
- 저장 중에는 제출 버튼을 잠급니다.
- 등록 성공 후 목록 또는 새 데이터의 상세로 이동합니다.
- 수정 성공 후 상세 페이지나 목록을 갱신합니다.

등록과 수정 폼을 복사하기보다 mode나 initialValue prop을 받는 하나의 ItemForm으로 재사용하는 것이 좋습니다.

### 8단계: 삭제 연결

- 삭제 버튼을 상세 페이지에 둡니다.
- 실수로 누르지 않도록 확인 단계를 둡니다.
- 삭제 중에는 버튼을 잠급니다.
- 삭제 성공 후 목록으로 이동합니다.
- 목록이 다시 조회되거나 로컬 목록에서 해당 항목이 제거되는지 확인합니다.

### 9단계: 세 가지 이상의 상태-렌더링 흐름 확인

| 이벤트 | 상태 변화 | 화면 변화 |
| --- | --- | --- |
| 목록 조회 시작 | isLoading = true | 로딩 표시 |
| 조회 성공 | items에 데이터 저장 | 카드 목록 표시 |
| 데이터 없음 | 빈 배열 확인 | 빈 상태 표시 |
| 입력값 변경 | form.title 변경 | input 값과 검증 상태 변경 |
| 저장 중 | isSubmitting = true | 저장 버튼 비활성화 |
| 저장 성공 | successMessage 또는 라우트 변경 | 성공 안내 또는 상세 이동 |
| 삭제 성공 | 목록 다시 조회 | 삭제된 카드 사라짐 |

### 10단계: 배포와 최종 점검

- 로컬에서 npm run build가 성공하는지 확인합니다.
- 배포 서비스에 환경변수를 등록합니다.
- 배포 URL에서 목록·상세·등록·수정·삭제를 직접 테스트합니다.
- 새로고침 후에도 라우트가 정상적으로 열리는지 확인합니다.
- GitHub 저장소 URL과 배포 URL을 README에 기록합니다.

## 5. 초보자용 추천 폴더 구조

서비스의 핵심 데이터 이름을 Item이라고 가정하면 다음처럼 구성할 수 있습니다.

```text
src/
├── components/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Textarea.tsx
│   ├── Loading.tsx
│   ├── ErrorState.tsx
│   ├── EmptyState.tsx
│   ├── ItemCard.tsx
│   ├── ItemList.tsx
│   ├── ItemForm.tsx
│   ├── Header.tsx
│   └── Layout.tsx
├── hooks/
│   ├── useItems.js
│   └── useItemDetail.js
├── lib/
│   ├── supabase.js
│   └── itemApi.js
├── pages/
│   ├── HomePage.tsx
│   ├── ItemListPage.tsx
│   ├── ItemDetailPage.tsx
│   ├── ItemNewPage.tsx
│   ├── ItemEditPage.tsx
│   └── NotFoundPage.tsx
├── App.tsx
└── main.tsx
```

역할은 다음처럼 구분하면 됩니다.

- pages: URL에 연결되는 큰 화면
- components: 버튼·카드·폼처럼 여러 곳에서 사용하는 화면 조각
- hooks: 데이터 조회와 로딩·에러 상태를 묶은 재사용 로직
- lib: 외부 서비스 설정과 API 함수
- App.tsx: 라우팅과 공통 레이아웃

## 6. 꼭 직접 설명할 수 있어야 하는 React 흐름

### 목록 조회 흐름

```text
ItemListPage가 표시됨
  ↓
useItems가 실행됨
  ↓
isLoading을 true로 변경
  ↓
Supabase/Firebase에 목록 요청
  ↓
성공하면 items state에 저장
  ↓
ItemList가 items를 props로 받음
  ↓
ItemCard 여러 개가 렌더링됨
```

### 상세 조회 흐름

```text
/items/123 접속
  ↓
useParams로 id = 123 추출
  ↓
useItemDetail(123) 실행
  ↓
원격 데이터에서 ID 123 조회
  ↓
성공하면 상세 내용 표시
```

### 등록 흐름

```text
사용자가 input에 입력
  ↓
onChange 이벤트 실행
  ↓
form state 변경
  ↓
화면의 input 값 변경
  ↓
submit 이벤트 실행
  ↓
검증 후 원격 데이터 저장
  ↓
성공하면 목록 또는 상세로 이동
```

이 흐름을 코드의 어느 파일에서 담당하는지 설명할 수 있어야 합니다.

## 7. 작업 전·중·후 체크리스트

### 시작 전

- [ ] 서비스 주제를 한 문장으로 설명할 수 있다.
- [ ] 핵심 데이터의 필드와 필수값을 정했다.
- [ ] Supabase 또는 Firebase 중 하나를 선택했다.
- [ ] 최소 라우트 목록을 정했다.
- [ ] .env 파일을 Git에 올리지 않도록 .gitignore를 확인했다.

### 구현 중

- [ ] pages, components, hooks 또는 lib가 분리되어 있다.
- [ ] 공통 헤더와 네비게이션이 있다.
- [ ] 5개 이상의 라우트가 동작한다.
- [ ] 목록·상세 조회가 원격 데이터로 동작한다.
- [ ] 등록·수정·삭제가 원격 데이터로 동작한다.
- [ ] Loading, ErrorState, EmptyState를 재사용한다.
- [ ] 폼 input이 controlled input이다.
- [ ] 제출 중 버튼이 비활성화된다.
- [ ] 커스텀 훅을 하나 이상 만들었다.
- [ ] 상태 변화가 화면 변화를 일으키는 사례가 3개 이상 있다.

### 제출 전

- [ ] 잘못된 주소에서 Not Found 페이지가 보인다.
- [ ] 빈 데이터 화면을 확인했다.
- [ ] 네트워크 또는 요청 실패 화면을 확인했다.
- [ ] 필수값이 비어 있을 때 에러가 보인다.
- [ ] 등록 후 목록 또는 상세로 이동한다.
- [ ] 수정 후 변경된 값이 보인다.
- [ ] 삭제 후 목록에서 항목이 사라진다.
- [ ] 배포 URL에서 새로고침해도 라우트가 동작한다.
- [ ] README에 실행 방법과 기술 스택을 작성했다.
- [ ] README에 GitHub 저장소 URL과 배포 URL을 작성했다.

## 8. 자주 하는 실수

### 기능을 너무 많이 만드는 경우

로그인, 댓글, 검색, 좋아요, 알림을 한꺼번에 추가하면 핵심 CRUD가 늦어집니다. 먼저 단일 데이터의 CRUD를 끝낸 뒤 보너스 기능을 고려합니다.

### 모든 코드를 App.tsx에 넣는 경우

처음에는 편해 보여도 파일이 빠르게 복잡해집니다. 페이지·컴포넌트·데이터 로직을 역할별로 분리합니다.

### 원격 데이터 없이 배열만 사용하는 경우

임시 배열은 화면을 만드는 초기 단계에서만 사용합니다. 최종 제출에서는 Supabase 또는 Firebase의 원격 데이터가 실제 기준이 되어야 합니다.

### 로딩과 에러를 생략하는 경우

데이터가 바로 온다고 가정하면 느린 네트워크나 실패 상황에서 화면이 깨집니다. 요청 전·성공·실패·빈 배열을 모두 별도로 처리합니다.

### useEffect 의존성을 무시하는 경우

상세 페이지의 id가 바뀌었는데도 의존성 배열이 비어 있으면 이전 데이터가 남을 수 있습니다. effect 안에서 사용하는 외부 값이 무엇인지 확인합니다.

### 환경변수를 GitHub에 올리는 경우

키가 노출되면 즉시 키를 폐기하고 새로 발급해야 할 수 있습니다. .env 파일은 반드시 .gitignore에 추가합니다.

### 배포 후 직접 확인하지 않는 경우

로컬 환경변수와 배포 환경변수는 별개입니다. 배포 URL에서 목록·상세·등록·수정·삭제를 직접 실행해야 합니다.

## 9. 평가에서 설명할 수 있는 30초 답변

> 저는 하나의 핵심 데이터만 관리하는 React SPA를 만들었습니다. React Router로 홈, 목록, 등록, 상세, 수정, Not Found 페이지를 구성했고, Supabase 또는 Firebase의 원격 데이터를 기준으로 CRUD를 구현했습니다. 목록과 상세 조회는 커스텀 훅으로 분리했으며, 폼은 controlled input으로 관리하고 필수값 검증과 제출 중 상태를 표시했습니다. 모든 주요 화면에서 로딩·에러·빈 상태를 재사용 컴포넌트로 처리했습니다. 사용자의 입력이나 클릭이 state를 변경하고, 그 결과 목록·폼·알림·라우트가 다시 렌더링되는 흐름을 확인할 수 있습니다.

## 10. 마지막으로 기억할 핵심

이 과제에서 가장 중요한 질문은 다음 한 가지입니다.

> 사용자가 무엇을 했을 때, 어떤 state가 바뀌고, 그 결과 화면의 무엇이 달라지는가?

각 기능을 만들 때 아래 세 줄을 먼저 적어 보면 구현 방향이 선명해집니다.

```text
이벤트: 사용자가 무엇을 하는가?
상태: 어떤 값을 변경해야 하는가?
렌더링: 변경된 값을 화면 어디에 보여주는가?
```

예를 들어 삭제 기능은 다음과 같습니다.

```text
이벤트: 삭제 버튼 클릭
상태: isDeleting, items 또는 현재 데이터 상태 변경
렌더링: 버튼 비활성화, 성공 메시지, 목록에서 카드 제거
```

화면의 완성도보다 이 데이터 흐름을 정확히 만들고 설명하는 것이 이번 과제의 목표입니다.
