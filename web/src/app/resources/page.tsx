import { BookOpenCheck, HandHeart, Languages, WifiOff } from "lucide-react";
import { resourceGroups } from "@/lib/data";

export default function ResourcesPage() {
  return (
    <main>
      <section className="page-hero">
        <div className="page-shell narrow">
          <p className="eyebrow">Peace resources</p>
          <h1>Practical guidance for safer civic participation.</h1>
          <p>
            Resources should stay short, multilingual, and usable under stress.
            The production app can cache this content for offline access.
          </p>
        </div>
      </section>

      <section className="section-band">
        <div className="page-shell resources-grid">
          {resourceGroups.map((group) => (
            <article className="resource-card" key={group.title}>
              <BookOpenCheck aria-hidden="true" />
              <h2>{group.title}</h2>
              <ul>
                {group.items.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>

      <section className="section-band muted">
        <div className="page-shell resource-strip">
          <div>
            <Languages aria-hidden="true" />
            <h2>Multilingual by design</h2>
            <p>English, Swahili, Sheng, and local dialect mixtures need human review loops.</p>
          </div>
          <div>
            <WifiOff aria-hidden="true" />
            <h2>Low-data access</h2>
            <p>Plain text, cached content, and SMS/USSD paths keep the platform useful.</p>
          </div>
          <div>
            <HandHeart aria-hidden="true" />
            <h2>Human-centered AI</h2>
            <p>AI should explain risk and support peace actors, not make final decisions alone.</p>
          </div>
        </div>
      </section>
    </main>
  );
}
