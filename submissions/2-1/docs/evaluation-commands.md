# Subject 2-1 평가용 명령 시나리오

아래 순서대로 실행하면 과제의 필수 기능을 시연할 수 있다.

```bash
cd /Users/seungwookim/Code/edu/Codyssey/2026_codyssey/submissions/2-1
```

## 1. 도움말과 초기 데이터 확인

```bash
python -m budget_app --help
python -m budget_app add --help
python -m budget_app search --help
python -m budget_app category list
python -m budget_app list --limit 3
```

## 2. 카테고리 관리

```bash
python -m budget_app category add
```

입력:

```text
카테고리명: health
```

```bash
python -m budget_app category list
python -m budget_app category remove culture
```

`culture`는 더미 거래에서 사용 중이므로 삭제 차단 메시지가 나와야 한다.

## 3. 거래 추가 — 대화형 입력

```bash
python -m budget_app add
```

입력:

```text
날짜(YYYY-MM-DD): 2024-02-28
타입(income/expense): expense
카테고리: health
금액(양수): 30000
메모(선택): 헬스장 이용권
태그(쉼표로 구분, 없으면 엔터): exercise,health
```

저장 성공 메시지와 새 거래 ID가 출력되어야 한다.

## 4. 목록과 검색

```bash
python -m budget_app list --limit 5
python -m budget_app search --from 2024-01-01 --to 2024-01-31
python -m budget_app search --category food --tag meal
python -m budget_app search --type income --q 급여
```

## 5. 월별 요약과 예산

```bash
python -m budget_app summary --month 2024-01 --top 3
python -m budget_app budget set --month 2024-02 --amount 500000
python -m budget_app summary --month 2024-02 --top 3
python -m budget_app summary --month 2023-12
```

마지막 명령은 `데이터 없음`을 출력해야 한다. 2월 예산은 지출보다 작으므로 초과 경고도 확인할 수 있다.

## 6. 거래 수정과 삭제

앞에서 추가한 거래 ID가 `TX-000011`이라면 다음처럼 실행한다.

```bash
python -m budget_app update --id TX-000011 --amount 35000 --memo "헬스장 1개월"
python -m budget_app search --tag health
python -m budget_app delete --id TX-000011
python -m budget_app delete --id TX-999999
```

마지막 명령은 없는 ID에 대한 오류와 해결 힌트, 비정상 종료 코드를 보여야 한다.

## 7. CSV 내보내기와 가져오기

```bash
python -m budget_app export --out february.csv --month 2024-02
python -m budget_app export --out january.csv --from 2024-01-01 --to 2024-01-31
python -m budget_app import --from february.csv
```

`import` 후 `list` 또는 `search`로 추가된 거래를 확인한다.

## 8. 입력 검증

```bash
python -m budget_app add
```

아래처럼 잘못된 값을 입력해 오류 메시지와 재입력 흐름을 확인한다.

```text
날짜(YYYY-MM-DD): 2024-13-40
날짜(YYYY-MM-DD): 2024-02-29
타입(income/expense): spend
타입(income/expense): expense
카테고리: unknown
카테고리: food
금액(양수): 0
금액(양수): 12000
메모(선택):
태그(쉼표로 구분, 없으면 엔터):
```
