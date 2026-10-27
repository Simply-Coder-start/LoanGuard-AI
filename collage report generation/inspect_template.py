import pdfplumber
import json

with pdfplumber.open(r"C:\Users\soumy\Downloads\Smart_Disease_Prediction_Project_Report_Final.pdf") as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    
    # Analyze styles across key pages: 1 (Cert), 2 (Decl), 3 (Ack), 4 (Abstract), 5 (TOC), 7 (LOF), 8 (Ch1), 12 (Ch3), 16 (Ch4), 21 (Table), 30 (Ch7)
    sample_pages = [0, 1, 2, 3, 4, 6, 7, 11, 15, 20, 29]
    for p_idx in sample_pages:
        page = pdf.pages[p_idx]
        words = page.extract_words(extra_attrs=['fontname', 'size', 'top', 'bottom', 'x0', 'x1', 'upright'])
        
        # Determine margins
        if words:
            left_margin = min(w['x0'] for w in words)
            right_margin = page.width - max(w['x1'] for w in words)
            top_margin = min(w['top'] for w in words)
            bottom_margin = page.height - max(w['bottom'] for w in words)
        else:
            left_margin = right_margin = top_margin = bottom_margin = 0
            
        print(f"\n--- Page {p_idx+1} ---")
        print(f"Margins (pt): Left={left_margin:.1f}, Right={right_margin:.1f}, Top={top_margin:.1f}, Bottom={bottom_margin:.1f}")
        
        # Group by font and size
        font_sizes = {}
        for w in words:
            key = (w['fontname'], round(w['size'], 1))
            font_sizes[key] = font_sizes.get(key, 0) + 1
        
        print("Font distribution (top 5):")
        for k, v in sorted(font_sizes.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {k[0]} at {k[1]}pt: {v} words")

        # Sample headings
        lines = page.extract_text_lines()
        for l in lines[:6]:
            print(f"  Line: '{l['text']}' (size={l['chars'][0]['size']:.1f}, font={l['chars'][0]['fontname']}, top={l['top']:.1f}, x0={l['x0']:.1f})")
        if len(lines) > 6:
            last = lines[-1]
            print(f"  Bottom line: '{last['text']}' (size={last['chars'][0]['size']:.1f}, font={last['chars'][0]['fontname']}, top={last['top']:.1f}, x0={last['x0']:.1f})")
