from pyfpdf import FPDF

pdf=FPDF(unit='mm', format=(120,120))
#pdf.set_margins(left,top,right=-1)
pdf.set_left_margin(0)
pdf.set_top_margin(0)
pdf.set_right_margin(0)
pdf.set_auto_page_break(False,margin=0)
pdf.add_page()

pdf.set_font('Arial','B',16)

# dummy boxes
for x in range(2):
    for y in range(4):
        pdf.set_fill_color(255 * x,85 * y,0)
        pdf.set_xy(30 * x ,30 * y)
        pdf.cell(w=30, h=30, txt='dummy', border=1, align='C', fill=True)

# title of cd
pdf.set_xy(65,0)
pdf.set_font('Arial','B',36)
pdf.cell(w=50, h=12, txt="TH001", border=0, align='C', fill=False)
pdf.set_xy(65,12)
pdf.set_font('Arial','B',10)
pdf.cell(w=50, h=5, txt="Tech House", border=1, align='C', fill=False)

# tracks
for y in range(8):
    pdf.set_xy(62,21 + 12*y)
    pdf.set_font('Arial','B',10)
    pdf.cell(w=50, h=4, txt=str(y+1) + ': Awesome Song (Original Mix)', border=0, align='L', fill=False, ln='2')
    pdf.set_font('Arial','',8)
    pdf.cell(w=50, h=4, txt='      DJ Overzero / dirtybird', border=0, align='L', fill=False, ln='2')
    pdf.cell(w=50, h=4, txt='      128BPM, 5B', border=0, align='L', fill=False)


# move to right
#pdf.cell(60)
# move down
#pdf.cell(0,5)

# title
#pdf.set_font('Arial','B',16)
#pdf.cell(60,20,'Tech House 001',1,1,'C')

#pdf.cell(w,h=60,10, border=1, txt='Hello World!')
pdf.output('tuto1.pdf','F')
