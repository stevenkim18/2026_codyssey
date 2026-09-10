"""OpenAI Chat Completions REST 클라이언트."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import json
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request


API_URL = "https://api.openai.com/v1/chat/completions"


class AIClientError(RuntimeError):
    """AI API 요청 또는 응답 해석 실패."""


@dataclass(frozen=True)
class GenerationOptions:
    model: str = "gpt-4.1-mini"
    temperature: float = 0.2
    max_tokens: int = 600
    timeout: float = 30.0


def _error_detail(raw: bytes) -> str:
    try:
        payload = json.loads(raw.decode("utf-8", errors="replace"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return ""
    if isinstance(payload, dict):
        error_payload = payload.get("error")
        if isinstance(error_payload, dict) and isinstance(error_payload.get("message"), str):
            return error_payload["message"].strip()
    return ""


class OpenAIChatClient:
    """표준 라이브러리만 사용해 Chat Completions를 한 번 호출한다."""

    def __init__(
        self,
        api_key: str,
        *,
        endpoint: str = API_URL,
        timeout: float = 30.0,
        opener: Callable[..., Any] | None = None,
    ) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.timeout = timeout
        self._opener = opener or urllib_request.urlopen

    def generate(
        self,
        messages: Sequence[dict[str, str]],
        options: GenerationOptions,
    ) -> str:
        payload = {
            "model": options.model,
            "messages": list(messages),
            "temperature": options.temperature,
            "max_completion_tokens": options.max_tokens,
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        http_request = urllib_request.Request(
            self.endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with self._opener(http_request, timeout=self.timeout) as response:
                raw_response = response.read()
        except urllib_error.HTTPError as exc:
            raw_error = exc.read()
            detail = _error_detail(raw_error)
            if exc.code == 401:
                reason = "HTTP 401 인증에 실패했습니다. AI_API_KEY를 확인하세요."
            elif exc.code == 429:
                reason = "HTTP 429 요청 한도 또는 사용량 제한에 걸렸습니다. 잠시 후 다시 시도하세요."
            else:
                reason = f"HTTP {exc.code} 오류가 발생했습니다."
            if detail:
                reason = f"{reason} 원인: {detail}"
            raise AIClientError(f"AI API 요청 실패: {reason}") from exc
        except urllib_error.URLError as exc:
            raise AIClientError(f"AI API 네트워크 오류: {exc.reason}") from exc
        except TimeoutError as exc:
            raise AIClientError("AI API 요청 시간이 초과되었습니다.") from exc
        except OSError as exc:
            raise AIClientError(f"AI API 통신 오류: {exc}") from exc

        try:
            response_payload = json.loads(raw_response.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AIClientError("AI API 응답이 올바른 JSON 형식이 아닙니다.") from exc

        try:
            if not isinstance(response_payload, dict):
                raise TypeError("응답 본문이 객체가 아님")
            choices = response_payload["choices"]
            message = choices[0]["message"]
            if not isinstance(message, dict):
                raise TypeError("message가 객체가 아님")
            content = message.get("content")
        except (KeyError, IndexError, TypeError, AttributeError) as exc:
            raise AIClientError("AI API 응답에 choices[0].message.content가 없습니다.") from exc

        if not isinstance(content, str) or not content.strip():
            refusal = message.get("refusal") if isinstance(message, dict) else None
            suffix = f" 원인: {refusal}" if isinstance(refusal, str) and refusal else ""
            raise AIClientError(f"AI API가 비어 있는 결과를 반환했습니다.{suffix}")
        return content.strip()
