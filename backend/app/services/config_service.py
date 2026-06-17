from app.domain.schemas import AppConfigResponse


class ConfigService:
    def get_app_config(self, platform: str, version: str, language: str) -> AppConfigResponse:
        disclaimer = {
            "en": "AmaniPulse is not an emergency response service.",
            "sw": "AmaniPulse si huduma ya dharura.",
        }.get(language, "AmaniPulse is not an emergency response service.")

        return AppConfigResponse(
            minimum_supported_version="1.0.0",
            feature_flags={
                "media_uploads": False,
                "push_notifications": False,
                "report_status_lookup": True,
                "support_channels_enabled": False,
            },
            emergency_disclaimer=disclaimer,
            support_channels={},
        )


config_service = ConfigService()
