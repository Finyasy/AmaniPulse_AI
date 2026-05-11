import Foundation

@MainActor
public final class ReportFlowViewModel: ObservableObject {
    @Published public var draft: ReportDraft
    @Published public private(set) var validationErrors: [ReportValidationError] = []
    @Published public private(set) var didSaveDraft = false

    private let validation: ReportValidation

    public init(
        draft: ReportDraft = ReportDraft(),
        validation: ReportValidation = ReportValidation()
    ) {
        self.draft = draft
        self.validation = validation
    }

    public var canSubmit: Bool {
        validation.canSubmit(draft)
    }

    public func setLanguage(_ language: AppLanguage) {
        draft.language = language
    }

    public func validate() -> Bool {
        validationErrors = validation.errors(for: draft)
        return validationErrors.isEmpty
    }

    public func markDraftSaved() {
        didSaveDraft = true
        draft.status = .draft
    }

    public func prepareForSubmission() -> ReportDraft? {
        guard validate() else {
            return nil
        }

        draft.status = .submitted
        return draft
    }
}
