import XCTest

@MainActor
final class AmaniPulseCitizenAppUITests: XCTestCase {
    override func setUp() {
        continueAfterFailure = false
    }

    func testOnboardingCompletesToReportHome() {
        let app = launchFreshApp()

        XCTAssertTrue(app.staticTexts["Report safely"].waitForExistence(timeout: 5))
        app.swipeLeft()
        app.swipeLeft()
        app.swipeLeft()
        app.buttons["onboarding.continue"].tap()

        XCTAssertTrue(app.buttons["report.incidentButton"].waitForExistence(timeout: 5))
    }

    func testSettingsCanSwitchLanguageToSwahili() {
        let app = launchFreshApp()
        completeOnboarding(in: app)

        app.tabBars.buttons["Settings"].tap()
        let swahiliOption = app.buttons["Kiswahili"]
        XCTAssertTrue(swahiliOption.waitForExistence(timeout: 5))
        swahiliOption.tap()

        XCTAssertTrue(app.navigationBars["Mipangilio"].waitForExistence(timeout: 5))
    }

    func testReportDraftCanBeSaved() {
        let app = launchFreshApp()
        completeOnboarding(in: app)

        startAndFillVoterReport(in: app)
        app.buttons["report.saveDraftButton"].tap()

        let savedDraft = app.descendants(matching: .any)["report.draftRow.voter_intimidation"]
        XCTAssertTrue(savedDraft.waitForExistence(timeout: 5))
    }

    func testReportCanBeSubmittedAndStatusRefreshed() {
        let app = launchFreshApp()
        completeOnboarding(in: app)

        startAndFillVoterReport(in: app)
        acceptSafetyReminderAndSubmit(in: app)

        XCTAssertTrue(app.alerts["AmaniPulse"].waitForExistence(timeout: 5))
        app.alerts["AmaniPulse"].buttons["Close"].tap()

        let receivedStatus = app.staticTexts["report.draftStatus.voter_intimidation"]
        XCTAssertTrue(receivedStatus.waitForExistence(timeout: 5))
        XCTAssertEqual(receivedStatus.label, "Received")

        app.buttons["report.refreshStatusButton"].tap()
        XCTAssertTrue(waitForLabel("Under review", on: receivedStatus))
    }

    func testOfflineSubmissionIsSavedForRecovery() {
        let app = launchFreshApp(networkAvailable: false)
        completeOnboarding(in: app)

        startAndFillVoterReport(in: app)
        acceptSafetyReminderAndSubmit(in: app)

        XCTAssertTrue(app.alerts["AmaniPulse"].waitForExistence(timeout: 5))
        app.alerts["AmaniPulse"].buttons["Close"].tap()

        let waitingStatus = app.staticTexts["report.draftStatus.voter_intimidation"]
        XCTAssertTrue(waitingStatus.waitForExistence(timeout: 5))
        XCTAssertEqual(waitingStatus.label, "Waiting for network")
        XCTAssertTrue(app.buttons["report.retryOfflineButton"].waitForExistence(timeout: 5))
    }

    func testReportValidationRemainsReachableWithAccessibilityDynamicType() {
        let app = launchFreshApp(dynamicTypeSize: "accessibility3")
        completeOnboarding(in: app)

        app.buttons["report.incidentButton"].tap()
        tapWhenReachable(app.buttons["report.submitButton"], in: app)

        let validationSummary = app.descendants(matching: .any)["report.validationSummary"]
        XCTAssertTrue(validationSummary.waitForExistence(timeout: 5))
    }

    private func startAndFillVoterReport(in app: XCUIApplication) {
        app.buttons["report.incidentButton"].tap()
        app.buttons["report.category.voter_intimidation"].tap()
        app.swipeUp()
        let descriptionEditor = app.textFields["report.descriptionEditor"]
        XCTAssertTrue(descriptionEditor.waitForExistence(timeout: 5))
        descriptionEditor.tap()
        descriptionEditor.typeText("People are being warned not to attend registration.")
        if app.keyboards.element.exists {
            app.navigationBars["Report an incident"].tap()
        }
        app.swipeUp()
    }

    private func acceptSafetyReminderAndSubmit(in app: XCUIApplication) {
        let safetyToggle = app.switches["report.safetyToggle"]
        XCTAssertTrue(safetyToggle.waitForExistence(timeout: 5))
        if safetyToggle.value as? String != "1" {
            safetyToggle.coordinate(withNormalizedOffset: CGVector(dx: 0.9, dy: 0.5)).tap()
        }
        XCTAssertTrue(waitForSwitchOn(safetyToggle))
        app.buttons["report.submitButton"].tap()
    }

    private func launchFreshApp(networkAvailable: Bool = true, dynamicTypeSize: String? = nil) -> XCUIApplication {
        let app = XCUIApplication()
        app.launchArguments = ["-resetOnboarding"]
        var environment = [
            "AMANIPULSE_USE_REMOTE_API": "0",
            "AMANIPULSE_DRAFT_STORE": "in_memory",
            "AMANIPULSE_NETWORK_AVAILABLE": networkAvailable ? "1" : "0"
        ]
        if let dynamicTypeSize {
            environment["AMANIPULSE_DYNAMIC_TYPE_SIZE"] = dynamicTypeSize
        }
        app.launchEnvironment = environment
        app.launch()
        return app
    }

    private func completeOnboarding(in app: XCUIApplication) {
        if app.buttons["report.incidentButton"].exists {
            return
        }

        app.swipeLeft()
        app.swipeLeft()
        app.swipeLeft()
        app.buttons["onboarding.continue"].tap()
        XCTAssertTrue(app.buttons["report.incidentButton"].waitForExistence(timeout: 5))
    }

    private func waitForLabel(_ label: String, on element: XCUIElement, timeout: TimeInterval = 5) -> Bool {
        let predicate = NSPredicate(format: "label == %@", label)
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: element)
        return XCTWaiter.wait(for: [expectation], timeout: timeout) == .completed
    }

    private func waitForSwitchOn(_ element: XCUIElement, timeout: TimeInterval = 5) -> Bool {
        let predicate = NSPredicate(format: "value == %@", "1")
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: element)
        return XCTWaiter.wait(for: [expectation], timeout: timeout) == .completed
    }

    private func tapWhenReachable(_ element: XCUIElement, in app: XCUIApplication, maxSwipes: Int = 8) {
        for _ in 0..<maxSwipes {
            if element.exists && element.isHittable {
                element.tap()
                return
            }
            app.swipeUp()
        }

        XCTAssertTrue(element.exists && element.isHittable)
        element.tap()
    }
}
