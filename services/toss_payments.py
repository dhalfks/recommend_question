import base64
from dataclasses import dataclass
from typing import Any

import httpx

from config import settings


@dataclass
class TossPaymentError(Exception):
    status_code: int
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class TossPaymentsClient:
    def __init__(self, secret_key: str, base_url: str, timeout_seconds: float = 15.0):
        self.secret_key = secret_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def _authorization(self) -> str:
        if not self.secret_key:
            raise TossPaymentError(503, "TOSS_NOT_CONFIGURED", "토스 시크릿 키가 설정되지 않았습니다.")
        credential = base64.b64encode(f"{self.secret_key}:".encode()).decode()
        return f"Basic {credential}"

    def confirm_payment(
        self,
        *,
        payment_key: str,
        order_id: str,
        amount: int,
        idempotency_key: str,
    ) -> dict[str, Any]:
        try:
            response = httpx.post(
                f"{self.base_url}/v1/payments/confirm",
                headers={
                    "Authorization": self._authorization(),
                    "Content-Type": "application/json",
                    "Idempotency-Key": idempotency_key,
                },
                json={
                    "paymentKey": payment_key,
                    "orderId": order_id,
                    "amount": amount,
                },
                timeout=self.timeout_seconds,
            )
        except httpx.RequestError as exc:
            raise TossPaymentError(
                503,
                "TOSS_NETWORK_ERROR",
                "토스페이먼츠에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요.",
            ) from exc

        try:
            data = response.json()
        except ValueError:
            data = {}
        if response.is_error:
            raise TossPaymentError(
                response.status_code,
                str(data.get("code") or "TOSS_API_ERROR"),
                str(data.get("message") or "토스페이먼츠 결제 승인에 실패했습니다."),
            )
        if not isinstance(data, dict):
            raise TossPaymentError(502, "INVALID_TOSS_RESPONSE", "잘못된 결제 승인 응답입니다.")
        return data


def get_toss_client() -> TossPaymentsClient:
    return TossPaymentsClient(
        secret_key=settings.TOSS_SECRET_KEY,
        base_url=settings.TOSS_API_BASE_URL,
        timeout_seconds=settings.TOSS_API_TIMEOUT_SECONDS,
    )
