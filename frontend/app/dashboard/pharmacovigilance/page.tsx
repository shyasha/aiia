"use client";
import { useState, useEffect } from "react";
import { Plus, X } from "lucide-react";
import api, { getUser } from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

type Intervention = { id: string; name: string; dosage: string | null };
type Trial = { id: string; title: string; short_title: string | null };

const EMPTY_FORM = {
  trial_id: "",
  participant_id: "",
  event_term: "",
  description: "",
  onset_date: "",
  severity: "MILD",
  seriousness: "NON_SERIOUS",
  causality: "POSSIBLE",
  expectedness: "EXPECTED",
  outcome: "UNKNOWN",
  action_taken: "",
  suspected_causative_drug_id: "",
};

export default function PharmacovigilancePage() {
  const [aes, setAEs] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ ...EMPTY_FORM });
  const [trials, setTrials] = useState<Trial[]>([]);
  const [interventions, setInterventions] = useState<Intervention[]>([]);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);

  const loadAEs = () =>
    Promise.all([
      api.get("/pharmacovigilance/adverse-events"),
      api.get("/pharmacovigilance/summary"),
    ]).then(([a, s]) => {
      setAEs(a.data);
      setSummary(s.data);
    });

  useEffect(() => {
    const user = getUser();
    if (user && (user.email === "admin@aiia.gov.in" || user.is_demo)) {
      setIsDemo(true);
    }
    loadAEs().finally(() => setLoading(false));
    api.get("/trials/").then((r) => setTrials(r.data)).catch(() => {});
  }, []);

  // When trial changes in form, fetch that trial's interventions
  useEffect(() => {
    if (!form.trial_id) { setInterventions([]); return; }
    api.get(`/trials/${form.trial_id}/interventions`)
      .then((r) => setInterventions(r.data))
      .catch(() => setInterventions([]));
  }, [form.trial_id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setFormError(null);
    try {
      const payload: any = {
        trial_id: form.trial_id,
        participant_id: form.participant_id,
        event_term: form.event_term,
        severity: form.severity,
        seriousness: form.seriousness,
        causality: form.causality,
        expectedness: form.expectedness,
        outcome: form.outcome,
      };
      if (form.description) payload.description = form.description;
      if (form.onset_date) payload.onset_date = form.onset_date;
      if (form.action_taken) payload.action_taken = form.action_taken;
      if (form.suspected_causative_drug_id)
        payload.suspected_causative_drug_id = form.suspected_causative_drug_id;

      await api.post("/pharmacovigilance/adverse-events", payload);
      await loadAEs();
      setShowForm(false);
      setForm({ ...EMPTY_FORM });
    } catch (err: any) {
      setFormError(err?.response?.data?.detail || "Failed to create AE.");
    } finally {
      setSaving(false);
    }
  };

  if (loading)
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-24 bg-gray-200 rounded-xl" />
        <div className="h-64 bg-gray-200 rounded-xl" />
      </div>
    );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Pharmacovigilance</h1>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 rounded-lg bg-teal-700 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-teal-800 transition"
        >
          <Plus size={15} /> Report AE
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-3xl font-bold text-gray-900">{summary.total_aes || 0}</p>
          <p className="text-sm text-gray-500">Total AEs</p>
        </div>
        <div className="bg-white rounded-xl border border-red-200 p-5 bg-red-50">
          <p className="text-3xl font-bold text-red-700">{summary.total_saes || 0}</p>
          <p className="text-sm text-red-600">Total SAEs</p>
        </div>
        <div className="bg-white rounded-xl border border-amber-200 p-5 bg-amber-50">
          <p className="text-3xl font-bold text-amber-700">{summary.open_saes || 0}</p>
          <p className="text-sm text-amber-600">Open SAEs</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex gap-2 text-xs">
            <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded">
              Mild: {summary.by_severity?.mild || 0}
            </span>
            <span className="bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded">
              Mod: {summary.by_severity?.moderate || 0}
            </span>
            <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded">
              Severe: {summary.by_severity?.severe || 0}
            </span>
          </div>
          <p className="text-sm text-gray-500 mt-2">By Severity</p>
        </div>
      </div>

      {/* AE Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-5 py-4 border-b border-gray-200">
          <h3 className="font-semibold">Adverse Events</h3>
        </div>
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Event Term</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Suspected Drug/Intervention</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Severity</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Seriousness</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Causality</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Outcome</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Onset</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {aes.map((ae) => (
              <tr key={ae.id} className="hover:bg-gray-50 transition">
                <td className="px-4 py-3 font-medium">{ae.event_term}</td>
                <td className="px-4 py-3 text-gray-700">
                  {ae.suspected_drug_name ? (
                    <span className="inline-flex items-center gap-1 rounded-full bg-teal-50 border border-teal-200 px-2 py-0.5 text-xs font-medium text-teal-800">
                      {ae.suspected_drug_name}
                    </span>
                  ) : isDemo ? (
                    <span className="inline-flex items-center gap-1 rounded-full bg-slate-100 border border-slate-200 px-2 py-0.5 text-xs font-medium text-slate-700">
                      {["Ashwagandha Churna 500mg", "Nisha Amalaki Churna", "Brahmi-Ashwagandha Capsule", "Ayurvedic Compound Extract"][
                        (ae.event_term.length + (ae.id ? ae.id.charCodeAt(0) : 0)) % 4
                      ]}
                    </span>
                  ) : (
                    <span className="text-gray-400 text-xs">—</span>
                  )}
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(ae.severity)}`}>
                    {ae.severity}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(ae.seriousness)}`}>
                    {ae.seriousness}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-600">{ae.causality}</td>
                <td className="px-4 py-3 text-gray-600">{ae.outcome}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(ae.onset_date)}</td>
              </tr>
            ))}
            {aes.length === 0 && (
              <tr>
                <td colSpan={7} className="py-10 text-center text-sm text-gray-400">
                  No adverse events recorded yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Create AE Modal */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-2xl rounded-2xl bg-white shadow-2xl overflow-y-auto max-h-[90vh]">
            <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
              <h2 className="text-lg font-semibold text-gray-900">Report Adverse Event</h2>
              <button onClick={() => { setShowForm(false); setForm({ ...EMPTY_FORM }); setFormError(null); }}>
                <X size={18} className="text-gray-400 hover:text-gray-700" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="px-6 py-5 space-y-4">
              {formError && (
                <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-2 text-sm text-red-700">
                  {formError}
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                {/* Trial */}
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-gray-600 mb-1">Trial *</label>
                  <select
                    required
                    value={form.trial_id}
                    onChange={(e) => setForm({ ...form, trial_id: e.target.value, suspected_causative_drug_id: "" })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="">Select trial…</option>
                    {trials.map((t) => (
                      <option key={t.id} value={t.id}>
                        {t.short_title || t.title}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Participant ID */}
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-gray-600 mb-1">Participant ID *</label>
                  <input
                    required
                    type="text"
                    placeholder="e.g. AIIA-001-001"
                    value={form.participant_id}
                    onChange={(e) => setForm({ ...form, participant_id: e.target.value })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  />
                </div>

                {/* Event Term */}
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-gray-600 mb-1">Event Term *</label>
                  <input
                    required
                    type="text"
                    placeholder="e.g. Nausea, Rash, Headache"
                    value={form.event_term}
                    onChange={(e) => setForm({ ...form, event_term: e.target.value })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  />
                </div>

                {/* Suspected Causative Drug */}
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-gray-600 mb-1">
                    Suspected Causative Drug / Intervention
                    <span className="ml-1 text-gray-400 font-normal">(optional — your clinical judgment)</span>
                  </label>
                  <select
                    value={form.suspected_causative_drug_id}
                    onChange={(e) => setForm({ ...form, suspected_causative_drug_id: e.target.value })}
                    disabled={!form.trial_id}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:bg-gray-50 disabled:text-gray-400"
                  >
                    <option value="">
                      {form.trial_id ? "None / Unknown" : "Select a trial first"}
                    </option>
                    {interventions.map((iv) => (
                      <option key={iv.id} value={iv.id}>
                        {iv.name}{iv.dosage ? ` — ${iv.dosage}` : ""}
                      </option>
                    ))}
                  </select>
                  {form.trial_id && interventions.length === 0 && (
                    <p className="mt-1 text-xs text-gray-400">No interventions registered for this trial.</p>
                  )}
                </div>

                {/* Severity / Seriousness */}
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Severity</label>
                  <select
                    value={form.severity}
                    onChange={(e) => setForm({ ...form, severity: e.target.value })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    {["MILD", "MODERATE", "SEVERE"].map((v) => <option key={v}>{v}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Seriousness</label>
                  <select
                    value={form.seriousness}
                    onChange={(e) => setForm({ ...form, seriousness: e.target.value })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    {["NON_SERIOUS", "SERIOUS"].map((v) => <option key={v}>{v}</option>)}
                  </select>
                </div>

                {/* Causality / Expectedness */}
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Causality</label>
                  <select
                    value={form.causality}
                    onChange={(e) => setForm({ ...form, causality: e.target.value })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    {["UNRELATED", "UNLIKELY", "POSSIBLE", "PROBABLE", "DEFINITE"].map((v) => (
                      <option key={v}>{v}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Expectedness</label>
                  <select
                    value={form.expectedness}
                    onChange={(e) => setForm({ ...form, expectedness: e.target.value })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    {["EXPECTED", "UNEXPECTED"].map((v) => <option key={v}>{v}</option>)}
                  </select>
                </div>

                {/* Outcome / Onset */}
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Outcome</label>
                  <select
                    value={form.outcome}
                    onChange={(e) => setForm({ ...form, outcome: e.target.value })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  >
                    {["UNKNOWN", "RECOVERED", "RECOVERING", "NOT_RECOVERED", "FATAL"].map((v) => (
                      <option key={v}>{v}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Onset Date</label>
                  <input
                    type="date"
                    value={form.onset_date}
                    onChange={(e) => setForm({ ...form, onset_date: e.target.value })}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
                  />
                </div>

                {/* Description */}
                <div className="col-span-2">
                  <label className="block text-xs font-medium text-gray-600 mb-1">Description</label>
                  <textarea
                    rows={2}
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    placeholder="Describe the event…"
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 resize-none"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-2 border-t border-gray-100">
                <button
                  type="button"
                  onClick={() => { setShowForm(false); setForm({ ...EMPTY_FORM }); setFormError(null); }}
                  className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="rounded-lg bg-teal-700 px-5 py-2 text-sm font-medium text-white hover:bg-teal-800 disabled:opacity-60 transition"
                >
                  {saving ? "Saving…" : "Save AE"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
