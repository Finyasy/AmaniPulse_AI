from app.domain.enums import IncidentCategory
from app.domain.schemas import IncidentTaxonomyItem, IncidentTaxonomyResponse


class TaxonomyService:
    _content = {
        "en": {
            IncidentCategory.violence_threat: (
                "Violence threat",
                "A warning, threat, or plan suggesting possible violence.",
            ),
            IncidentCategory.active_violence: (
                "Active violence or unrest",
                "Violence, clashes, destruction, or unrest happening now or recently.",
            ),
            IncidentCategory.voter_intimidation: (
                "Voter intimidation",
                "Threats, coercion, or pressure related to voting or registration.",
            ),
            IncidentCategory.hate_speech_or_incitement: (
                "Hate speech or incitement",
                "Language encouraging hostility or violence toward a group.",
            ),
            IncidentCategory.misinformation_or_rumor: (
                "Misinformation or rumor",
                "Unverified claims that could cause panic or suppress participation.",
            ),
            IncidentCategory.corruption_bribery_or_coercion: (
                "Corruption, bribery, or coercion",
                "Bribes, threats, or improper pressure connected to election activity.",
            ),
            IncidentCategory.authority_abuse: (
                "Police or authority abuse",
                "Misuse of authority affecting civic safety or election participation.",
            ),
            IncidentCategory.suspicious_mobilization: (
                "Suspicious mobilization",
                "Unusual movement, organizing, or preparation that may raise safety concerns.",
            ),
            IncidentCategory.other_election_safety_concern: (
                "Other election safety concern",
                "Another issue that may affect peace or community safety.",
            ),
        },
        "sw": {
            IncidentCategory.violence_threat: (
                "Tishio la vurugu",
                "Onyo, tishio, au mpango unaoweza kuashiria vurugu.",
            ),
            IncidentCategory.active_violence: (
                "Vurugu zinazoendelea",
                "Mapigano, uharibifu, au hali ya fujo iliyopo sasa au karibuni.",
            ),
            IncidentCategory.voter_intimidation: (
                "Vitisho kwa wapiga kura",
                "Vitisho au shinikizo linalohusiana na kupiga kura au kujiandikisha.",
            ),
            IncidentCategory.hate_speech_or_incitement: (
                "Matamshi ya chuki",
                "Lugha inayochochea uhasama au vurugu dhidi ya kundi.",
            ),
            IncidentCategory.misinformation_or_rumor: (
                "Taarifa potofu au uvumi",
                "Madai ambayo hayajathibitishwa na yanaweza kuleta hofu.",
            ),
            IncidentCategory.corruption_bribery_or_coercion: (
                "Rushwa au shinikizo",
                "Rushwa, vitisho, au shinikizo lisilofaa kwenye shughuli za uchaguzi.",
            ),
            IncidentCategory.authority_abuse: (
                "Matumizi mabaya ya mamlaka",
                "Matumizi mabaya ya mamlaka yanayoathiri usalama wa raia.",
            ),
            IncidentCategory.suspicious_mobilization: (
                "Mkusanyiko unaotia shaka",
                "Harakati au maandalizi yasiyo ya kawaida yanayoibua wasiwasi wa usalama.",
            ),
            IncidentCategory.other_election_safety_concern: (
                "Wasiwasi mwingine wa usalama",
                "Jambo lingine linaloweza kuathiri amani au usalama wa jamii.",
            ),
        },
    }

    def get_taxonomy(self, language: str) -> IncidentTaxonomyResponse:
        localized = self._content.get(language, self._content["en"])
        return IncidentTaxonomyResponse(
            language=language if language in self._content else "en",
            categories=[
                IncidentTaxonomyItem(
                    id=category,
                    name=name,
                    description=description,
                    safety_guidance="Move to safety first. You can report when it is safe.",
                )
                for category, (name, description) in localized.items()
            ],
        )


taxonomy_service = TaxonomyService()
