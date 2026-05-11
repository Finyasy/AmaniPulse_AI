import Foundation

public enum LocationChoice: Codable, Equatable, Sendable {
    case none
    case manualArea(country: String = "KE", county: String, areaLabel: String?)
    case approximateCoordinates(country: String = "KE", county: String?, latitudeRounded: Double, longitudeRounded: Double, precisionKilometers: Int)

    public var mode: String {
        switch self {
        case .none:
            "none"
        case .manualArea:
            "manual_area"
        case .approximateCoordinates:
            "approximate_coordinates"
        }
    }

    enum CodingKeys: String, CodingKey {
        case mode
        case country
        case county
        case areaLabel
        case latitudeRounded
        case longitudeRounded
        case precisionKilometers
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        let mode = try container.decode(String.self, forKey: .mode)

        switch mode {
        case "none":
            self = .none
        case "manual_area":
            self = .manualArea(
                country: try container.decodeIfPresent(String.self, forKey: .country) ?? "KE",
                county: try container.decode(String.self, forKey: .county),
                areaLabel: try container.decodeIfPresent(String.self, forKey: .areaLabel)
            )
        case "approximate_coordinates":
            self = .approximateCoordinates(
                country: try container.decodeIfPresent(String.self, forKey: .country) ?? "KE",
                county: try container.decodeIfPresent(String.self, forKey: .county),
                latitudeRounded: try container.decode(Double.self, forKey: .latitudeRounded),
                longitudeRounded: try container.decode(Double.self, forKey: .longitudeRounded),
                precisionKilometers: try container.decode(Int.self, forKey: .precisionKilometers)
            )
        default:
            throw DecodingError.dataCorruptedError(
                forKey: .mode,
                in: container,
                debugDescription: "Unsupported location mode: \(mode)"
            )
        }
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(mode, forKey: .mode)

        switch self {
        case .none:
            break
        case let .manualArea(country, county, areaLabel):
            try container.encode(country, forKey: .country)
            try container.encode(county, forKey: .county)
            try container.encodeIfPresent(areaLabel, forKey: .areaLabel)
        case let .approximateCoordinates(country, county, latitudeRounded, longitudeRounded, precisionKilometers):
            try container.encode(country, forKey: .country)
            try container.encodeIfPresent(county, forKey: .county)
            try container.encode(latitudeRounded, forKey: .latitudeRounded)
            try container.encode(longitudeRounded, forKey: .longitudeRounded)
            try container.encode(precisionKilometers, forKey: .precisionKilometers)
        }
    }
}
