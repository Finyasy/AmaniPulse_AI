import Foundation

enum AccessibilityIdentifiers {
    static let onboardingContinue = "onboarding.continue"
    static let onboardingLanguagePicker = "onboarding.languagePicker"
    static let reportIncidentButton = "report.incidentButton"
    static let reportDescriptionEditor = "report.descriptionEditor"
    static let reportSafetyToggle = "report.safetyToggle"
    static let reportValidationSummary = "report.validationSummary"
    static let reportSaveDraftButton = "report.saveDraftButton"
    static let reportSubmitButton = "report.submitButton"
    static let reportStatusRefreshButton = "report.refreshStatusButton"
    static let reportOfflineRetryButton = "report.retryOfflineButton"
    static func reportDraftRow(category: IncidentCategory) -> String {
        "report.draftRow.\(category.rawValue)"
    }
    static func reportDraftStatus(category: IncidentCategory) -> String {
        "report.draftStatus.\(category.rawValue)"
    }
    static let settingsLanguagePicker = "settings.languagePicker"
    static let reportTab = "tab.report"
    static let riskTab = "tab.risk"
    static let resourcesTab = "tab.resources"
    static let settingsTab = "tab.settings"
}
