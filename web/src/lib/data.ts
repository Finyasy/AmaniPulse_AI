import {
  AlertTriangle,
  Bell,
  ChartNoAxesCombined,
  CircleCheck,
  Clock,
  HandHeart,
  MapPinned,
  Megaphone,
  MessageSquareWarning,
  RadioTower,
  ShieldCheck,
  Smartphone,
  Users,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export type RiskLevel = "LOW" | "GUARDED" | "ELEVATED" | "HIGH" | "CRITICAL";

export type CountyRisk = {
  county: string;
  region: string;
  score: number;
  level: RiskLevel;
  trend: "up" | "down" | "flat";
  drivers: string[];
  reports: number;
};

export type Incident = {
  id: string;
  county: string;
  area: string;
  category: string;
  language: string;
  received: string;
  severity: RiskLevel;
  summary: string;
};

export type Alert = {
  title: string;
  county: string;
  level: RiskLevel;
  window: string;
  rationale: string;
  recommendation: string;
};

export type Channel = {
  name: string;
  description: string;
  status: string;
  icon: LucideIcon;
};

export const channels: Channel[] = [
  {
    name: "iPhone App",
    description: "Offline drafts, controlled location sharing, English and Swahili support.",
    status: "Citizen MVP",
    icon: Smartphone,
  },
  {
    name: "SMS and USSD",
    description: "Short-code reporting for low-bandwidth access during network congestion.",
    status: "Roadmap",
    icon: RadioTower,
  },
  {
    name: "WhatsApp",
    description: "Familiar chat-based intake for communities already using mobile messaging.",
    status: "Roadmap",
    icon: MessageSquareWarning,
  },
  {
    name: "Web Report",
    description: "A light anonymous form for citizens, observers, and civil society partners.",
    status: "Demo-ready",
    icon: Megaphone,
  },
];

export const riskFeatures = [
  "Anonymous report volume",
  "Hate speech and incitement terms",
  "Negative sentiment trend",
  "Threat and mobilization keywords",
  "Rapid message surge",
  "Historical hotspot weight",
  "Protest and intimidation mentions",
  "Trusted partner verification signals",
];

export const countyRisks: CountyRisk[] = [
  {
    county: "Nairobi",
    region: "Urban core",
    score: 84,
    level: "HIGH",
    trend: "up",
    drivers: ["Report surge", "Intimidation mentions", "Rumor escalation"],
    reports: 128,
  },
  {
    county: "Kisumu",
    region: "Lake region",
    score: 76,
    level: "ELEVATED",
    trend: "up",
    drivers: ["Protest chatter", "Transport disruption", "Localized fear sentiment"],
    reports: 83,
  },
  {
    county: "Uasin Gishu",
    region: "Rift Valley",
    score: 69,
    level: "ELEVATED",
    trend: "flat",
    drivers: ["Inciting speech", "Youth mobilization", "Partner watchlist"],
    reports: 62,
  },
  {
    county: "Mombasa",
    region: "Coast",
    score: 58,
    level: "GUARDED",
    trend: "down",
    drivers: ["Rumor corrections", "Observer presence", "Low verified threats"],
    reports: 41,
  },
  {
    county: "Nakuru",
    region: "Rift Valley",
    score: 72,
    level: "ELEVATED",
    trend: "up",
    drivers: ["Bribery reports", "Night meeting mentions", "Rising anxiety"],
    reports: 57,
  },
  {
    county: "Garissa",
    region: "North Eastern",
    score: 43,
    level: "GUARDED",
    trend: "flat",
    drivers: ["Low signal density", "Access barriers", "Needs more verification"],
    reports: 18,
  },
  {
    county: "Machakos",
    region: "Lower Eastern",
    score: 31,
    level: "LOW",
    trend: "down",
    drivers: ["Stable reports", "Peace forum activity", "No surge detected"],
    reports: 12,
  },
];

export const incidents: Incident[] = [
  {
    id: "AP-2714",
    county: "Nairobi",
    area: "Mathare",
    category: "Threat mobilization",
    language: "Sheng",
    received: "12 min ago",
    severity: "HIGH",
    summary: "Multiple anonymous reports mention youth groups gathering after a campaign rally.",
  },
  {
    id: "AP-2713",
    county: "Nakuru",
    area: "Naivasha",
    category: "Bribery",
    language: "Swahili",
    received: "19 min ago",
    severity: "ELEVATED",
    summary: "Residents report cash distribution near a transit point with rising crowd tension.",
  },
  {
    id: "AP-2712",
    county: "Kisumu",
    area: "Kondele",
    category: "Protest escalation",
    language: "English",
    received: "31 min ago",
    severity: "ELEVATED",
    summary: "Observer signal notes protest planning and fear of confrontation with police.",
  },
  {
    id: "AP-2711",
    county: "Uasin Gishu",
    area: "Eldoret",
    category: "Inciting speech",
    language: "Swahili",
    received: "46 min ago",
    severity: "HIGH",
    summary: "Speech excerpts include coded references flagged for human peace actor review.",
  },
  {
    id: "AP-2710",
    county: "Mombasa",
    area: "Likoni",
    category: "Misinformation",
    language: "Swahili",
    received: "1 hr ago",
    severity: "GUARDED",
    summary: "Viral claim corrected by two partner organizations; risk trend is easing.",
  },
];

export const alerts: Alert[] = [
  {
    title: "Rapid escalation risk near Nairobi rally corridor",
    county: "Nairobi",
    level: "HIGH",
    window: "Next 24 hours",
    rationale:
      "Anonymous reports increased 42% while threat and intimidation keywords clustered around two neighboring wards.",
    recommendation:
      "Ask trusted community mediators to verify the signal, increase observer presence, and publish rumor-correction messaging.",
  },
  {
    title: "Potential protest-police confrontation",
    county: "Kisumu",
    level: "ELEVATED",
    window: "Next 48 hours",
    rationale:
      "Protest mentions are rising with localized fear sentiment and repeated transport disruption references.",
    recommendation:
      "Coordinate with peace committees and observer coalitions before planned gatherings begin.",
  },
  {
    title: "Coded incitement requires human review",
    county: "Uasin Gishu",
    level: "HIGH",
    window: "Immediate review",
    rationale:
      "Multilingual classifier flagged repeated coded phrases that match previous escalation narratives.",
    recommendation:
      "Escalate to a trained language and context reviewer before automated action is taken.",
  },
];

export const dashboardStats = [
  {
    label: "National posture",
    value: "Elevated",
    detail: "3 counties trending upward",
    icon: AlertTriangle,
  },
  {
    label: "Anonymous reports",
    value: "401",
    detail: "Last 24 hours",
    icon: Bell,
  },
  {
    label: "Human reviews",
    value: "29",
    detail: "Queued for partners",
    icon: Users,
  },
  {
    label: "Interventions",
    value: "12",
    detail: "Recommended today",
    icon: HandHeart,
  },
];

export const publicPrinciples = [
  {
    title: "Anonymity first",
    body: "Citizens can report risk signals without creating an account or sharing identity details.",
    icon: ShieldCheck,
  },
  {
    title: "Prevention before escalation",
    body: "AI turns report patterns into early warnings before incidents become widespread harm.",
    icon: ChartNoAxesCombined,
  },
  {
    title: "Trusted human action",
    body: "Risk scores support trained peace actors and observers; they do not replace judgment.",
    icon: CircleCheck,
  },
];

export const resourceGroups = [
  {
    title: "Before You Report",
    items: [
      "Move to a safe place before typing sensitive details.",
      "Do not name yourself unless a trusted partner has told you it is safe.",
      "Share approximate location if exact location could expose you.",
    ],
  },
  {
    title: "During Tension",
    items: [
      "Avoid forwarding unverified election claims.",
      "Use calm language when correcting rumors in group chats.",
      "Leave crowded confrontation zones early when possible.",
    ],
  },
  {
    title: "For Peace Actors",
    items: [
      "Verify AI alerts with local context before intervention.",
      "Separate rumor correction from partisan messaging.",
      "Document interventions without exposing reporter identity.",
    ],
  },
];

export const siteMap = [
  { href: "/", label: "Overview", description: "Public explanation of AmaniPulse AI." },
  { href: "/site-map", label: "Site Map", description: "Frontend route map and implementation phases." },
  { href: "/report", label: "Report", description: "Anonymous low-bandwidth web reporting." },
  { href: "/resources", label: "Resources", description: "Safety and civic participation guidance." },
  { href: "/dashboard", label: "Dashboard", description: "Partner intelligence overview." },
  { href: "/dashboard/map", label: "Risk Map", description: "County risk heatmap." },
  { href: "/dashboard/incidents", label: "Incidents", description: "Anonymized incident stream." },
  { href: "/dashboard/review", label: "Review", description: "Read-only human review queue and audit trail." },
  { href: "/dashboard/alerts", label: "Alerts", description: "AI alerts and recommended interventions." },
];

export const mapPins = [
  { county: "Nairobi", x: 54, y: 57, level: "HIGH" as RiskLevel },
  { county: "Kisumu", x: 30, y: 51, level: "ELEVATED" as RiskLevel },
  { county: "Uasin Gishu", x: 39, y: 35, level: "ELEVATED" as RiskLevel },
  { county: "Mombasa", x: 73, y: 83, level: "GUARDED" as RiskLevel },
  { county: "Nakuru", x: 45, y: 47, level: "ELEVATED" as RiskLevel },
  { county: "Garissa", x: 73, y: 47, level: "GUARDED" as RiskLevel },
  { county: "Machakos", x: 59, y: 64, level: "LOW" as RiskLevel },
];

export const responseTimeline = [
  {
    time: "Signal",
    title: "Anonymous report spike",
    body: "Citizen reports and trusted observer notes cluster around a localized concern.",
    icon: MapPinned,
  },
  {
    time: "Model",
    title: "Risk score recalculates",
    body: "The scoring engine weighs volume, language, severity, trend, and historical hotspot context.",
    icon: ChartNoAxesCombined,
  },
  {
    time: "Action",
    title: "Partner review starts",
    body: "Peace actors receive a plain-language explanation and a suggested prevention action.",
    icon: Clock,
  },
];
