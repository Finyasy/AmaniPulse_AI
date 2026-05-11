import SwiftUI

struct SettingsView: View {
    @ObservedObject var appModel: AppViewModel

    var body: some View {
        NavigationStack {
            Form {
                Section(appModel.text(.language)) {
                    Picker(appModel.text(.language), selection: $appModel.language) {
                        ForEach(AppLanguage.allCases) { language in
                            Text(language.displayName).tag(language)
                        }
                    }
                    .pickerStyle(.segmented)
                    .accessibilityIdentifier(AccessibilityIdentifiers.settingsLanguagePicker)
                }

                Section(appModel.text(.privacyTitle)) {
                    Text(appModel.text(.safetyPromiseBody))
                    Button(role: .destructive) {
                        Task {
                            for draft in appModel.savedDrafts {
                                await appModel.deleteDraft(draft)
                            }
                        }
                    } label: {
                        Label(appModel.text(.deleteLocalData), systemImage: "trash")
                    }
                }
            }
            .navigationTitle(appModel.text(.settingsTitle))
        }
    }
}
