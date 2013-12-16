import csv
import getopt
import os
import sys
import time
import quadraticsieve

def main(argv):
    file_name = ""
    program_name = ""
    try:
        opts, args = getopt.getopt(argv,"hf:p:",["file=", "program="])
    except getopt.GetoptError:
        print("benchmark.py -p <program and options string> -f <benchmarkdata.csv>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("benchmark.py -f <benchmarkdata.csv>")
            sys.exit()
        elif opt in ("-f", "--file"):
            file_name = arg
        elif opt in ("-p", "--program"):
            program_name = arg
    with open(file_name, 'rt') as csvfile:
        semiprimes = csv.reader(csvfile)
        with open('benchmarkresults.csv', 'w') as resultsfile:
            results = csv.writer(resultsfile)
            for row in semiprimes:
                start = time.clock()
                quadraticsieve.qsieve(int(row[3]))
                end = time.clock()
                results.writerow([row[0], "%f" % (end - start)])
                resultsfile.flush() #because this WILL hit swap

                
if __name__ == "__main__":
        main(sys.argv[1:])
