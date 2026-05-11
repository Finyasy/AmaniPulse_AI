import SwiftUI

struct OnboardingView: View {
    @ObservedObject var appModel: AppViewModel
    let onComplete: () -> Void

    var body: some View {
        NavigationStack {
            onboardingPages
            .navigationTitle(appModel.text(.appName))
        }
    }

    @ViewBuilder
    private var onboardingPages: some View {
        #if os(iOS)
        pages
            .tabViewStyle(.page)
        #else
        pages
            .tabViewStyle(.automatic)
        #endif
    }

    private var pages: some View {
        TabView {
                OnboardingPage(
                    systemImage: "hand.raised.fill",
                    title: appModel.text(.welcomeTitle),
                    bodyText: appModel.text(.welcomeBody)
                )

                OnboardingPage(
                    systemImage: "lock.shield.fill",
                    title: appModel.text(.safetyPromiseTitle),
                    bodyText: appModel.text(.safetyPromiseBody)
                )

                OnboardingPage(
                    systemImage: "exclamationmark.triangle.fill",
                    title: appModel.text(.emergencyLimit),
                    bodyText: appModel.text(.locationEducationBody)
                )

                VStack(spacing: 24) {
                    OnboardingPage(
                        systemImage: "globe",
                        title: appModel.text(.language),
                        bodyText: appModel.text(.locationEducationTitle)
                    )

                    Picker(appModel.text(.language), selection: $appModel.language) {
                        ForEach(AppLanguage.allCases) { language in
                            Text(language.displayName).tag(language)
                        }
                    }
                    .pickerStyle(.segmented)
                    .accessibilityIdentifier(AccessibilityIdentifiers.onboardingLanguagePicker)
                    .padding(.horizontal)

                    Button {
                        onComplete()
                    } label: {
                        Label(appModel.text(.continueAction), systemImage: "arrow.forward.circle.fill")
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)
                    .accessibilityIdentifier(AccessibilityIdentifiers.onboardingContinue)
                    .padding(.horizontal)
                }
                .padding(.vertical)
            }
        }
}

private struct OnboardingPage: View {
    let systemImage: String
    let title: String
    let bodyText: String

    var body: some View {
        VStack(spacing: 18) {
            Image(systemName: systemImage)
                .font(.system(size: 52, weight: .semibold))
                .foregroundStyle(.tint)
                .accessibilityHidden(true)

            Text(title)
                .font(.title.weight(.semibold))
                .multilineTextAlignment(.center)

            Text(bodyText)
                .font(.body)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(28)
        .accessibilityElement(children: .combine)
    }
}
