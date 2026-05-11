import { AlertTriangle, LockKeyhole, RadioTower } from "lucide-react";
import { ReportForm } from "@/components/report-form";

export default function ReportPage() {
  return (
    <main>
      <section className="page-hero compact-hero">
        <div className="page-shell narrow">
          <p className="eyebrow">Anonymous web report</p>
          <h1>Share an election peace signal without creating an account.</h1>
          <p>
            This low-bandwidth form is for the capstone demo. A production
            version would encrypt submissions, minimize metadata, and route
            reports through the FastAPI backend.
          </p>
        </div>
      </section>

      <section className="section-band">
        <div className="page-shell report-layout">
          <aside className="safety-panel">
            <h2>Safety first</h2>
            <div className="safety-item">
              <LockKeyhole aria-hidden="true" />
              <p>Do not include your name, phone number, or exact address.</p>
            </div>
            <div className="safety-item">
              <AlertTriangle aria-hidden="true" />
              <p>Move away from danger before submitting any information.</p>
            </div>
            <div className="safety-item">
              <RadioTower aria-hidden="true" />
              <p>For real deployment, SMS and USSD should work when data is weak.</p>
            </div>
          </aside>
          <ReportForm />
        </div>
      </section>
    </main>
  );
}
