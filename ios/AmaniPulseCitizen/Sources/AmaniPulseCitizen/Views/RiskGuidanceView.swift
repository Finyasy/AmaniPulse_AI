import SwiftUI

struct RiskGuidanceView: View {
    @ObservedObject var appModel: AppViewModel

    var body: some View {
        NavigationStack {
            List(appModel.riskGuidance) { guidance in
                Section {
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text(guidance.countyName)
                                .font(.headline)
                            Spacer()
                            Label(
                                appModel.localization.riskLevelTitle(guidance.level, language: appModel.language),
                                systemImage: "circle.fill"
                            )
                            .font(.subheadline.weight(.semibold))
                        }

                        Text(guidance.summary)
                            .font(.body)

                        ForEach(guidance.guidance, id: \.self) { item in
                            Label(item, systemImage: "checkmark.circle")
                                .font(.callout)
                        }
                    }
                    .padding(.vertical, 4)
                    .accessibilityElement(children: .combine)
                }
            }
            .navigationTitle(appModel.text(.riskTitle))
            .overlay {
                if appModel.riskGuidance.isEmpty {
                    ContentUnavailableView(
                        appModel.text(.riskTitle),
                        systemImage: "wifi.slash",
                        description: Text(appModel.text(.riskUnavailable))
                    )
                }
            }
        }
    }
}
