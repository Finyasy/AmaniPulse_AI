from datetime import UTC, datetime
from hashlib import sha256
from secrets import compare_digest

from sqlalchemy import select

from app.core.config import get_settings
from app.db.models import InternalApiKeyModel
from app.db.session import AsyncSessionLocal
from app.domain.auth import InternalReviewerIdentity


class InternalAuthService:
    def hash_token(self, token: str) -> str:
        return sha256(token.encode("utf-8")).hexdigest()

    async def authenticate(self, token: str | None) -> InternalReviewerIdentity | None:
        if token is None:
            return None

        settings = get_settings()
        if settings.storage_backend == "postgres":
            return await self._authenticate_postgres(token)

        if compare_digest(token, settings.internal_api_token):
            return InternalReviewerIdentity(
                reviewer_id="dev-reviewer",
                role="reviewer",
                label="Local development reviewer",
            )

        return None

    async def _authenticate_postgres(self, token: str) -> InternalReviewerIdentity | None:
        token_hash = self.hash_token(token)
        async with AsyncSessionLocal() as session:
            model = await session.scalar(
                select(InternalApiKeyModel).where(
                    InternalApiKeyModel.key_hash == token_hash,
                    InternalApiKeyModel.active.is_(True),
                )
            )
            if model is None:
                return None

            model.last_used_at = datetime.now(UTC)
            await session.commit()
            return InternalReviewerIdentity(
                reviewer_id=model.reviewer_id,
                role=model.role,
                label=model.label,
            )


internal_auth_service = InternalAuthService()
