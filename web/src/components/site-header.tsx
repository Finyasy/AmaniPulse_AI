"use client";

import Link from "next/link";
import { Activity, LayoutDashboard, Menu, ShieldAlert } from "lucide-react";
import { useState } from "react";

const navItems = [
  { href: "/report", label: "Report" },
  { href: "/resources", label: "Resources" },
  { href: "/dashboard", label: "Dashboard" },
];

export function SiteHeader() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="site-header">
      <div className="page-shell nav-shell">
        <Link className="brand" href="/" aria-label="AmaniPulse AI home">
          <span className="brand-mark">
            <Activity aria-hidden="true" />
          </span>
          <span>AmaniPulse AI</span>
        </Link>
        <nav className="desktop-nav" aria-label="Main navigation">
          {navItems.map((item) => (
            <Link href={item.href} key={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="nav-actions">
          <Link className="icon-button" href="/dashboard" aria-label="Open dashboard">
            <LayoutDashboard aria-hidden="true" />
          </Link>
          <Link className="button button-compact button-primary" href="/report">
            <ShieldAlert aria-hidden="true" />
            Report
          </Link>
          <button
            aria-controls="mobile-navigation"
            aria-expanded={isMenuOpen}
            className="icon-button mobile-menu"
            onClick={() => setIsMenuOpen((current) => !current)}
            type="button"
            aria-label="Menu"
          >
            <Menu aria-hidden="true" />
          </button>
        </div>
      </div>
      <nav
        aria-label="Mobile navigation"
        className={`mobile-nav ${isMenuOpen ? "open" : ""}`}
        id="mobile-navigation"
      >
        <div className="page-shell">
          {navItems.map((item) => (
            <Link href={item.href} key={item.href} onClick={() => setIsMenuOpen(false)}>
              {item.label}
            </Link>
          ))}
        </div>
      </nav>
    </header>
  );
}
