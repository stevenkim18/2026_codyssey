# 6-2 AI 커밋·PR 생성기

Git의 변경사항을 읽어 OpenAI Chat Completions API로 커밋 메시지와 Pull Request 초안을 생성하는 터미널 도구다. 실제 `git commit`, `git push`, GitHub PR 생성은 수행하지 않으며, 사용자가 검토하고 복사해 적용할 텍스트만 출력한다.

## 요구 환경

- Python 3.10 이상
- Git이 초기화된 프로젝트
- OpenAI API Key

외부 Python 패키지는 사용하지 않는다. `argparse`, `subprocess`, `urllib.request`, `json` 등 Python 표준 라이브러리만 사용한다.

## 실행 방법

현재 Codyssey 저장소 루트에서 실행한다.

```bash
export AI_API_KEY="YOUR_OPENAI_API_KEY"

python submissions/6-2/main.py commit
python submissions/6-2/main.py pr
```

이 폴더를 별도의 프로젝트 루트로 복사한 경우에는 해당 폴더에서 다음처럼 실행할 수 있다.

```bash
python main.py commit
python main.py pr --safe-mode
```

명령은 현재 작업 디렉터리에서 `git status --short`와 `git diff --no-color`를 실행한다. 따라서 실제로 요약할 변경사항이 있는 Git 프로젝트 루트에서 실행해야 한다.

## 옵션

각 옵션은 `commit`, `pr` 뒤에 작성한다.

| 옵션 | 기본값 | 설명 |
|---|---:|---|
| `--model` | `gpt-4.1-mini` | 사용할 OpenAI 모델 |
| `--temperature` | `0.2` | 응답 다양성. 0~2 범위 |
| `--max-tokens` | `600` | 최대 출력 토큰 수. 양의 정수 |
| `--safe-mode` | 꺼짐 | 민감정보 마스킹과 diff 전송량 제한 |

예시:

```bash
python submissions/6-2/main.py commit --model gpt-4.1-mini --temperature 0.2 --max-tokens 600
python submissions/6-2/main.py pr --safe-mode
python submissions/6-2/main.py commit --help
```

CLI의 `--max-tokens`는 과제에서 이해하기 쉬운 이름으로 유지하고, OpenAI 요청에는 현재 권장되는 `max_completion_tokens` 필드로 보낸다. 한 명령은 변경사항이 있을 때 AI API를 최대 1회 호출한다.

## 동작 흐름

1. `git status --short`로 변경 파일과 상태를 수집한다.
2. `git diff --no-color`로 변경 내용을 수집한다.
3. 변경사항이 없으면 API를 호출하지 않고 종료한다.
4. `AI_API_KEY`를 확인하고 Git 상태·diff를 프롬프트에 넣어 OpenAI Chat Completions API를 호출한다.
5. 생성 결과의 제목 길이와 본문 구조를 후처리한 뒤 터미널에 출력한다.

API Key는 소스 코드에 저장하지 않는다. 쉘 환경변수 또는 운영체제의 안전한 비밀 저장소를 사용한다.

## safe-mode

`--safe-mode`를 사용하면 다음 정책을 적용한다.

- `sk-...` 형태의 OpenAI Key, Bearer 토큰, `api_key`·`secret`·`token`·`password` 대입값을 마스킹한다.
- 이메일 주소를 `[MASKED_EMAIL]`로 치환한다.
- 최대 10개 파일과 최대 200줄의 diff만 API에 전달한다.
- 원본 diff는 로그에 출력하지 않는다.

정규표현식 기반 마스킹은 모든 비밀정보를 식별할 수 없다. API Key나 개인정보가 포함될 가능성이 있는 저장소에서는 safe-mode를 켜고, 실행 전 `git diff`를 직접 확인해야 한다. 생성 결과도 최종 정답이 아니므로 커밋이나 PR에 적용하기 전에 사람이 검토한다.

## 출력 예시

### 커밋 메시지

```text
[INFO] Git status 수집 완료: 2개 파일 변경 감지
[INFO] Git diff 수집 완료: 18줄
[INFO] AI API 요청 중... (1회)
[DONE] 커밋 메시지 생성 완료
--- Commit Message ---
feat: Git 변경사항 기반 커밋 메시지 생성

- git status와 git diff를 수집하는 흐름을 추가했습니다.
- submissions/6-2/main.py의 CLI 처리를 정리했습니다.
----------------------
[INFO] API 호출 횟수: 1
```

### PR 초안

```text
--- PR Title ---
feat: Git 변경사항 기반 커밋·PR 초안 생성

--- PR Body ---
## Why
- 커밋 메시지와 PR 설명을 일관된 형식으로 작성하기 위해 생성 도구를 추가했습니다.

## What
- Git status와 diff를 AI 입력으로 전달합니다.
- commit과 pr CLI 명령을 제공합니다.

## How to Test
- AI_API_KEY를 설정한 뒤 `python submissions/6-2/main.py pr`를 실행합니다.
----------------------
```

### 오류와 변경사항 없음

```text
[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다. 예: export AI_API_KEY="YOUR_KEY"
```

```text
[INFO] 변경 사항이 없습니다. 커밋 메시지를 생성하지 않고 종료합니다.
```

## 비용·보안 주의사항

- `commit`, `pr` 명령은 각각 AI API를 최대 1회 호출한다.
- `--max-tokens`를 필요 이상으로 크게 설정하지 않고, 같은 변경사항으로 명령을 반복 실행하지 않는다.
- diff에는 API Key, 개인정보, 내부 코드가 포함될 수 있으므로 공유 전 내용을 확인한다.
- API Key는 절대 소스 코드, README, 커밋 메시지에 기록하지 않는다.
- 생성된 문구는 AI 초안이므로 사실관계, 테스트 결과, 표현을 검토한 후 사용한다.

## 테스트

테스트는 실제 API를 호출하지 않고 API 응답을 모킹한다.

```bash
python -m unittest discover -s submissions/6-2/tests -v
```

실제 API 확인이 필요한 경우에만 `AI_API_KEY`를 설정하고 각 명령을 한 번씩 실행한다.
