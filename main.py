import argparse
import sys
import os
from datetime import datetime
from parser_agent import parse_pdf_to_json
from tailor_agent import tailor_cv
from pdf_generator import generate_pdf

def get_multiline_jd():
    """ يسمح بإدخال نص الـ JD متعدد الأسطر عبر التيرمينال """
    print("\n[?] Paste the Target Job Description below.")
    print("[*] Press Ctrl+D (on Mac) or Enter then Ctrl+Z (on Windows) when finished saving it:\n")
    lines = sys.stdin.read()
    return lines.strip()

def run_pipeline():
    parser = argparse.ArgumentParser(description="AI CV Tailorer CLI Tool")
    parser.add_argument("-i", "--input", type=str, default="CV Rafah Al Nabulsy (10).pdf", help="Path to original CV PDF")
    # جعل المخرج يحمل تايم-ستامب لمنع كاش الـ PDF تماماً
    timestamp = datetime.now().strftime("%H%M%S")
    parser.add_argument("-o", "--output", type=str, default=f"Tailored_CV_{timestamp}.pdf", help="Path to output tailored PDF")
    parser.add_argument("-j", "--jd", type=str, help="Job description text (optional, will prompt if missing)")
    
    args = parser.parse_args()

    print("=== STARTING AI CV TAILORING PIPELINE ===")
    
    job_description = args.jd
    if not job_description:
        job_description = get_multiline_jd()
        
    if not job_description.strip():
        print("❌ Error: Job description cannot be empty.")
        return

    try:
        # 1. Parsing
        parsed_json = parse_pdf_to_json(args.input)
        
        # 2. Tailoring
        tailored_json = tailor_cv(parsed_json, job_description)
        
        # 3. فحص المخرجات بالـ Terminal للتأكد من التعديل قبل الطباعة
        print("\n--- [DEBUG] Verified Tailored Summary From LLM ---")
        # إذا كان الكلاس يمتلك حقل باسم professional_summary أو summary، رح يطبعه هون لتتأكدي بنفسك
        summary_attr = getattr(tailored_json, 'professional_summary', getattr(tailored_json, 'summary', 'No summary field found'))
        print(summary_attr)
        print("--------------------------------------------------\n")
        
        # 4. الـ Render النهائي
        generate_pdf(tailored_json, output_filename=args.output)
        
        print(f"=== PIPELINE EXECUTION COMPLETED SECURELY ===")
        print(f"[+] Brand New tailored resume saved as: {args.output}")
        
        # فتح الملف الجديد فوراً على الماك
        os.system(f"open {args.output}")
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")

if __name__ == "__main__":
    run_pipeline()