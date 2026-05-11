import Foundation

public enum ReportValidationError: Equatable, Sendable {
    case missingCategory
    case descriptionTooShort
    case safetyReminderNotAccepted
}

public struct ReportValidation: Sendable {
    public let minimumDescriptionCharacters: Int

    public init(minimumDescriptionCharacters: Int = 12) {
        self.minimumDescriptionCharacters = minimumDescriptionCharacters
    }

    public func errors(for draft: ReportDraft) -> [ReportValidationError] {
        var errors: [ReportValidationError] = []

        if draft.category == nil {
            errors.append(.missingCategory)
        }

        if draft.description.trimmingCharacters(in: .whitespacesAndNewlines).count < minimumDescriptionCharacters {
            errors.append(.descriptionTooShort)
        }

        if !draft.acceptedSafetyReminder {
            errors.append(.safetyReminderNotAccepted)
        }

        return errors
    }

    public func canSubmit(_ draft: ReportDraft) -> Bool {
        errors(for: draft).isEmpty
    }
}
