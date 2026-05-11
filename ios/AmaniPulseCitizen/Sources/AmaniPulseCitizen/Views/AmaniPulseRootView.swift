import SwiftUI

public struct AmaniPulseRootView: View {
    @StateObject private var appModel: AppViewModel
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding = false
    @Environment(\.scenePhase) private var scenePhase

    public init(appModel: AppViewModel = AppViewModel()) {
        _appModel = StateObject(wrappedValue: appModel)
    }

    public var body: some View {
        Group {
            if hasCompletedOnboarding {
                MainTabView(appModel: appModel)
            } else {
                OnboardingView(appModel: appModel) {
                    hasCompletedOnboarding = true
                }
            }
        }
        .overlay {
            if scenePhase != .active {
                PrivacyShieldView()
            }
        }
        .task(id: appModel.language) {
            await appModel.refreshContent()
        }
    }
}

private struct MainTabView: View {
    @ObservedObject var appModel: AppViewModel

    var body: some View {
        TabView {
            ReportHomeView(appModel: appModel)
                .tabItem {
                    Label(appModel.text(.reportTab), systemImage: "square.and.pencil")
                }
                .accessibilityIdentifier(AccessibilityIdentifiers.reportTab)

            RiskGuidanceView(appModel: appModel)
                .tabItem {
                    Label(appModel.text(.riskTab), systemImage: "shield.lefthalf.filled")
                }
                .accessibilityIdentifier(AccessibilityIdentifiers.riskTab)

            ResourcesView(appModel: appModel)
                .tabItem {
                    Label(appModel.text(.resourcesTab), systemImage: "book.closed")
                }
                .accessibilityIdentifier(AccessibilityIdentifiers.resourcesTab)

            SettingsView(appModel: appModel)
                .tabItem {
                    Label(appModel.text(.settingsTab), systemImage: "gearshape")
                }
                .accessibilityIdentifier(AccessibilityIdentifiers.settingsTab)
        }
    }
}

#Preview {
    AmaniPulseRootView(appModel: AppViewModel(language: .english))
}
