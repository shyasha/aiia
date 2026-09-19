"use client";
import { useState, useEffect } from "react";
import { Bot, AlertTriangle, Clock, TrendingDown, RefreshCw, CheckCircle } from "lucide-react";
import api from "@/lib/api";

type WorkflowAlert = {
  id: string;
  entity_type: "AE" | "Visit" | "Milestone";
  entity_id: string;
  alert_type: "bottleneck" | "deadline_risk" | "delay";
  message: string;
  severity: "low" | "medium" | "high";
  created_at: string | null;
};

function severityConfig(severity: WorkflowAlert["severity"]) {
  if (severity === "high") return { bg: "bg-red-50 border-red-200", badge: "bg-red-100 text-red-700", dot: "bg-red-500" };
  if (severity === "medium") return { bg: "bg-amber-50 border-amber-200", badge: "bg-amber-100 text-amber-700", dot: "bg-amber-500" };
  return { bg: "bg-blue-50 border-blue-200", badge: "bg-blue-100 text-blue-700", dot: "bg-blue-400" };
}

function alertTypeIcon(type: WorkflowAlert["alert_type"]) {
  if (type === "bottleneck") return <AlertTriangle size={13} className="shrink-0" />;
  if (type === "deadline_risk") return <Clock size={13} className="shrink-0" />;
  return <TrendingDown size={13} className="shrink-0" />;
}

function entityLabel(entity_type: WorkflowAlert["entity_type"]) {
  if (entity_type === "AE") return "Adverse Event";
  if (entity_type === "Visit") return "Visit";
  return "Milestone";
}

export default function CopilotPage() {
  const [alerts, setAlerts] = useState<WorkflowAlert[]>([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [lastScanned, setLastScanned] = useState<string | null>(null);
  const [scanMessage, setScanMessage] = useState<string | null>(null);

  const fetchAlerts = async () => {
    try {
      const res = await api.get("/workflow-alerts");
      setAlerts(res.data);
    } catch {
      setAlerts([]);
    }
  };

  useEffect(() => {
    fetchAlerts().finally(() => setLoading(false));
  }, []);

  const runScan = async () => {
    setScanning(true);
    setScanMessage(null);
    try {
      const res = await api.post("/workflow-alerts/scan", {});
      setScanMessage(res.data.message);
      setLastScanned(new Date().toLocaleTimeString());
      await fetchAlerts();
    } catch {
      setScanMessage("Scan failed — check API connection.");
    } finally {
      setScanning(false);
    }
  };

  const highCount = alerts.filter(a => a.severity === "high").length;
  const mediumCount = alerts.filter(a => a.severity === "medium").length;
  const lowCount = alerts.filter(a => a.severity === "low").length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Bot size={22} className="text-teal-700" />
            <h1 className="text-2xl font-bold text-gray-900">AI Co-Pilot</h1>
          </div>
          <p className="text-sm text-gray-500">
            Operational workflow monitor — spots bottlenecks, deadline risks, and delays across the trial.
            Does not make clinical or medical judgments.
          </p>
        </div>
        <button
          onClick={runScan}
          disabled={scanning}
          className="flex items-center gap-2 rounded-lg bg-teal-700 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-teal-800 disabled:opacity-60 transition"
        >
          <RefreshCw size={14} className={scanning ? "animate-spin" : ""} />
          {scanning ? "Scanning…" : "Run scan"}
        </button>
      </div>

      {/* Scan message */}
      {scanMessage && (
        <div className="rounded-lg border border-teal-200 bg-teal-50 px-4 py-2 text-sm text-teal-800">
          {scanMessage}{lastScanned && <span className="text-teal-500 ml-2 text-xs">at {lastScanned}</span>}
        </div>
      )}

      {/* Summary bar */}
      {alerts.length > 0 && (
        <div className="flex gap-3">
          {highCount > 0 && <span className="rounded-full bg-red-100 px-3 py-1 text-xs font-semibold text-red-700">{highCount} High</span>}
          {mediumCount > 0 && <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">{mediumCount} Medium</span>}
          {lowCount > 0 && <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">{lowCount} Low</span>}
        </div>
      )}

      {/* Alert list */}
      {loading ? (
        <div className="animate-pulse space-y-3">
          {[1, 2, 3].map(i => <div key={i} className="h-20 rounded-xl bg-gray-100" />)}
        </div>
      ) : alerts.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-xl border border-gray-200 bg-white py-16 text-center">
          <CheckCircle size={32} className="mb-3 text-teal-600" />
          <p className="font-medium text-gray-700">No workflow alerts</p>
          <p className="mt-1 text-sm text-gray-400">Run a scan to check current trial health, or all items are on track.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {alerts.map(alert => {
            const cfg = severityConfig(alert.severity);
            return (
              <div key={alert.id} className={`rounded-xl border p-4 ${cfg.bg}`}>
                <div className="flex items-start gap-3">
                  <span className={`mt-1 h-2.5 w-2.5 rounded-full shrink-0 ${cfg.dot}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-center gap-2 mb-1.5">
                      <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${cfg.badge}`}>
                        {alert.severity.toUpperCase()}
                      </span>
                      <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600 font-medium">
                        {alertTypeIcon(alert.alert_type)}
                        {alert.alert_type.replace("_", " ")}
                      </span>
                      <span className="rounded-full bg-white/70 border border-gray-200 px-2 py-0.5 text-xs text-gray-500">
                        {entityLabel(alert.entity_type)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-800 leading-snug">{alert.message}</p>
                    {alert.created_at && (
                      <p className="mt-1.5 text-xs text-gray-400">
                        {new Date(alert.created_at).toLocaleString()}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
