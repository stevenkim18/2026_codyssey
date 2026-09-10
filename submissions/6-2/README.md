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

## API 파라미터와 결과 품질

AI 결과의 품질은 모델과 파라미터뿐 아니라 프롬프트에 전달하는 Git status, diff, 출력 형식의 영향을 함께 받는다. 파라미터를 조절해도 입력 diff가 잘못되었거나 프롬프트에 필요한 맥락이 없으면 좋은 결과를 얻기 어렵다.

| 파라미터 | 결과에 미치는 영향 | 이 프로젝트의 선택 |
|---|---|---|
| `model` | 지시 이해 능력, 요약 품질, 응답 속도와 비용에 영향을 준다. | 기본값은 `gpt-4.1-mini`이며 `--model`로 변경할 수 있다. |
| `temperature` | 출력의 무작위성을 조절한다. 낮으면 표현이 집중되고 결과가 일정해지며, 높으면 표현이 다양해지지만 결과가 흔들릴 수 있다. | 형식과 일관성이 중요한 커밋·PR 생성을 위해 기본값을 `0.2`로 둔다. |
| `max_tokens` | 생성할 수 있는 최대 출력 길이를 제한한다. 너무 작으면 본문이 잘릴 수 있고, 크게 설정해도 내용의 정확성이 자동으로 좋아지지는 않는다. | CLI에서는 `--max-tokens`로 받고, API에는 `max_completion_tokens`로 전달한다. 기본값은 `600`이다. |
| `messages`와 프롬프트 | AI가 참고할 변경 파일, diff, 작성 규칙을 결정한다. 결과 품질에 가장 직접적인 영향을 주는 입력이다. | status·diff와 커밋/PR 템플릿을 함께 전달한다. |
| `top_p` | temperature와 비슷하게 선택할 토큰 범위를 조절하는 대안이다. 일반적으로 두 값을 동시에 조절하지 않는다. | 이 도구에서는 혼란을 줄이기 위해 제공하지 않고 `temperature`만 사용한다. |

OpenAI 공식 문서에서는 `temperature`를 0~2 범위로 설명하며, 낮은 값은 더 집중된 결과를 만들고 높은 값은 더 무작위적인 결과를 만든다고 안내한다. 또한 현재 Chat Completions API에서는 `max_tokens`보다 `max_completion_tokens` 사용이 권장된다. [Chat Completions API 공식 문서](https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions/methods/create)

`--safe-mode`는 생성 파라미터는 아니지만 결과 품질과 보안 사이의 trade-off가 있다. 민감정보를 마스킹하고 diff를 줄이면 안전성은 높아지지만, AI가 참고할 수 있는 변경 맥락이 줄어들어 요약 품질이 낮아질 수 있다.

### 파라미터 비교 실습

같은 Git 변경사항을 대상으로 다음 명령을 실행하고 제목의 일관성, 표현의 다양성, 본문이 잘리는지를 비교한다.

```bash
python submissions/6-2/main.py commit --temperature 0.2 --max-tokens 600
python submissions/6-2/main.py commit --temperature 1.0 --max-tokens 600
python submissions/6-2/main.py commit --temperature 0.2 --max-tokens 30
```

`temperature`가 높다고 항상 더 좋은 결과가 나오는 것은 아니며, 같은 입력에서도 모델의 결과가 매번 달라질 수 있다. 이 도구에서는 반복 실행 횟수와 비용을 줄이기 위해 커밋·PR 명령마다 API 호출을 1회로 제한한다.

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
