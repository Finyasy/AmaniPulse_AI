import CryptoKit
import Foundation
import Security

public enum DraftStorageError: Error, Equatable, Sendable {
    case keyUnavailable
    case unreadableStore
}

public protocol EncryptionKeyProviding: Sendable {
    func symmetricKey() throws -> SymmetricKey
}

public struct EphemeralEncryptionKeyProvider: EncryptionKeyProviding {
    private let keyData: Data

    public init(keyData: Data = Data(repeating: 7, count: 32)) {
        self.keyData = keyData
    }

    public func symmetricKey() throws -> SymmetricKey {
        SymmetricKey(data: keyData)
    }
}

public struct KeychainEncryptionKeyProvider: EncryptionKeyProviding {
    private let service: String
    private let account: String

    public init(service: String = "org.amanipulse.citizen", account: String = "draft-encryption-key") {
        self.service = service
        self.account = account
    }

    public func symmetricKey() throws -> SymmetricKey {
        if let existing = try loadKeyData() {
            return SymmetricKey(data: existing)
        }

        let data = SymmetricKey(size: .bits256).withUnsafeBytes { Data($0) }
        try saveKeyData(data)
        return SymmetricKey(data: data)
    }

    private func loadKeyData() throws -> Data? {
        var query = baseQuery
        query[kSecReturnData as String] = true
        query[kSecMatchLimit as String] = kSecMatchLimitOne

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        if status == errSecItemNotFound {
            return nil
        }

        guard status == errSecSuccess else {
            throw DraftStorageError.keyUnavailable
        }

        return result as? Data
    }

    private func saveKeyData(_ data: Data) throws {
        var query = baseQuery
        query[kSecValueData as String] = data
        query[kSecAttrAccessible as String] = kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess || status == errSecDuplicateItem else {
            throw DraftStorageError.keyUnavailable
        }
    }

    private var baseQuery: [String: Any] {
        [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account
        ]
    }
}

public actor EncryptedReportDraftStore: ReportDraftStoring {
    private let fileURL: URL
    private let keyProvider: EncryptionKeyProviding
    private let encoder: JSONEncoder
    private let decoder: JSONDecoder

    public init(
        fileURL: URL,
        keyProvider: EncryptionKeyProviding = KeychainEncryptionKeyProvider()
    ) {
        self.fileURL = fileURL
        self.keyProvider = keyProvider

        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        self.encoder = encoder

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        self.decoder = decoder
    }

    public static func appSupportStore() throws -> EncryptedReportDraftStore {
        let directory = try FileManager.default.url(
            for: .applicationSupportDirectory,
            in: .userDomainMask,
            appropriateFor: nil,
            create: true
        )
        .appending(path: "AmaniPulseCitizen", directoryHint: .isDirectory)

        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)

        return EncryptedReportDraftStore(fileURL: directory.appending(path: "drafts.bin"))
    }

    public func loadDrafts() async throws -> [ReportDraft] {
        guard FileManager.default.fileExists(atPath: fileURL.path) else {
            return []
        }

        let sealedData = try Data(contentsOf: fileURL)
        let box = try AES.GCM.SealedBox(combined: sealedData)
        let data = try AES.GCM.open(box, using: keyProvider.symmetricKey())
        let drafts = try decoder.decode([ReportDraft].self, from: data)

        return drafts.sorted { $0.incidentTime > $1.incidentTime }
    }

    public func save(_ draft: ReportDraft) async throws {
        var drafts = try await loadDrafts()

        if let index = drafts.firstIndex(where: { $0.id == draft.id }) {
            drafts[index] = draft
        } else {
            drafts.append(draft)
        }

        try persist(drafts)
    }

    public func delete(_ draft: ReportDraft) async throws {
        var drafts = try await loadDrafts()
        drafts.removeAll { $0.id == draft.id }
        try persist(drafts)
    }

    private func persist(_ drafts: [ReportDraft]) throws {
        let directory = fileURL.deletingLastPathComponent()
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)

        let data = try encoder.encode(drafts)
        let sealed = try AES.GCM.seal(data, using: keyProvider.symmetricKey())

        guard let combined = sealed.combined else {
            throw DraftStorageError.unreadableStore
        }

        try combined.write(to: fileURL, options: [.atomic, .completeFileProtection])
    }
}
