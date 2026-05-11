import {
  createMockReceipt,
  mockCountyRiskResponses,
  mockReviewEvents,
  mockReviewQueue,
  reviewSummaries,
} from "@/lib/mock-backend";
import type {
  CountyRiskResponse,
  ReportCreatePayload,
  ReportReceipt,
  ReviewEventItem,
  ReviewReportDetail,
  ReviewReportSummary,
} from "@/lib/contracts";

const apiBaseUrl = process.env.NEXT_PUBLIC_AMANIPULSE_API_BASE_URL;

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  if (!apiBaseUrl) {
    throw new Error("AmaniPulse API base URL is not configured.");
  }

  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`AmaniPulse API request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function submitReport(payload: ReportCreatePayload): Promise<ReportReceipt> {
  if (!apiBaseUrl) {
    return createMockReceipt(payload);
  }

  return apiFetch<ReportReceipt>("/api/v1/reports", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getCountyRisks(): Promise<CountyRiskResponse[]> {
  if (!apiBaseUrl) {
    return mockCountyRiskResponses;
  }

  const countyCodes = ["047", "042", "027", "001"];
  return Promise.all(
    countyCodes.map((countyCode) => apiFetch<CountyRiskResponse>(`/api/v1/risk/county/${countyCode}`)),
  );
}

export async function getReviewQueue(): Promise<ReviewReportSummary[]> {
  return reviewSummaries();
}

export async function getReviewDetails(): Promise<ReviewReportDetail[]> {
  return mockReviewQueue;
}

export async function getReviewEvents(): Promise<ReviewEventItem[]> {
  return mockReviewEvents;
}
