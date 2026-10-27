import os
import pypdfium2 as pdfium

os.makedirs("validation_renders", exist_ok=True)
pdf = pdfium.PdfDocument("Final_Project_Report.pdf")
print("Total pages in generated PDF:", len(pdf))

# Render key pages: 1, 2, 3, 4, 5, 7, 8, 12, 16, 23, 30, 38, 44, 46
key_pages = [1, 2, 3, 4, 5, 7, 8, 12, 16, 23, 30, 38, 44, 46]

for p_num in key_pages:
    page = pdf[p_num - 1]
    bitmap = page.render(scale=1.5)
    pil_image = bitmap.to_pil()
    out_path = f"validation_renders/page_{p_num}.png"
    pil_image.save(out_path)
    print(f"Rendered Page {p_num} -> {out_path} ({pil_image.size})")

print("Validation rendering complete!")
