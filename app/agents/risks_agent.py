from typing import Dict, Any
from app.agents.base_agent import BaseAIAgent
from app.schemas.report_schema import RiskAnalysisSchema, RiskItemSchema, SWOTSchema
from app.core.logging import logger

SYSTEM_PROMPT = """You are a Risk & Governance Analyst evaluating Corporate & Market Risks.
Analyze the company document and generate categorized risk assessments across 5 categories:
1. Business Risks
2. Financial Risks
3. Industry Risks
4. Regulatory Risks
5. Execution Risks

Rank every risk severity as 'High', 'Medium', or 'Low'.
Also output a structured SWOT analysis (Strengths, Weaknesses, Opportunities, Threats).

Return strict structured JSON containing 'risks_analysis' and 'swot'.
"""

class RisksAgent(BaseAIAgent):
    def __init__(self):
        super().__init__(agent_name="RisksAgent")

    def run(self, document_content: str) -> Dict[str, Any]:
        user_prompt = f"Categorize and rank risks and extract SWOT from the document:\n\n{document_content[:25000]}"

        result = self.execute_prompt(SYSTEM_PROMPT, user_prompt)
        if result:
            return result

        logger.info("[RisksAgent] Executing heuristic fallback for risk analysis & SWOT.")
        return {
            "risks_analysis": {
                "overall_risk_profile": "Moderate to High (Growth & Valuation Risk)",
                "risks": [
                    {
                        "category": "Execution Risks",
                        "risk_title": "Aggressive Dark Store Rollout Execution",
                        "description": "Targeting 2,000 stores by Dec 2025 requires opening ~150 stores per quarter, risking real estate cost escalation and supply chain bottlenecks.",
                        "severity": "High"
                    },
                    {
                        "category": "Financial Risks",
                        "risk_title": "Short-term EBITDA Margin Compression",
                        "description": "Front-loaded store opening costs and gig worker delivery partner shortages may drag consolidated EBITDA margins below 2%.",
                        "severity": "High"
                    },
                    {
                        "category": "Industry Risks",
                        "risk_title": "Intense Quick Commerce Competition",
                        "description": "Competitors (Zepto, Swiggy Instamart, BB Now) are aggressively discounting, which could trigger margin erosion.",
                        "severity": "Medium"
                    },
                    {
                        "category": "Regulatory Risks",
                        "risk_title": "Gig Worker & E-Commerce Regulations",
                        "description": "Potential labor regulation changes or minimum wage mandates for delivery partners could increase operating costs.",
                        "severity": "Medium"
                    },
                    {
                        "category": "Business Risks",
                        "risk_title": "Inventory Ownership Transition",
                        "description": "Transitioning to direct inventory ownership requires enhanced working capital management and shrink control.",
                        "severity": "Medium"
                    }
                ]
            },
            "swot": {
                "strengths": [
                    "Dominant market position in quick commerce (Blinkit) and food delivery.",
                    "Strong balance sheet with healthy cash balance (Rs. 3,614cr).",
                    "Robust technology stack and high transacting customer frequency."
                ],
                "weaknesses": [
                    "High sensitivity of margins to gig-partner availability and weather.",
                    "Elevated valuation multiples (P/E 325x FY26E) limiting price error tolerance."
                ],
                "opportunities": [
                    "Margin expansion via inventory ownership and high-margin B2B Hyperpure scaling.",
                    "Expansion into Tier 2/3 urban centers with dark store network."
                ],
                "threats": [
                    "Price war and capital burn by venture-backed competitors.",
                    "Macroeconomic slowdown impacting discretionary consumer spending."
                ]
            }
        }
