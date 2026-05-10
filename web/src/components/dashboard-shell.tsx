import Link from "next/link";
import { Bell, ListFilter, Map, Radar } from "lucide-react";

const dashboardNav = [
  { href: "/dashboard", label: "Overview", icon: Radar },
  { href: "/dashboard/map", label: "Risk Map", icon: Map },
  { href: "/dashboard/incidents", label: "Incidents", icon: ListFilter },
  { href: "/dashboard/alerts", label: "Alerts", icon: Bell },
];

export function DashboardShell({
  title,
  eyebrow,
  children,
}: {
  title: string;
  eyebrow: string;
  children: React.ReactNode;
}) {
  return (
    <main className="dashboard-page">
      <div className="page-shell dashboard-layout">
        <aside className="dashboard-sidebar" aria-label="Dashboard navigation">
          <span className="dashboard-kicker">Partner dashboard</span>
          <nav>
            {dashboardNav.map((item) => {
              const Icon = item.icon;
              return (
                <Link href={item.href} key={item.href}>
                  <Icon aria-hidden="true" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </aside>
        <section className="dashboard-main">
          <div className="dashboard-title">
            <p className="eyebrow">{eyebrow}</p>
            <h1>{title}</h1>
          </div>
          {children}
        </section>
      </div>
    </main>
  );
}
