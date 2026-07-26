from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Agent 1: Company Profile Schemas ---
class RevenueSegmentSchema(BaseModel):
    segment_name: str = Field(..., description="Segment or division name")
    revenue_rs_cr: Optional[str] = Field(default="Not Available")
    growth_yoy_pct: Optional[str] = Field(default="Not Available")
    share_pct: Optional[str] = Field(default="Not Available")

class CompanyProfileSchema(BaseModel):
    company_name: str = Field(default="Target Company Ltd.", description="Full official company name")
    sector: str = Field(default="Diversified", description="Industry or business sector")
    industry: str = Field(default="General Corporate", description="Sub-industry classification")
    business_model: str = Field(default="", description="Detailed description of business model")
    key_products: List[str] = Field(default_factory=list, description="Primary products or services offered")
    geography: str = Field(default="Domestic & International", description="Geographic presence")
    revenue_segments: List[RevenueSegmentSchema] = Field(default_factory=list, description="Breakdown of revenue by segment")

# --- Agent 2: Financial Metrics Schema ---
class KeyFinancialMetricsSchema(BaseModel):
    revenue: str = Field(default="Not Available", description="Total Revenue / Sales (Rs. cr)")
    operating_revenue: str = Field(default="Not Available", description="Operating Revenue (Rs. cr)")
    ebitda: str = Field(default="Not Available", description="EBITDA (Rs. cr)")
    operating_profit: str = Field(default="Not Available", description="Operating Profit (Rs. cr)")
    pat: str = Field(default="Not Available", description="Profit After Tax (Rs. cr)")
    eps: str = Field(default="Not Available", description="Earnings Per Share (Rs.)")
    book_value: str = Field(default="Not Available", description="Book Value per share (Rs.)")
    net_worth: str = Field(default="Not Available", description="Net Worth / Shareholder Funds (Rs. cr)")
    debt: str = Field(default="Not Available", description="Total Debt (Rs. cr)")
    cash: str = Field(default="Not Available", description="Cash & Cash Equivalents (Rs. cr)")
    operating_margin_pct: str = Field(default="Not Available", description="Operating Margin %")
    ebitda_margin_pct: str = Field(default="Not Available", description="EBITDA Margin %")
    pat_margin_pct: str = Field(default="Not Available", description="PAT Margin %")
    roe_pct: str = Field(default="Not Available", description="Return on Equity %")
    roa_pct: str = Field(default="Not Available", description="Return on Assets %")
    roce_pct: str = Field(default="Not Available", description="Return on Capital Employed %")
    # Banking / Financial Services specific metrics
    casa_ratio_pct: Optional[str] = Field(default="Not Available", description="CASA Ratio % (Banking)")
    gnpa_pct: Optional[str] = Field(default="Not Available", description="Gross NPA % (Banking)")
    nnpa_pct: Optional[str] = Field(default="Not Available", description="Net NPA % (Banking)")
    loan_growth_pct: Optional[str] = Field(default="Not Available", description="Loan / Advances Growth %")
    deposit_growth_pct: Optional[str] = Field(default="Not Available", description="Deposit Growth %")
    nim_pct: Optional[str] = Field(default="Not Available", description="Net Interest Margin %")
    capital_adequacy_pct: Optional[str] = Field(default="Not Available", description="Capital Adequacy Ratio (CAR) %")

# --- Header & Snapshot Tables ---
class CompanyDataSchema(BaseModel):
    market_cap_rs_cr: Optional[str] = Field(default="Not Available", description="Market Cap in Rs. cr")
    high_low_52wk: Optional[str] = Field(default="Not Available", description="52 Week High - Low in Rs.")
    enterprise_value_rs_cr: Optional[str] = Field(default="Not Available", description="Enterprise Value in Rs. cr")
    outstanding_shares_cr: Optional[str] = Field(default="Not Available", description="Outstanding Shares in cr")
    free_float_pct: Optional[str] = Field(default="Not Available", description="Free Float %")
    dividend_yield_pct: Optional[str] = Field(default="Not Available", description="Dividend Yield %")
    avg_volume_6m_cr: Optional[str] = Field(default="Not Available", description="6 Month average volume in cr")
    beta: Optional[str] = Field(default="Not Available", description="Beta")
    face_value_rs: Optional[str] = Field(default="Not Available", description="Face Value in Rs.")

class ShareholdingRowSchema(BaseModel):
    category: str = Field(..., description="Category (Promoters, FIIs, MFs/Institutions, Public, Others, Total)")
    q3: Optional[str] = Field(default="-")
    q4: Optional[str] = Field(default="-")
    q1: Optional[str] = Field(default="-")

class PricePerformanceRowSchema(BaseModel):
    period: str = Field(..., description="Metric name (Absolute Return, Absolute Sensex, Relative Return)")
    m3: Optional[str] = Field(default="-")
    m6: Optional[str] = Field(default="-")
    y1: Optional[str] = Field(default="-")

# --- Agent 3: Quarterly Performance Schemas ---
class QuarterlyFinancialRowSchema(BaseModel):
    metric: str = Field(..., description="Financial metric name (Sales, EBITDA, Margin %, EBIT, PBT, Rep PAT, Adj PAT, Adj EPS)")
    q1_current: Optional[str] = Field(default="-")
    q1_previous: Optional[str] = Field(default="-")
    yoy_growth_pct: Optional[str] = Field(default="-")
    q4_previous: Optional[str] = Field(default="-")
    qoq_growth_pct: Optional[str] = Field(default="-")

class QuarterlyAnalysisSchema(BaseModel):
    revenue_analysis: str = Field(default="", description="Detailed revenue trend analysis")
    profitability_analysis: str = Field(default="", description="Detailed profit and margin trend analysis")
    operational_highlights: List[str] = Field(default_factory=list, description="Key operational milestones and volume metrics")
    management_commentary: str = Field(default="", description="Management transcript & call highlights")
    quarterly_table: List[QuarterlyFinancialRowSchema] = Field(default_factory=list)

# --- Agent 4: Investment Thesis Schemas ---
class InvestmentThesisItemSchema(BaseModel):
    title: str = Field(..., description="Core thesis point header")
    description: str = Field(..., description="Detailed explanation of rationale")
    evidence: str = Field(..., description="Concrete data point or fact extracted from doc supporting thesis")

class InvestmentThesisSchema(BaseModel):
    summary_headline: str = Field(default="", description="Overall investment thesis summary")
    thesis_points: List[InvestmentThesisItemSchema] = Field(default_factory=list, description="5-8 detailed investment points")

# --- Agent 5: Risk Analysis Schemas ---
class RiskItemSchema(BaseModel):
    category: str = Field(..., description="Risk category: Business, Financial, Industry, Regulatory, or Execution")
    risk_title: str = Field(..., description="Brief title of risk")
    description: str = Field(..., description="Explanation of impact and potential downside")
    severity: str = Field(default="Medium", description="High, Medium, or Low")

class RiskAnalysisSchema(BaseModel):
    overall_risk_profile: str = Field(default="Moderate", description="Overall risk assessment")
    risks: List[RiskItemSchema] = Field(default_factory=list, description="Ranked risk list")

# --- Agent 6: Future Outlook Schemas ---
class FutureOutlookSchema(BaseModel):
    guidance_summary: str = Field(default="", description="Management revenue and profit guidance")
    growth_drivers: List[str] = Field(default_factory=list, description="Key secular and strategic growth drivers")
    expansion_plans: str = Field(default="", description="Capex, store additions, or capacity expansion plans")
    long_term_vision: str = Field(default="", description="3-5 year corporate trajectory")

# --- Agent 7: Financial Statements & Tables ---
class FinancialStatementRowSchema(BaseModel):
    line_item: str = Field(..., description="Line item description")
    fy1: Optional[str] = Field(default="-")
    fy2: Optional[str] = Field(default="-")
    fy3: Optional[str] = Field(default="-")
    fy4_est: Optional[str] = Field(default="-")
    fy5_est: Optional[str] = Field(default="-")

class YearlyFinancialsSchema(BaseModel):
    years: List[str] = Field(default_factory=lambda: ["FY23A", "FY24A", "FY25A", "FY26E", "FY27E"])
    profit_and_loss: List[FinancialStatementRowSchema] = Field(default_factory=list)
    balance_sheet: List[FinancialStatementRowSchema] = Field(default_factory=list)
    cashflow: List[FinancialStatementRowSchema] = Field(default_factory=list)
    ratios: List[FinancialStatementRowSchema] = Field(default_factory=list)

class EstimateChangeRowSchema(BaseModel):
    metric: str = Field(..., description="Metric name (Revenue, EBITDA, Margins %, Adj PAT, EPS)")
    old_fy1: Optional[str] = Field(default="-")
    old_fy2: Optional[str] = Field(default="-")
    new_fy1: Optional[str] = Field(default="-")
    new_fy2: Optional[str] = Field(default="-")
    change_fy1_pct: Optional[str] = Field(default="-")
    change_fy2_pct: Optional[str] = Field(default="-")

# --- SWOT Schema ---
class SWOTSchema(BaseModel):
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    threats: List[str] = Field(default_factory=list)

# --- Agent 8: Charts Schemas ---
class ChartSeriesSchema(BaseModel):
    title: str
    periods: List[str] = Field(default_factory=list)
    bars: List[float] = Field(default_factory=list)
    lines: List[float] = Field(default_factory=list)

class ReportChartsSchema(BaseModel):
    revenue_trend: Optional[ChartSeriesSchema] = None
    gross_order_value: Optional[ChartSeriesSchema] = None
    ebitda_trend: Optional[ChartSeriesSchema] = None
    pat_trend: Optional[ChartSeriesSchema] = None

# --- Unified Master Financial Report JSON Schema ---
class FinancialReportJSONSchema(BaseModel):
    company_name: str = Field(default="Target Company Ltd.", description="Full official company name")
    sector: str = Field(default="Internet & Catalogue Retail", description="Industry or business sector")
    recommendation: str = Field(default="HOLD", description="BUY, ACCUMULATE, HOLD, REDUCE, or SELL")
    target_price: str = Field(default="Rs. 337", description="Target price with currency")
    cmp: str = Field(default="Rs. 306", description="Current market price with currency")
    return_pct: str = Field(default="+10%", description="Expected return percentage")
    report_date: str = Field(default="29th July, 2025", description="Date of research report release")
    analyst_name: str = Field(default="Gopika Gopan", description="Research Analyst Name")
    
    # Metadata Header
    stock_type: str = Field(default="Large Cap", description="Large Cap, Mid Cap, or Small Cap")
    bloomberg_code: str = Field(default="ETERNAL:IN", description="Ticker symbol on Bloomberg")
    sensex: str = Field(default="81,334", description="Benchmark Sensex level")
    nse_code: str = Field(default="ETERNAL", description="NSE Trading symbol")
    bse_code: str = Field(default="543320", description="BSE Scrip code")
    time_frame: str = Field(default="12 Months", description="Investment horizon")
    
    # Company Snapshot & Company Data
    company_data: CompanyDataSchema = Field(default_factory=CompanyDataSchema)
    shareholding: List[ShareholdingRowSchema] = Field(default_factory=list)
    price_performance: List[PricePerformanceRowSchema] = Field(default_factory=list)
    
    # Agent 1: Company Profile & Business Overview
    company_profile: CompanyProfileSchema = Field(default_factory=CompanyProfileSchema)
    business_overview: str = Field(default="", description="Detailed narrative on business model, segments, and operations")
    
    # Agent 2: Metrics Summary
    key_metrics: KeyFinancialMetricsSchema = Field(default_factory=KeyFinancialMetricsSchema)
    
    # Agent 3: Quarterly Performance & Analysis
    headline_highlight: str = Field(default="Strong revenue growth; valuation limits upside", description="Main catchy report headline")
    key_highlights: List[str] = Field(default_factory=list, description="Bullet points summarizing financial and operational performance")
    quarterly_analysis: QuarterlyAnalysisSchema = Field(default_factory=QuarterlyAnalysisSchema)
    quarterly_financials: List[QuarterlyFinancialRowSchema] = Field(default_factory=list)
    
    # Agent 4: Investment Thesis
    investment_thesis: InvestmentThesisSchema = Field(default_factory=InvestmentThesisSchema)
    investment_thesis_narrative: str = Field(default="", description="Unified text of investment rationale")
    
    # Agent 5: Categorized Risks & SWOT
    risks_analysis: RiskAnalysisSchema = Field(default_factory=RiskAnalysisSchema)
    risks: List[str] = Field(default_factory=list, description="Flattened risk list for compatibility")
    swot: SWOTSchema = Field(default_factory=SWOTSchema)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    
    # Agent 6: Future Outlook & Valuation
    outlook_data: FutureOutlookSchema = Field(default_factory=FutureOutlookSchema)
    outlook: str = Field(default="", description="Industry and company growth outlook narrative")
    valuation: str = Field(default="", description="Detailed valuation method and target price calculation explanation")
    
    # Agent 7: Financial Statements & Estimates
    yearly_financials: YearlyFinancialsSchema = Field(default_factory=YearlyFinancialsSchema)
    change_in_estimates: List[EstimateChangeRowSchema] = Field(default_factory=list)
    
    # Agent 8: Charts Input Data
    chart_data: ReportChartsSchema = Field(default_factory=ReportChartsSchema)

