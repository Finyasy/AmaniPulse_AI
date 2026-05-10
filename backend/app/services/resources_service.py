from datetime import UTC, datetime

from app.domain.schemas import ResourceItem, ResourcesResponse


class ResourcesService:
    def get_resources(self, language: str, country: str) -> ResourcesResponse:
        now = datetime.now(UTC)
        if language == "sw":
            resources = [
                ResourceItem(
                    id="digital-safety",
                    title="Usalama wa kidijitali",
                    body="Epuka kusambaza taarifa ambazo hujathibitisha.",
                    category="digital_safety",
                    updated_at=now,
                ),
                ResourceItem(
                    id="move-to-safety",
                    title="Jilinde kwanza",
                    body="Ondoka kwenye eneo hatari kabla ya kutuma ripoti.",
                    category="personal_safety",
                    updated_at=now,
                ),
            ]
        else:
            resources = [
                ResourceItem(
                    id="digital-safety",
                    title="Digital safety",
                    body="Avoid sharing claims that you have not verified.",
                    category="digital_safety",
                    updated_at=now,
                ),
                ResourceItem(
                    id="move-to-safety",
                    title="Move to safety first",
                    body="Leave unsafe areas before submitting a report.",
                    category="personal_safety",
                    updated_at=now,
                ),
            ]

        return ResourcesResponse(language=language, country=country, resources=resources)


resources_service = ResourcesService()
