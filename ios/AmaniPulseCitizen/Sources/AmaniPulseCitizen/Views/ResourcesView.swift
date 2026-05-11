import SwiftUI

struct ResourcesView: View {
    @ObservedObject var appModel: AppViewModel

    var body: some View {
        NavigationStack {
            List {
                Section {
                    Text(appModel.text(.offlineResourcesNote))
                        .foregroundStyle(.secondary)
                }

                ForEach(appModel.resources) { resource in
                    Section {
                        VStack(alignment: .leading, spacing: 8) {
                            Text(resource.title)
                                .font(.headline)
                            Text(resource.body)
                                .font(.body)
                        }
                        .padding(.vertical, 4)
                        .accessibilityElement(children: .combine)
                    }
                }
            }
            .navigationTitle(appModel.text(.resourcesTitle))
        }
    }
}
