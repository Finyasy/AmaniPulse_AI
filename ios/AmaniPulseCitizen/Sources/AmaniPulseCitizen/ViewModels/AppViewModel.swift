import Foundation

@MainActor
public final class AppViewModel: ObservableObject {
    @Published public var language: AppLanguage
    @Published public var isNetworkAvailable: Bool
    @Published public private(set) var resources: [ResourceItem] = []
    @Published public private(set) var riskGuidance: [RiskGuidance] = []
    @Published public private(set) var savedDrafts: [ReportDraft] = []

    public let localization: LocalizationCatalog
    private let contentService: ContentProviding
    private let draftStore: ReportDraftStoring
    private let reportSubmitter: ReportSubmitting

    public init(
        language: AppLanguage = .preferred(),
        isNetworkAvailable: Bool = true,
        localization: LocalizationCatalog = LocalizationCatalog(),
        contentService: ContentProviding = MockContentService(),
        draftStore: ReportDraftStoring = InMemoryReportDraftStore(),
        reportSubmitter: ReportSubmitting = MockReportSubmitter()
    ) {
        self.language = language
        self.isNetworkAvailable = isNetworkAvailable
        self.localization = localization
        self.contentService = contentService
        self.draftStore = draftStore
        self.reportSubmitter = reportSubmitter
    }

    public func text(_ key: TextKey) -> String {
        localization.text(key, language: language)
    }

    public func categoryCopy(for category: IncidentCategory) -> CategoryCopy {
        localization.categoryCopy(for: category, language: language)
    }

    public func refreshContent() async {
        resources = await contentService.resources(language: language)
        riskGuidance = await contentService.riskGuidance(language: language)
        savedDrafts = (try? await draftStore.loadDrafts()) ?? []
    }

    public func saveDraft(_ draft: ReportDraft) async {
        try? await draftStore.save(draft)
        savedDrafts = (try? await draftStore.loadDrafts()) ?? savedDrafts
    }

    public func deleteDraft(_ draft: ReportDraft) async {
        try? await draftStore.delete(draft)
        savedDrafts = (try? await draftStore.loadDrafts()) ?? []
    }

    public func submitDraft(_ draft: ReportDraft) async -> SubmissionOutcome {
        guard isNetworkAvailable else {
            var waitingDraft = draft
            waitingDraft.status = .waitingForNetwork
            try? await draftStore.save(waitingDraft)
            savedDrafts = (try? await draftStore.loadDrafts()) ?? []
            return .savedForNetwork
        }

        guard let payload = draft.submissionPayload() else {
            return .failed
        }

        do {
            let response = try await reportSubmitter.submit(payload)
            var submittedDraft = draft
            submittedDraft.status = response.status
            submittedDraft.reportReference = response.reportReference
            try? await draftStore.save(submittedDraft)
            savedDrafts = (try? await draftStore.loadDrafts()) ?? []
            return .submitted(response)
        } catch {
            var waitingDraft = draft
            waitingDraft.status = .waitingForNetwork
            try? await draftStore.save(waitingDraft)
            savedDrafts = (try? await draftStore.loadDrafts()) ?? []
            return .savedForNetwork
        }
    }

    public func refreshStatus(for draft: ReportDraft) async {
        guard let reference = draft.reportReference else {
            return
        }

        do {
            let response = try await reportSubmitter.reportStatus(reference: reference)
            var updatedDraft = draft
            updatedDraft.status = response.status
            try? await draftStore.save(updatedDraft)
            savedDrafts = (try? await draftStore.loadDrafts()) ?? savedDrafts
        } catch {
            savedDrafts = (try? await draftStore.loadDrafts()) ?? savedDrafts
        }
    }

    public func retryWaitingDrafts() async {
        guard isNetworkAvailable else {
            return
        }

        let drafts = (try? await draftStore.loadDrafts()) ?? savedDrafts
        for draft in drafts where draft.status == .waitingForNetwork {
            _ = await submitDraft(draft)
        }
    }
}

public enum SubmissionOutcome: Equatable, Sendable {
    case submitted(ReportSubmissionResponse)
    case savedForNetwork
    case failed
}
