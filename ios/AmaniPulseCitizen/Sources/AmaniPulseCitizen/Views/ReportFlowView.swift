import SwiftUI

struct ReportFlowView: View {
    @ObservedObject var appModel: AppViewModel
    @StateObject private var model = ReportFlowViewModel()
    @Environment(\.dismiss) private var dismiss
    @State private var statusMessage: String?
    @FocusState private var isDescriptionFocused: Bool

    var body: some View {
        NavigationStack {
            Form {
                Section(appModel.text(.safetyPromiseTitle)) {
                    Text(appModel.text(.safetyPromiseBody))
                    Text(appModel.text(.personalInfoWarning))
                        .font(.callout.weight(.medium))
                }

                Section(appModel.text(.reportTab)) {
                    CategoryPicker(appModel: appModel, selection: $model.draft.category)

                    TextField(
                        appModel.text(.reportDescriptionPrompt),
                        text: $model.draft.description,
                        axis: .vertical
                    )
                        .lineLimit(4...8)
                        .focused($isDescriptionFocused)
                        .accessibilityIdentifier(AccessibilityIdentifiers.reportDescriptionEditor)

                    DatePicker(
                        appModel.text(.incidentTime),
                        selection: $model.draft.incidentTime,
                        displayedComponents: [.date, .hourAndMinute]
                    )
                }

                LocationChoiceSection(appModel: appModel, draft: $model.draft)

                Section(appModel.text(.reviewTitle)) {
                    Toggle(appModel.text(.acceptSafetyReminder), isOn: $model.draft.acceptedSafetyReminder)
                        .toggleStyle(.switch)
                        .accessibilityIdentifier(AccessibilityIdentifiers.reportSafetyToggle)

                    if !model.validationErrors.isEmpty {
                        ValidationSummary(appModel: appModel, errors: model.validationErrors)
                    }

                    Button(appModel.text(.submitReport)) {
                        isDescriptionFocused = false
                        guard let draft = model.prepareForSubmission() else {
                            return
                        }

                        Task {
                            let outcome = await appModel.submitDraft(draft)
                            switch outcome {
                            case let .submitted(response):
                                statusMessage = response.message.isEmpty ? appModel.text(.reportReceived) : response.message
                            case .savedForNetwork:
                                statusMessage = appModel.text(.waitingForNetwork)
                            case .failed:
                                statusMessage = appModel.text(.draftSaved)
                            }
                        }
                    }
                    .accessibilityIdentifier(AccessibilityIdentifiers.reportSubmitButton)

                    Button(appModel.text(.saveDraft)) {
                        isDescriptionFocused = false
                        model.setLanguage(appModel.language)
                        model.markDraftSaved()
                        Task {
                            await appModel.saveDraft(model.draft)
                            dismiss()
                        }
                    }
                    .accessibilityIdentifier(AccessibilityIdentifiers.reportSaveDraftButton)
                }
            }
            .scrollDismissesKeyboard(.interactively)
            .navigationTitle(appModel.text(.startReport))
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button(appModel.text(.close)) {
                        dismiss()
                    }
                }
            }
            .onAppear {
                model.setLanguage(appModel.language)
            }
            .alert(appModel.text(.appName), isPresented: Binding(
                get: { statusMessage != nil },
                set: { isPresented in
                    if !isPresented {
                        statusMessage = nil
                        dismiss()
                    }
                }
            )) {
                Button(appModel.text(.close)) {
                    statusMessage = nil
                    dismiss()
                }
            } message: {
                Text(statusMessage ?? "")
            }
        }
    }
}

private struct CategoryPicker: View {
    @ObservedObject var appModel: AppViewModel
    @Binding var selection: IncidentCategory?

    var body: some View {
        ForEach(IncidentCategory.allCases) { category in
            Button {
                selection = category
            } label: {
                HStack(alignment: .firstTextBaseline) {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(appModel.categoryCopy(for: category).title)
                            .font(.headline)
                        Text(appModel.categoryCopy(for: category).description)
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                    Spacer()
                    if selection == category {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundStyle(.tint)
                    }
                }
            }
            .buttonStyle(.plain)
            .accessibilityLabel(appModel.categoryCopy(for: category).title)
            .accessibilityHint(appModel.categoryCopy(for: category).description)
            .accessibilityIdentifier("report.category.\(category.rawValue)")
        }
    }
}

private enum LocationMode: String, CaseIterable, Identifiable {
    case none
    case manual
    case approximate

    var id: String { rawValue }
}

private struct LocationChoiceSection: View {
    @ObservedObject var appModel: AppViewModel
    @Binding var draft: ReportDraft
    @State private var mode: LocationMode = .none
    @State private var county = "Nairobi"
    @State private var area = ""

    var body: some View {
        Section(appModel.text(.locationTitle)) {
            Picker(appModel.text(.locationTitle), selection: $mode) {
                Text(appModel.text(.locationNone)).tag(LocationMode.none)
                Text(appModel.text(.locationManual)).tag(LocationMode.manual)
                Text(appModel.text(.locationApproximate)).tag(LocationMode.approximate)
            }

            if mode == .manual {
                TextField(appModel.text(.county), text: $county)
                TextField(appModel.text(.areaOptional), text: $area)
            }
        }
        .onChange(of: mode) {
            updateLocation()
        }
        .onChange(of: county) {
            updateLocation()
        }
        .onChange(of: area) {
            updateLocation()
        }
    }

    private func updateLocation() {
        switch mode {
        case .none:
            draft.location = .none
        case .manual:
            draft.location = .manualArea(
                county: county.trimmingCharacters(in: .whitespacesAndNewlines),
                areaLabel: area.trimmingCharacters(in: .whitespacesAndNewlines).nilIfEmpty
            )
        case .approximate:
            draft.location = .approximateCoordinates(
                county: county.trimmingCharacters(in: .whitespacesAndNewlines).nilIfEmpty,
                latitudeRounded: -1.29,
                longitudeRounded: 36.82,
                precisionKilometers: 5
            )
        }
    }
}

private struct ValidationSummary: View {
    @ObservedObject var appModel: AppViewModel
    let errors: [ReportValidationError]

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            ForEach(errors, id: \.self) { error in
                Label(title(for: error), systemImage: "exclamationmark.circle")
                    .font(.callout)
            }
        }
        .foregroundStyle(.red)
        .accessibilityElement(children: .combine)
        .accessibilityIdentifier(AccessibilityIdentifiers.reportValidationSummary)
    }

    private func title(for error: ReportValidationError) -> String {
        switch error {
        case .missingCategory:
            appModel.text(.validationMissingCategory)
        case .descriptionTooShort:
            appModel.text(.validationDescriptionTooShort)
        case .safetyReminderNotAccepted:
            appModel.text(.validationSafetyReminder)
        }
    }
}

private extension String {
    var nilIfEmpty: String? {
        isEmpty ? nil : self
    }
}
