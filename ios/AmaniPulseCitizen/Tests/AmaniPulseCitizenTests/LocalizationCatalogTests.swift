import XCTest
@testable import AmaniPulseCitizen

final class LocalizationCatalogTests: XCTestCase {
    func testSwahiliCoreCopyIsAvailable() {
        let catalog = LocalizationCatalog()

        XCTAssertEqual(catalog.text(.reportTab, language: .swahili), "Ripoti")
        XCTAssertEqual(catalog.text(.settingsTab, language: .swahili), "Mipangilio")
    }

    func testIncidentCategoriesUseBackendStableIds() {
        XCTAssertEqual(IncidentCategory.voterIntimidation.rawValue, "voter_intimidation")
        XCTAssertEqual(IncidentCategory.otherElectionSafetyConcern.rawValue, "other_election_safety_concern")
    }

    func testCategoryCopyFallsBackToEnglishForSupportedCategories() {
        let catalog = LocalizationCatalog()
        let copy = catalog.categoryCopy(for: .authorityAbuse, language: .english)

        XCTAssertEqual(copy.title, "Police or authority abuse")
        XCTAssertFalse(copy.description.isEmpty)
    }
}
