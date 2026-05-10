"use client";

import { useState } from "react";
import { Send, ShieldCheck } from "lucide-react";

const categories = [
  "Violence threat",
  "Hate speech",
  "Intimidation",
  "Bribery",
  "Misinformation",
  "Protest escalation",
  "Police/community incident",
];

export function ReportForm() {
  const [submitted, setSubmitted] = useState(false);

  return (
    <form
      className="report-form"
      onSubmit={(event) => {
        event.preventDefault();
        setSubmitted(true);
      }}
    >
      {submitted ? (
        <div className="success-panel" role="status">
          <ShieldCheck aria-hidden="true" />
          <h2>Report captured for demo review</h2>
          <p>
            This prototype does not transmit live reports yet. In production,
            the report would be encrypted, stripped of unnecessary identifiers,
            and routed for risk scoring.
          </p>
        </div>
      ) : null}

      <label>
        County or nearest area
        <input name="location" placeholder="Example: Mathare, Nairobi" required />
      </label>

      <label>
        What are you reporting?
        <select name="category" required defaultValue="">
          <option value="" disabled>
            Select a category
          </option>
          {categories.map((category) => (
            <option value={category} key={category}>
              {category}
            </option>
          ))}
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
          <input type="radio" name="locationSharing" value="approximate" defaultChecked />
          Use approximate location only
        </label>
        <label className="choice-row">
          <input type="radio" name="locationSharing" value="none" />
          Do not attach location
        </label>
      </fieldset>

      <label className="choice-row consent-row">
        <input type="checkbox" required />
        I understand this is a prototype and should not be used for emergency response.
      </label>

      <button className="button button-primary form-submit" type="submit">
        <Send aria-hidden="true" />
        Submit anonymous report
      </button>
    </form>
  );
}
