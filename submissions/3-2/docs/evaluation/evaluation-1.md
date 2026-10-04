# 3-2 평가 항목 1 시연·답변 가이드

이 문서는 `evaluations/evaluation3-2.md`의 **항목 1**을 실제 Mini Git CLI에서 재현하고, 각 결과를 평가자에게 어떻게 설명할지 정리한 가이드다. 평가에서는 **명령 입력 → 출력 확인 → 결과가 증명하는 규칙 설명** 순서로 진행한다.

## 0. 시연 준비

저장소 루트에서 다음과 같이 실행한다.

```bash
cd submissions/3-2
python3 main.py
```

아래 프롬프트가 나타나면 준비가 끝난 것이다.

```text
mini-git>
```

이 문서의 `c000001` 같은 hash는 프로그램을 새로 실행한 뒤 명령을 적힌 순서대로 입력했을 때의 값이다. 커밋 시각은 실행한 현재 시각에 따라 달라진다.

1~6절은 첫 번째 REPL에서 이어서 시연할 수 있다. 4절의 연결되지 않은 커밋은 별도의 저장소 상태가 필요하므로 `quit`으로 종료하고 프로그램을 다시 실행한다.

## 1. `INIT` 후 초기 상태

### 평가 질문

> `INIT <user_name>` 실행 후 `main` 브랜치/HEAD/현재 사용자 설정이 정상적으로 초기화되어 있는가?

### 시작할 때 말할 문장

> 저장소를 `Alice Kim` 사용자로 초기화하여 기본 브랜치, HEAD, 현재 사용자가 올바르게 설정되는지 확인하겠습니다.

### 입력과 기대 결과

```text
mini-git> INIT "Alice Kim"
Initialized repository.
Current branch: main
Current user: Alice Kim
```

### 답변

`INIT`은 현재 사용자를 `Alice Kim`, 현재 브랜치를 `main`으로 설정하고 `main` 브랜치를 생성한다. 아직 커밋이 없으므로 `main`이 가리키는 hash는 `None`이고 HEAD도 커밋을 가리키지 않는 상태다.

현재 구현에는 별도의 HEAD 객체가 없다. `current_branch`에 현재 브랜치 이름을 저장하고, `branches[current_branch]`를 조회한 값을 HEAD hash로 사용한다. 따라서 초기 상태는 다음처럼 이해할 수 있다.

```text
current_user   = "Alice Kim"
current_branch = "main"
branches       = {"main": None}
HEAD           = branches["main"] = None
```

첫 커밋을 만들면 `branches["main"]`이 그 커밋의 hash로 갱신되고, 같은 방식으로 HEAD도 그 커밋을 가리키게 된다.

### 코드·테스트 근거

- 초기화 구현: [`repository.py`](../../mini_git/repository.py#L53-L66)
- HEAD 계산: [`repository.py`](../../mini_git/repository.py#L200-L203)
- 초기 상태 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L37-L43)

## 2. 브랜치 생성·전환과 브랜치별 커밋 반영

### 평가 질문

> `BRANCH <name>` 생성 후 `SWITCH <name>`로 전환되며, 이후 `COMMIT`이 해당 브랜치에 반영되는가?

### 시작할 때 말할 문장

> 루트 커밋에서 `feature` 브랜치를 만들고, feature와 main에서 각각 커밋하겠습니다. 마지막에 feature로 다시 전환해 커밋하여 두 브랜치가 독립된 HEAD를 유지하는지 보여드리겠습니다.

### 입력과 기대 결과

1절의 초기화에 이어 아래 명령을 입력한다.

```text
mini-git> COMMIT "Initial commit"
[main c000001] Initial commit
mini-git> BRANCH feature
Created branch: feature
mini-git> SWITCH feature
Switched to branch: feature
mini-git> COMMIT "Add login feature"
[feature c000002] Add login feature
mini-git> SWITCH main
Switched to branch: main
mini-git> COMMIT "Add payment feature"
[main c000003] Add payment feature
mini-git> SWITCH feature
Switched to branch: feature
mini-git> COMMIT "Continue feature"
[feature c000004] Continue feature
```

출력의 `[feature c000002]`, `[main c000003]`, `[feature c000004]` 부분에서 커밋이 어느 브랜치에 반영되었는지 바로 확인할 수 있다.

### 답변

`BRANCH feature`는 현재 HEAD인 `c000001`을 새 브랜치의 시작점으로 복사하지만 현재 브랜치를 바꾸지는 않는다. `SWITCH feature`를 실행해야 `current_branch`가 `feature`로 바뀐다.

`COMMIT`은 현재 브랜치가 가리키던 커밋을 새 커밋의 부모로 저장한 뒤, **현재 브랜치의 hash만** 새 커밋으로 갱신한다. 위 시연이 끝난 상태는 다음과 같다.

```text
c000001 ─┬─→ c000002 ─→ c000004  [feature]
         └─→ c000003             [main]

branches = {
    "main": "c000003",
    "feature": "c000004"
}
```

main에서 만든 `c000003`이 feature의 부모가 되지 않고, feature로 돌아가 만든 `c000004`의 부모가 `c000002`라는 점이 브랜치별 HEAD가 독립적으로 유지된 증거다. 이는 4절의 `PATH`와 5절의 `ANCESTORS` 출력에서도 다시 확인할 수 있다.

### 코드·테스트 근거

- 브랜치 생성과 전환: [`repository.py`](../../mini_git/repository.py#L68-L86)
- 부모 결정과 현재 브랜치 갱신: [`repository.py`](../../mini_git/repository.py#L88-L112)
- 브랜치별 HEAD 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L45-L57)

## 3. `LOG`의 부모 우선 출력

### 평가 질문

> `LOG`가 “부모 커밋이 자식 커밋보다 먼저” 출력되도록 동작하는가?

### 시작할 때 말할 문장

> 방금 만든 분기 그래프 전체를 `LOG`로 출력하여 모든 부모가 해당 자식보다 앞에 나오는지 확인하겠습니다.

### 입력과 확인할 결과

```text
mini-git> LOG
commit c000001 (Alice Kim, <실행 시각>)
Initial commit

commit c000002 (Alice Kim, <실행 시각>)
Add login feature

commit c000003 (Alice Kim, <실행 시각>)
Add payment feature

commit c000004 (Alice Kim, <실행 시각>)
Continue feature
```

다음 부모-자식 순서가 모두 지켜졌는지 확인한다.

| 부모 | 자식 | 확인할 출력 순서 |
| --- | --- | --- |
| `c000001` | `c000002` | `c000001`이 먼저 |
| `c000001` | `c000003` | `c000001`이 먼저 |
| `c000002` | `c000004` | `c000002`가 먼저 |

### 답변

기본 `LOG`는 최신순 정렬이 아니라 Kahn 방식의 위상 정렬을 사용한다. 각 커밋의 부모 수를 진입 차수로 계산하고, 부모가 모두 출력되어 진입 차수가 0이 된 커밋만 다음 출력 후보로 선택한다. 따라서 부모는 항상 자식보다 먼저 출력된다.

동시에 출력 가능한 형제 커밋이 여러 개라면 생성 순서가 빠른 커밋을 먼저 골라 결과를 일정하게 만든다. 위상 정렬에서는 형제끼리의 순서보다 **모든 부모가 자식보다 먼저인지**가 핵심이다.

### 코드·테스트 근거

- `LOG`가 위상 정렬을 호출하는 부분: [`repository.py`](../../mini_git/repository.py#L114-L127)
- Kahn 방식 위상 정렬: [`algorithms.py`](../../mini_git/algorithms.py#L43-L74)
- 부모 우선 출력 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L66-L78)

## 4. `PATH`의 최단 경로와 `No path`

### 평가 질문

> `PATH <a> <b>`가 경로가 있으면 최단 경로를, 없으면 `No path`를 출력하는가?

### 4-1. 연결된 두 커밋의 최단 경로

첫 번째 REPL에서 다음 명령을 입력한다.

```text
mini-git> PATH c000004 c000003
Path: c000004 -> c000002 -> c000001 -> c000003
```

### 답변

과제에서는 커밋과 부모의 연결을 무방향 간선으로 본다. 따라서 feature의 끝인 `c000004`에서 부모 방향으로 공통 조상 `c000001`까지 이동한 뒤, 자식 방향으로 main의 `c000003`까지 갈 수 있다.

모든 간선의 이동 비용이 1이므로 BFS로 도착점까지의 거리를 계산한다. 그다음 남은 거리가 1씩 감소하는 이웃을 따라가므로 간선 수가 가장 적은 최단 경로가 만들어진다. 최단 경로가 여러 개라면 조건을 만족하는 이웃 중 hash가 가장 작은 것을 선택해 경로 문자열 기준 사전순 최소 경로를 만든다.

### 4-2. 연결되지 않은 커밋의 `No path`

이 시연은 5~6절까지 첫 번째 시나리오를 모두 확인한 뒤 실행하거나, 새 터미널에서 별도로 실행한다. `quit`을 입력한 뒤 `python3 main.py`로 프로그램을 다시 실행한다. 커밋이 하나도 없을 때 두 브랜치를 만들면 두 브랜치 모두 `None`을 가리킨다. 이후 각 브랜치의 첫 커밋은 서로 부모가 없는 별도의 루트가 된다.

```text
mini-git> INIT "Alice Kim"
Initialized repository.
Current branch: main
Current user: Alice Kim
mini-git> BRANCH isolated
Created branch: isolated
mini-git> COMMIT "Main root"
[main c000001] Main root
mini-git> SWITCH isolated
Switched to branch: isolated
mini-git> COMMIT "Isolated root"
[isolated c000002] Isolated root
mini-git> PATH c000001 c000002
No path
```

두 루트 사이에는 부모-자식 연결이 하나도 없다. BFS의 거리 정보에 출발점이 포함되지 않으므로 경로 없음으로 판단하고 정확히 `No path`를 출력한다.

### 코드·테스트 근거

- `PATH` 명령과 `No path` 출력: [`repository.py`](../../mini_git/repository.py#L129-L139)
- 무방향 BFS와 경로 복원: [`algorithms.py`](../../mini_git/algorithms.py#L100-L159)
- 무방향 경로 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L93-L102)
- 연결되지 않은 루트 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L104-L111)
- 여러 최단 경로의 사전순 선택 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L113-L130)

## 5. `ANCESTORS`의 모든 조상 출력

### 평가 질문

> `ANCESTORS <hash>`가 모든 조상을 빠짐없이 출력하는가?

### 시작할 때 말할 문장

> feature의 마지막 커밋인 `c000004`의 조상을 조회하여 직접 부모와 그 위의 조상이 모두 나오고, 자기 자신과 다른 브랜치 커밋은 제외되는지 확인하겠습니다.

### 입력과 기대 결과

첫 번째 REPL의 분기 시나리오에서 실행한다.

```text
mini-git> ANCESTORS c000004
commit c000001 (Alice Kim, <실행 시각>)
Initial commit

commit c000002 (Alice Kim, <실행 시각>)
Add login feature
```

### 답변

`c000004`의 직접 부모는 `c000002`이고, `c000002`의 부모는 `c000001`이므로 두 커밋이 모두 출력된다. 시작 커밋 자신인 `c000004`와 조상이 아닌 다른 갈래의 `c000003`은 출력되지 않는다.

탐색은 시작 커밋의 부모부터 스택에 넣고 부모 방향으로 반복한다. 방문한 hash는 집합에 기록하므로 여러 경로에서 같은 조상을 만나도 중복 출력하지 않는다. 수집한 모든 조상은 위상 정렬하여 먼 조상이 가까운 조상보다 먼저 나오게 한다.

루트 커밋도 간단히 확인할 수 있다.

```text
mini-git> ANCESTORS c000001
No ancestors.
```

### 코드·테스트 근거

- `ANCESTORS` 명령 처리: [`repository.py`](../../mini_git/repository.py#L141-L150)
- 조상 수집 알고리즘: [`algorithms.py`](../../mini_git/algorithms.py#L86-L97)
- 전체 조상·중복 제외·루트 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L132-L144)

## 6. 키워드·작성자 검색과 날짜·작성자 정렬

### 평가 질문

> `SEARCH <keyword>` / `SEARCH --author=<name>` / `LOG --sort-by=date|author`가 요구사항대로 동작하는가?

### 6-1. 키워드 검색

```text
mini-git> SEARCH "login"
Found 1 commit(s):

- c000002: Add login feature
```

커밋 메시지를 공백으로 나누고 소문자로 정규화해 역색인에 등록하므로, `SEARCH "LOGIN"`처럼 대문자로 입력해도 같은 결과가 나온다. 검색 시 모든 메시지를 다시 분해하지 않고 `login -> [c000002]` 목록에서 후보를 가져온다.

여러 단어를 입력하면 각 토큰의 목록을 교집합한다.

```text
mini-git> SEARCH "login feature"
Found 1 commit(s):

- c000002: Add login feature
```

### 6-2. 작성자 검색

공백이 포함된 옵션 전체를 CLI의 인자 하나로 전달하기 위해 따옴표로 묶는다.

```text
mini-git> SEARCH "--author=alice kim"
Found 4 commit(s):

- c000001: Initial commit
- c000002: Add login feature
- c000003: Add payment feature
- c000004: Continue feature
```

작성자 이름도 소문자로 정규화하여 `Alice Kim`과 `alice kim`을 같은 키로 조회한다. 네 커밋 모두 현재 사용자 `Alice Kim`이 만들었으므로 모두 출력된다.

### 6-3. 날짜·작성자 정렬

```text
mini-git> LOG --sort-by=date
commit c000001 (Alice Kim, <실행 시각>)
Initial commit

commit c000002 (Alice Kim, <실행 시각>)
Add login feature

commit c000003 (Alice Kim, <실행 시각>)
Add payment feature

commit c000004 (Alice Kim, <실행 시각>)
Continue feature
```

날짜 정렬은 `timestamp` 오름차순이며, 초 단위 화면 출력이 같아 보이더라도 내부 `datetime` 값으로 비교한다. timestamp까지 같으면 생성 순서로 동률을 처리한다.

```text
mini-git> LOG --sort-by=author
commit c000001 (Alice Kim, <실행 시각>)
Initial commit

commit c000002 (Alice Kim, <실행 시각>)
Add login feature

commit c000003 (Alice Kim, <실행 시각>)
Add payment feature

commit c000004 (Alice Kim, <실행 시각>)
Continue feature
```

작성자 정렬은 작성자 이름을 소문자로 바꾼 값을 기준으로 오름차순 정렬한다. 현재 CLI는 `INIT`에서 한 명의 현재 사용자를 설정하므로 한 세션에서 만든 커밋들의 작성자는 모두 같다. 이 경우 동률 처리 기준인 생성 순서대로 출력되는 것이 정상이다. 서로 다른 작성자 값에 대한 정렬은 단위 테스트에서 별도의 `Commit`들을 만들어 검증한다.

두 정렬 모두 `sorted()`나 `list.sort()`를 사용하지 않고 직접 구현한 안정 병합 정렬을 사용한다. 비교 키가 같을 때 왼쪽 원소를 먼저 선택하므로 원래의 상대 순서를 유지한다.

### 코드·테스트 근거

- 검색·정렬 명령 처리: [`repository.py`](../../mini_git/repository.py#L114-L176)
- 키워드·작성자 역색인 갱신: [`repository.py`](../../mini_git/repository.py#L178-L198)
- 안정 병합 정렬: [`algorithms.py`](../../mini_git/algorithms.py#L12-L40)
- 키워드 검색 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L146-L157)
- 작성자 검색 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L159-L165)
- 날짜·작성자 키와 안정 정렬 테스트: [`test_mini_git.py`](../../tests/test_mini_git.py#L80-L91)

## 7. 평가 직전 자동 테스트

CLI 시연 전에 다음 명령으로 회귀 테스트를 실행한다.

```bash
cd submissions/3-2
python3 -m unittest discover -s tests -v
```

현재 결과는 총 14개 테스트가 모두 통과하는 것이다.

```text
Ran 14 tests

OK
```

## 8. 한 번에 마무리하는 답변

> `INIT`은 `main` 브랜치와 현재 사용자, 현재 브랜치를 설정하며 브랜치가 가리키는 hash를 HEAD로 사용합니다. 브랜치는 현재 HEAD hash만 복사하고, `SWITCH` 후 커밋하면 그 브랜치의 hash만 갱신되므로 분기가 독립적으로 유지됩니다. 기본 `LOG`는 Kahn 방식의 위상 정렬로 모든 부모를 자식보다 먼저 출력합니다. `PATH`는 부모 연결을 무방향으로 본 BFS로 최단 경로를 찾고 연결되지 않으면 `No path`를 출력합니다. `ANCESTORS`는 부모 방향으로 방문 집합을 사용해 모든 조상을 중복 없이 수집합니다. 검색은 키워드와 작성자 역색인을 사용하고, 날짜·작성자 로그는 직접 구현한 안정 병합 정렬로 출력합니다.

## 9. 문항별 최종 체크리스트

- [ ] `INIT` 출력에서 `main`, 현재 사용자, 커밋 전 HEAD 상태를 설명했다.
- [ ] `BRANCH`는 생성만 하고 `SWITCH`가 실제 전환을 담당한다고 설명했다.
- [ ] feature와 main의 커밋이 서로 다른 HEAD를 유지하는 것을 보여 줬다.
- [ ] 기본 `LOG`에서 각 부모가 자식보다 앞에 있는지 짚었다.
- [ ] `PATH`의 최단 경로와 별도 세션의 `No path`를 모두 시연했다.
- [ ] `ANCESTORS c000004`에서 `c000001`, `c000002`가 나오고 자기 자신과 다른 갈래는 제외됨을 설명했다.
- [ ] 키워드·작성자 검색과 날짜·작성자 정렬을 각각 실행했다.
- [ ] 현재 세션의 작성자가 한 명이라 작성자 정렬이 생성 순서로 보이는 이유를 설명했다.
