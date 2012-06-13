from pyfpdf import FPDF
# NOTE: I have patched hsaudiotag to include label, bpm, and initial_key tags. I will post that when it is more tested
from hsaudiotag import auto
from imghdr import what
import argparse

#TODO throw error if playlist cannot load
#TODO throw error if 0 files are found in playlist
#TODO throw error if we cannot load a file from playlist
#TODO throw error if we cannot write output file or image cache
#TODO add year and/or length
#TODO add watermark 


# verbose output
verbose = False
default_image = 'cache/default.jpg'


def v_print(p):
    if verbose:
        print p


def read_playlist(file_name):
    f = open(file_name, 'U')
    lines = f.readlines()

    # Initialize List
    file_list = []

    for line in lines:
        if (not line.startswith('#')) and len(line.strip()) > 0:
            v_print('adding ' + line.rstrip() + ' to file_list')
            file_list.append(line.rstrip())

    return file_list

    
def get_meta_info(file_list=None):
    # initialize tracks[] for return 
    track_list = []

    # Only use the first 8 songs
    for i, file_path in enumerate(file_list[:8]):
        track = dict()

        v_print('getting meta data for ' + file_path)

        # Get meta data
        hs = auto.File(file_path)
        track['title'] = hs.title
        track['artist'] = hs.artist
        track['label'] = hs.label
        track['bpm'] = hs.bpm
        track['initial_key'] = hs.initial_key

        # Generate artwork
        track['image'] = default_image
        try:
            v_print('getting artwork for ' + file_path)

            artwork = hs.picture
            image_name = 'cache/' + str(i + 1)
            with open(image_name, 'wb') as img:
                img.write(artwork)
            v_print('writing artwork to ' + image_name)

            track['image'] = image_name
        except:
            v_print('could not load art for ' + str(file_path))

        track_list.append(track)

    return track_list


def generate_pdf(track_list=None, output='output.pdf', short_name='CD001', long_name='CD Cover'):
    v_print('generating pdf')

    # Initialize PDF
    pdf=FPDF(unit='mm', format=(120,120))

    # Set Margins
    pdf.set_left_margin(0)
    pdf.set_top_margin(0)
    pdf.set_right_margin(0)
    pdf.set_auto_page_break(False,margin=0)

    # Start Page
    pdf.add_page()

    v_print('drawing album art')

    # Album art boxes
    for y in range(4):
        for x in range(2):
            pdf.set_xy(30 * x ,30 * y)
            pdf.set_font('Arial','B',16)

            # Print album art
            if len(track_list) > (x*4 + y):
                pdf.image(name = track_list[x*4 + y]['image'], type = what(track_list[x*4 + y]['image']), x=30 * x , y=30 * y, w=30, h=30)


    v_print('drawing cd titles')

    # Print title of cd
    pdf.set_xy(65,2)
    pdf.set_font('Arial','B',36)
    pdf.cell(w=50, h=12, txt=short_name, border=0, align='C', fill=False)

    # Print subtitle of cd
    pdf.set_xy(65,14)
    pdf.set_font('Arial','B',10)
    pdf.cell(w=50, h=5, txt=long_name, border=1, align='C', fill=False)


    v_print('drawing tracklist')

    # Print tracklist
    for y in range(len(track_list)):
        pdf.set_xy(62,23 + 12*y)

        # Line 1
        pdf.set_font('Arial','B',10)
        pdf.cell(w=50, h=4, txt=str(y+1) + ': ' + track_list[y]['title'], border=0, align='L', fill=False, ln='2')

        # Line 2
        line2 = '      '
        line2 = line2 + track_list[y]['artist']
        pdf.set_font('Arial','',8)
        pdf.cell(w=50, h=3, txt=line2, border=0, align='L', fill=False, ln='2')

        # Line 3
        line3 = '      ' 
        if(track_list[y]['bpm']):
            line3 = line3 + track_list[y]['bpm'] +'BPM ' 
        if(track_list[y]['initial_key']):
            line3 = line3 + track_list[y]['initial_key']
        if(track_list[y]['label']):
            line3 = line3 + ' [' + track_list[y]['label'] + ']'
        pdf.cell(w=50, h=3, txt=line3, border=0, align='L', fill=False)

    v_print('writing pdf file to ' + output)

    # Write pdf file
    pdf.output(output,'F')


def main():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Generate a CD Cover from an M3U Playlist')
    parser.add_argument('-v', '--verbose', help='output logging information', action='store_true')
    parser.add_argument('playlist', help='m3u playlist to read')
    parser.add_argument('short_name', help='short name of the CD')
    parser.add_argument('long_name', help='long name of the CD')
    parser.add_argument('output', help='output filename of PDF')
    args = parser.parse_args()

    if args.verbose:
        global verbose
        verbose = True

    files = read_playlist(args.playlist)
    tracks = get_meta_info(files)
    generate_pdf(tracks, args.output, args.short_name, args.long_name)


if __name__ == '__main__':
    main()

