"use client";

import Link from "next/link";
import { BookOpen, Bot, FileText, LayoutPanelTop, BadgeCheck, ShieldCheck, Activity, ShieldAlert, Database, ChevronRight } from "lucide-react";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const mainNav = [
  { name: "Workspace", href: "/dashboard", icon: LayoutPanelTop },
  { name: "Study record", href: "/dashboard/study", icon: FileText },
  { name: "Pharmacovigilance", href: "/dashboard/pharmacovigilance", icon: ShieldAlert },
  { name: "AI Co-Pilot", href: "/dashboard/copilot", icon: Bot },
];

const demoWorkflows = [
  { name: "Protocol review", href: "/dashboard/study/protocol-review", icon: FileText },
  { name: "Operational handoff", href: "/dashboard/study/operational-handoff", icon: BadgeCheck },
  { name: "Data safeguards", href: "/dashboard/study/data-safeguards", icon: ShieldCheck },
  { name: "Clinical monitoring", href: "/dashboard/study/clinical-monitoring", icon: Activity },
  { name: "Safety surveillance", href: "/dashboard/study/safety-surveillance", icon: ShieldAlert },
  { name: "CDISC export", href: "/dashboard/study/cdisc-standards", icon: Database },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 border-r border-slate-200 bg-white lg:flex lg:flex-col">
      <div className="border-b border-slate-200 p-5">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-teal-700 text-sm font-bold text-white shadow-sm">
            A
          </div>
          <div>
            <p className="text-sm font-bold text-slate-950">AIIA CTMS</p>
            <p className="text-[11px] text-slate-500 font-medium">Ayurveda Clinical Trials</p>
          </div>
        </Link>
      </div>

      <nav className="flex-1 overflow-y-auto p-3 scrollbar-thin" aria-label="Presentation navigation">
        {/* Main Section */}
        <div className="mb-4">
          <p className="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Overview
          </p>
          <div className="mt-1 space-y-0.5">
            {mainNav.map(({ name, href, icon: Icon }) => {
              const active = pathname === href;
              return (
                <Link
                  key={href}
                  href={href}
                  className={cn(
                    "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition",
                    active
                      ? "bg-teal-50 text-teal-900 font-semibold"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-950"
                  )}
                >
                  <Icon size={16} aria-hidden="true" />
                  {name}
                </Link>
              );
            })}
          </div>
        </div>

        {/* Demo Account Records Section */}
        <div className="mb-4 border-t border-slate-100 pt-3">
          <div className="flex items-center justify-between px-3">
            <p className="text-[10px] font-bold uppercase tracking-wider text-teal-800">
              Demo Workflows
            </p>
            <span className="rounded bg-teal-100 px-1.5 py-0.2 text-[9px] font-bold text-teal-900">
              DEMO ONLY
            </span>
          </div>
          <div className="mt-1 space-y-0.5">
            {demoWorkflows.map(({ name, href, icon: Icon }) => {
              const active = pathname === href;
              return (
                <Link
                  key={href}
                  href={href}
                  className={cn(
                    "flex items-center justify-between rounded-md px-3 py-1.5 text-xs font-medium transition",
                    active
                      ? "bg-teal-700 text-white font-semibold shadow-sm"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-950"
                  )}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon size={14} className={active ? "text-white" : "text-teal-700"} aria-hidden="true" />
                    <span>{name}</span>
                  </div>
                  {active && <ChevronRight size={12} />}
                </Link>
              );
            })}
          </div>
        </div>

        {/* Presentation Guide Section */}
        <div className="border-t border-slate-100 pt-3">
          <p className="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Assistance
          </p>
          <div className="mt-1">
            <Link
              href="/dashboard/guide"
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition",
                pathname === "/dashboard/guide"
                  ? "bg-teal-50 text-teal-900 font-semibold"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-950"
              )}
            >
              <BookOpen size={16} aria-hidden="true" />
              Demo guide
            </Link>
          </div>
        </div>
      </nav>

      <div className="border-t border-slate-200 bg-slate-50/50 p-4 text-xs leading-relaxed text-slate-500">
        <p className="font-semibold text-slate-700">Presentation Demo Mode</p>
        <p className="text-[11px] text-slate-400 mt-0.5">Account: admin@aiia.gov.in</p>
      </div>
    </aside>
  );
}
