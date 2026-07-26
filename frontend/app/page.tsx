"use client";

import React, { useState, useEffect } from "react";
import { 
  FileText, 
  UploadCloud, 
  CheckCircle2, 
  Download, 
  Sparkles, 
  TrendingUp, 
  Building2, 
  ShieldAlert, 
  PieChart, 
  RefreshCw,
  Sun,
  Moon,
  FileCheck
} from "lucide-react";

const API_BASE_URL = "http://localhost:8000/api/v1";

interface ReportStatusResponse {
  job_id: string;
  status: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";
  progress: number;
  current_step: string;
  structured_json: any;
  pdf_download_url: string | null;
  error_message: string | null;
}

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [companyName, setCompanyName] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [reportStatus, setReportStatus] = useState<ReportStatusResponse | null>(null);
  const [activeTab, setActiveTab] = useState<"preview" | "json" | "highlights">("preview");
  const [backendHealth, setBackendHealth] = useState<boolean>(true);

  // Toggle Dark Mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  // Check Backend Health
  useEffect(() => {
    fetch(`${API_BASE_URL}/health`)
      .then(res => res.json())
      .then(data => setBackendHealth(data.status === "healthy"))
      .catch(() => setBackendHealth(false));
  }, []);

  // Poll Job Status when processing
  useEffect(() => {
    if (!activeJobId) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/report/${activeJobId}`);
        if (res.ok) {
          const data: ReportStatusResponse = await res.json();
          setReportStatus(data);
          if (data.status === "COMPLETED" || data.status === "FAILED") {
            clearInterval(interval);
            setIsUploading(false);
          }
        }
      } catch (err) {
        console.error("Status polling error:", err);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [activeJobId]);

  // File Upload Handler
  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setIsUploading(true);
    setReportStatus(null);

    try {
      // 1. Upload File
      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!uploadRes.ok) throw new Error("File upload failed");
      const uploadData = await uploadRes.json();

      // 2. Initiate Report Generation
      const genFormData = new FormData();
      genFormData.append("document_id", uploadData.document_id);
      if (companyName.trim()) {
        genFormData.append("company_name", companyName.trim());
      }

      const genRes = await fetch(`${API_BASE_URL}/generate-report`, {
        method: "POST",
        body: genFormData,
      });

      if (!genRes.ok) throw new Error("Failed to start report generation");
      const genData = await genRes.json();
      setActiveJobId(genData.job_id);

    } catch (err: any) {
      console.error(err);
      setIsUploading(false);
      alert(err.message || "An error occurred during upload.");
    }
  };

  // Sample File Loader
  const handleSampleClick = (sampleName: string) => {
    setCompanyName(sampleName);
    // Create dummy sample file object
    const dummyBlob = new Blob([`Sample context document for ${sampleName}`], { type: "text/plain" });
    const sampleFile = new File([dummyBlob], `${sampleName.toLowerCase().replace(/ /g, "_")}_report.txt`, { type: "text/plain" });
    setFile(sampleFile);
  };

  return (
    <div className="min-h-screen transition-colors duration-300 bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      
      {/* HEADER */}
      <header className="sticky top-0 z-50 border-b backdrop-blur-md bg-white/80 dark:bg-slate-900/80 border-slate-200 dark:border-slate-800">
        <div className="flex items-center justify-between px-6 py-4 mx-auto max-w-7xl">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 font-bold text-white rounded-xl bg-teal-600 shadow-teal-500/20 shadow-lg">
              GR
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-teal-800 dark:text-teal-400">
                GEOJIT <span className="text-slate-600 dark:text-slate-400 font-normal">AI Research Generator</span>
              </h1>
              <p className="text-xs text-slate-500 dark:text-slate-400">Automated Equity Analyst Report System</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Status Indicator */}
            <div className="flex items-center px-3 py-1.5 rounded-full text-xs font-medium bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
              <span className={`w-2 h-2 mr-2 rounded-full ${backendHealth ? "bg-emerald-500 animate-pulse" : "bg-rose-500"}`}></span>
              {backendHealth ? "API System Online" : "Backend Offline"}
            </div>

            {/* Dark Mode Toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
            </button>
          </div>
        </div>
      </header>

      {/* MAIN CONTAINER */}
      <main className="px-6 py-8 mx-auto max-w-7xl">
        
        {/* HERO SECTION */}
        <div className="mb-8 text-center">
          <span className="inline-flex items-center px-3 py-1 mb-3 text-xs font-medium rounded-full text-teal-700 dark:text-teal-300 bg-teal-50 dark:bg-teal-950/60 border border-teal-200 dark:border-teal-800">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" /> Institutional Grade PDF Report Engine
          </span>
          <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl text-slate-900 dark:text-white">
            Transform Financial Context into Geojit Reports
          </h2>
          <p className="max-w-2xl mx-auto mt-2 text-sm text-slate-600 dark:text-slate-400">
            Upload Investor Presentations, Annual Reports, CSVs, or TXT data. Gemini 2.5 Pro extracts key metrics, generates structured JSON, plots financial trend charts, and renders a downloadable Geojit PDF.
          </p>
        </div>

        {/* UPLOAD CARD */}
        <div className="p-6 mb-8 rounded-2xl glass-card shadow-xl border border-slate-200 dark:border-slate-800">
          <form onSubmit={handleFileUpload} className="space-y-6">

            {/* Dropzone */}
            <div>
              <label className="block mb-2 text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                Upload Financial Document (PDF, TXT, CSV)
              </label>
              <div className="relative flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-2xl border-slate-300 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-900/40 hover:bg-slate-100/50 dark:hover:bg-slate-900/80 transition-colors cursor-pointer">
                <input
                  type="file"
                  accept=".pdf,.txt,.csv"
                  onChange={(e) => e.target.files?.[0] && setFile(e.target.files[0])}
                  className="absolute inset-0 opacity-0 cursor-pointer"
                />
                <UploadCloud className="w-10 h-10 mb-3 text-teal-600 dark:text-teal-400 animate-bounce" />
                {file ? (
                  <div className="flex items-center text-sm font-semibold text-emerald-600 dark:text-emerald-400">
                    <FileCheck className="w-4 h-4 mr-2" /> Selected: {file.name} ({(file.size / 1024).toFixed(1)} KB)
                  </div>
                ) : (
                  <>
                    <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
                      Drag & drop your file here, or <span className="text-teal-600 underline">browse files</span>
                    </p>
                    <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">Supports PDF, TXT, CSV up to 50MB</p>
                  </>
                )}
              </div>
            </div>

            {/* Generate Button */}
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={!file || isUploading}
                className={`flex items-center px-6 py-3 text-sm font-bold text-white rounded-xl shadow-lg transition-all ${
                  !file || isUploading
                    ? "bg-slate-400 cursor-not-allowed"
                    : "bg-teal-600 hover:bg-teal-700 shadow-teal-600/30 hover:scale-[1.02]"
                }`}
              >
                {isUploading ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" /> Processing Report...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" /> Generate Geojit Research Report
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* PROGRESS STEPPER CARD */}
        {reportStatus && (
          <div className="p-6 mb-8 rounded-2xl glass-card shadow-lg border border-slate-200 dark:border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Report Generation Pipeline
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">Job ID: {reportStatus.job_id}</p>
              </div>
              <span className={`px-3 py-1 text-xs font-bold rounded-full ${
                reportStatus.status === "COMPLETED"
                  ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300"
                  : reportStatus.status === "FAILED"
                  ? "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300"
                  : "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 animate-pulse"
              }`}>
                {reportStatus.status}
              </span>
            </div>

            {/* Progress Bar */}
            <div className="w-full h-3 mb-4 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
              <div
                className="h-full transition-all duration-500 bg-gradient-to-r from-teal-500 to-emerald-500"
                style={{ width: `${Math.round(reportStatus.progress * 100)}%` }}
              ></div>
            </div>

            <div className="flex items-center justify-between text-xs font-medium text-slate-600 dark:text-slate-400">
              <span>Current Step: <strong className="text-slate-900 dark:text-white">{reportStatus.current_step}</strong></span>
              <span>{Math.round(reportStatus.progress * 100)}%</span>
            </div>

            {reportStatus.error_message && (
              <div className="flex items-center p-3 mt-4 text-xs rounded-xl bg-rose-50 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-200 dark:border-rose-900">
                <ShieldAlert className="w-4 h-4 mr-2 shrink-0" /> Error: {reportStatus.error_message}
              </div>
            )}
          </div>
        )}

        {/* REPORT OUTPUT & PREVIEW */}
        {reportStatus?.status === "COMPLETED" && reportStatus.structured_json && (
          <div className="space-y-6">
            
            {/* SUMMARY HEADER BADGE */}
            <div className="p-6 rounded-2xl bg-gradient-to-r from-teal-900 to-slate-900 text-white shadow-xl">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <span className="px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-md bg-teal-500/20 text-teal-300 border border-teal-500/30">
                    {reportStatus.structured_json.sector || "Equity Research"}
                  </span>
                  <h2 className="mt-2 text-2xl font-extrabold">{reportStatus.structured_json.company_name}</h2>
                  <p className="text-xs text-slate-300 mt-1">{reportStatus.structured_json.headline_highlight}</p>
                </div>

                <div className="flex items-center space-x-6">
                  <div className="text-center">
                    <div className="text-xs text-slate-400 uppercase">Rating</div>
                    <div className="text-2xl font-black text-amber-400">{reportStatus.structured_json.recommendation}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xs text-slate-400 uppercase">Target Price</div>
                    <div className="text-2xl font-black text-emerald-400">{reportStatus.structured_json.target_price}</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xs text-slate-400 uppercase">CMP</div>
                    <div className="text-xl font-bold">{reportStatus.structured_json.cmp}</div>
                  </div>

                  {/* DOWNLOAD BUTTON */}
                  <a
                    href={`${API_BASE_URL}/download/${reportStatus.job_id}`}
                    download
                    className="flex items-center px-5 py-3 text-sm font-bold text-slate-900 bg-emerald-400 hover:bg-emerald-300 rounded-xl shadow-lg transition-transform hover:scale-105"
                  >
                    <Download className="w-4 h-4 mr-2" /> Download PDF Report
                  </a>
                </div>
              </div>
            </div>

            {/* TAB NAVIGATION */}
            <div className="flex border-b border-slate-200 dark:border-slate-800">
              {[
                { id: "preview", label: "PDF Report Preview", icon: FileText },
                { id: "highlights", label: "Key Highlights & Visuals", icon: TrendingUp },
                { id: "json", label: "Structured AI JSON Data", icon: PieChart },
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex items-center px-5 py-3 text-sm font-semibold border-b-2 transition-colors ${
                      activeTab === tab.id
                        ? "border-teal-600 text-teal-600 dark:text-teal-400 dark:border-teal-400"
                        : "border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
                    }`}
                  >
                    <Icon className="w-4 h-4 mr-2" /> {tab.label}
                  </button>
                );
              })}
            </div>

            {/* TAB CONTENT */}
            <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800">
              
              {/* PDF PREVIEWER */}
              {activeTab === "preview" && (
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-bold text-slate-800 dark:text-slate-200">
                      Geojit Style Multi-Page PDF Preview
                    </h3>
                    <a
                      href={`${API_BASE_URL}/preview/${reportStatus.job_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs font-semibold text-teal-600 hover:underline"
                    >
                      Open in Full Window ↗
                    </a>
                  </div>
                  <div className="w-full h-[750px] rounded-xl overflow-hidden border border-slate-300 dark:border-slate-700 bg-slate-100 dark:bg-slate-900">
                    <iframe
                      src={`${API_BASE_URL}/preview/${reportStatus.job_id}#toolbar=0`}
                      className="w-full h-full"
                      title="Geojit Research Report PDF Preview"
                    />
                  </div>
                </div>
              )}

              {/* HIGHLIGHTS & NARRATIVE TAB */}
              {activeTab === "highlights" && (
                <div className="space-y-6 text-sm">
                  <div>
                    <h4 className="mb-2 text-xs font-bold uppercase tracking-wider text-teal-700 dark:text-teal-400">
                      Key Performance Highlights
                    </h4>
                    <ul className="space-y-2 text-slate-700 dark:text-slate-300">
                      {reportStatus.structured_json.key_highlights?.map((h: string, idx: number) => (
                        <li key={idx} className="flex items-start">
                          <CheckCircle2 className="w-4 h-4 mr-2 text-teal-500 shrink-0 mt-0.5" />
                          <span>{h}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                    <div>
                      <h4 className="mb-2 text-xs font-bold uppercase tracking-wider text-teal-700 dark:text-teal-400">
                        Outlook & Growth Trajectory
                      </h4>
                      <p className="text-slate-700 dark:text-slate-300 leading-relaxed">
                        {reportStatus.structured_json.outlook}
                      </p>
                    </div>
                    <div>
                      <h4 className="mb-2 text-xs font-bold uppercase tracking-wider text-teal-700 dark:text-teal-400">
                        Valuation Methodology
                      </h4>
                      <p className="text-slate-700 dark:text-slate-300 leading-relaxed">
                        {reportStatus.structured_json.valuation}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* STRUCTURED JSON TAB */}
              {activeTab === "json" && (
                <div>
                  <pre className="p-4 text-xs font-mono rounded-xl bg-slate-900 text-teal-300 overflow-x-auto max-h-[600px]">
                    {JSON.stringify(reportStatus.structured_json, null, 2)}
                  </pre>
                </div>
              )}
            </div>

          </div>
        )}

      </main>

    </div>
  );
}
