# 01. Mini Git 시작하기: 실행 방법과 기본 명령어

## 이번 문서에서 배울 것

이번 과제는 실제 Git 전체를 만드는 과제가 아니다. 커밋과 브랜치의 관계를 작은 프로그램으로 직접 구현하면서 그래프, 탐색, 정렬, 역색인을 공부하는 과제다.

첫 단계에서는 내부 알고리즘보다 프로그램을 직접 실행하고 명령을 입력하는 데 익숙해지는 것을 목표로 한다. 이 문서를 끝까지 따라 하면 다음 내용을 설명할 수 있다.

- Mini Git을 실행하고 종료하는 방법
- 저장소를 초기화하고 첫 커밋을 만드는 방법
- 브랜치를 만들고 전환하는 방법
- 만들어진 커밋을 조회하는 기본 방법

## 1. 프로그램 실행하기

```bash
python3 main.py
```

실행하면 다음 프롬프트가 나타난다.

```text
mini-git>
```

`mini-git>`이 나타나면 명령을 입력할 수 있다.

## 2. 이번 예제에서 사용할 명령어

| 명령어 | 하는 일 | 예시 |
| --- | --- | --- |
| `INIT <user_name>` | 저장소와 `main` 브랜치를 만들고 작성자를 설정한다. | `INIT "Alice Kim"` |
| `COMMIT <message>` | 현재 브랜치에 새 커밋을 만든다. | `COMMIT "Initial commit"` |
| `BRANCH <branch_name>` | 현재 커밋을 가리키는 새 브랜치를 만든다. | `BRANCH feature` |
| `SWITCH <branch_name>` | 작업할 브랜치를 바꾼다. | `SWITCH feature` |
| `LOG` | 모든 커밋을 부모가 자식보다 먼저 나오도록 보여 준다. | `LOG` |
| `SEARCH <keyword>` | 메시지에 해당 단어가 있는 커밋을 찾는다. | `SEARCH login` |
| `ANCESTORS <hash>` | 해당 커밋의 모든 조상 커밋을 보여 준다. | `ANCESTORS c000002` |
| `PATH <hash1> <hash2>` | 두 커밋 사이의 최단 경로를 보여 준다. | `PATH c000001 c000002` |
| `exit` 또는 `quit` | 프로그램을 종료한다. | `quit` |

`<user_name>`, `<message>`, `<hash>`처럼 꺾쇠괄호 안에 쓴 이름은 그대로 입력하는 글자가 아니라 사용자가 알맞은 값으로 바꿔 넣는 자리다.

작성자 검색과 날짜·작성자 기준 정렬 옵션은 이후 학습 문서에서 다룬다.

## 3. 기본 동작 따라하기

Mini Git을 새로 실행한 뒤 다음 명령을 순서대로 입력한다.

```text
mini-git> INIT "Alice Kim"
Initialized repository.
Current branch: main
Current user: Alice Kim

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
```

`INIT`은 `main` 브랜치와 작성자를 설정한다. 첫 `COMMIT`으로 만든 `c000001`은 이전 커밋이 없으므로 부모가 없다. 이후 `feature` 브랜치를 만들어 전환하고 `c000002`를 만들었다. 다시 `main`으로 전환해 커밋하면 `c000003`도 `c000001`을 부모로 가지므로 이력이 두 갈래로 나뉜다.

```text
              ┌──→ c000002  [feature]
c000001 ──────┤
              └──→ c000003  [main]
```

브랜치는 커밋의 복사본이 아니라 해당 브랜치의 마지막 커밋을 가리키는 이름이다. 커밋을 만들면 현재 브랜치만 새 커밋으로 이동한다.

## 4. 만들어진 커밋 확인하기

### 전체 로그 보기

```text
mini-git> LOG
commit c000001 (Alice Kim, <실행 시각>)
Initial commit

commit c000002 (Alice Kim, <실행 시각>)
Add login feature

commit c000003 (Alice Kim, <실행 시각>)
Add payment feature
```

실제 timestamp는 커밋을 만든 로컬 시각으로 표시된다. `LOG`에서는 부모인 `c000001`이 자식인 `c000002`, `c000003`보다 먼저 나온다. 이 순서를 만드는 알고리즘은 이후 문서에서 자세히 공부한다.

### 커밋 메시지 검색하기

```text
mini-git> SEARCH login
Found 1 commit(s):

- c000002: Add login feature
```

검색어는 대소문자를 구분하지 않지만, 메시지를 공백으로 나눈 단어 단위로 검색한다.

### 조상 커밋 보기

```text
mini-git> ANCESTORS c000002
commit c000001 (Alice Kim, <실행 시각>)
Initial commit
```

`c000002`가 만들어질 때 기반이 된 이전 커밋 `c000001`이 조상이다. 자기 자신은 조상 목록에 포함하지 않는다.

### 서로 다른 브랜치의 커밋 사이 경로 보기

```text
mini-git> PATH c000002 c000003
Path: c000002 -> c000001 -> c000003
```

두 브랜치의 커밋 사이를 이동하려면 공통 부모인 `c000001`을 거친다. `PATH`가 최단 경로를 찾는 방법은 이후에 BFS와 함께 살펴본다.

## 5. 프로그램 종료하기

다음 두 명령 중 하나를 입력한다.

```text
mini-git> quit
```

```text
mini-git> exit
```

macOS나 Linux 터미널에서는 `Ctrl+D`, 실행 중 `Ctrl+C`로도 종료할 수 있다.

## 6. 자주 만나는 오류

| 출력 | 주된 원인 | 해결 방법 |
| --- | --- | --- |
| `Invalid args` | 인자 개수가 틀렸거나 공백이 있는 값을 따옴표로 묶지 않았다. | 명령 형식과 따옴표를 확인한다. |
| `Repository not initialized.` | `INIT` 전에 다른 명령을 사용했다. | 먼저 `INIT <user_name>`을 실행한다. |
| `Unknown branch: 이름` | 존재하지 않는 브랜치로 전환했다. | 먼저 `BRANCH <branch_name>`으로 만든다. |
| `Unknown commit: hash` | 존재하지 않는 커밋 hash를 사용했다. | `LOG`에서 실제 hash를 확인한다. |
| `Branch already exists: 이름` | 같은 이름의 브랜치가 이미 있다. | 다른 이름을 사용하거나 기존 브랜치로 전환한다. |

오류가 출력되어도 프로그램은 종료되지 않는다. 올바른 명령을 다시 입력하면 된다.

## 7. 확인할 내용

명령을 모두 실행한 뒤 다음 질문에 자신의 말로 답해 본다.

- `BRANCH`와 `SWITCH`는 무엇이 다른가?
- 첫 커밋에는 왜 부모가 없는가?
- `c000001` 같은 hash는 어디에 사용하는가?

## 다음 학습 주제

다음에는 [커밋 그래프: DAG, LOG, PATH, ANCESTORS](02-commit-graph.md)에서 커밋과 브랜치가 그래프를 만드는 과정과 그래프 탐색 알고리즘을 공부한다.
