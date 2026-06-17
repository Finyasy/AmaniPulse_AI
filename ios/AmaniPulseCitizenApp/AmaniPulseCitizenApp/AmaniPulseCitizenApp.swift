import SwiftUI

@main
struct AmaniPulseCitizenApp: App {
    @StateObject private var appModel: AppViewModel
    private let connectivityMonitor: NetworkConnectivityMonitor

    init() {
        if ProcessInfo.processInfo.arguments.contains("-resetOnboarding") {
            UserDefaults.standard.removeObject(forKey: "hasCompletedOnboarding")
        }

        let draftStore: any ReportDraftStoring
        if ProcessInfo.processInfo.environment["AMANIPULSE_DRAFT_STORE"] == "in_memory" {
            draftStore = InMemoryReportDraftStore()
        } else {
            draftStore = (try? EncryptedReportDraftStore.appSupportStore()) ?? InMemoryReportDraftStore()
        }

        let environment: AppEnvironment
        #if DEBUG
        environment = AppEnvironment.resolve(
            environment: ProcessInfo.processInfo.environment,
            bundleAPIProfile: "local",
            bundleAPIBaseURL: "http://127.0.0.1:8000"
        )
        #else
        environment = AppEnvironment.current()
        #endif
        let forcedNetworkAvailable = ProcessInfo.processInfo.environment["AMANIPULSE_NETWORK_AVAILABLE"].map { $0 == "1" }
        let model: AppViewModel

        switch environment {
        case .mock:
            model = AppViewModel(isNetworkAvailable: forcedNetworkAvailable ?? true, draftStore: draftStore)
        case let .remote(_, baseURL):
            let apiClient = AmaniPulseAPIClient(baseURL: baseURL)
            model = AppViewModel(
                isNetworkAvailable: forcedNetworkAvailable ?? true,
                contentService: apiClient,
                draftStore: draftStore,
                reportSubmitter: apiClient
            )
        }

        let monitor = NetworkConnectivityMonitor()

        monitor.onAvailabilityChange = { isAvailable in
            Task { @MainActor in
                if let forcedValue = ProcessInfo.processInfo.environment["AMANIPULSE_NETWORK_AVAILABLE"] {
                    model.isNetworkAvailable = forcedValue == "1"
                    return
                }

                model.isNetworkAvailable = isAvailable
                if isAvailable {
                    await model.retryWaitingDrafts()
                }
            }
        }
        monitor.start()

        _appModel = StateObject(wrappedValue: model)
        connectivityMonitor = monitor
    }

    var body: some Scene {
        WindowGroup {
            rootView
        }
    }

    @ViewBuilder
    private var rootView: some View {
        if let dynamicTypeSize = Self.dynamicTypeSizeOverride() {
            AmaniPulseRootView(appModel: appModel)
                .dynamicTypeSize(dynamicTypeSize)
        } else {
            AmaniPulseRootView(appModel: appModel)
        }
    }

    private static func dynamicTypeSizeOverride() -> DynamicTypeSize? {
        switch ProcessInfo.processInfo.environment["AMANIPULSE_DYNAMIC_TYPE_SIZE"] {
        case "xSmall":
            return .xSmall
        case "small":
            return .small
        case "medium":
            return .medium
        case "large":
            return .large
        case "xLarge":
            return .xLarge
        case "xxLarge":
            return .xxLarge
        case "xxxLarge":
            return .xxxLarge
        case "accessibility1":
            return .accessibility1
        case "accessibility2":
            return .accessibility2
        case "accessibility3":
            return .accessibility3
        case "accessibility4":
            return .accessibility4
        case "accessibility5":
            return .accessibility5
        default:
            return nil
        }
    }
}
