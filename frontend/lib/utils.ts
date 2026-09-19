import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }

export function formatDate(d: string | null | undefined): string {
  if (!d) return "—";
  return new Date(d).toLocaleDateString("en-IN", { year: "numeric", month: "short", day: "numeric" });
}

export function statusColor(status: string): string {
  const colors: Record<string, string> = {
    PLANNING: "bg-gray-100 text-gray-700",
    ETHICS_PENDING: "bg-yellow-100 text-yellow-800",
    ETHICS_APPROVED: "bg-blue-100 text-blue-800",
    REGULATORY_PENDING: "bg-orange-100 text-orange-800",
    REGISTERED: "bg-indigo-100 text-indigo-800",
    RECRUITING: "bg-emerald-100 text-emerald-800",
    ACTIVE: "bg-green-100 text-green-800",
    COMPLETED: "bg-teal-100 text-teal-800",
    SUSPENDED: "bg-red-100 text-red-800",
    TERMINATED: "bg-red-200 text-red-900",
    SCREENED: "bg-gray-100 text-gray-700",
    ELIGIBLE: "bg-blue-100 text-blue-700",
    CONSENTED: "bg-indigo-100 text-indigo-700",
    ENROLLED: "bg-cyan-100 text-cyan-800",
    RANDOMIZED: "bg-purple-100 text-purple-800",
    WITHDRAWN: "bg-red-100 text-red-700",
    SCHEDULED: "bg-blue-100 text-blue-700",
    OVERDUE: "bg-red-100 text-red-700",
    MISSED: "bg-gray-200 text-gray-600",
    OPEN: "bg-amber-100 text-amber-800",
    CLOSED: "bg-gray-100 text-gray-600",
    MILD: "bg-green-100 text-green-700",
    MODERATE: "bg-yellow-100 text-yellow-800",
    SEVERE: "bg-red-100 text-red-700",
    SERIOUS: "bg-red-200 text-red-800",
    NON_SERIOUS: "bg-gray-100 text-gray-700",
    APPROVED: "bg-green-100 text-green-800",
    REJECTED: "bg-red-100 text-red-800",
    SUBMITTED: "bg-blue-100 text-blue-700",
    UNDER_REVIEW: "bg-yellow-100 text-yellow-800",
    DRAFT: "bg-gray-100 text-gray-600",
    REPORTED: "bg-orange-100 text-orange-800",
    NOT_STARTED: "bg-gray-100 text-gray-600",
    PREPARING: "bg-yellow-100 text-yellow-700",
  };
  return colors[status] || "bg-gray-100 text-gray-700";
}

