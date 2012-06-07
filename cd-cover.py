from pyfpdf import FPDF

pdf=FPDF(unit='mm', format=(120,120))
#pdf.set_margins(left,top,right=-1)
pdf.set_left_margin(0)
pdf.set_top_margin(0)
pdf.set_right_margin(0)
pdf.set_auto_page_break(False,margin=0)
pdf.add_page()

# dummy boxes
pdf.set_font('Arial','B',16)
#pdf.cell(w=30, h=30, txt='dummy', border=1, ln=0, align='C')
#pdf.cell(w=30, h=30, txt='dummy', border=1, ln=1, align='C')
#pdf.cell(w=30, h=30, txt='dummy', border=1, ln=0, align='C')
#pdf.cell(w=30, h=30, txt='dummy', border=1, ln=1, align='C')
#pdf.cell(w=30, h=30, txt='dummy', border=1, ln=0, align='C')
#pdf.cell(w=30, h=30, txt='dummy', border=1, ln=1, align='C')
#pdf.cell(w=30, h=30, txt='dummy', border=1, ln=0, align='C')
#pdf.cell(w=30, h=30, txt='dummy', border=1, ln=1, align='C')

for x in range(2):
    pdf.set_fill_color(255,255 * x,0)
    for y in range(4):
        pdf.set_xy(30 * x ,30 * y)
        pdf.cell(w=30, h=30, txt='dummy', border=1, align='C', fill=True)



# move to right
#pdf.cell(60)
# move down
#pdf.cell(0,5)

# title
#pdf.set_font('Arial','B',16)
#pdf.cell(60,20,'Tech House 001',1,1,'C')

#pdf.cell(w,h=60,10, border=1, txt='Hello World!')
pdf.output('tuto1.pdf','F')
