# AmaniPulse Citizen iPhone Frontend

This is the first native SwiftUI frontend slice for the AmaniPulse AI Citizen MVP.

The package currently contains:

- SwiftUI tab surfaces for Report, Risk, Resources, and Settings.
- First-launch onboarding for safety promise, limits, language, and location control.
- Anonymous report draft models and validation.
- English and Swahili copy for core MVP screens.
- Mock county risk guidance and bundled offline resources.
- Encrypted on-device draft persistence backed by CryptoKit and Keychain-managed keys.
- URLSession API client scaffolding for report submission, report status, app configuration, taxonomy, risk guidance, and resources.
- Network-aware submission handling that keeps unsent reports on device.
- Local report receipts, retry controls for waiting reports, and status refresh for submitted reports.
- App icon, accent color, and launch image assets wired into the Xcode app target.
- App privacy manifest declaring no tracking or collected data and documenting local UserDefaults access.
- XCTest coverage for validation, localization, API payloads, and draft lifecycle behavior.
- XCUITest coverage for onboarding, saving a report draft, switching language, online submission, status refresh, and offline recovery on an iPhone simulator.
- A privacy shield that obscures app content when the app is backgrounded or inactive.

## Run Checks

From this directory:

```bash
swift test
```

To build the runnable iPhone app target from the repo root:

```bash
xcodebuild -project ios/AmaniPulseCitizenApp/AmaniPulseCitizenApp.xcodeproj \
  -scheme AmaniPulseCitizenApp \
  -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath ios/build/DerivedData \
  build
```

To run the simulator UI suite from the repo root:

```bash
xcodebuild test -project ios/AmaniPulseCitizenApp/AmaniPulseCitizenApp.xcodeproj \
  -scheme AmaniPulseCitizenApp \
  -destination 'id=<installed-iPhone-simulator-id>' \
  -derivedDataPath ios/build/DerivedData \
  test
```

The current local simulator verification uses an `AmaniPulse iPhone 16 Pro Max` simulator on the installed iOS runtime. The app target supports iPhone 16 Pro Max-class devices on iOS 17 and newer.

## Run Local MVP Demo

From the repo root:

```bash
scripts/local_mvp_demo.sh
```

The script starts the FastAPI backend at `http://127.0.0.1:8000`, smoke-checks the local API, builds the Debug iPhone simulator app, creates or reuses an `AmaniPulse iPhone 16 Pro Max` simulator, installs the app, opens Simulator, and launches AmaniPulse against the local backend.

## Accelerator And Staging Configuration

The Swift package defaults to mock services so tests remain safe and deterministic. The Debug app target is configured for the local API by default. Use environment variables to override the app for local or accelerator-provided staging APIs:

```bash
AMANIPULSE_API_PROFILE=local
AMANIPULSE_API_BASE_URL=http://127.0.0.1:8000
```

```bash
AMANIPULSE_API_PROFILE=staging
AMANIPULSE_API_BASE_URL=https://<andela-open-accelerator-staging-host>
```

Supported profiles are `mock`, `local`, `staging`, and `production`. The legacy `AMANIPULSE_USE_REMOTE_API=1` flag still maps to the local profile for existing simulator scripts.

For repeatable accessibility-size simulator checks, launch with:

```bash
AMANIPULSE_DYNAMIC_TYPE_SIZE=accessibility3
```

## Next Frontend Milestones

1. Connect the confirmed Andela x Open Accelerator staging API base URL.
2. Expand VoiceOver QA beyond identifiers into manual screen-reader walkthroughs.
3. Convert the MVP release checklist into TestFlight submission metadata.
4. Add Apple Developer signing configuration.
5. Run a device-family pass on an installed iPhone 16 Pro Max simulator or physical device before release.
