import { DashboardShell } from "@/components/dashboard-shell";
import { ReviewQueue } from "@/components/review-queue";
import { getReviewDetails, getReviewEvents } from "@/lib/api";

export default async function ReviewPage() {
  const [reports, events] = await Promise.all([getReviewDetails(), getReviewEvents()]);

  return (
    <DashboardShell eyebrow="Partner verification" title="Review queue">
      <ReviewQueue reports={reports} events={events} />
    </DashboardShell>
  );
}
