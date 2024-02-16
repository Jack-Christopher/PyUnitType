import os
import sys 
import json
import time
import argparse

import constants as c
import utils as ut
import settings as sett
import file_generator as fg
import tester as t
import classifier as cl
import sampler as sm


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
        ut.print_separator(c.LightHorizontalLine)
        ut.print_info('Generating tests for module: {}'.format(module_name))
        fg.file_generator(src, dst, module_name)
    for folder in settings['folders']:
        ut.print_separator(c.DoubleHorizontalLine)
        for module_name in os.listdir(os.path.join(src, folder)):
            ut.print_separator(c.LightHorizontalLine)
            ut.print_info('Generating tests for module: {}'.format(module_name))
            fg.file_generator(src, dst, module_name)

    end = time.time()
    ut.print_header(header_text='Statistics')
    ut.print_info('Time elapsed: {:.2f} seconds'.format(end - start))
    ut.print_info('Total number of files generated: {}'.format(num_files))
    ut.print_separator(c.DoubleHorizontalLine)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample', action='store_true', help='Sample the dataset')
    parser.add_argument('--train', action='store_true', help='Train the classifier')
    parser.add_argument('--generate-tests', nargs=2, metavar=('source_folder', 'destination_folder'), help='Generate tests')
    parser.add_argument('--run-tests', type=str, help='Run tests')

    args = parser.parse_args()

    if args.sample:
        ut.print_header(header_text='AllForOne - Sampling Mode')
        ut.print_info('Sampling the dataset...')
        sm.sample()
        ut.print_info('Sampling complete.')        
        ut.print_separator(c.DoubleHorizontalLine)

    if args.train:
        ut.print_header(header_text='AllForOne - Training Mode')
        ut.print_info('Training the classifier...')
        cl.train()
        ut.print_info('Training complete.')        
        ut.print_separator(c.DoubleHorizontalLine)

    if args.generate_tests:
        source_folder, destination_folder = args.generate_tests

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

        # store the source and destination folders in a settings file
        settings = {
            'source_folder': source_folder,
            'destination_folder': destination_folder
        }

        settings = sett.get_settings(source_folder)
        settings['source_folder'] = source_folder
        settings['destination_folder'] = destination_folder

        sett.store_settings(source_folder, settings)

        generate_tests(source_folder, destination_folder)
    
    if args.run_tests:
        destination_folder = args.run_tests
        ut.print_header(header_text='AllForOne - Running Tests Mode')
        ut.print_info('Running tests...')        
        t.run_tests(destination_folder)
        ut.print_info('Tests complete.')        
        ut.print_separator(c.DoubleHorizontalLine)


    if not args.sample and not args.train and not args.generate_tests and not args.run_tests:
        ut.print_info('Usage: python main.py <source_folder> <destination_folder>')
        ut.print_info('Example: python main.py /path/to/source /path/to/destination')

        ut.print_info('Optional flags:')
        ut.print_info('  --sample: Sample the dataset')
        ut.print_info('  --train: Train the classifier')
        sys.exit(1)
