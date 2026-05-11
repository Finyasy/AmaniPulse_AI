"use client";

import { useState } from "react";
import { Send, ShieldCheck } from "lucide-react";
import { incidentCategoryOptions } from "@/lib/contracts";
import type { ApiIncidentCategory, ApiLanguage, ApiLocationMode, ReportReceipt } from "@/lib/contracts";
import { submitReport } from "@/lib/api";

export function ReportForm() {
  const [receipt, setReceipt] = useState<ReportReceipt | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  return (
    <form
      className="report-form"
      onSubmit={async (event) => {
        event.preventDefault();
        setIsSubmitting(true);
        setError(null);

        const formData = new FormData(event.currentTarget);
        const locationMode = formData.get("locationMode") as ApiLocationMode;
        const county = String(formData.get("county") ?? "").trim();
        const area = String(formData.get("area") ?? "").trim();
        const description = String(formData.get("summary") ?? "").trim();

        try {
          const nextReceipt = await submitReport({
            client_report_id: `web-${crypto.randomUUID()}`,
            category: formData.get("category") as ApiIncidentCategory,
            description,
            incident_time: new Date().toISOString(),
            location:
              locationMode === "none"
                ? { mode: "none" }
                : {
                    mode: "manual_area",
                    country: "KE",
                    county,
                    area_label: area || undefined,
                  },
            language: formData.get("language") as ApiLanguage,
            source: "ios_citizen_app",
            app_version: "web-demo-0.1.0",
            consents: {
              anonymous_submission: true,
              risk_analysis: true,
            },
          });

          setReceipt(nextReceipt);
          event.currentTarget.reset();
        } catch {
          setError("The report could not be prepared. Please check the required fields and try again.");
        } finally {
          setIsSubmitting(false);
        }
      }}
    >
      {receipt ? (
        <div className="success-panel" role="status">
          <ShieldCheck aria-hidden="true" />
          <h2>Report captured for demo review</h2>
          <p>
            Reference {receipt.report_reference} is marked {receipt.status}. The
            production flow will route this backend-shaped payload through
            encrypted storage and risk scoring.
          </p>
        </div>
      ) : null}

      {error ? (
        <div className="error-panel" role="alert">
          {error}
        </div>
      ) : null}

      <label>
        County
        <input name="county" placeholder="Example: Nairobi" required />
      </label>

      <label>
        Nearest area
        <input name="area" placeholder="Example: Mathare" />
      </label>

      <label>
        What are you reporting?
        <select name="category" required defaultValue="">
          <option value="" disabled>
            Select a category
          </option>
          {incidentCategoryOptions.map((category) => (
            <option value={category.value} key={category.value}>
              {category.label}
            </option>
          ))}
        </select>
      </label>

      <label>
        Language
        <select name="language" required defaultValue="en">
          <option value="en">English</option>
          <option value="sw">Swahili</option>
        </select>
      </label>

      <label>
        What happened?
        <textarea
          name="summary"
          placeholder="Share only what feels safe. Avoid names if they could expose you."
          rows={6}
          required
        />
      </label>

      <fieldset>
        <legend>Location safety</legend>
        <label className="choice-row">
          <input type="radio" name="locationMode" value="manual_area" defaultChecked />
          Use county and area only
        </label>
        <label className="choice-row">
          <input type="radio" name="locationMode" value="none" />
          Do not attach location
        </label>
      </fieldset>

      <label className="choice-row consent-row">
        <input type="checkbox" required />
        I consent to anonymous submission and aggregated risk analysis for this prototype.
      </label>

      <button className="button button-primary form-submit" type="submit" disabled={isSubmitting}>
        <Send aria-hidden="true" />
        {isSubmitting ? "Preparing report" : "Submit anonymous report"}
      </button>
    </form>
  );
}
