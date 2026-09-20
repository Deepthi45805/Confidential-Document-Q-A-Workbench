import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from services.document_service import DocumentService
from config.settings import SAMPLE_DOCS_DIR

def create_pdf(filename, title, text_blocks):
    filepath = os.path.join(SAMPLE_DOCS_DIR, filename)
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph(f"<b>{title}</b>", styles['Title']), Spacer(1, 12)]
    
    for block in text_blocks:
        story.append(Paragraph(block, styles['Normal']))
        story.append(Spacer(1, 10))
        
    doc.build(story)
    print(f"Generated sample PDF: {filepath}")
    return filepath

def main():
    os.makedirs(SAMPLE_DOCS_DIR, exist_ok=True)

    # 1. Policy V1
    v1_content = [
        "Employee Policy Version 1.0 (Effective Jan 2025)",
        "Section 1: Working Hours & Leave Entitlements",
        "All full-time employees are entitled to standard 12 days of paid annual leave per year. Remote work is permitted up to 1 day per week with manager approval.",
        "Section 2: Security & Data Handling",
        "Employees must lock their workstations when leaving their desks. Confidential documents must be encrypted prior to transmission over email."
    ]
    pdf1 = create_pdf("Employee_Policy_V1.pdf", "Employee Policy V1.0", v1_content)

    # 2. Policy V2
    v2_content = [
        "Employee Policy Version 2.0 (Effective Jan 2026)",
        "Section 1: Working Hours & Leave Entitlements",
        "All full-time employees are entitled to an increased total of 15 days of paid annual leave per year. Remote work is now permitted up to 2 days per week automatically.",
        "Section 2: Security & Data Handling",
        "Employees must lock their workstations when leaving their desks. All confidential documents must stay on local storage; public cloud uploading is strictly prohibited."
    ]
    pdf2 = create_pdf("Employee_Policy_V2.pdf", "Employee Policy V2.0", v2_content)

    # 3. Security SOP
    sop_content = [
        "Security Standard Operating Procedure (SOP)",
        "Standard SOP-88: Password and Credentials Protocol",
        "All staff passwords must be at least 16 characters long and updated every 90 days. Multi-Factor Authentication (MFA) is compulsory for all system access.",
        "Standard SOP-89: Incident Reporting",
        "Any suspected data breach or unauthorized file access must be reported to the IT Security Desk within 30 minutes of detection."
    ]
    pdf3 = create_pdf("Security_SOP.pdf", "Security SOP Handbook", sop_content)

    # Index files automatically into local ChromaDB
    doc_service = DocumentService()
    for f in [pdf1, pdf2, pdf3]:
        doc_service.process_and_store_document(f)
    print("Sample documents automatically parsed and stored into ChromaDB!")

if __name__ == "__main__":
    main()
