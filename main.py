import os
import sys 
import json
import time

import constants as c
import utils as ut
import settings as sett
import file_generator as fg
import tester as t



def parse_input(argv):
    ut.print_header(header_text='AllForOne - Automatic Test Generator')
    if len(argv) < 3:
        print('Usage: python main.py <source_folder> <destination_folder>\n')
        sys.exit(1)

    source_folder = argv[1]
    destination_folder = argv[2]

    # Check if src folder exists
    if not os.path.isdir(source_folder):
        print('[ERROR] Source folder does not exist.')
        sys.exit(1)

    # Check if dst folder exists, create if not
    if not os.path.isdir(destination_folder):
        ut.print_info('Destination folder does not exist, creating it...')
        os.makedirs(destination_folder)
        ut.print_info('Destination folder created.')
    
    ut.print_info('Source folder: "{}"'.format(source_folder))
    ut.print_info('Destination folder: "{}"'.format(destination_folder))

    return source_folder, destination_folder


def generate_tests(src, dst):
    start = time.time()
    settings = sett.get_settings(src)    
    num_files = 0
    num_files += len(settings['files'])
    for folder in settings['folders']:
        num_files += len(os.listdir(os.path.join(src, folder)))
    ut.print_info('Number of files from source folder: {}'.format(num_files))
    ut.print_separator(c.LightHorizontalLine)
    
    ut.print_header(header_text='Tests Generation')
    for module_name in settings['files']:
        ut.print_info('Generating tests for module: {}'.format(module_name))
        fg.file_generator(src, dst, module_name)
    for folder in settings['folders']:
        for module_name in os.listdir(os.path.join(src, folder)):
            ut.print_info('Generating tests for module: {}'.format(module_name))
            fg.file_generator(src, dst, module_name)

    end = time.time()
    ut.print_header(header_text='Statistics')
    ut.print_info('Time elapsed: {:.2f} seconds'.format(end - start))
    ut.print_info('Total number of files generated: {}'.format(num_files))
    ut.print_separator(c.DoubleHorizontalLine)
    

if __name__ == '__main__':
    src, dst = parse_input(sys.argv)
    generate_tests(src, dst)
    t.run_tests(dst)
    ut.print_separator(c.DoubleHorizontalLine)
