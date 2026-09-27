"""
MediFederate PDF Report Generator
Generates professional medical reports for patient predictions
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io


PRIMARY_COLOR = colors.HexColor("#667eea")
SECONDARY_COLOR = colors.HexColor("#764ba2")
DANGER_COLOR = colors.HexColor("#ef4444")
SUCCESS_COLOR = colors.HexColor("#10b981")
LIGHT_BG = colors.HexColor("#f5f7ff")
DARK_TEXT = colors.HexColor("#1e1e2e")


def _header_footer(canvas, doc):
    """Add header and footer to every page"""
    canvas.saveState()
    width, height = A4
    
    canvas.setFillColor(colors.HexColor("#808090"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(width / 2, 0.6 * cm, 
        f"MediFederate | Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')} | Page {doc.page}")
    
    canvas.drawString(1.5 * cm, 0.6 * cm, "Confidential Medical Report")
    canvas.drawRightString(width - 1.5 * cm, 0.6 * cm, "medi-federate.app")
    
    canvas.setStrokeColor(PRIMARY_COLOR)
    canvas.setLineWidth(2)
    canvas.line(1.5 * cm, height - 1.5 * cm, width - 1.5 * cm, height - 1.5 * cm)
    
    canvas.restoreState()


def generate_medical_report(disease_type, patient_data, prediction_result):
    """Generate a professional medical PDF report"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=1.5 * cm,
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'],
        fontSize=22, textColor=PRIMARY_COLOR, spaceAfter=6,
        alignment=TA_CENTER, fontName='Helvetica-Bold',
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor("#808090"),
        alignment=TA_CENTER, spaceAfter=20,
    )
    
    section_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'],
        fontSize=13, textColor=PRIMARY_COLOR, spaceBefore=14,
        spaceAfter=8, fontName='Helvetica-Bold',
    )
    
    body_style = ParagraphStyle(
        'BodyText', parent=styles['Normal'],
        fontSize=10, textColor=DARK_TEXT, alignment=TA_JUSTIFY,
        spaceAfter=6, leading=14,
    )
    
    story = []
    
    # Header
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("🏥 MediFederate", title_style))
    story.append(Paragraph("AI-Powered Medical Prediction Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY_COLOR, spaceAfter=15))
    
    # Report Info
    report_id = f"MF-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    info_data = [
        ["Report ID:", report_id, "Date:", datetime.now().strftime("%B %d, %Y")],
        ["Disease Model:", disease_type, "Time:", datetime.now().strftime("%H:%M")],
    ]
    info_table = Table(info_data, colWidths=[3 * cm, 5.5 * cm, 2.5 * cm, 5.5 * cm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_TEXT),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5 * cm))
    
    # Prediction Result
    story.append(Paragraph("📊 AI Prediction Result", section_style))
    
    prob_pct = prediction_result['probability'] * 100
    is_high = prediction_result['is_high_risk']
    result_color = DANGER_COLOR if is_high else SUCCESS_COLOR
    result_label = "HIGH RISK" if is_high else "LOW RISK"
    result_emoji = "🔴" if is_high else "🟢"
    
    result_data = [
        [Paragraph(f"<b>{result_emoji} {result_label}</b>", 
                   ParagraphStyle('R', parent=body_style, fontSize=16, textColor=colors.white, alignment=TA_CENTER))],
        [Paragraph(f"<b>Probability: {prob_pct:.1f}%</b>",
                   ParagraphStyle('P', parent=body_style, fontSize=14, textColor=colors.white, alignment=TA_CENTER))],
    ]
    result_table = Table(result_data, colWidths=[16.5 * cm])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), result_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(prediction_result.get('summary', ''), body_style))
    
    # Patient Data
    story.append(Paragraph("👤 Patient Details", section_style))
    
    patient_rows = [["Parameter", "Value", "Parameter", "Value"]]
    items = list(patient_data.items())
    
    for i in range(0, len(items), 2):
        row = []
        for j in range(2):
            if i + j < len(items):
                key, val = items[i + j]
                formatted_key = key.replace('_', ' ').title()
                row.extend([formatted_key, str(val)])
            else:
                row.extend(["", ""])
        patient_rows.append(row)
    
    patient_table = Table(patient_rows, colWidths=[4.5 * cm, 3.5 * cm, 4.5 * cm, 4 * cm])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d0e0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(patient_table)
    
    # Recommendations
    story.append(Paragraph("💡 Recommendations", section_style))
    
    if is_high:
        recommendations = _get_high_risk_recommendations(disease_type)
    else:
        recommendations = _get_low_risk_recommendations(disease_type)
    
    for rec in recommendations:
        story.append(Paragraph(f"• {rec}", body_style))
    
    # Disclaimer
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#d0d0e0")))
    story.append(Spacer(1, 0.3 * cm))
    
    disclaimer_style = ParagraphStyle(
        'Disclaimer', parent=body_style, fontSize=8,
        textColor=colors.HexColor("#808090"), alignment=TA_JUSTIFY,
    )
    
    story.append(Paragraph(
        "<b>⚠️ Important Disclaimer:</b> This report is generated by an AI system using "
        "Federated Learning and Differential Privacy techniques. It is meant for "
        "informational purposes only and should NOT replace professional medical advice. "
        "Always consult a qualified healthcare provider for diagnosis and treatment.",
        disclaimer_style
    ))
    
    # Doctor's Notes
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph("✍️ Doctor's Notes", section_style))
    
    note_data = [[""], [""], [""]]
    note_table = Table(note_data, colWidths=[16.5 * cm], rowHeights=[0.8 * cm] * 3)
    note_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#d0d0e0")),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor("#e0e0f0")),
    ]))
    story.append(note_table)
    
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Doctor's Signature: _________________________    "
        "Date: _______________",
        body_style
    ))
    
    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def _get_high_risk_recommendations(disease_type):
    """Get high-risk recommendations based on disease"""
    recs = {
        "Diabetes": [
            "Consult an endocrinologist or your primary care physician immediately.",
            "Monitor blood sugar levels 2-3 times daily.",
            "Reduce sugar, refined carbs, and processed foods.",
            "Increase physical activity: 30 minutes walk daily.",
            "Take prescribed medications strictly on time.",
            "Attend follow-up appointments every 2-4 weeks.",
            "Watch for warning signs: extreme thirst, blurred vision, fatigue.",
        ],
        "Heart Disease": [
            "Consult a cardiologist as soon as possible.",
            "Get an ECG and echocardiogram if not done recently.",
            "Reduce salt intake to less than 1 teaspoon/day.",
            "Avoid fried food, red meat, and full-fat dairy.",
            "Take BP and cholesterol medications regularly.",
            "Quit smoking and limit alcohol immediately.",
            "Call 1122 IMMEDIATELY if you experience chest pain or shortness of breath.",
        ],
        "Stroke": [
            "Consult a neurologist for comprehensive evaluation.",
            "Control blood pressure strictly (target: below 130/80).",
            "Manage diabetes and cholesterol aggressively.",
            "Learn the FAST test: Face, Arm, Speech, Time.",
            "Avoid smoking and excessive alcohol.",
            "Regular follow-up every 3 months.",
            "Call 1122 IMMEDIATELY for any sudden weakness or speech difficulty.",
        ],
        "Kidney Disease": [
            "Consult a nephrologist immediately for comprehensive evaluation.",
            "Get kidney function tests: creatinine, BUN, eGFR, and urine analysis.",
            "Control blood pressure strictly (target: below 130/80 mm Hg).",
            "Manage diabetes aggressively if present — it's a leading cause of kidney disease.",
            "Reduce salt, potassium, and phosphorus-rich foods (bananas, oranges, dairy).",
            "Avoid painkillers like ibuprofen and naproxen — they harm kidneys.",
            "Stay hydrated — drink 8-10 glasses of water daily (unless restricted by doctor).",
            "Avoid high-protein diets and processed foods.",
            "Get regular follow-up every 1-3 months.",
            "Watch for warning signs: swelling in legs, fatigue, decreased urination, foamy urine.",
        ],
    }
    return recs.get(disease_type, ["Consult a doctor immediately."])


def _get_low_risk_recommendations(disease_type):
    """Get low-risk recommendations based on disease"""
    recs = {
        "Diabetes": [
            "Continue maintaining a healthy, balanced diet.",
            "Exercise 30 minutes, 5 days a week.",
            "Check blood sugar levels monthly.",
            "Attend annual health checkups.",
            "Maintain a healthy weight.",
            "Stay hydrated with 8-10 glasses of water daily.",
        ],
        "Heart Disease": [
            "Keep up your healthy lifestyle — it's working!",
            "Continue regular exercise (30 min/day).",
            "Maintain normal BP and cholesterol levels.",
            "Eat a heart-healthy diet rich in vegetables and fish.",
            "Get annual cardiac checkups.",
            "Manage stress with meditation or yoga.",
        ],
        "Stroke": [
            "Great! Continue your healthy habits.",
            "Maintain normal blood pressure and blood sugar.",
            "Exercise regularly (30 minutes, 5 days/week).",
            "Avoid smoking and excessive alcohol.",
            "Get annual health checkups.",
            "Stay mentally active with reading, puzzles, etc.",
        ],
        "Kidney Disease": [
            "Great! Your kidney health appears normal. Continue healthy habits.",
            "Stay hydrated — 8-10 glasses of water daily.",
            "Maintain normal blood pressure and blood sugar.",
            "Reduce salt intake to less than 1 teaspoon/day.",
            "Avoid unnecessary painkillers (NSAIDs like ibuprofen).",
            "Eat a balanced diet rich in fruits and vegetables.",
            "Get annual kidney function tests (creatinine, BUN).",
            "Maintain a healthy weight and exercise regularly.",
        ],
    }
    return recs.get(disease_type, ["Continue healthy lifestyle."])


if __name__ == "__main__":
    print("Testing PDF Generator...")
    
    test_patient = {
        "Age": 65,
        "Time in Hospital (days)": 7,
        "Number of Medications": 25,
    }
    
    test_result = {
        "probability": 0.78,
        "is_high_risk": True,
        "summary": "This patient has a high probability of readmission.",
    }
    
    pdf = generate_medical_report("Kidney Disease", test_patient, test_result)
    
    with open("test_report.pdf", "wb") as f:
        f.write(pdf)
    
    print(f"✅ Test report saved ({len(pdf)} bytes)")