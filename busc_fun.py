def busco(input_dir, output_dir,):
    import subprocess
    cmd = 'busco -i %scontigs.fasta -o %s -m genome -c 2'%(input_dir, output_dir)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while process.returncode == None:
        process.stdout.read()
        #data = process.stdout.read()
        #sys.stdout.write(data)
        process.poll()

    ### Parse BUSCO results ###
    import os
    import re

    # Locates BUSCO summary file output in -o directory
    f = ''
    for file in os.listdir(output_dir):
        if re.match('short_summary.', file):
            f = open(output_dir + '/' + file, 'r')

    # regex pattern used to locate percentages in output file (xx.x%) to insert other values
    pattern = r'[A-Z]:\b(?<!\.)(?!0+(?:\.)?%)(?:\d|[0-9]\d|100)(?:(?<!100)\.\d+)?%'

    for line in f:
        # 'C:' locates summary starting line
        if 'C:' in line:
            out = open('busco_results.txt', 'a')
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

busco('/export/home/laaguirre/example/spades/', 'out_test_bac')