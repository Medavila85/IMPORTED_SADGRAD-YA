import os
import subprocess
import argparse
import re

# Creates arguments for BUSCO
parser = argparse.ArgumentParser(description='Parameters for BUSCO')

parser.add_argument(
    '-i',
    '--in',
    dest = 'sequence',
    metavar="Sequence File",
    required=True,
    help='Assembled genome sequence file in FASTA format.')

parser.add_argument(
    '-o', '--out',
    dest = 'outdir',
    metavar="Output Folder",
    required=True,
    help='Name for output forlder and files. DO NOT PROVIDE A PATH.')

parser.add_argument(
    '-m', '--Mode',
    dest = 'mode',
    metavar ="Mode", 
    required =True, 
    help='Specify which BUSCO run to run.')

parser.add_argument(
    "-c",
    "--cpu",
    dest="cpu",
    type=int,
    required=False,
    metavar="CPU cores",
    help="Specify the number (N=integer) " "of threads/cores to use.",
    default = 16)

args = parser.parse_args()

# run BUSCO function
cmd = 'busco -i %s -o %s -m %s -c %s'%(args.sequence, args.outdir, args.mode, args.cpu)
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
while process.returncode == None:
    process.stdout.read()
    #data = process.stdout.read()
    #sys.stdout.write(data)
    process.poll()

### Parse BUSCO results ###
# Locates BUSCO summary file output in -o directory
f = ''
for file in os.listdir(args.outdir):
    if re.match('short_summary.', file):
        f = open(args.outdir + '/' + file, 'r')

# regex pattern used to locate percentages in output file (xx.x%) to insert other values
pattern = r'[A-Z]:\b(?<!\.)(?!0+(?:\.)?%)(?:\d|[0-9]\d|100)(?:(?<!100)\.\d+)?%'

for line in f:
    # 'C:' locates summary starting line
    if 'C:' in line:
        out = open(args.outdir + '/busco_summary_results.txt', 'a')
        out.writelines([line.strip(), '\n'])
        # busco_result and combined_result are separate variables to give user choice as to what format to use
        busco_result = line.strip()
        combined_result = busco_result
        match = re.findall(pattern, busco_result)
        line = next(f)
        i = 0
        for i in range(5):
            line = line.strip().split('\t')
            index = combined_result.index(match[i])
            combined_result = combined_result[:index + len(match[i])] + ' (' + line[0] + ' ' + line[1][:-4] + ')' + combined_result[index + len(match[i]):]
            i += 1
            line = next(f)
        out.write(combined_result)

