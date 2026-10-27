# generate_complete_report.py
# Complete build pipeline for Final_Project_Report.pdf and Final_Project_Report.docx

import os
import sys
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    sys.path.insert(0, base_dir)
    sys.path.insert(0, root_dir)
    os.chdir(base_dir)

    print("=" * 60)
    print(" LoanGuard-AI: Complete Project Report Generation Pipeline")
    print("=" * 60)

    # 1. Generate/verify high-fidelity web app and report assets
    print("\n[1/4] Generating & verifying high-fidelity report assets...")
    try:
        import render_web_app_images
        render_web_app_images.render_images()
    except Exception as e:
        print(f"Notice: Root renderer fallback: {e}")

    # 2. Build PDF Report
    print("\n[2/4] Compiling Final_Project_Report.pdf...")
    import build_pdf
    build_pdf.create_pdf_report("Final_Project_Report.pdf")

    # 3. Build Word Document
    print("\n[3/4] Compiling Final_Project_Report.docx...")
    import build_docx
    build_docx.create_docx_report("Final_Project_Report.docx")

    # 4. Verify & Render key PDF pages for visual validation
    print("\n[4/4] Generating visual page validation renders...")
    try:
        import pypdfium2 as pdfium
        val_dir = os.path.join(root_dir, "validation_renders")
        os.makedirs(val_dir, exist_ok=True)
        pdf = pdfium.PdfDocument("Final_Project_Report.pdf")
        key_pages = [1, 2, 5, 7, 15, 38, 39, 40, 41]
        for p_num in key_pages:
            if p_num <= len(pdf):
                page = pdf[p_num - 1]
                bitmap = page.render(scale=2.0)
                pil_image = bitmap.to_pil()
                out_path = os.path.join(val_dir, f"page_{p_num}.png")
                pil_image.save(out_path)
                print(f"  - Rendered Page {p_num} -> {out_path}")
    except Exception as e:
        print(f"Notice: Validation page rendering skipped: {e}")

    print("\n[SUCCESS] Report compilation complete!")
    print("Generated:")
    print("  - Final_Project_Report.pdf")
    print("  - Final_Project_Report.docx")

if __name__ == "__main__":
    main()
