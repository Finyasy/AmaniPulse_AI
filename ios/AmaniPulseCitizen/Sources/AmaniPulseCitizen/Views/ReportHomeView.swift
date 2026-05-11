import SwiftUI

struct ReportHomeView: View {
    @ObservedObject var appModel: AppViewModel
    @State private var isReporting = false
    @State private var isRetryingOfflineDrafts = false

    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 12) {
                        Text(appModel.text(.welcomeTitle))
                            .font(.title2.weight(.semibold))
                        Text(appModel.text(.welcomeBody))
                            .font(.body)
                        Text(appModel.text(.emergencyLimit))
                            .font(.callout.weight(.medium))
                            .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 6)
                    .accessibilityElement(children: .combine)
                }

                Section {
                    Button {
                        isReporting = true
                    } label: {
                        Label(appModel.text(.startReport), systemImage: "plus.circle.fill")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    .accessibilityIdentifier(AccessibilityIdentifiers.reportIncidentButton)
                }

                Section {
                    if appModel.savedDrafts.isEmpty {
                        Text(appModel.text(.noDrafts))
                            .foregroundStyle(.secondary)
                    } else {
                        if hasWaitingDrafts {
                            Button {
                                isRetryingOfflineDrafts = true
                                Task {
                                    await appModel.retryWaitingDrafts()
                                    isRetryingOfflineDrafts = false
                                }
                            } label: {
                                Label(appModel.text(.retrySavedReports), systemImage: "arrow.triangle.2.circlepath")
                            }
                            .disabled(!appModel.isNetworkAvailable || isRetryingOfflineDrafts)
                            .accessibilityIdentifier(AccessibilityIdentifiers.reportOfflineRetryButton)
                        }

                        ForEach(appModel.savedDrafts) { draft in
                            DraftRow(draft: draft, appModel: appModel)
                        }
                        .onDelete { offsets in
                            for offset in offsets {
                                let draft = appModel.savedDrafts[offset]
                                Task { await appModel.deleteDraft(draft) }
                            }
                        }
                    }
                } header: {
                    Text(appModel.text(.saveDraft))
                }
            }
            .navigationTitle(appModel.text(.appName))
            .sheet(isPresented: $isReporting) {
                ReportFlowView(appModel: appModel)
            }
        }
    }

    private var hasWaitingDrafts: Bool {
        appModel.savedDrafts.contains { $0.status == .waitingForNetwork }
    }
}

private struct DraftRow: View {
    let draft: ReportDraft
    @ObservedObject var appModel: AppViewModel

    var body: some View {
        HStack(alignment: .center, spacing: 12) {
            VStack(alignment: .leading, spacing: 4) {
                Text(categoryTitle)
                    .font(.headline)
                    .accessibilityIdentifier(draftRowIdentifier)
                Text(statusTitle)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .accessibilityIdentifier(draftStatusIdentifier)
            }

            Spacer()

            if draft.reportReference != nil {
                Button {
                    Task {
                        await appModel.refreshStatus(for: draft)
                    }
                } label: {
                    Image(systemName: "arrow.clockwise")
                }
                .buttonStyle(.borderless)
                .accessibilityLabel("Refresh report status")
                .accessibilityIdentifier(AccessibilityIdentifiers.reportStatusRefreshButton)
            }
        }
    }

    private var categoryTitle: String {
        guard let category = draft.category else {
            return appModel.text(.startReport)
        }

        return appModel.categoryCopy(for: category).title
    }

    private var draftRowIdentifier: String {
        guard let category = draft.category else {
            return "report.draftRow.uncategorized"
        }

        return AccessibilityIdentifiers.reportDraftRow(category: category)
    }

    private var draftStatusIdentifier: String {
        guard let category = draft.category else {
            return "report.draftStatus.uncategorized"
        }

        return AccessibilityIdentifiers.reportDraftStatus(category: category)
    }

    private var statusTitle: String {
        switch draft.status {
        case .draft:
            "Draft"
        case .waitingForNetwork:
            "Waiting for network"
        case .submitted:
            "Submitted"
        case .received:
            "Received"
        case .underReview:
            "Under review"
        case .aggregated:
            "Aggregated"
        case .closed:
            "Closed"
        case .unableToProcess:
            "Unable to process"
        }
    }
}
