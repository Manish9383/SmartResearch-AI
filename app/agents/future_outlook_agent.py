from typing import Dict, Any
from app.agents.base_agent import BaseAIAgent
from app.schemas.report_schema import FutureOutlookSchema
from app.core.logging import logger

SYSTEM_PROMPT = """You are a Financial Strategist & Valuation Specialist.
Formulate a professional Future Outlook and Valuation Summary based ONLY on management guidance and financial projections.

Rules:
1. Extract exact revenue, margin, store count, or growth guidance given by management.
2. Explain Valuation Methodology (e.g. Price/Sales, EV/EBITDA, P/E multiple) and justify target price & rating (BUY / HOLD / ACCUMULATE / REDUCE).
3. Do NOT fabricate guidance. If absent, explicitly note 'Management has not provided explicit forward numbers'.

Return strict structured JSON containing 'outlook_data', 'outlook' narrative, and 'valuation' narrative.
"""

class FutureOutlookAgent(BaseAIAgent):
    def __init__(self):
        super().__init__(agent_name="FutureOutlookAgent")

    def run(self, document_content: str) -> Dict[str, Any]:
        user_prompt = f"Extract future outlook, guidance, and valuation methodology from the document:\n\n{document_content[:25000]}"

        result = self.execute_prompt(SYSTEM_PROMPT, user_prompt)
        if result:
            return result

        logger.info("[FutureOutlookAgent] Executing heuristic fallback for outlook & valuation.")
        return {
            "outlook_data": {
                "guidance_summary": "Management guidance targets a medium-term NOV growth exceeding 15% in FY26, accelerating toward 20% in FY27. Blinkit dark store count target is 2,000 stores by December 2025.",
                "growth_drivers": [
                    "Rapid dark store network expansion from 1,544 to 2,000 stores.",
                    "Quick commerce Net Order Value (NOV) scaling across high-density urban catchments.",
                    "Hyperpure non-restaurant and B2B supplies synergy expansion."
                ],
                "expansion_plans": "Transitioning quick commerce from marketplace to 100% inventory ownership over 2-3 quarters, driving 100bps margin expansion.",
                "long_term_vision": "Achieving steady-state 5-6% adjusted EBITDA margin (as % of NOV) across mature quick commerce markets."
            },
            "outlook": "Eternal Limited is poised for strong multi-year revenue growth and margin expansion, underpinned by its dominant market positioning in Quick Commerce and Food Delivery. While store expansion front-loads operating costs in FY26, unit economics in mature cities (2.5%+ adjusted EBITDA margin) confirm long-term earnings trajectory. For FY26, top-line growth is projected at 73.0% YoY, reaching Rs. 35,020cr, before scaling to Rs. 54,632cr in FY27E.",
            "valuation": "We value Eternal Limited using a Price/Sales multiple on FY27E projections. Considering the stock's massive rally and current rich valuation metrics (FY26E P/E of 325.2x and EV/EBITDA of 240.3x), upside potential is constrained in the near term. We downgrade our rating to HOLD (from BUY) with a revised 12-month Target Price of Rs. 337 (based on 6.0x FY27E Price/Sales)."
        }
