import Foundation
import Network

public protocol ConnectivityMonitoring: AnyObject, Sendable {
    var onAvailabilityChange: (@Sendable (Bool) -> Void)? { get set }
    func start()
    func cancel()
}

public final class NetworkConnectivityMonitor: ConnectivityMonitoring, @unchecked Sendable {
    private let monitor = NWPathMonitor()
    private let queue = DispatchQueue(label: "org.amanipulse.connectivity")

    public var onAvailabilityChange: (@Sendable (Bool) -> Void)?

    public init() {}

    public func start() {
        monitor.pathUpdateHandler = { [weak self] path in
            self?.onAvailabilityChange?(path.status == .satisfied)
        }
        monitor.start(queue: queue)
    }

    public func cancel() {
        monitor.cancel()
    }
}
