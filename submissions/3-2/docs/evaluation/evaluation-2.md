# 3-2 평가 항목 2 답변 가이드

이 문서는 `evaluations/evaluation3-2.md`의 **항목 2**를 현재 구현 코드와 연결하여 설명하기 위한 가이드다. 항목 2는 명령의 출력보다 **자료구조를 어떻게 나눴는지, 언제 상태를 갱신하는지, 알고리즘을 어떻게 분리했는지**를 코드에서 짚어 설명하는 것이 중요하다.

## 0. 전체 구조 먼저 설명하기

평가를 시작할 때 다음처럼 전체 구조를 먼저 말하면 각 문항을 연결하기 쉽다.

> CLI는 입력을 파싱하고, `MiniGit`은 저장소 상태와 명령 흐름을 관리합니다. `Commit`은 변경되지 않는 커밋 데이터를 표현하고, 그래프 탐색과 정렬은 `algorithms.py`의 독립 함수로 분리했습니다. 따라서 입출력, 상태 관리, 데이터 모델, 알고리즘의 책임이 섞이지 않습니다.

| 파일 | 주요 책임 |
| --- | --- |
| `main.py` | 프로그램 진입점, REPL 실행 |
| `mini_git/cli.py` | 입력 반복, `shlex` 파싱, 종료 명령, 결과 출력 |
| `mini_git/model.py` | 하나의 커밋을 나타내는 불변 `Commit` 데이터 모델 |
| `mini_git/repository.py` | 커밋·브랜치·인덱스 상태 관리와 명령 처리 |
| `mini_git/algorithms.py` | 병합 정렬, 위상 정렬, 조상 수집, BFS 최단 경로 |

## 1. 커밋 저장소·브랜치·HEAD·사용자 정보의 분리

### 평가 질문

> 커밋 저장소/브랜치/HEAD/사용자 정보를 어떤 구조로 분리했고, 각 책임을 설명할 수 있는가?

### 핵심 답변

> 커밋 자체는 `Commit` 데이터 클래스로 표현하고, 전체 커밋은 `hash -> Commit` 딕셔너리에 저장했습니다. 브랜치는 `branch name -> 마지막 commit hash` 딕셔너리입니다. 별도의 HEAD 객체 대신 현재 브랜치 이름을 `current_branch`에 저장하고 `branches[current_branch]`를 조회해 HEAD hash를 계산합니다. 현재 사용자는 `current_user`에 따로 보관하여 새 커밋의 작성자로 사용합니다.

### 구조와 책임

| 상태 | 자료구조·타입 | 책임 |
| --- | --- | --- |
| `commits` | `Dict[str, Commit]` | hash를 키로 커밋 메타데이터를 저장하고 조회 |
| `branches` | `Dict[str, Optional[str]]` | 브랜치 이름별 마지막 커밋, 즉 브랜치 HEAD 관리 |
| `current_branch` | `Optional[str]` | 현재 선택된 브랜치 이름 관리 |
| HEAD | `branches[current_branch]`에서 계산 | 현재 브랜치가 가리키는 커밋 확인 |
| `current_user` | `Optional[str]` | 새 커밋의 작성자 관리 |
| `children` | `Dict[str, List[str]]` | 부모 hash에서 자식 hash로 빠르게 이동하기 위한 역방향 연결 |
| `keyword_index` | `Dict[str, List[str]]` | 메시지 토큰별 커밋 hash 목록 |
| `author_index` | `Dict[str, List[str]]` | 작성자별 커밋 hash 목록 |

`Commit`에는 다음 값이 들어간다.

```text
Commit
├── hash       세션 안에서 유일한 식별자
├── message    커밋 메시지와 키워드 검색 대상
├── author     작성자와 작성자 검색·정렬 기준
├── timestamp  생성 시각과 날짜 정렬 기준
├── parents    부모 커밋 hash 튜플
└── sequence   생성 순서와 hash 생성·동률 처리 기준
```

`Commit`은 `@dataclass(frozen=True)`로 선언했다. 커밋은 생성된 뒤 메시지·작성자·부모 관계가 바뀌면 안 되는 기록이므로 불변 객체로 표현했다. 브랜치는 커밋 객체를 복사하지 않고 hash만 가리킨다. 따라서 브랜치를 만들어도 커밋 데이터가 중복되지 않는다.

### HEAD를 별도 객체로 만들지 않은 이유

현재 과제 범위에서 HEAD는 항상 특정 브랜치를 가리킨다. 그래서 다음 계산만으로 현재 커밋을 찾을 수 있다.

```text
현재 브랜치 이름 = current_branch
현재 HEAD hash   = branches[current_branch]
```

`INIT` 직후에는 `branches["main"]`이 `None`이므로 아직 HEAD 커밋이 없다. 커밋이 생기면 현재 브랜치의 값만 새 hash로 바뀐다. 이 구조는 HEAD 상태와 브랜치 상태가 서로 어긋나는 것을 막고 필요한 상태의 수를 줄인다.

### 코드에서 짚을 위치

- 커밋 데이터 모델: [`model.py`](../../mini_git/model.py#L8-L17)
- 저장소 상태 초기화: [`repository.py`](../../mini_git/repository.py#L10-L22)
- HEAD 계산: [`repository.py`](../../mini_git/repository.py#L200-L203)
- 현재 HEAD를 복사하는 브랜치 생성: [`repository.py`](../../mini_git/repository.py#L68-L76)

## 2. hash 기반 빠른 조회와 중복·충돌 방지

### 평가 질문

> 커밋 hash로 빠르게 조회하기 위해 어떤 키-값 구조를 사용했고, 중복/충돌을 어떻게 방지했는지 설명할 수 있는가?

### 핵심 답변

> `commits` 딕셔너리에 커밋 hash를 키, `Commit` 객체를 값으로 저장해 평균 `O(1)`에 조회합니다. hash는 난수나 커밋 내용으로 만들지 않고 단조 증가하는 `sequence`를 `c000001` 형식으로 변환합니다. 커밋 성공 후 sequence를 한 번만 증가시키고 이전 번호를 다시 쓰지 않으므로 세션 안에서 논리적인 hash 중복이 발생하지 않습니다.

### 저장 구조

예를 들어 커밋이 세 개라면 다음처럼 저장된다.

```text
commits = {
    "c000001": Commit(hash="c000001", ...),
    "c000002": Commit(hash="c000002", ...),
    "c000003": Commit(hash="c000003", ...),
}
```

리스트만 사용하면 특정 hash를 찾기 위해 최악의 경우 모든 커밋을 순회해야 하므로 `O(V)`가 필요하다. 딕셔너리는 hash 문자열을 키로 바로 조회하므로 평균 `O(1)`이다. `PATH`, `ANCESTORS`, 출력 포맷 등 여러 기능이 이 구조를 공통으로 사용한다.

### hash 생성 순서

```text
1. _next_sequence 값을 읽는다.
2. c + 6자리 숫자 형식으로 commit_hash를 만든다.
3. Commit을 생성해 commits[commit_hash]에 저장한다.
4. 그래프·브랜치·역색인을 갱신한다.
5. _next_sequence를 1 증가시킨다.
```

초기값이 1이고 성공한 커밋마다 증가하므로 같은 세션에서 같은 번호를 두 번 만들지 않는다. 6자리를 넘을 만큼 커밋이 많아져도 Python의 숫자 포맷은 값을 잘라내지 않고 자릿수를 늘리므로 중복되지 않는다.

여기서 말하는 충돌은 두 커밋이 같은 Mini Git hash 문자열을 받는 **논리적 식별자 충돌**이다. 카운터 방식은 이 충돌을 원천적으로 피한다. Python 딕셔너리 내부 해시 함수에서 서로 다른 문자열의 내부 해시 값이 우연히 같아지는 경우는 딕셔너리 구현이 키 동등성 비교로 처리하므로, Mini Git의 두 논리 키가 같은 것으로 취급되지 않는다.

### 카운터 기반 방식을 선택한 이유

- 유일성을 단순하게 보장할 수 있다.
- 실행할 때마다 `c000001`, `c000002`처럼 결과가 예측 가능하다.
- 테스트의 기대값이 고정되어 재현성과 디버깅이 좋다.
- 이 과제는 실제 Git의 암호학적 내용 hash 구현보다 그래프와 탐색 학습이 목적이다.

단, 프로그램을 종료하면 상태가 사라지는 메모리 기반 구현이므로 hash 유일성의 범위도 **한 세션 안**이다.

### 코드·테스트 근거

- hash 생성과 저장: [`repository.py`](../../mini_git/repository.py#L88-L112)
- hash 직접 조회 예시: [`repository.py`](../../mini_git/repository.py#L129-L150)
- 유일하고 결정적인 hash 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L59-L64)

## 3. 커밋 추가 시 역색인 갱신 시점과 방식

### 평가 질문

> 커밋이 추가될 때 역색인(author/keyword)을 어떤 시점에, 어떤 방식으로 갱신하도록 설계했는지 설명할 수 있는가?

### 핵심 답변

> 역색인은 검색할 때 만드는 것이 아니라 `COMMIT`이 성공하는 시점에 커밋 저장·그래프 연결·브랜치 HEAD 갱신과 함께 즉시 갱신합니다. 작성자는 소문자로 정규화한 전체 이름을 키로 사용하고, 키워드는 메시지를 공백으로 분리한 뒤 소문자로 바꾼 토큰을 키로 사용합니다. 한 메시지에 같은 단어가 반복되어도 `seen` 집합으로 한 커밋 hash가 같은 posting list에 중복 등록되지 않게 합니다.

### 커밋 한 건이 추가되는 전체 순서

```text
COMMIT "Add Login Feature login"
        │
        ├─ 1. sequence와 hash 생성
        ├─ 2. 현재 HEAD를 부모로 Commit 생성
        ├─ 3. commits에 저장
        ├─ 4. children에 부모→자식 연결 추가
        ├─ 5. 현재 브랜치 HEAD 갱신
        ├─ 6. author_index와 keyword_index 갱신
        └─ 7. sequence 증가 후 결과 반환
```

예를 들어 작성자가 `Alice Kim`이고 메시지가 `Add Login Feature login`이면 다음과 같이 인덱싱된다.

```text
author_index
"alice kim" → ["c000001"]

keyword_index
"add"     → ["c000001"]
"login"   → ["c000001"]
"feature" → ["c000001"]
```

`login`은 메시지에서 두 번 나왔지만 posting list에는 `c000001`이 한 번만 들어간다. 이 중복 제거는 커밋 하나를 인덱싱하는 동안 사용하는 `seen` 집합이 담당한다.

### 검색할 때의 사용 방식

- `SEARCH --author=<name>`은 소문자로 정규화한 작성자 키의 hash 목록을 바로 조회한다.
- `SEARCH <keyword>`는 토큰에 해당하는 posting list를 조회한다.
- 여러 키워드는 posting list들을 집합으로 바꿔 교집합한다.
- 조회된 hash를 `commits[hash]`로 바꿔 결과를 출력한다.

이처럼 쓰기 시점에 인덱스를 함께 갱신했기 때문에 검색할 때 모든 커밋 메시지를 다시 토큰화할 필요가 없다. 다만 현재 키워드 검색은 최종 결과를 생성 순서로 만들기 위해 `commits`의 hash들을 한 번 확인한다. 따라서 현재 구현 전체의 키워드 검색 비용을 무조건 결과 수 `K`에만 비례한다고 설명하지는 않는다.

### 코드·테스트 근거

- 커밋 생성 중 인덱스 갱신 시점: [`repository.py`](../../mini_git/repository.py#L92-L112)
- 역색인 갱신과 토큰화: [`repository.py`](../../mini_git/repository.py#L178-L198)
- 검색과 posting list 교집합: [`repository.py`](../../mini_git/repository.py#L152-L183)
- 중복 토큰·대소문자 검색 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L146-L157)
- 작성자 검색 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L159-L165)

## 4. 그래프 탐색 로직의 분리와 재사용

### 평가 질문

> `LOG`, `PATH`, `ANCESTORS`에서 사용하는 그래프 탐색 로직을 어떻게 재사용 가능하게 구성했는지 설명할 수 있는가?

### 핵심 답변

> 명령 처리와 그래프 알고리즘을 분리했습니다. `repository.py`는 인자 검증, 존재 여부 확인, 결과 포맷을 담당하고, `algorithms.py`의 함수는 커밋 그래프를 입력받아 커밋 순서·hash 집합·경로 같은 계산 결과만 반환합니다. 특히 `topological_order()`는 전체 `LOG`와 `ANCESTORS`의 조상 부분 그래프 출력에 모두 재사용합니다.

### 공통 그래프 표현

모든 알고리즘은 같은 두 구조를 사용한다.

```text
commits[hash].parents  : 자식 → 부모 방향 연결
children[parent_hash]  : 부모 → 자식 방향 연결
```

부모와 자식을 모두 저장하므로 기능마다 전체 커밋을 다시 훑어 반대 방향 연결을 만들 필요가 없다.

### 명령별 알고리즘 조합

| 명령 | 저장소 계층의 역할 | 알고리즘 계층의 역할 |
| --- | --- | --- |
| `LOG` | 옵션 확인, 커밋 출력 포맷 | `topological_order()`로 전체 커밋을 부모 우선 순서로 반환 |
| `PATH` | 두 hash의 존재 확인, `Path:`/`No path` 출력 | `shortest_path()`와 내부 BFS로 무방향 최단 경로 계산 |
| `ANCESTORS` | hash 존재 확인, 결과 출력 포맷 | `collect_ancestors()`로 조상 집합 수집 후 `topological_order()`로 정렬 |

`topological_order()`의 `included` 인자가 재사용의 핵심이다.

- `included=None`: 모든 커밋을 대상으로 하므로 기본 `LOG`에 사용한다.
- `included=ancestor_hashes`: 선택된 조상 부분 그래프만 대상으로 하므로 `ANCESTORS` 출력에 사용한다.

`PATH`는 목적이 최단거리 계산이라 위상 정렬을 재사용하지 않고 BFS 전용 함수로 분리했다. 대신 `_neighbors()`가 부모와 자식을 합친 무방향 이웃 생성 규칙을 한곳에 모으고, `_breadth_first_distances()`와 경로 복원이 같은 규칙을 사용한다.

즉 모든 명령을 억지로 하나의 범용 탐색 함수에 넣은 것이 아니라, 다음 두 수준에서 재사용 가능하게 만들었다.

1. `commits`와 `children`이라는 공통 그래프 표현을 모든 알고리즘이 사용한다.
2. 의미가 같은 알고리즘은 독립 함수로 만들어 여러 호출자가 사용한다.

알고리즘 함수는 `input()`이나 `print()`를 직접 호출하지 않는다. 그래서 CLI 없이도 테스트에서 그래프를 만들어 `shortest_path()`나 `merge_sort()`를 직접 검증할 수 있다.

### 코드·테스트 근거

- 저장소가 알고리즘을 가져오는 부분: [`repository.py`](../../mini_git/repository.py#L1-L7)
- 명령과 알고리즘 연결: [`repository.py`](../../mini_git/repository.py#L114-L150)
- 재사용 가능한 위상 정렬: [`algorithms.py`](../../mini_git/algorithms.py#L43-L74)
- 조상 수집: [`algorithms.py`](../../mini_git/algorithms.py#L86-L97)
- 최단 경로·BFS·이웃 생성: [`algorithms.py`](../../mini_git/algorithms.py#L100-L159)
- 알고리즘 직접 호출 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L113-L130)

## 5. docstring과 주석의 작성 기준

### 평가 질문

> 주요 함수/클래스에 docstring/주석을 어떤 기준으로 작성했는지 설명할 수 있는가?

### 핵심 답변

> 파일에는 모듈의 책임, 주요 클래스에는 객체의 역할, 알고리즘 함수에는 입력으로 무엇을 계산하고 어떤 성질을 보장하는지를 docstring으로 작성했습니다. 코드를 그대로 번역하는 주석은 피하고, 안정 정렬·부모 우선·무방향 최단 경로·정규화처럼 구현 의도를 모르면 오해하기 쉬운 규칙을 중심으로 기록했습니다.

### 적용한 기준

#### 1. 모듈 docstring은 파일의 책임을 설명한다

각 Python 파일의 첫 줄에서 해당 모듈이 담당하는 영역을 한 문장으로 알 수 있게 했다.

```python
"""Mini Git의 정렬과 그래프 탐색 알고리즘."""
```

#### 2. 주요 클래스와 데이터 모델은 존재 이유를 설명한다

- `Commit`: 커밋 메타데이터와 부모 연결을 나타낸다.
- `MiniGit`: 브랜치, 커밋 그래프, 탐색, 검색 기능을 제공한다.

필드 이름만 반복하기보다 객체가 시스템에서 맡는 책임을 적었다.

#### 3. 알고리즘 docstring은 결과와 핵심 보장을 설명한다

| 함수 | docstring에서 강조한 보장 |
| --- | --- |
| `merge_sort()` | 표준 정렬 API를 사용하지 않는 안정 병합 정렬 |
| `_merge()` | 동일한 키에서 왼쪽 원소를 먼저 선택해 안정성 유지 |
| `topological_order()` | 부모가 자식보다 먼저 나오는 순서 |
| `collect_ancestors()` | 부모 방향으로 도달 가능한 모든 hash 반환 |
| `shortest_path()` | 무방향 최단 경로 중 사전순 최소 경로 반환 |
| `_neighbors()` | 부모와 자식을 합쳐 무방향 이웃 생성 |

#### 4. 내부 상태 주석은 자료구조의 의미를 보완한다

`commits`, `branches`, `children`, 역색인은 이름과 타입을 함께 보고 구조를 빠르게 파악할 수 있도록 선언부에 타입 주석을 두었다. `_index_commit()`에는 작성자와 메시지 토큰을 함께 갱신한다는 목적을 적었다.

#### 5. 짧고 자명한 명령 래퍼에는 불필요한 주석을 반복하지 않는다

`_branch()`, `_switch()`처럼 검증 후 상태 하나를 바꾸는 짧은 메서드는 함수 이름과 코드 흐름이 역할을 직접 보여준다. 모든 줄에 “브랜치를 전환한다” 같은 주석을 달면 코드와 주석을 함께 유지해야 하고 오히려 핵심 알고리즘 설명이 묻힐 수 있다. 대신 클래스의 전체 책임과 핵심 알고리즘·불변 조건에 docstring을 집중했다.

### 코드에서 보여 줄 예시

- 모듈·클래스·메서드 docstring: [`repository.py`](../../mini_git/repository.py#L1-L30)
- 커밋 모델 docstring: [`model.py`](../../mini_git/model.py#L1-L17)
- 알고리즘별 docstring: [`algorithms.py`](../../mini_git/algorithms.py#L12-L25)
- 그래프 알고리즘 docstring: [`algorithms.py`](../../mini_git/algorithms.py#L43-L48)
- 검색 인덱스 docstring: [`repository.py`](../../mini_git/repository.py#L178-L198)

## 6. 예상 꼬리 질문과 답변

### 왜 브랜치에 `Commit` 객체를 직접 저장하지 않았는가?

> 커밋의 기준 저장소를 `commits` 하나로 유지하기 위해서입니다. 브랜치는 hash만 참조하므로 커밋 객체의 복사나 중복 상태가 생기지 않고, 모든 기능이 동일한 객체를 조회합니다.

### 왜 `parents`뿐 아니라 `children`도 저장했는가?

> `parents`만 있으면 자식을 찾을 때 전체 커밋을 순회해야 합니다. `children`을 커밋 생성 시 함께 갱신하면 `LOG`의 위상 정렬과 `PATH`의 자식 방향 이동에서 바로 이웃을 찾을 수 있습니다. 대신 두 표현을 일관되게 갱신해야 하는 비용이 있습니다.

### 커밋 생성 도중 역색인 갱신에 실패하면 어떻게 되는가?

> 현재 구현은 메모리의 기본 자료형만 사용하고 정상 입력에서 인덱싱이 실패할 외부 작업은 없습니다. 더 큰 시스템에서 원자성이 필요하다면 새 상태를 임시로 만든 뒤 한 번에 교체하거나, 실패 시 앞선 변경을 되돌리는 트랜잭션 전략을 추가할 수 있습니다.

### 실제 Git hash와 같은가?

> 아닙니다. 실제 Git은 객체 내용으로 식별자를 계산하지만 이 과제는 세션 내 유일성만 요구합니다. 현재 구현은 그래프 결과와 테스트를 쉽게 재현할 수 있도록 증가 카운터 기반 식별자를 사용했습니다.

### 하나의 범용 DFS/BFS 함수로 모두 합치지 않은 이유는 무엇인가?

> `LOG`는 선행 관계를 지키는 위상 정렬, `PATH`는 최단거리를 구하는 BFS, `ANCESTORS`는 부모 방향의 도달 가능 집합이 필요해 종료 조건과 결과가 서로 다릅니다. 공통 그래프 표현은 재사용하되 서로 다른 의미의 알고리즘은 독립 함수로 유지하는 편이 읽기와 테스트에 더 명확합니다.

## 7. 한 번에 마무리하는 답변

> `Commit`은 불변 데이터 모델이고, 커밋은 `hash -> Commit`, 브랜치는 `name -> HEAD hash` 딕셔너리로 분리했습니다. 현재 브랜치 이름을 통해 HEAD를 계산하고 현재 사용자는 별도 필드에서 새 커밋의 author로 사용합니다. hash는 증가 카운터로 생성해 세션 내 중복을 막고 딕셔너리에서 평균 `O(1)`에 조회합니다. 커밋이 성공할 때 작성자와 메시지 토큰 역색인을 함께 갱신하며, 중복 토큰은 집합으로 제거합니다. 명령 처리는 검증과 출력만 담당하고 위상 정렬, BFS, 조상 수집은 독립 함수로 분리했습니다. docstring은 모듈·클래스의 책임과 알고리즘이 보장하는 중요한 규칙을 중심으로 작성했습니다.

## 8. 문항별 최종 체크리스트

- [ ] `commits`, `branches`, `current_branch`, `current_user`의 자료구조와 책임을 설명했다.
- [ ] 별도 HEAD 객체 대신 `branches[current_branch]`를 사용하는 이유를 설명했다.
- [ ] `children`을 함께 저장하는 이유와 일관성 유지 비용을 설명했다.
- [ ] 카운터 기반 hash가 세션 내 중복을 막는 방법을 설명했다.
- [ ] 커밋 생성 과정에서 역색인을 갱신하는 정확한 시점을 짚었다.
- [ ] 작성자·키워드 정규화와 같은 메시지 안의 중복 토큰 제거를 설명했다.
- [ ] `LOG`, `PATH`, `ANCESTORS`의 명령 처리와 알고리즘 계산이 분리되어 있음을 보여 줬다.
- [ ] `topological_order()`가 전체 로그와 조상 부분 그래프에 재사용됨을 설명했다.
- [ ] docstring과 주석이 코드 번역보다 책임·보장·의도를 기록한다는 기준을 설명했다.
