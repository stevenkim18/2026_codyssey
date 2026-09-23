# Mini Git

커밋을 DAG(방향성 비순환 그래프)로 표현하고, 그래프 탐색·직접 구현한 정렬·역색인을 이용해 만든 CLI 기반 Mini Git입니다. 실제 파일 내용은 다루지 않고 커밋 메타데이터와 브랜치 관계에 집중합니다.

## 실행 방법

Python 3.10 이상이 필요하며 외부 라이브러리는 사용하지 않습니다.

```bash
cd submissions/3-2
python3 main.py
```

프롬프트에서 명령을 반복해서 입력하며 `exit` 또는 `quit`으로 종료합니다.

```text
mini-git> INIT "Alice Kim"
Initialized repository.
Current branch: main
Current user: Alice Kim
```

테스트는 다음 명령으로 실행합니다.

```bash
python3 -m unittest discover -s tests -v
```

## 입력 규칙

- 명령어는 대소문자를 구분하지 않습니다.
- 공백이 포함된 사용자명, 메시지, 검색어는 따옴표로 묶습니다.
- 브랜치 이름과 커밋 hash는 대소문자를 구분합니다.
- 저장소를 먼저 `INIT`해야 나머지 명령을 사용할 수 있습니다.
- 데이터는 프로그램이 실행되는 동안에만 메모리에 유지됩니다.

## 명령어

| 명령 | 설명 |
| --- | --- |
| `INIT <user_name>` | 저장소를 초기화하고 `main` 브랜치와 작성자를 설정 |
| `BRANCH <branch_name>` | 현재 HEAD를 가리키는 새 브랜치 생성 |
| `SWITCH <branch_name>` | 현재 브랜치 변경 |
| `COMMIT <message>` | 현재 HEAD를 부모로 하는 커밋 생성 |
| `LOG` | 부모가 자식보다 먼저 나오는 전체 로그 출력 |
| `LOG --sort-by=date` | 작성 시각 오름차순으로 로그 출력 |
| `LOG --sort-by=author` | 작성자 이름 오름차순으로 로그 출력 |
| `PATH <commit1> <commit2>` | 부모 연결을 무방향으로 본 최단 경로 출력 |
| `ANCESTORS <commit_hash>` | 도달 가능한 모든 조상 출력 |
| `SEARCH <keyword>` | 메시지 토큰 역색인으로 검색 |
| `SEARCH --author=<name>` | 작성자 역색인으로 검색 |

`SEARCH "login feature"`처럼 여러 단어를 검색하면 모든 토큰을 포함하는 커밋만 반환합니다.

## 실행 예시

```text
mini-git> init "Alice Kim"
Initialized repository.
Current branch: main
Current user: Alice Kim
mini-git> commit "Initial commit"
[main c000001] Initial commit
mini-git> branch feature
Created branch: feature
mini-git> switch feature
Switched to branch: feature
mini-git> commit "Add login feature"
[feature c000002] Add login feature
mini-git> switch main
Switched to branch: main
mini-git> commit "Add payment feature"
[main c000003] Add payment feature
mini-git> path c000002 c000003
Path: c000002 -> c000001 -> c000003
mini-git> ancestors c000002
commit c000001 (Alice Kim, 2026-01-01 09:00:00)
Initial commit
mini-git> search "login"
Found 1 commit(s):

- c000002: Add login feature
```

실제 timestamp는 커밋을 만든 로컬 시각을 사용합니다.

## 자료구조

### 커밋 그래프

각 `Commit`은 다음 정보를 가집니다.

- `hash`: 세션 내에서 유일한 `c000001` 형식의 식별자
- `message`: 커밋 메시지
- `author`: `INIT`에서 정한 작성자
- `timestamp`: 커밋 생성 시각
- `parents`: 부모 커밋 hash 튜플

커밋은 이미 존재하는 HEAD만 부모로 삼으므로 과거 커밋에서 새 커밋으로만 연결됩니다. 따라서 자기 자신으로 되돌아오는 사이클이 생길 수 없고 DAG가 유지됩니다. `hash -> Commit` 딕셔너리를 사용해 hash 조회는 평균 `O(1)`입니다.

브랜치는 `branch name -> HEAD hash` 딕셔너리입니다. 브랜치를 만들 때 현재 HEAD만 복사하므로 이후 각 브랜치의 커밋은 독립적으로 진행됩니다.

### 역색인

커밋 생성 시 아래 두 인덱스를 함께 갱신합니다.

- `keyword -> commit hash 목록`
- `author -> commit hash 목록`

메시지는 공백으로 나눈 후 소문자로 바꿉니다. 한 메시지에 같은 토큰이 반복되어도 해당 커밋은 posting list에 한 번만 넣습니다. 검색 때 모든 커밋 `V`개를 순회하는 대신 해당 posting list만 확인하므로, 결과 후보가 `K`개라면 단일 키워드 조회는 평균 `O(K)`입니다. 여러 키워드는 posting list의 교집합을 구합니다.

## 알고리즘

### 위상 정렬 `LOG`

각 커밋의 선택된 부모 수를 진입 차수로 계산한 뒤 Kahn 알고리즘을 사용합니다. 진입 차수가 0인 커밋부터 출력하고 자식의 진입 차수를 줄이므로 부모가 자식보다 먼저 나옵니다. 동시에 출력할 수 있는 커밋은 생성 순서가 빠른 것을 선택해 결과를 일정하게 유지합니다.

- 시간복잡도: 준비 목록 선택 비용까지 포함해 최악 `O(V² + E)`
- 공간복잡도: `O(V + E)`

### 최단 경로 `PATH`

부모와 자식 모두를 이웃으로 취급해 무방향 그래프를 만듭니다. 도착점에서 BFS를 수행하면 모든 노드의 최단거리를 `O(V + E)`에 구할 수 있습니다. 시작점부터 남은 거리가 정확히 1씩 감소하는 이웃 중 hash가 가장 작은 것을 고르면 최단거리와 경로 문자열의 사전순 최소 조건을 모두 만족합니다.

- 시간복잡도: `O(V + E)`
- 공간복잡도: `O(V)`

연결되지 않은 두 커밋 사이에는 `No path`를 출력합니다.

### 조상 탐색 `ANCESTORS`

대상 커밋의 부모부터 스택을 이용해 방문하며 `set`으로 중복 방문을 막습니다. 수집한 조상 부분 그래프는 위상 정렬해 먼 조상이 가까운 조상보다 먼저 나오도록 출력합니다.

- 탐색 시간복잡도: `O(V + E)`
- 공간복잡도: `O(V)`

### 안정 병합 정렬

Python의 표준 정렬 API는 사용하지 않습니다. 리스트를 절반씩 나눈 뒤 정렬된 두 리스트를 합치는 병합 정렬을 직접 구현했습니다. 키가 같으면 왼쪽 원소를 먼저 선택하므로 안정 정렬입니다.

- 평균·최악 시간복잡도: `O(V log V)`
- 공간복잡도: `O(V)`
- 날짜 정렬: timestamp, 생성 순서 순으로 비교
- 작성자 정렬: 소문자 작성자 이름, 생성 순서 순으로 비교

## 오류 처리

대표 오류는 다음처럼 표시합니다.

```text
Invalid args
Unknown branch: missing
Unknown commit: c999999
Branch already exists: main
Repository not initialized.
```

이미 초기화된 저장소에서 `INIT`을 다시 실행해도 기존 커밋을 지우지 않고 `Repository already initialized.`를 반환합니다.

## 구현 범위

과제의 필수 기능만 구현했습니다. 파일 내용 추적, 영속 저장, 네트워크 통신과 보너스 기능인 `DIFF`, `MERGE`, 정렬 성능 비교는 포함하지 않습니다.
