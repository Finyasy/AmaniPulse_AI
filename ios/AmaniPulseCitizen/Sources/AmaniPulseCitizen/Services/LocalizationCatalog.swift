import Foundation

public struct CategoryCopy: Equatable, Sendable {
    public let title: String
    public let description: String
}

public struct LocalizationCatalog: Sendable {
    public init() {}

    public func text(_ key: TextKey, language: AppLanguage) -> String {
        Self.copy[language]?[key.rawValue] ?? Self.copy[.english]?[key.rawValue] ?? key.rawValue
    }

    public func categoryCopy(for category: IncidentCategory, language: AppLanguage) -> CategoryCopy {
        let localized = Self.categoryCopy[language]?[category] ?? Self.categoryCopy[.english]?[category]
        return localized ?? CategoryCopy(title: category.rawValue, description: "")
    }

    public func riskLevelTitle(_ level: RiskLevel, language: AppLanguage) -> String {
        Self.riskCopy[language]?[level] ?? Self.riskCopy[.english]?[level] ?? level.rawValue
    }
}

public enum TextKey: String, Sendable {
    case appName
    case reportTab
    case riskTab
    case resourcesTab
    case settingsTab
    case welcomeTitle
    case welcomeBody
    case continueAction
    case locationEducationTitle
    case locationEducationBody
    case safetyPromiseTitle
    case safetyPromiseBody
    case emergencyLimit
    case startReport
    case reportDescriptionPrompt
    case personalInfoWarning
    case incidentTime
    case locationTitle
    case locationNone
    case locationManual
    case locationApproximate
    case county
    case areaOptional
    case reviewTitle
    case acceptSafetyReminder
    case saveDraft
    case retrySavedReports
    case submitReport
    case reportReceived
    case waitingForNetwork
    case draftSaved
    case noDrafts
    case close
    case validationMissingCategory
    case validationDescriptionTooShort
    case validationSafetyReminder
    case riskTitle
    case riskUnavailable
    case resourcesTitle
    case settingsTitle
    case language
    case privacyTitle
    case deleteLocalData
    case offlineResourcesNote
}

private extension LocalizationCatalog {
    static let copy: [AppLanguage: [String: String]] = [
        .english: [
            "appName": "AmaniPulse",
            "reportTab": "Report",
            "riskTab": "Risk",
            "resourcesTab": "Resources",
            "settingsTab": "Settings",
            "welcomeTitle": "Report safely",
            "welcomeBody": "AmaniPulse helps you share election safety concerns anonymously, with control over what location you include.",
            "continueAction": "Continue",
            "locationEducationTitle": "You control location",
            "locationEducationBody": "You can choose approximate location, enter a county or area, or submit without location.",
            "safetyPromiseTitle": "Your safety comes first",
            "safetyPromiseBody": "No account is required. Avoid names, phone numbers, exact home addresses, or details that could identify you unless sharing them is truly necessary.",
            "emergencyLimit": "AmaniPulse is not an emergency response service. Move to safety first.",
            "startReport": "Report an incident",
            "reportDescriptionPrompt": "Describe what happened in a few words",
            "personalInfoWarning": "Do not include personal details unless they are necessary for safety.",
            "incidentTime": "When did it happen?",
            "locationTitle": "Location",
            "locationNone": "Submit without location",
            "locationManual": "Choose county or area",
            "locationApproximate": "Use approximate location",
            "county": "County",
            "areaOptional": "Area, optional",
            "reviewTitle": "Review before sending",
            "acceptSafetyReminder": "I understand this report is anonymous but not an emergency request.",
            "saveDraft": "Save draft",
            "retrySavedReports": "Submit saved reports",
            "submitReport": "Submit report",
            "reportReceived": "Your anonymous report was received.",
            "waitingForNetwork": "No network is available. This report is saved on this device until you submit it.",
            "draftSaved": "Draft saved on this device.",
            "noDrafts": "You have no saved drafts.",
            "close": "Close",
            "validationMissingCategory": "Choose a category.",
            "validationDescriptionTooShort": "Add a few more details.",
            "validationSafetyReminder": "Confirm the safety reminder.",
            "riskTitle": "County risk guidance",
            "riskUnavailable": "Local guidance is temporarily unavailable.",
            "resourcesTitle": "Safety resources",
            "settingsTitle": "Settings",
            "language": "Language",
            "privacyTitle": "Privacy",
            "deleteLocalData": "Delete local data",
            "offlineResourcesNote": "Essential resources are available without network."
        ],
        .swahili: [
            "appName": "AmaniPulse",
            "reportTab": "Ripoti",
            "riskTab": "Hatari",
            "resourcesTab": "Msaada",
            "settingsTab": "Mipangilio",
            "welcomeTitle": "Ripoti kwa usalama",
            "welcomeBody": "AmaniPulse hukusaidia kutuma taarifa za usalama wa uchaguzi bila kujitambulisha, huku ukichagua taarifa za eneo utakazoshiriki.",
            "continueAction": "Endelea",
            "locationEducationTitle": "Unadhibiti taarifa za eneo",
            "locationEducationBody": "Unaweza kuchagua eneo la kukadiria, kuandika kaunti au eneo, au kutuma bila eneo.",
            "safetyPromiseTitle": "Usalama wako kwanza",
            "safetyPromiseBody": "Huhitaji akaunti. Epuka majina, namba za simu, anwani kamili, au maelezo yanayoweza kukutambulisha isipokuwa ni muhimu kabisa.",
            "emergencyLimit": "AmaniPulse si huduma ya dharura. Kwanza nenda mahali salama.",
            "startReport": "Ripoti tukio",
            "reportDescriptionPrompt": "Eleza kilichotokea kwa maneno machache",
            "personalInfoWarning": "Usiweke taarifa binafsi isipokuwa ni muhimu kwa usalama.",
            "incidentTime": "Ilitokea lini?",
            "locationTitle": "Eneo",
            "locationNone": "Tuma bila eneo",
            "locationManual": "Chagua kaunti au eneo",
            "locationApproximate": "Tumia eneo la kukadiria",
            "county": "Kaunti",
            "areaOptional": "Eneo, si lazima",
            "reviewTitle": "Kagua kabla ya kutuma",
            "acceptSafetyReminder": "Ninaelewa ripoti hii ni ya siri lakini si ombi la dharura.",
            "saveDraft": "Hifadhi rasimu",
            "retrySavedReports": "Tuma ripoti zilizohifadhiwa",
            "submitReport": "Tuma ripoti",
            "reportReceived": "Ripoti yako ya siri imepokelewa.",
            "waitingForNetwork": "Hakuna mtandao. Ripoti hii imehifadhiwa kwenye kifaa hiki hadi uitume.",
            "draftSaved": "Rasimu imehifadhiwa kwenye kifaa hiki.",
            "noDrafts": "Huna rasimu zilizohifadhiwa.",
            "close": "Funga",
            "validationMissingCategory": "Chagua aina ya tukio.",
            "validationDescriptionTooShort": "Ongeza maelezo machache zaidi.",
            "validationSafetyReminder": "Thibitisha ujumbe wa usalama.",
            "riskTitle": "Mwongozo wa hatari kwa kaunti",
            "riskUnavailable": "Mwongozo wa eneo haupatikani kwa sasa.",
            "resourcesTitle": "Rasilimali za usalama",
            "settingsTitle": "Mipangilio",
            "language": "Lugha",
            "privacyTitle": "Faragha",
            "deleteLocalData": "Futa taarifa za kifaa",
            "offlineResourcesNote": "Rasilimali muhimu zinapatikana bila intaneti."
        ]
    ]

    static let categoryCopy: [AppLanguage: [IncidentCategory: CategoryCopy]] = [
        .english: [
            .violenceThreat: CategoryCopy(title: "Violence threat", description: "Threats of harm, attacks, or planned violence."),
            .activeViolence: CategoryCopy(title: "Active violence or unrest", description: "Fighting, destruction, or unrest happening now."),
            .voterIntimidation: CategoryCopy(title: "Voter intimidation", description: "Pressure, threats, or blocking civic participation."),
            .hateSpeechOrIncitement: CategoryCopy(title: "Hate speech or incitement", description: "Messages encouraging harm toward a group."),
            .misinformationOrRumor: CategoryCopy(title: "Misinformation or rumor", description: "Unverified claims that may raise tension."),
            .corruptionBriberyOrCoercion: CategoryCopy(title: "Corruption or coercion", description: "Bribery, forced support, or threats tied to benefits."),
            .authorityAbuse: CategoryCopy(title: "Police or authority abuse", description: "Misuse of authority connected to election safety."),
            .suspiciousMobilization: CategoryCopy(title: "Suspicious mobilization", description: "Groups gathering in ways that may create risk."),
            .otherElectionSafetyConcern: CategoryCopy(title: "Other safety concern", description: "Anything else connected to election tension.")
        ],
        .swahili: [
            .violenceThreat: CategoryCopy(title: "Tishio la vurugu", description: "Vitisho vya madhara, mashambulizi, au vurugu zinazopangwa."),
            .activeViolence: CategoryCopy(title: "Vurugu zinaendelea", description: "Mapigano, uharibifu, au machafuko yanayotokea sasa."),
            .voterIntimidation: CategoryCopy(title: "Vitisho kwa wapiga kura", description: "Shinikizo, vitisho, au kuzuia ushiriki wa kiraia."),
            .hateSpeechOrIncitement: CategoryCopy(title: "Chuki au uchochezi", description: "Ujumbe unaochochea madhara dhidi ya kundi."),
            .misinformationOrRumor: CategoryCopy(title: "Taarifa potofu au uvumi", description: "Madai ambayo hayajathibitishwa na yanaweza kuongeza mvutano."),
            .corruptionBriberyOrCoercion: CategoryCopy(title: "Rushwa au kulazimishwa", description: "Hongo, kulazimishwa kuunga mkono, au vitisho vinavyohusiana na manufaa."),
            .authorityAbuse: CategoryCopy(title: "Matumizi mabaya ya mamlaka", description: "Matumizi mabaya ya mamlaka yanayohusu usalama wa uchaguzi."),
            .suspiciousMobilization: CategoryCopy(title: "Mkusanyiko unaotia shaka", description: "Makundi yanayokusanyika kwa namna inayoweza kuongeza hatari."),
            .otherElectionSafetyConcern: CategoryCopy(title: "Wasiwasi mwingine wa usalama", description: "Jambo lingine lolote linalohusiana na mvutano wa uchaguzi.")
        ]
    ]

    static let riskCopy: [AppLanguage: [RiskLevel: String]] = [
        .english: [
            .low: "Low",
            .moderate: "Moderate",
            .high: "High",
            .critical: "Critical"
        ],
        .swahili: [
            .low: "Chini",
            .moderate: "Wastani",
            .high: "Juu",
            .critical: "Kubwa sana"
        ]
    ]
}
