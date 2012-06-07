from pyfpdf import FPDF
# NOTE: I have patched hsaudiotag to include label, bpm, and initial_key tags. I will post that when it is more tested
from hsaudiotag import auto
from mutagen import File
from imghdr import what

# TODO Make functions for everything


# TODO Get this loaded from m3u or something
files = [
    'temp-music/01.mp3',
    'temp-music/02.mp3',
    'temp-music/03.mp3',
    'temp-music/04.mp3',
    'temp-music/05.mp3',
    'temp-music/06.mp3',
    'temp-music/07.mp3',
    'temp-music/08.mp3'
]


# Get Track Information
tracks = []
for i in range(8):
    track = dict()
    # Get meta data
    hs = auto.File(files[i])
    track['title'] = hs.title
    track['artist'] = hs.artist
    track['label'] = hs.label
    track['bpm'] = hs.bpm
    track['initial_key'] = hs.initial_key


    # Generate artwork
    # TODO Get artwork for aiff files
    track['image'] = 'tmp/default.jpg'
    track['image_type'] = 'jpg'
    try:
        mutagen = File(files[i])
        artwork = mutagen.tags['APIC:'].data
        image_name = 'tmp/img0' + str(i + 1)
        with open(image_name, 'wb') as img:
            img.write(artwork)

        track['image'] = image_name
        track['image_type'] = what(image_name)
    except:
        print 'Could not load art for ' + str(files[i])

    tracks.append(track)


# Initialize PDF
pdf=FPDF(unit='mm', format=(120,120))

# Set Margins
pdf.set_left_margin(0)
pdf.set_top_margin(0)
pdf.set_right_margin(0)
pdf.set_auto_page_break(False,margin=0)

# Start Page
pdf.add_page()


# Album art boxes
for y in range(4):
    for x in range(2):
        pdf.set_xy(30 * x ,30 * y)
        pdf.set_font('Arial','B',16)

        # Set fill color to pink to be noticed
        pdf.set_fill_color(255, 20, 147)

        # Default text if album art fails to load
        pdf.cell(w=30, h=30, txt='FAIL', border=1, align='C', fill=True)

        # Print album art
        pdf.image(name = tracks[x*4 + y]['image'], type = tracks[x*4 + y]['image_type'], x=30 * x , y=30 * y, w=30, h=30)

# Print title of cd
pdf.set_xy(65,2)
pdf.set_font('Arial','B',36)
# TODO Grab text from command line or m3u
pdf.cell(w=50, h=12, txt="DM001", border=0, align='C', fill=False)


# Print subtitle of cd
pdf.set_xy(65,14)
pdf.set_font('Arial','B',10)
# TODO Grab text from command line or m3u
pdf.cell(w=50, h=5, txt="Demo Cover", border=1, align='C', fill=False)


# Print tracklist
for y in range(8):
    pdf.set_xy(62,23 + 12*y)

    # Line 1
    pdf.set_font('Arial','B',10)
    pdf.cell(w=50, h=4, txt=str(y+1) + ': ' + tracks[y]['title'], border=0, align='L', fill=False, ln='2')

    # Line 2
    line2 = '      '
    line2 = line2 + tracks[y]['artist']
    pdf.set_font('Arial','',8)
    pdf.cell(w=50, h=3, txt=line2, border=0, align='L', fill=False, ln='2')

    # Line 3
    line3 = '      ' 
    if(tracks[y]['bpm']):
        line3 = line3 + tracks[y]['bpm'] +'BPM ' 
    if(tracks[y]['initial_key']):
        line3 = line3 + tracks[y]['initial_key']
    if(tracks[y]['label']):
        line3 = line3 + ' [' + tracks[y]['label'] + ']'
    pdf.cell(w=50, h=3, txt=line3, border=0, align='L', fill=False)


# Write pdf file
pdf.output('output.pdf','F')
