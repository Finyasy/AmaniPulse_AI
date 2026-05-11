import XCTest
@testable import AmaniPulseCitizen

final class ReportValidationTests: XCTestCase {
    func testValidationRequiresCategoryDescriptionAndSafetyConsent() {
        let draft = ReportDraft(description: "short")

        let errors = ReportValidation().errors(for: draft)

        XCTAssertEqual(errors, [
            .missingCategory,
            .descriptionTooShort,
            .safetyReminderNotAccepted
        ])
    }

    func testValidationAllowsAnonymousReportWithoutLocation() {
        let draft = ReportDraft(
            category: .voterIntimidation,
            description: "People are being warned not to attend registration.",
            location: .none,
            acceptedSafetyReminder: true
        )

        XCTAssertTrue(ReportValidation().canSubmit(draft))
    }

    func testValidationAllowsManualAreaWithoutPreciseCoordinates() {
        let draft = ReportDraft(
            category: .misinformationOrRumor,
            description: "A rumor is spreading quickly in the area.",
            location: .manualArea(county: "Kisumu", areaLabel: "Ahero"),
            acceptedSafetyReminder: true
        )

        XCTAssertTrue(ReportValidation().canSubmit(draft))
    }
}
