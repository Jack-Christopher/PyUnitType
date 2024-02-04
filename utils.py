import constants as c

def print_separator(unicode_char, n=100):
    print('\n' + unicode_char*n)

def print_header(n=100, header_text='AllForOne'):
    header_size = len(header_text)
    side = ((n - header_size) // 2) -2
    print('\n' + c.DoubleHorizontalLine*side + '  ' + header_text + '  ' + c.DoubleHorizontalLine*side)
    
def print_info(msg):
    print(c.LightVerticalLine + '[INFO] {}'.format(msg))
