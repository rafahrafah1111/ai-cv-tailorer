import streamlit as st
import os
import pypdf
import yaml
import subprocess
from tailor_agent import tailor_cv

# إعدادات الصفحة الفخمة
st.set_page_config(page_title="AI CV Tailorer Pro", page_icon="🚀", layout="wide")

st.title("🚀 AI CV Tailorer & RenderCV Generator")
st.subheader("Tailor your tech resume instantly with dynamic context placement")

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("DeepSeek/OpenRouter API Key", type="password", value=os.environ.get("DEEPSEEK_API_KEY", ""))
    if api_key:
        os.environ["DEEPSEEK_API_KEY"] = api_key
        
    uploaded_cv = st.file_uploader("Upload Original CV (PDF)", type=["pdf"])

# تقسيم الشاشة
col1, col2 = st.columns(2)

with col1:
    st.header("📝 Target Job Description")
    jd_input = st.text_area("Paste the job description here...", height=400)

with col2:
    st.header("⚡ Actions")
    if st.button("Generate Tailored CV", type="primary"):
        if not uploaded_cv or not jd_input.strip():
            st.error("Please upload your CV and paste a Job Description first!")
        elif not os.environ.get("DEEPSEEK_API_KEY"):
            st.error("API Key is missing!")
        else:
            with st.spinner("Analyzing and tailoring with AI..."):
                try:
                    # 1. قراءة الـ PDF المرفوع
                    pdf_reader = pypdf.PdfReader(uploaded_cv)
                    raw_cv_text = ""
                    for page in pdf_reader.pages:
                        raw_cv_text += page.extract_text() or ""
                    
                    # 2. استدعاء الـ Agent للحصول على الـ Object
                    tailored_object = tailor_cv(raw_cv_text, jd_input)
                    tailored_dict = tailored_object.model_dump()
                    
                    # 3. تنظيف التواريخ والبيانات برمجياً لتطابق مواصفات RenderCV بالملي
                    clean_experience = []
                    for exp in tailored_dict.get("experience", []):
                        # تنظيف التواريخ لتكون أرقام سنين فقط (وهاد اللي بتحبه RenderCV)
                        duration = str(exp.get("duration", ""))
                        start_date = "2025" if "2025" in duration else ("2021" if "2021" in duration else "2022")
                        end_date = "present" if "Present" in duration or "present" in duration or not duration else "2026"
                        
                        clean_experience.append({
                            "company": exp.get("company", "Company Name"),
                            "position": exp.get("role", "AI Engineer"),
                            "start_date": start_date,
                            "end_date": end_date,
                            "highlights": exp.get("bullet_points", ["Key contribution"])
                        })

                    clean_education = []
                    for edu in tailored_dict.get("education", []):
                        duration = str(edu.get("duration", ""))
                        start_date = "2021" if "2021" in duration else "2025"
                        end_date = "2026" if "2026" in duration or "February" in duration else "present"
                        
                        clean_education.append({
                            "institution": edu.get("institution", "University Name"),
                            "area": edu.get("degree", "B.Sc. Data Science & AI"),
                            "start_date": start_date,
                            "end_date": end_date
                        })

                    # تجميع الهيكل النهائي المطلق لـ RenderCV
                    rendercv_data = {
                        "cv": {
                            "name": "Rafah Alnabulsy",
                            "location": "Amman, Jordan",
                            "email": "rafahr007@gmail.com",
                            "phone": "+962787175383",
                            "social_networks": [
                                {
                                    "network": "LinkedIn",
                                    "username": "rafah-alnabulsy"
                                }
                            ],
                            "sections": {
                                "summary": [tailored_dict.get("objective", "AI and Data Science professional.")],
                                "experience": clean_experience,
                                "education": clean_education,
                                "skills": [
                                    {
                                        "label": "Technical Skills",
                                        "details": ", ".join(tailored_dict.get("skills", ["Python", "Generative AI"]))
                                    }
                                ]
                            }
                        }
                    }
                    
                    # 4. حفظ ملف الـ YAML في المجلد الحالي لتجنب مشاكل المسارات المعقدة
                    yaml_path = "tailored_cv.yaml"
                    with open(yaml_path, "w", encoding="utf-8") as f:
                        yaml.dump(rendercv_data, f, allow_unicode=True, default_flow_style=False)
                    
                    st.success("🤖 AI Tailoring complete! Rendering PDF...")
                    
                    # 5. تشغيل الـ Render Engine بالخلفية بدون الفولد الـ مسبب للمشكلة
                    result = subprocess.run(
                        ["rendercv", "render", yaml_path],
                        capture_output=True, text=True
                    )
                    
                    # 6. التقاط الـ PDF وعرض زر التحميل من المجلد الافتراضي المستقر
                    output_dir = "rendercv_output"
                    generated_files = os.listdir(output_dir) if os.path.exists(output_dir) else []
                    pdf_file = next((f for f in generated_files if f.endswith(".pdf")), None)
                    
                    if pdf_file:
                        pdf_path = os.path.join(output_dir, pdf_file)
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="📥 Download Your Tailored CV (PDF)",
                                data=f,
                                file_name="Rafah_Alnabulsy_Tailored_CV.pdf",
                                mime="application/pdf"
                            )
                        st.balloons()
                    else:
                        st.error("RenderCV could not generate the PDF file. Check logs below:")
                        st.code(result.stderr)
                        
                except Exception as e:
                    st.error(f"Pipeline crashed: {e}")