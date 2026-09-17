import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(df: pd.DataFrame, output_pdf: str = "outputs/drivetest_report.pdf"):
    """Tong hop so lieu thong ke tu log va xuat bao cao tong ket dang pdf."""
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    doc = SimpleDocTemplate(output_pdf, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1A365D'), spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#2B6CB0'), spaceBefore=10, spaceAfter=6)
    body_style = styles['Normal']
    
    story.append(Paragraph("DRIVE TEST PERFORMANCE & COVERAGE REPORT", title_style))
    story.append(Paragraph(f"<b>Khu vuc do kiem: Mang di dong 4G/5G (Mock Route) | Tong so mau:</b> {len(df)}", body_style))
    story.append(Spacer(1, 10))
    
    # Thống kê KPIs
    avg_rsrp = df['RSRP_dBm'].mean()
    min_rsrp = df['RSRP_dBm'].min()
    max_rsrp = df['RSRP_dBm'].max()
    avg_sinr = df['SINR_dB'].mean()
    avg_dl = df['Throughput_DL_Mbps'].mean()
    poor_coverage_pct = (len(df[df['RSRP_dBm'] < -100]) / len(df)) * 100
    
    story.append(Paragraph("1. Tong quan chi so vo tuyen (KPIs Summary)", heading_style))
    
    summary_data = [
        ["Chi so ky thuat (KPI)", "Gia tri thong ke"],
        ["RSRP Trung binh (Min / Max)", f"{avg_rsrp:.2f} dBm ({min_rsrp} / {max_rsrp})"],
        ["SINR Trung binh", f"{avg_sinr:.2f} dB"],
        ["Toc do Download trung binh", f"{avg_dl:.2f} Mbps"],
        ["Ty le vung song yeu (RSRP < -100dBm)", f"{poor_coverage_pct:.1f}%"]
    ]
    
    t = Table(summary_data, colWidths=[250, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#E2E8F0')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.HexColor('#1A202C')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    # Đánh giá & Khuyến nghị
    story.append(Paragraph("2. Danh gia chuyen gia & Khuyen nghi toi uu", heading_style))
    insight_text = f"""
    - <b>Chat luong vung phu:</b> co khoang <b>{poor_coverage_pct:.1f}%</b> diem dopy -m pip install -r requirements.txt ghi nhan suy hao nang (RSRP < -100 dBm).<br/>
    - <b>Toc do du lieu:</b> Toc do tai xuong trung binh dat <b>{avg_dl:.2f} Mbps</b>, hoat dong on dinh.<br/>
    - <b>Khuyen nghi:</b> Can toi uu goc huong ang-ten cua tram phat gan cac diem ghi nhan su kien RSRP Drop.
    """
    story.append(Paragraph(insight_text, body_style))
    
    doc.build(story)