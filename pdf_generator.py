import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from models import TailoredCV

def generate_pdf(cv_data: TailoredCV, output_filename: str = "tailored_cv.pdf"):
    # Setup document with standard margins
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    story = []

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CVTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A1A1A"),
        spaceAfter=4
    )
    
    contact_style = ParagraphStyle(
        'CVContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#555555"),
        spaceAfter=15
    )
    
    section_heading = ParagraphStyle(
        'CVSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F4C81"), # Professional Navy Accent
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'CVBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'CVBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#333333"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    # 1. Header Section
    prof = cv_data.profile
    story.append(Paragraph(prof.name.upper(), title_style))
    
    contact_info = f"Email: {prof.email}  |  Phone: {prof.phone}"
    if prof.linkedin:
        contact_info += f"  |  LinkedIn: {prof.linkedin}"
    story.append(Paragraph(contact_info, contact_style))

    # 2. Objective Section
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    story.append(Paragraph(cv_data.objective, body_style))
    story.append(Spacer(1, 6))

    # 3. Experience Section
    if cv_data.experience:
        story.append(Paragraph("PROFESSIONAL & VOLUNTEER EXPERIENCE", section_heading))
        for exp in cv_data.experience:
            exp_elements = []
            header_text = f"<b>{exp.role}</b> — {exp.company} ({exp.duration})"
            exp_elements.append(Paragraph(header_text, body_style))
            for bullet in exp.bullet_points:
                exp_elements.append(Paragraph(f"&bull; {bullet}", bullet_style))
            story.append(KeepTogether(exp_elements))
        story.append(Spacer(1, 6))

    # 4. Education Section
    if cv_data.education:
        story.append(Paragraph("EDUCATION", section_heading))
        for edu in cv_data.education:
            edu_text = f"<b>{edu.degree}</b><br/>{edu.institution} ({edu.duration})"
            story.append(Paragraph(edu_text, body_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 6))

    # 5. Skills Section
    if cv_data.skills:
        story.append(Paragraph("TECHNICAL SKILLS", section_heading))
        for skill_category in cv_data.skills:
            story.append(Paragraph(f"&bull; {skill_category}", bullet_style))

    # Build PDF
    doc.build(story)
    print(f"Successfully generated PDF: {output_filename}")

if __name__ == "__main__":
    print("PDF Generator module loaded.")