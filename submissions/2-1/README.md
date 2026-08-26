# 나만의 용돈 기입장 프로그램

Python 표준 라이브러리만 사용해 구현한 JSONL 기반 콘솔 가계부입니다. 거래를 파일에 영구 저장하고, 목록·검색은 파일 전체를 읽어 목록으로 만들지 않는 제너레이터 스트리밍 방식으로 처리합니다.

## 실행 방법

```bash
cd submissions/2-1
python -m budget_app --help
python -m unittest discover -s tests -v
```

모든 명령은 기본적으로 현재 폴더의 `./data`를 사용합니다. 다른 저장 폴더는 각 명령 끝에 `--data-dir 경로`를 붙여 지정합니다.

```bash
python -m budget_app list --data-dir ./my-data
```

첫 실행 시 `data` 폴더와 `transactions.jsonl`, `categories.jsonl`, `budgets.jsonl` 파일이 생성됩니다. 카테고리에는 `food`, `transport`, `rent`, `salary`, `etc`가 자동 등록됩니다.

## 명령 예시

```bash
# 대화형 거래 추가
python -m budget_app add

# 최근 거래와 조건 검색
python -m budget_app list --limit 3
python -m budget_app search --from 2024-01-01 --to 2024-01-31 --category food --tag meal

# 월 요약과 예산
python -m budget_app budget set --month 2024-01 --amount 500000
python -m budget_app summary --month 2024-01 --top 3

# 카테고리 관리 (사용 중인 카테고리는 삭제할 수 없음)
python -m budget_app category add
python -m budget_app category list
python -m budget_app category remove etc

# 거래 수정은 옵션 기반으로 고정
python -m budget_app update --id TX-000001 --amount 18000 --memo "저녁" --tags meal,dinner
python -m budget_app delete --id TX-000001

# CSV 입출력
python -m budget_app import --from import.csv
python -m budget_app export --out export.csv --month 2024-01
python -m budget_app export --out export.csv --from 2024-01-01 --to 2024-01-31
```

모든 명령과 하위 명령은 `--help`를 지원합니다. 예를 들어 `python -m budget_app search --help`로 검색 옵션을 확인할 수 있습니다.

## 저장 형식

세 파일은 UTF-8 JSONL 형식입니다. 한 줄이 하나의 독립된 JSON 객체이므로 앞에서부터 순차 처리할 수 있습니다. 거래 목록·검색은 파일 끝에서 블록 단위로 읽어 최근 등록 순을 유지합니다.

`transactions.jsonl` 예시:

```json
{"id":"TX-000001","date":"2024-01-15","type":"expense","amount":15000,"category":"food","memo":"점심","tags":["meal"],"created_at":"2024-01-15T12:00:00"}
```

거래 수정과 삭제는 임시 파일에 전체 결과를 쓴 뒤 `os.replace()`로 교체하므로, 작업 중 오류가 나도 기존 파일 손상 위험을 줄입니다.

## CSV 가져오기·내보내기 스키마

CSV는 UTF-8, 헤더 포함 형식이며 다음 열을 사용합니다.

| 열 | 필수 | 설명 |
| --- | --- | --- |
| `date` | 예 | `YYYY-MM-DD` |
| `type` | 예 | `income` 또는 `expense` |
| `category` | 예 | 등록된 카테고리 |
| `amount` | 예 | 양의 정수 |
| `memo` | 아니오 | 메모 문자열 |
| `tags` | 아니오 | 쉼표로 구분한 태그 |

가져오기에서 형식 오류 또는 미등록 카테고리인 행은 건너뛰며, 처리 건수와 이유를 출력합니다. 내보내기는 `--month` 또는 `--from`과 `--to` 기간 조건이 반드시 필요합니다.

## 구조와 학습 포인트

- `models.py`: dataclass 및 입력값 계약
- `repositories.py`: JSONL 파일 I/O, 제너레이터, 원자적 재작성
- `services.py`: 가계부 규칙과 집계
- `cli.py`: 입력·출력과 예외 처리 데코레이터

CLI 명령은 데코레이터를 통해 예외를 일관된 원인·힌트 메시지로 바꾸고, 실행 시간을 표준 오류로 기록합니다. 정상 종료 코드는 0, 사용자 오류는 1입니다.
