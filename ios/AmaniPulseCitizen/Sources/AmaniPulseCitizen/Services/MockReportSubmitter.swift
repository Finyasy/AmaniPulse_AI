import Foundation

public struct MockReportSubmitter: ReportSubmitting {
    public init() {}

    public func submit(_ payload: ReportSubmissionPayload) async throws -> ReportSubmissionResponse {
        ReportSubmissionResponse(
            reportReference: "AP-2027-DEMO",
            status: .received,
            receivedAt: .now,
            message: "Your anonymous report was received."
        )
    }

    public func reportStatus(reference: String) async throws -> ReportStatusResponse {
        ReportStatusResponse(
            reportReference: reference,
            status: .underReview,
            updatedAt: .now,
            displayMessage: "Your report has been received and is being reviewed."
        )
    }
}
