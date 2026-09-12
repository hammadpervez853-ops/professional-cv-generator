import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image
from io import BytesIO
import os

st.set_page_config(
    page_title="Professional CV Generator",
    page_icon="📄",
    layout="wide"
)

# ============================================================
# STYLING
# ============================================================

st.markdown("""
<style>
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #172B4D;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #667085;
        margin-bottom: 30px;
    }

    .section-title {
        color: #172B4D;
        font-size: 22px;
        font-weight: 700;
        border-bottom: 2px solid #2F80ED;
        padding-bottom: 6px;
        margin-top: 20px;
    }

    .stButton button {
        background-color: #2F80ED;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">Professional CV Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Create a modern professional CV in PDF format</div>',
    unsafe_allow_html=True
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def wrap_text(text, font_name, font_size, max_width):
    words = str(text).split()
    lines = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word

        if stringWidth(test, font_name, font_size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_wrapped(c, text, x, y, width, font="Helvetica",
                 size=8.5, leading=11, color=colors.black):
    lines = wrap_text(text, font, size, width)

    c.setFont(font, size)
    c.setFillColor(color)

    for line in lines:
        c.drawString(x, y, line)
        y -= leading

    return y


def draw_sidebar_heading(c, title, x, y):
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y, title.upper())

    y -= 4

    c.setStrokeColor(colors.HexColor("#2F80ED"))
    c.setLineWidth(1.2)
    c.line(x, y, x + 25 * mm, y)

    return y - 9


def draw_main_heading(c, title, x, y, right):
    c.setFillColor(colors.HexColor("#2F80ED"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, title.upper())

    c.setStrokeColor(colors.HexColor("#D9E1EA"))
    c.setLineWidth(0.7)
    c.line(x, y - 4, right, y - 4)

    return y - 17


def draw_sidebar_bullet(c, text, x, y, width):
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 7.5)

    lines = wrap_text(
        "• " + text,
        "Helvetica",
        7.5,
        width
    )

    for line in lines:
        c.drawString(x, y, line)
        y -= 10

    return y - 2


# ============================================================
# INPUT FORM
# ============================================================

st.markdown(
    '<div class="section-title">Personal Information</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("Full Name", "Hammad")
    professional_title = st.text_input(
        "Professional Title",
        "Aspiring Python Developer"
    )
    email = st.text_input("Email", "hammad@example.com")
    phone = st.text_input("Phone", "+92 300 0000000")

with col2:
    location = st.text_input("Location", "Faisalabad, Pakistan")
    linkedin = st.text_input(
        "LinkedIn",
        "linkedin.com/in/hammad"
    )
    github = st.text_input(
        "GitHub",
        "github.com/hammad"
    )
    photo = st.file_uploader(
        "Profile Photo",
        type=["jpg", "jpeg", "png"]
    )

st.markdown(
    '<div class="section-title">Professional Profile</div>',
    unsafe_allow_html=True
)

profile = st.text_area(
    "Profile Summary",
    value=(
        "Motivated and hardworking aspiring Python developer with a strong "
        "interest in software development, automation, and practical technology "
        "solutions. Currently improving programming knowledge through hands-on "
        "projects and continuous learning."
    ),
    height=120
)

st.markdown(
    '<div class="section-title">Skills and Languages</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    skills_input = st.text_area(
        "Skills - separate with commas",
        "Python, HTML, CSS, ReportLab, PDF Generation, Git, Problem Solving, Communication, Teamwork"
    )

with col2:
    languages_input = st.text_area(
        "Languages - one per line",
        "Urdu - Native\nEnglish - Basic\nPunjabi - Native"
    )

st.markdown(
    '<div class="section-title">Education</div>',
    unsafe_allow_html=True
)

education_input = st.text_area(
    "One education entry per line: Degree | Institute | Year",
    "Intermediate / Higher Secondary Education | Local College, Faisalabad | 2024 - 2026\n"
    "Matriculation | Local School, Faisalabad | 2022 - 2024"
)

st.markdown(
    '<div class="section-title">Experience</div>',
    unsafe_allow_html=True
)

experience_input = st.text_area(
    "One experience entry per line: Job Title | Company | Duration | Description",
    "Python Developer - Personal Projects | Independent Learning & Development | 2025 - Present | Practicing Python through applications, automation tasks, PDF generation, and programming exercises.\n"
    "Student Project Developer | Academic & Personal Practice | 2024 - 2025 | Created beginner-level software projects and improved programming logic."
)

st.markdown(
    '<div class="section-title">Projects</div>',
    unsafe_allow_html=True
)

projects_input = st.text_area(
    "One project per line: Project Name | Technologies | Description",
    "Professional CV Generator | Python, ReportLab, Pillow | Created a professional PDF CV generator with photo, skills, education, projects, and experience sections.\n"
    "Invoice Generator | Python, ReportLab | Developed a basic invoice-generation concept with customer details, items, prices, and totals.\n"
    "Calculator Application | Python | Built a calculator application to practice variables, operators, conditions, and programming logic."
)

st.markdown(
    '<div class="section-title">Certifications and Strengths</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    certifications_input = st.text_area(
        "Certifications - one per line",
        "Python Programming Crash Course\nIntroduction to Computer Programming\nSelf-Learning: Python and Software Development"
    )

with col2:
    strengths_input = st.text_area(
        "Strengths - one per line",
        "Quick Learner\nHardworking\nProblem Solver\nSelf-Motivated\nTeam Player"
    )

# ============================================================
# DATA PROCESSING
# ============================================================

skills = [
    item.strip()
    for item in skills_input.split(",")
    if item.strip()
]

languages = [
    item.strip()
    for item in languages_input.splitlines()
    if item.strip()
]

certifications = [
    item.strip()
    for item in certifications_input.splitlines()
    if item.strip()
]

strengths = [
    item.strip()
    for item in strengths_input.splitlines()
    if item.strip()
]

education = []

for line in education_input.splitlines():
    parts = [p.strip() for p in line.split("|")]

    if len(parts) >= 3:
        education.append({
            "degree": parts[0],
            "institute": parts[1],
            "year": "|".join(parts[2:])
        })

experience = []

for line in experience_input.splitlines():
    parts = [p.strip() for p in line.split("|")]

    if len(parts) >= 4:
        experience.append({
            "title": parts[0],
            "company": parts[1],
            "duration": parts[2],
            "description": "|".join(parts[3:])
        })

projects = []

for line in projects_input.splitlines():
    parts = [p.strip() for p in line.split("|")]

    if len(parts) >= 3:
        projects.append({
            "name": parts[0],
            "tech": parts[1],
            "description": "|".join(parts[2:])
        })

# ============================================================
# PDF GENERATION
# ============================================================

def generate_cv():
    output = BytesIO()

    pdf = canvas.Canvas(output, pagesize=A4)

    page_width, page_height = A4

    sidebar_color = colors.HexColor("#172B4D")
    accent_color = colors.HexColor("#2F80ED")
    dark_text = colors.HexColor("#1F2937")
    gray_text = colors.HexColor("#5B6472")
    light_line = colors.HexColor("#D9E1EA")
    soft_bg = colors.HexColor("#F7F9FC")
    white = colors.white

    sidebar_width = 62 * mm
    main_left = sidebar_width + 13 * mm
    main_right = page_width - 13 * mm
    main_width = main_right - main_left

    # Background
    pdf.setFillColor(soft_bg)
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    pdf.setFillColor(sidebar_color)
    pdf.rect(0, 0, sidebar_width, page_height, fill=1, stroke=0)

    # Photo
    if photo is not None:
        try:
            image = Image.open(photo).convert("RGB")
            image.thumbnail((600, 600))

            image_buffer = BytesIO()
            image.save(image_buffer, format="JPEG")
            image_buffer.seek(0)

            photo_size = 37 * mm
            photo_x = (sidebar_width - photo_size) / 2
            photo_y = page_height - 52 * mm

            pdf.setFillColor(white)
            pdf.circle(
                photo_x + photo_size / 2,
                photo_y + photo_size / 2,
                photo_size / 2 + 2,
                fill=1,
                stroke=0
            )

            pdf.drawImage(
                ImageReader(image_buffer),
                photo_x,
                photo_y,
                width=photo_size,
                height=photo_size,
                preserveAspectRatio=True,
                mask="auto"
            )

        except Exception:
            pass

    # Sidebar
    side_y = page_height - 65 * mm
    side_x = 10 * mm

    side_y = draw_sidebar_heading(pdf, "Contact", side_x, side_y)

    for item in [email, phone, location, linkedin, github]:
        if item.strip():
            side_y = draw_wrapped(
                pdf,
                item,
                side_x,
                side_y,
                sidebar_width - 18 * mm,
                font="Helvetica",
                size=7.2,
                leading=9,
                color=white
            )
            side_y -= 4

    side_y -= 6
    side_y = draw_sidebar_heading(pdf, "Technical Skills", side_x, side_y)

    for skill in skills:
        side_y = draw_sidebar_bullet(
            pdf,
            skill,
            side_x,
            side_y,
            sidebar_width - 18 * mm
        )

    side_y -= 6
    side_y = draw_sidebar_heading(pdf, "Languages", side_x, side_y)

    for language in languages:
        side_y = draw_sidebar_bullet(
            pdf,
            language,
            side_x,
            side_y,
            sidebar_width - 18 * mm
        )

    side_y -= 6
    side_y = draw_sidebar_heading(pdf, "Strengths", side_x, side_y)

    for strength in strengths:
        side_y = draw_sidebar_bullet(
            pdf,
            strength,
            side_x,
            side_y,
            sidebar_width - 18 * mm
        )

    # Main content
    main_y = page_height - 25 * mm

    pdf.setFillColor(dark_text)
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(main_left, main_y, full_name)

    main_y -= 11

    pdf.setFillColor(accent_color)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(main_left, main_y, professional_title.upper())

    main_y -= 11

    pdf.setFillColor(gray_text)
    pdf.setFont("Helvetica", 7.5)
    pdf.drawString(
        main_left,
        main_y,
        "Python • Software Development • Automation • Problem Solving"
    )

    main_y -= 17

    pdf.setStrokeColor(accent_color)
    pdf.setLineWidth(2)
    pdf.line(main_left, main_y, main_right, main_y)

    main_y -= 17

    # Profile
    main_y = draw_main_heading(
        pdf,
        "Professional Profile",
        main_left,
        main_y,
        main_right
    )

    main_y = draw_wrapped(
        pdf,
        profile,
        main_left,
        main_y,
        main_width,
        font="Helvetica",
        size=8.5,
        leading=11.5,
        color=gray_text
    )

    main_y -= 13

    # Experience
    if experience:
        main_y = draw_main_heading(
            pdf,
            "Experience",
            main_left,
            main_y,
            main_right
        )

        for exp in experience:
            pdf.setFillColor(dark_text)
            pdf.setFont("Helvetica-Bold", 9.5)
            pdf.drawString(main_left, main_y, exp["title"])

            duration_width = stringWidth(
                exp["duration"],
                "Helvetica-Bold",
                7.5
            )

            pdf.setFillColor(accent_color)
            pdf.setFont("Helvetica-Bold", 7.5)
            pdf.drawString(
                main_right - duration_width,
                main_y,
                exp["duration"]
            )

            main_y -= 11

            pdf.setFillColor(accent_color)
            pdf.setFont("Helvetica-Bold", 8)
            pdf.drawString(main_left, main_y, exp["company"])

            main_y -= 11

            main_y = draw_wrapped(
                pdf,
                exp["description"],
                main_left,
                main_y,
                main_width,
                font="Helvetica",
                size=8.2,
                leading=10.5,
                color=gray_text
            )

            main_y -= 10

    # Education
    if education:
        main_y = draw_main_heading(
            pdf,
            "Education",
            main_left,
            main_y,
            main_right
        )

        for edu in education:
            pdf.setFillColor(dark_text)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(main_left, main_y, edu["degree"])

            year_width = stringWidth(
                edu["year"],
                "Helvetica",
                7.5
            )

            pdf.setFillColor(accent_color)
            pdf.setFont("Helvetica", 7.5)
            pdf.drawString(
                main_right - year_width,
                main_y,
                edu["year"]
            )

            main_y -= 11

            pdf.setFillColor(gray_text)
            pdf.setFont("Helvetica", 8)
            pdf.drawString(main_left, main_y, edu["institute"])

            main_y -= 14

    # Projects
    if projects:
        main_y = draw_main_heading(
            pdf,
            "Featured Projects",
            main_left,
            main_y,
            main_right
        )

        for project in projects:
            pdf.setFillColor(dark_text)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(main_left, main_y, project["name"])

            main_y -= 10

            pdf.setFillColor(accent_color)
            pdf.setFont("Helvetica-Bold", 7.5)
            main_y = draw_wrapped(
                pdf,
                "Technologies: " + project["tech"],
                main_left,
                main_y,
                main_width,
                font="Helvetica-Bold",
                size=7.5,
                leading=9,
                color=accent_color
            )

            main_y -= 3

            main_y = draw_wrapped(
                pdf,
                project["description"],
                main_left,
                main_y,
                main_width,
                font="Helvetica",
                size=8.1,
                leading=10.5,
                color=gray_text
            )

            main_y -= 9

    # Certifications
    if certifications:
        main_y = draw_main_heading(
            pdf,
            "Certifications & Learning",
            main_left,
            main_y,
            main_right
        )

        for certification in certifications:
            main_y = draw_wrapped(
                pdf,
                "• " + certification,
                main_left,
                main_y,
                main_width,
                font="Helvetica",
                size=8.2,
                leading=10.5,
                color=gray_text
            )
            main_y -= 2

    # Footer
    pdf.setStrokeColor(light_line)
    pdf.setLineWidth(0.5)
    pdf.line(main_left, 13 * mm, main_right, 13 * mm)

    pdf.setFillColor(gray_text)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(
        main_left,
        8 * mm,
        "Professional Resume"
    )

    pdf.drawRightString(
        main_right,
        8 * mm,
        "References available upon request"
    )

    pdf.save()
    output.seek(0)

    return output.getvalue()


# ============================================================
# GENERATE BUTTON
# ============================================================

st.markdown("---")

if st.button("🚀 Generate Professional CV", use_container_width=True):
    try:
        pdf_data = generate_cv()

        st.success("Your professional CV has been generated successfully!")

        st.download_button(
            label="📥 Download CV PDF",
            data=pdf_data,
            file_name="Professional_CV.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as error:
        st.error(f"Error: {error}")
