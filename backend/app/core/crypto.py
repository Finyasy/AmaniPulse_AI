from cryptography.fernet import Fernet, InvalidToken

LEGACY_REDACTED_DESCRIPTION = "redacted-before-encryption-migration"
UNAVAILABLE_DESCRIPTION = "[description unavailable]"


class ReportCrypto:
    def __init__(self, key: str) -> None:
        self._fernet = Fernet(key.encode())

    def encrypt_text(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt_text(self, ciphertext: str) -> str:
        if ciphertext == LEGACY_REDACTED_DESCRIPTION:
            return "[description redacted before encryption migration]"
        try:
            return self._fernet.decrypt(ciphertext.encode()).decode()
        except InvalidToken:
            return UNAVAILABLE_DESCRIPTION
