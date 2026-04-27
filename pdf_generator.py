from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font("Arial", "B", 15)
        # Move to the right
        self.cell(80)
        # Line break
        self.ln(20)

    def chapter_title(self, title):
        # Arial 12
        self.set_font("Arial", "B", 14)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 8, title, 0, 1, "L", 1)
        # Line break
        self.ln(4)

    def sub_chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 6, title, 0, 1, "L")
        self.ln(2)

    def chapter_body(self, body):
        # Times 12
        self.set_font("Times", "", 12)
        # Output justified text
        self.multi_cell(0, 6, body)
        # Line break
        self.ln()

def generate_markdown_report(company_name: str, swot_results: dict) -> str:
    # We still keep this function for the Streamlit UI to use if we wanted or if we modify it
    # We will just bypass it for PDF generation and generate PDF directly from dict
    pass

def generate_pdf(company_name: str, swot_results: dict, output_path: str = None):
    pdf = PDF()
    pdf.add_page()
    
    # Main Title
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, f"SWOT Analysis Report: {company_name.upper()}", 0, 1, "C")
    pdf.ln(10)
    
    for category, subcategories in swot_results.items():
        pdf.chapter_title(category)
        for subcat_name, summary in subcategories.items():
            pdf.sub_chapter_title(subcat_name)
            
            # Clean summary to ASCII to prevent fpdf encoding issues
            clean_summary = summary.encode('latin-1', 'replace').decode('latin-1')
            pdf.chapter_body(clean_summary)
            
    if output_path:
        pdf.output(output_path)
        return output_path
    else:
        # Return as bytes for DB storage
        return pdf.output(dest='S')
