# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:16:51 2021

@author: ajr88
"""

import os
import subprocess
import sys
import argparse

FastQC ='/usr/local/FastQC/fastqc'




parser = argparse.ArgumentParser(description='Parameters')
parser.add_argument('-i', '--input_directory for FQ', metavar="DIRNAME", dest='raw', required=True, help='Required: Input directory with raw fastq files.')
parser.add_argument('-o', '--output_dir', metavar="DIRNAME", dest='outdir', required=True, help='Required: Name of output directory to create.')
args = parser.parse_args()

raw = args.raw
outdir = args.outdir

if os.path.exists(outdir):
      print("Error: Output directory already exists.  Please choose different directory or remove old directory.")
      quit()
os.mkdir(outdir)
os.mkdir('%s/FQ_output'%outdir)

fastq_log = open('%s/fastq_log.txt'%outdir,'a')

comm = '%s %s -o %s/FQ_output'%(FastQC, raw, outdir)
process = subprocess.Popen(comm, stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
process.wait()
fastq_log.write('\n'.join([x.decode('utf-8').rstrip('\n') for x in iter(process.stdout.readlines())]))
fastq_log.write('\n'.join([x.decode('utf-8').rstrip('\n') for x in iter(process.stderr.readlines())]))
fastq_log.write('bwa command: %s\n'%comm)
print("completed")
