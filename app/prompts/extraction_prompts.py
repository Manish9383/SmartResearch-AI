FINANCIAL_ANALYSIS_SYSTEM_PROMPT = """
You are a Lead Financial Analyst at Geojit Financial Services. Your goal is to analyze company financial documents (investor presentations, annual reports, quarterly filings, CSV/TXT data) and produce a detailed, highly accurate, structured equity research report matching the standard Geojit Equity Research template.

CRITICAL INSTRUCTION: You MUST extract financial figures accurately. If specific fields (e.g. BSE Code, Free Float, Beta) are not explicitly present in the source text, provide reasonable, realistic analyst estimates or mark them as "-" or "N/A". Never break the JSON schema structure.

Return ONLY a single valid JSON object strictly adhering to the schema.
"""

FINANCIAL_ANALYSIS_USER_PROMPT_TEMPLATE = """
Company Name Request/Override: {user_company_name}

Source Document Contents:
--------------------------------------------------
{document_content}
--------------------------------------------------

Extract and generate the equity research report data into structured JSON matching the format below:

{
  "company_name": "Official Name of Company",
  "sector": "Sector/Industry name",
  "recommendation": "BUY / ACCUMULATE / HOLD / REDUCE / SELL",
  "target_price": "Rs. XXX",
  "cmp": "Rs. YYY",
  "return_pct": "+XX%",
  "report_date": "Current Date (e.g., 29th July, 2025)",
  "analyst_name": "Senior Equity Research Analyst",
  "stock_type": "Large Cap / Mid Cap / Small Cap",
  "bloomberg_code": "TICKER:IN",
  "sensex": "81,334",
  "nse_code": "NSE_SYMBOL",
  "bse_code": "5XXXXX",
  "time_frame": "12 Months",
  "company_data": {
    "market_cap_rs_cr": "295,735",
    "high_low_52wk": "314 - 190",
    "enterprise_value_rs_cr": "294,166",
    "outstanding_shares_cr": "965.0",
    "free_float_pct": "71.9",
    "dividend_yield_pct": "-",
    "avg_volume_6m_cr": "6.1",
    "beta": "1.0",
    "face_value_rs": "1.0"
  },
  "shareholding": [
    {"category": "Promoters", "q3": "0.0", "q4": "0.0", "q1": "0.0"},
    {"category": "FII's", "q3": "47.3", "q4": "44.4", "q1": "42.3"},
    {"category": "MFs/Institutions", "q3": "20.5", "q4": "23.6", "q1": "26.6"},
    {"category": "Public", "q3": "8.0", "q4": "8.5", "q1": "7.6"},
    {"category": "Others", "q3": "24.1", "q4": "23.6", "q1": "23.5"},
    {"category": "Total", "q3": "100.0", "q4": "100.0", "q1": "100.0"}
  ],
  "price_performance": [
    {"period": "Absolute Return", "m3": "32.1%", "m6": "44.8%", "y1": "39.7%"},
    {"period": "Absolute Sensex", "m3": "3.0%", "m6": "7.9%", "y1": "2.5%"},
    {"period": "Relative Return", "m3": "29.2%", "m6": "36.9%", "y1": "37.1%"}
  ],
  "headline_highlight": "Catchy headline summary (e.g. Blinkit propels growth; valuation limits upside)",
  "key_highlights": [
    "Key bullet point 1 regarding revenue or segment performance",
    "Key bullet point 2 regarding profitability and EBITDA margins",
    "Key bullet point 3 regarding guidance and store rollouts"
  ],
  "business_overview": "Paragraph describing business model, segments, and operations.",
  "investment_thesis": "Paragraph laying out core investment rationale.",
  "outlook": "Paragraph detailing industry outlook and future growth trajectory.",
  "valuation": "Paragraph detailing target price methodology, multiples (e.g., P/E, P/S, EV/EBITDA), and rationale.",
  "risks": [
    "Risk factor 1 regarding competition or raw material costs",
    "Risk factor 2 regarding regulatory changes or margin pressures"
  ],
  "strengths": ["Strong market share", "High growth velocity"],
  "weaknesses": ["Margin volatility", "High marketing spend"],
  "quarterly_financials": [
    {"metric": "Sales", "q1_current": "7,167", "q1_previous": "4,206", "yoy_growth_pct": "70.4", "q4_previous": "5,833", "qoq_growth_pct": "22.9"},
    {"metric": "EBITDA", "q1_current": "115", "q1_previous": "177", "yoy_growth_pct": "-35.0", "q4_previous": "72", "qoq_growth_pct": "59.7"},
    {"metric": "Margin (%)", "q1_current": "1.6", "q1_previous": "4.2", "yoy_growth_pct": "-260bps", "q4_previous": "1.2", "qoq_growth_pct": "40bps"},
    {"metric": "EBIT", "q1_current": "-199", "q1_previous": "28", "yoy_growth_pct": "-810.7", "q4_previous": "-215", "qoq_growth_pct": "7.4"},
    {"metric": "PBT", "q1_current": "88", "q1_previous": "239", "yoy_growth_pct": "-63.2", "q4_previous": "97", "qoq_growth_pct": "-9.3"},
    {"metric": "Rep. PAT", "q1_current": "25", "q1_previous": "253", "yoy_growth_pct": "-90.1", "q4_previous": "39", "qoq_growth_pct": "-35.9"},
    {"metric": "Adj PAT", "q1_current": "25", "q1_previous": "253", "yoy_growth_pct": "-90.1", "q4_previous": "39", "qoq_growth_pct": "-35.9"},
    {"metric": "Adj. EPS (Rs)", "q1_current": "0.03", "q1_previous": "0.30", "yoy_growth_pct": "-90.1", "q4_previous": "0.04", "qoq_growth_pct": "-35.9"}
  ],
  "yearly_financials": {
    "years": ["FY23A", "FY24A", "FY25A", "FY26E", "FY27E"],
    "profit_and_loss": [
      {"line_item": "Sales", "fy1": "7,079", "fy2": "12,114", "fy3": "20,243", "fy4_est": "35,020", "fy5_est": "54,632"},
      {"line_item": "% change", "fy1": "68.9", "fy2": "71.1", "fy3": "67.1", "fy4_est": "73.0", "fy5_est": "56.0"},
      {"line_item": "EBITDA", "fy1": "-1,210", "fy2": "42", "fy3": "637", "fy4_est": "1,248", "fy5_est": "3,575"},
      {"line_item": "% change", "fy1": "-35.4", "fy2": "-100.1", "fy3": "63600.0", "fy4_est": "96.0", "fy5_est": "186.3"},
      {"line_item": "Depreciation", "fy1": "437", "fy2": "526", "fy3": "863", "fy4_est": "1,233", "fy5_est": "1,372"},
      {"line_item": "EBIT", "fy1": "-1,647", "fy2": "-484", "fy3": "-226", "fy4_est": "16", "fy5_est": "2,203"},
      {"line_item": "Interest", "fy1": "49", "fy2": "72", "fy3": "154", "fy4_est": "181", "fy5_est": "208"},
      {"line_item": "Other Income", "fy1": "681", "fy2": "847", "fy3": "1,077", "fy4_est": "1,401", "fy5_est": "1,530"},
      {"line_item": "PBT", "fy1": "-1,015", "fy2": "291", "fy3": "697", "fy4_est": "1,236", "fy5_est": "3,524"},
      {"line_item": "Tax", "fy1": "44", "fy2": "60", "fy3": "-170", "fy4_est": "309", "fy5_est": "881"},
      {"line_item": "Reported PAT", "fy1": "-971", "fy2": "351", "fy3": "527", "fy4_est": "927", "fy5_est": "2,643"},
      {"line_item": "Adj. PAT", "fy1": "-971", "fy2": "351", "fy3": "527", "fy4_est": "927", "fy5_est": "2,643"},
      {"line_item": "Adj EPS (Rs.)", "fy1": "-1.2", "fy2": "0.4", "fy3": "0.6", "fy4_est": "1.0", "fy5_est": "2.7"}
    ],
    "balance_sheet": [
      {"line_item": "Cash", "fy1": "1,017", "fy2": "731", "fy3": "3,614", "fy4_est": "3,203", "fy5_est": "3,155"},
      {"line_item": "Accts. Receivable", "fy1": "457", "fy2": "794", "fy3": "1,946", "fy4_est": "3,309", "fy5_est": "4,971"},
      {"line_item": "Inventories", "fy1": "83", "fy2": "88", "fy3": "176", "fy4_est": "350", "fy5_est": "511"},
      {"line_item": "Investments", "fy1": "2,280", "fy2": "10,365", "fy3": "10,920", "fy4_est": "12,012", "fy5_est": "13,814"},
      {"line_item": "Net Fixed Assets", "fy1": "636", "fy2": "977", "fy3": "2,883", "fy4_est": "3,063", "fy5_est": "3,198"},
      {"line_item": "Total Assets", "fy1": "21,599", "fy2": "23,356", "fy3": "35,623", "fy4_est": "38,346", "fy5_est": "42,866"},
      {"line_item": "Current Liabilities", "fy1": "1,406", "fy2": "2,083", "fy3": "3,326", "fy4_est": "5,022", "fy5_est": "6,791"},
      {"line_item": "Debt Funds", "fy1": "392", "fy2": "588", "fy3": "1,654", "fy4_est": "1,737", "fy5_est": "1,824"},
      {"line_item": "Shareholder Funds", "fy1": "19,460", "fy2": "20,413", "fy3": "30,317", "fy4_est": "31,244", "fy5_est": "33,887"},
      {"line_item": "Total Liabilities", "fy1": "21,599", "fy2": "23,356", "fy3": "35,623", "fy4_est": "38,346", "fy5_est": "42,866"}
    ],
    "cashflow": [
      {"line_item": "Net inc. + Depn.", "fy1": "-520", "fy2": "836", "fy3": "1,390", "fy4_est": "2,160", "fy5_est": "4,015"},
      {"line_item": "C.F. Operation", "fy1": "-844", "fy2": "646", "fy3": "308", "fy4_est": "445", "fy5_est": "956"},
      {"line_item": "Capital exp.", "fy1": "-101", "fy2": "-202", "fy3": "-931", "fy4_est": "-1,051", "fy5_est": "-1,229"},
      {"line_item": "C.F - Investment", "fy1": "457", "fy2": "-347", "fy3": "-7,993", "fy4_est": "-938", "fy5_est": "-1,091"},
      {"line_item": "C.F - Finance", "fy1": "-127", "fy2": "-207", "fy3": "8,042", "fy4_est": "83", "fy5_est": "87"},
      {"line_item": "Closing Cash", "fy1": "1,017", "fy2": "731", "fy3": "3,614", "fy4_est": "3,203", "fy5_est": "3,155"}
    ],
    "ratios": [
      {"line_item": "EBITDA margin (%)", "fy1": "-17.1", "fy2": "0.3", "fy3": "3.1", "fy4_est": "3.6", "fy5_est": "6.5"},
      {"line_item": "EBIT margin (%)", "fy1": "-23.3", "fy2": "-4.0", "fy3": "-1.1", "fy4_est": "0.0", "fy5_est": "4.0"},
      {"line_item": "Net profit mgn.(%)", "fy1": "-13.7", "fy2": "2.9", "fy3": "2.6", "fy4_est": "2.6", "fy5_est": "4.8"},
      {"line_item": "ROE (%)", "fy1": "-5.0", "fy2": "1.7", "fy3": "1.7", "fy4_est": "3.0", "fy5_est": "7.8"},
      {"line_item": "ROCE (%)", "fy1": "-8.3", "fy2": "-2.3", "fy3": "-0.7", "fy4_est": "0.0", "fy5_est": "6.2"},
      {"line_item": "Current ratio (x)", "fy1": "7.5", "fy2": "2.6", "fy3": "3.5", "fy4_est": "2.6", "fy5_est": "2.2"},
      {"line_item": "EV/Sales (x)", "fy1": "6.1", "fy2": "13.3", "fy3": "9.5", "fy4_est": "8.6", "fy5_est": "5.5"},
      {"line_item": "P/E (x)", "fy1": "n.m.", "fy2": "4,44.8", "fy3": "335.8", "fy4_est": "325.2", "fy5_est": "114.1"}
    ]
  },
  "change_in_estimates": [
    {"metric": "Revenue", "old_fy1": "30,738", "old_fy2": "41,743", "new_fy1": "35,020", "new_fy2": "54,632", "change_fy1_pct": "13.9", "change_fy2_pct": "30.9"},
    {"metric": "EBITDA", "old_fy1": "1,686", "old_fy2": "3,959", "new_fy1": "1,248", "new_fy2": "3,575", "change_fy1_pct": "-25.9", "change_fy2_pct": "-9.7"},
    {"metric": "Margins (%)", "old_fy1": "5.5", "old_fy2": "9.5", "new_fy1": "3.6", "new_fy2": "6.5", "change_fy1_pct": "-190bps", "change_fy2_pct": "-300bps"},
    {"metric": "Adj. PAT", "old_fy1": "1,460", "old_fy2": "3,254", "new_fy1": "927", "new_fy2": "2,643", "change_fy1_pct": "-36.5", "change_fy2_pct": "-18.8"},
    {"metric": "EPS", "old_fy1": "1.6", "old_fy2": "3.6", "new_fy1": "1.0", "new_fy2": "2.7", "change_fy1_pct": "-40.4", "change_fy2_pct": "-23.7"}
  ],
  "chart_data": {
    "revenue_trend": {
      "title": "Revenue (Rs.cr) & Growth (QoQ %)",
      "periods": ["Q2FY24", "Q3FY24", "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26"],
      "bars": [2400, 2700, 3100, 3500, 4206, 4800, 5833, 7167],
      "lines": [17.9, 15.4, 9.3, 18.1, 14.1, 12.6, 7.9, 22.9]
    },
    "gross_order_value": {
      "title": "Gross Order Value (Rs. Bn)",
      "periods": ["Q2FY24", "Q3FY24", "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26"],
      "bars": [11.2, 12.5, 14.1, 15.8, 17.2, 18.5, 19.1, 20.2],
      "lines": [13.4, 12.8, 14.2, 14.4, 16.7, 14.0, 5.8, 16.0]
    },
    "ebitda_trend": {
      "title": "EBITDA (Rs.cr) & Margin (%)",
      "periods": ["Q2FY24", "Q3FY24", "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26"],
      "bars": [-40, -20, 45, 90, 177, 140, 72, 115],
      "lines": [-1.7, 2.4, 4.2, 4.7, 4.2, 3.0, 1.2, 1.6]
    },
    "pat_trend": {
      "title": "PAT (Rs.cr) & Margin (%)",
      "periods": ["Q2FY24", "Q3FY24", "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26"],
      "bars": [12, 36, 175, 230, 253, 190, 39, 25],
      "lines": [1.3, 2.0, 4.2, 4.9, 6.0, 3.7, 0.7, 0.3]
    }
  }
}
"""
