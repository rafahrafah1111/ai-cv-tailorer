import pdfplumber



def extract_text_from_pdf(pdf_path: str) -> str:

    """

    هاي الدالة بتاخد مسار ملف الـ PDF، وبتقرأ كل الصفحات اللي جواته،

    وبترجّع النص كامل كـ سلسلة نصية واحدة (String).

    """

    full_text = ""

    

    # فتح ملف الـ PDF بأمان

    with pdfplumber.open(pdf_path) as pdf:

        # المرور على كل صفحة في ملف الـ PDF

        for page in pdf.pages:

            text = page.extract_text()

            if text:  # التأكد إن الصفحة مش فاضية

                full_text += text + "\n"  # إضافة النص مع سطر جديد

                

    return full_text



# --- الجزء الخاص بتجربة الكود (Test) ---

if __name__ == "__main__":

    test_pdf = "CV Rafah Al Nabulsy (8).pdf"

    

    try:

        print("جاري استخراج النص من الـ CV...")

        cv_text = extract_text_from_pdf(test_pdf)

        print("\n--- تم استخراج أول 500 حرف من النص بنجاح: ---")

        print(cv_text[:500]) 

    except FileNotFoundError:

        print(f"\n❌ خطأ: لم نجد ملف باسم '{test_pdf}' في المجلد.")

        print("💡 الحل: اسحبي ملف الـ CV تبعك وحطيه جوة المجلد وغيري اسمه لـ sample_cv.pdf")