# Subject 2-1 평가 설명 가이드

`evaluations/evaluation2-1.md`의 문항을 기준으로 구현을 점검한 문서다. 평가에서는 아래 **설명 예시**를 자신의 말로 설명하고, **시연 명령**으로 결과를 보여 준다.

## 점검 결과

| 평가 항목 | 결과 | 근거 |
| --- | --- | --- |
| 항목 1. 기능 및 영속성 | 충족 | 단위 테스트 5개 통과, 별도 임시 데이터 폴더에서 CLI 흐름 시연 완료 |
| 항목 2. 모듈 및 클래스 설계 | 충족 | 모델·저장소·서비스·CLI로 책임 분리 |
| 항목 3. 제너레이터·데코레이터·타입 힌트 | 충족 | `Iterator`, `yield`, `command_guard`, 데이터 모델 타입 힌트 사용 |
| 항목 4. 포맷·확장성·깨진 CSV | 충족 | JSONL 선택 근거와 부분 성공 가져오기 구현 |

## 항목 1. 기능 및 데이터 영속성

### 1-1. add/list/search/summary/export/import/update/delete가 요구사항대로 동작하는가?

**설명 예시**

`BudgetService`가 기능별 유스케이스를 제공하고, `cli.py`의 각 `run_*` 함수가 이를 명령행 명령에 연결했습니다. `add`는 대화형 입력이고, `update`는 README에 고정한 옵션 방식입니다. `list`와 `search`는 최신순, `summary`는 월별 수입·지출·잔액과 지출 TOP N을 출력합니다.

**코드 근거**

- `services.py`: `add_transaction`, `list_transactions`, `search`, `summary`, `import_csv`, `export_csv`, `update_transaction`, `delete_transaction`
- `cli.py`: 각 기능에 대응하는 `run_add`부터 `run_export` 함수 및 `argparse` 명령 등록
- `tests/test_budget_app.py`: CRUD, 검색, 요약, CSV 입출력을 서비스 단위로 검증

**시연 명령**

```bash
cd submissions/2-1
python -m budget_app list --limit 3
python -m budget_app search --from 2024-01-01 --to 2024-01-31 --category food
python -m budget_app summary --month 2024-01 --top 3
python -m budget_app export --out january.csv --month 2024-01
python -m budget_app import --from january.csv
```

`add`는 `python -m budget_app add`로 실행하고, 출력된 ID를 사용해 다음을 시연한다.

```bash
python -m budget_app update --id TX-000011 --amount 35000 --memo "수정한 메모"
python -m budget_app delete --id TX-000011
```

### 1-2. 프로그램 재실행 후에도 거래/카테고리/예산 데이터가 유지되는가?

**설명 예시**

저장소를 메모리가 아닌 `data/` 폴더의 JSONL 파일로 구성했습니다. 거래, 카테고리, 예산을 각각 분리했기 때문에 프로그램 프로세스가 끝나도 다음 실행에서 같은 파일을 다시 읽어 데이터가 유지됩니다. 첫 실행에는 저장 폴더와 세 파일을 만들고, 카테고리 파일이 비어 있으면 기본 카테고리를 자동 등록합니다.

**코드 근거**

- `repositories.py`의 `JsonlStore.path()`가 저장 폴더와 파일을 생성한다.
- `TransactionRepository`, `CategoryRepository`, `BudgetRepository`가 각각 `transactions.jsonl`, `categories.jsonl`, `budgets.jsonl`을 담당한다.
- 초기 파일 생성은 `test_initial_files_and_categories_are_created`에서 확인한다.

**시연 명령**

```bash
python -m budget_app budget set --month 2024-02 --amount 20000
python -m budget_app summary --month 2024-02
rg --files data
```

`data/` 아래의 JSONL 파일 3개를 확인한 뒤, 프로그램을 다시 실행해 마지막 `summary` 결과가 유지되는 것을 보여 준다.

### 1-3. category add/list/remove가 정상 동작하는가?

**설명 예시**

카테고리는 별도 저장소로 관리합니다. 추가 전에 이름 공백과 중복을 검증하고, 삭제 전에 모든 거래를 순회해 해당 카테고리를 사용하는 거래가 있는지 확인합니다. 사용 중이면 삭제를 차단하고 거래를 수정하거나 삭제하라는 힌트를 출력합니다.

**코드 근거**

- `BudgetService.add_category`, `list_categories`, `remove_category`
- `remove_category`는 사용 건수를 계산한 뒤 사용 중인 카테고리에 `AppError`를 발생시킨다.
- `test_search_summary_budget_and_category_removal`이 `food` 삭제 차단을 검증한다.

**시연 명령**

```bash
python -m budget_app category add
# 입력: health
python -m budget_app category list
python -m budget_app category remove food
```

마지막 명령은 예제 거래에서 사용 중인 `food` 카테고리이므로 삭제되지 않아야 한다.

### 1-4. budget set이 저장되며, summary에서 예산 사용률/초과 여부가 출력되는가?

**설명 예시**

예산은 월과 금액을 `Budget` 데이터 모델로 검증한 뒤 `budgets.jsonl`에 저장합니다. `summary`는 해당 월의 예산을 다시 읽어 지출 ÷ 예산으로 사용률을 계산하고, 지출이 예산보다 크면 경고를 붙입니다.

**코드 근거**

- `BudgetRepository.set()`은 같은 월의 이전 예산을 제거한 뒤 새 예산을 저장한다.
- `BudgetService.summary()`가 예산을 결과에 포함한다.
- `cli.py`의 `run_summary()`가 사용률과 `[경고: 예산 초과]`를 출력한다.

**시연 명령**

```bash
python -m budget_app budget set --month 2024-02 --amount 20000
python -m budget_app summary --month 2024-02 --top 3
```

해당 월 지출이 20,000원보다 크도록 데이터가 있을 때 `사용률 150.0% [경고: 예산 초과]`처럼 표시된다.

### 1-5. import/export가 명시된 CSV 스키마로 동작하는가?

**설명 예시**

외부 교환 형식은 UTF-8 CSV로 고정했습니다. 필수 헤더는 `date`, `type`, `category`, `amount`이고, 선택 열은 `memo`, `tags`입니다. 내보내기는 항상 여섯 개 헤더를 같은 순서로 작성하며, 가져오기는 헤더 누락을 오류로 처리합니다.

**코드 근거**

- `BudgetService.import_csv()`는 `utf-8-sig`로 읽고 필수 헤더를 확인한다.
- `BudgetService.export_csv()`는 UTF-8로 열고 여섯 개 헤더를 작성한다.
- `test_import_skips_invalid_rows_and_export_writes_schema`가 헤더와 처리 건수를 검증한다.

**시연 명령**

```bash
python -m budget_app export --out february.csv --month 2024-02
python -m budget_app import --from february.csv
```

### 1-6. 잘못된 입력/파일 오류에서 스택트레이스 없이 오류 메시지와 해결 힌트를 출력하는가?

**설명 예시**

도메인 검증 오류는 `AppError`와 `ValidationError`로 표현합니다. CLI의 `command_guard` 데코레이터가 이를 잡아 `[오류]`와 `[힌트]`만 출력하고 종료하므로 사용자는 Python 스택트레이스를 보지 않습니다. 파일 접근 오류도 `OSError`를 같은 방식으로 처리합니다.

**코드 근거**

- `models.py`: `AppError(message, hint)` 정의 및 날짜·타입·금액 검증
- `cli.py`: `command_guard`에서 `AppError`, `OSError`, 그 밖의 예외를 처리

**시연 명령**

```bash
python -m budget_app delete --id TX-999999
python -m budget_app import --from not-found.csv
```

### 1-7. 오류 상황에서 종료 코드가 0이 아님을 확인할 수 있는가?

**설명 예시**

정상 명령은 `0`을 반환하고, `command_guard`가 잡은 오류는 `1`을 반환합니다. 명령행 오류는 성공으로 보이면 안 되기 때문에 비정상 종료 코드를 명확히 구분했습니다.

**시연 명령**

```bash
python -m budget_app delete --id TX-999999
echo $?
```

확인 시 `1`이 출력되어야 한다.

## 항목 2. 모듈과 클래스 설계

### 2-1. 코드가 3개 이상 모듈로 분리되어 있고, 각 모듈의 책임을 어떻게 나눴는가?

**설명 예시**

변경 이유가 다른 코드는 함께 두지 않는 기준으로 나눴습니다. 데이터 형식과 검증이 바뀌면 `models.py`, 파일 저장 방식이 바뀌면 `repositories.py`, 가계부 규칙이 바뀌면 `services.py`, 사용자 명령과 출력이 바뀌면 `cli.py`를 수정합니다. 그래서 기능을 추가할 때 영향 범위가 작고 테스트하기도 쉽습니다.

| 모듈 | 책임 |
| --- | --- |
| `models.py` | 데이터 모델과 입력값 검증 |
| `repositories.py` | JSONL 파일 I/O, 순차·역순 스트리밍, 안전한 재작성 |
| `services.py` | 거래·예산·카테고리의 업무 규칙과 집계 |
| `cli.py` | 명령행 인자, 대화형 입력, 출력, 공통 오류 처리 |

### 2-2. 최소 2개 이상의 클래스에 부여한 책임 경계를 어떻게 정했는가?

**설명 예시**

`Transaction`은 올바른 거래 데이터만 생성되도록 날짜, 타입, 금액, 카테고리 값을 검증하는 불변 데이터 모델입니다. 반면 `TransactionRepository`는 거래가 유효한지 판단하지 않고, 유효한 거래를 파일에서 읽고 쓰는 일만 맡습니다. `BudgetService`는 두 계층을 조합해 “등록된 카테고리만 거래에 사용할 수 있다” 같은 업무 규칙을 담당합니다. 즉 데이터 규칙, 저장 기술, 업무 규칙을 서로 섞지 않았습니다.

**코드 근거**

- `models.py`: `Transaction`, `Budget`
- `repositories.py`: `JsonlStore`, `TransactionRepository`, `CategoryRepository`, `BudgetRepository`
- `services.py`: `BudgetService`

### 2-3. 파일 기반 update/delete를 어떻게 안전하게 처리했는가?

**설명 예시**

JSONL은 행 중간만 안전하게 수정하기 어렵기 때문에 update/delete 시 기존 파일을 읽으며 변경 결과 전체를 임시 파일에 씁니다. 임시 파일 쓰기가 끝난 뒤에만 `os.replace()`로 원본을 교체합니다. 따라서 쓰기 중 문제가 생기면 원본 파일은 그대로 남아 부분 저장 위험을 낮춥니다.

**코드 근거**

- `JsonlStore.rewrite()`가 `tempfile.NamedTemporaryFile()`에 쓴 뒤 `os.replace()`를 호출한다.
- `TransactionRepository.replace()`와 `delete()`가 재작성할 레코드를 제너레이터로 전달한다.

## 항목 3. Python 구현 요소

### 3-1. list/search를 제너레이터로 스트리밍 처리한 방식을 어떻게 구현했고, 왜 유리한가?

**설명 예시**

저장소의 `iter_recent()`와 `iter_all()`은 `Iterator[Transaction]`을 반환하며, 한 거래씩 `yield`합니다. `list_transactions()`는 필요한 `--limit` 개수에 도달하면 반복을 멈추고, `search()`는 각 거래를 읽는 즉시 조건을 검사해 맞는 것만 내보냅니다. 파일 전체를 리스트로 만들지 않으므로 데이터가 커져도 메모리 사용량이 일정하고, 목록의 일부만 보여 줄 때 더 효율적입니다.

**코드 근거**

- `JsonlStore.iter_records_reverse()`는 파일 뒤에서 블록 단위로 읽는다.
- `TransactionRepository.iter_recent()`과 `BudgetService.list_transactions()`, `search()`가 `yield`를 사용한다.

### 3-2. 데코레이터로 분리한 공통 기능이 무엇이며, 왜 분리가 필요했는가?

**설명 예시**

각 CLI 명령에는 오류를 사용자 문구로 바꾸고 실행 시간을 기록해야 하는 공통 요구가 있습니다. 이를 `command_guard` 데코레이터로 분리해 모든 `run_*` 함수에 적용했습니다. 명령마다 같은 try/except를 반복하지 않고, 오류 형식과 종료 코드가 일관되게 유지됩니다.

**코드 근거**

- `cli.py`: `@command_guard`가 `run_add`, `run_list`, `run_search` 등 모든 명령 실행 함수에 적용된다.

### 3-3. 타입 힌트를 적용해 얻는 이점을 실제 코드 예로 어떻게 확인했고, 왜 도움이 되는가?

**설명 예시**

타입 힌트는 함수가 받을 값과 반환할 값의 계약을 코드에 남깁니다. 예를 들어 `list_transactions(self, limit: int) -> Iterator[Transaction]`은 호출자가 목록이 아니라 순회 가능한 거래 스트림을 받는다는 점을 알 수 있게 합니다. `add_transaction(..., amount: int | str) -> Transaction`은 CLI 문자열과 서비스의 정수 처리를 모두 허용한다는 의도를 표현합니다. `Transaction`과 `Budget` dataclass는 필드 구조도 명확히 보여 줍니다.

**코드 근거**

- `models.py`: `Transaction`, `Budget`의 dataclass 필드 타입
- `repositories.py`: `Iterator[dict[str, Any]]`, `Iterator[Transaction]`
- `services.py`: 서비스 메서드의 입력·반환 타입

## 항목 4. 저장 포맷과 확장성

### 4-1. JSONL과 CSV 중 선택한 저장 포맷의 장단점을 비교하고, 왜 JSONL을 택했는가?

**설명 예시**

내부 저장에는 JSONL을 선택했습니다. 한 줄이 독립된 JSON 객체이므로 레코드를 한 줄씩 스트리밍할 수 있고, `tags`처럼 배열인 값도 자연스럽게 저장할 수 있습니다. CSV는 스프레드시트와 호환이 좋지만 배열을 표현하려면 쉼표와 따옴표 규칙을 추가로 관리해야 합니다. 대신 외부 전달이 필요한 경우에는 CSV import/export를 제공해 두 형식의 장점을 함께 활용했습니다.

### 4-2. 거래가 10만 건으로 늘어난다면 병목은 어디이고, 어떻게 개선할 것인가?

**설명 예시**

현재 `list`와 `search`는 스트리밍이라 메모리는 적게 쓰지만, 조건에 맞는 거래를 찾으려면 파일을 선형으로 읽어야 합니다. `summary`도 월별 합계를 만들기 위해 전체 파일을 순회하고, `update/delete`는 전체 파일을 다시 작성합니다. 10만 건에서는 이 디스크 I/O가 병목입니다. 규모가 커지면 날짜·카테고리 인덱스를 별도 파일로 두거나, 트랜잭션과 인덱스를 제공하는 SQLite로 이전하겠습니다. 월별 요약 캐시도 함께 둘 수 있습니다.

### 4-3. import CSV에 일부 깨진 행이 섞이면 어떻게 처리해 사용자 신뢰를 지키는가?

**설명 예시**

현재 구현은 부분 성공 정책입니다. 각 행을 독립적으로 검증하고 정상 행은 저장하며, 잘못된 행은 건너뜁니다. 마지막에 `imported`, `skipped` 수와 오류 사유별 건수를 출력하므로 사용자가 실제 반영 결과를 알 수 있습니다. 모든 행이 반드시 함께 반영되어야 하는 업무라면, 먼저 임시 목록에서 전체 행을 검증하고 오류가 하나라도 있으면 저장하지 않는 롤백 모드를 추가할 수 있습니다.

**코드 근거**

- `BudgetService.import_csv()`가 행마다 `AppError`를 잡아 성공·실패 건수와 사유를 집계한다.
- `test_import_skips_invalid_rows_and_export_writes_schema`가 정상 행 1건, 잘못된 행 1건의 부분 성공을 검증한다.

## 추가 작업 권장 사항

필수 기능은 현재 평가 항목을 충족한다. 다만 다음 두 가지를 보완하면 평가 시 더 안전하다.

1. `argparse`가 직접 처리하는 인자 누락 오류(예: `python -m budget_app summary`)는 스택트레이스 없이 종료 코드 `2`로 끝나지만, `command_guard`를 거치지 않아 프로젝트 형식의 `[힌트]` 문구는 출력하지 않는다. 모든 입력 오류에 같은 형식의 해결 힌트를 요구받을 수 있으므로, `main()`에서 `SystemExit` 또는 `ArgumentParser.error()` 출력을 통일하는 보완을 권장한다.
2. `docs/evaluation-commands.md`의 2월 예산 예시는 `500000`원인데, 추가 거래가 `30000`원이어서 예산 초과가 발생하지 않는다. 초과 경고를 확실히 시연하려면 예산을 `20000`원처럼 지출보다 작게 설정한다.

## 실행 검증 기록

2026-08-26에 다음을 확인했다.

- `python -m unittest discover -s tests -v`: 5개 테스트 모두 통과
- 새 임시 데이터 폴더에서 카테고리 추가, 거래 추가, 목록, 검색, 예산 설정, 요약의 초과 경고, CSV 내보내기, 수정, 삭제, 카테고리 삭제를 순서대로 시연
- 존재하지 않는 ID 삭제 시 `[오류]`, `[힌트]`가 출력되고 종료 코드 `1` 확인
- 임시 데이터 폴더에 `transactions.jsonl`, `categories.jsonl`, `budgets.jsonl` 생성 확인
