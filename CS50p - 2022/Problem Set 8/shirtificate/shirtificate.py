from fpdf import FPDF

def main():
    name = input("Name: ")

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=False, margin=0)

    pdf.set_font("Arial", "B", size=48)
    pdf.cell(0, 64, txt="CS50 Shirtificate", align="C")
    pdf.ln()

    pdf.image("./shirtificate.png", w=190)

    pdf.set_font(size=20)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, h=-250 ,align="C", txt=f"{name} took CS50")
    pdf.output("shirtificate.pdf")


if __name__ == "__main__":
    main()