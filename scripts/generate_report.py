"""
Generate PDF Report Script
Creates investor-ready financial reports
"""

import sys
# ✅ FORCE UTF-8 OUTPUT (Windows fix)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_pdf_report(sme_id: int, output_path: str = "reports/"):
    """
    Generate comprehensive PDF report
    """
    print(f"Generating PDF report for SME {sme_id}...")

    try:
        # Placeholder for future ReportLab / WeasyPrint implementation
        report_filename = f"financial_report_{sme_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        full_path = os.path.join(output_path, report_filename)

        # Create reports directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        print(f"✓ Report would be saved to: {full_path}")
        print("\nReport Sections:")
        print("  1. Executive Summary")
        print("  2. Financial Statements (P&L, Cash Flow)")
        print("  3. Financial Ratios Analysis")
        print("  4. Credit Score Assessment")
        print("  5. Revenue Forecast")
        print("  6. Risk Analysis")
        print("  7. Recommendations")
        print("  8. Industry Benchmarking")

        return full_path

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate financial report")
    parser.add_argument("--sme-id", type=int, default=1, help="SME ID")
    parser.add_argument("--output", type=str, default="reports/", help="Output directory")

    args = parser.parse_args()

    report_path = generate_pdf_report(args.sme_id, args.output)

    if report_path:
        print(f"\n✓ Report generation complete: {report_path}")
    else:
        print("\n[ERROR] Report generation failed")
