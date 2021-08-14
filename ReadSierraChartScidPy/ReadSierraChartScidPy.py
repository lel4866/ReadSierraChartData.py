# this program reads data from a local C:/SierraChart/data directory
# it only reads files which start with ESmyy and have a .scid extension
# these are native binary Sierra Chart data files
# m is a futures contract month code: H, M, U, or Z
# yy is a 2 digit year

# the following struct definitions are taken from the Sierra Chart scdatetime.h file
# Times are in UTC

import os
from datetime import datetime, timedelta
import glob
from zoneinfo import ZoneInfo
from ScidStructs import read_hdr, read_ir

datafile_dir = "C:/SierraChart/Data/";
datafile_outdir = "C:/Users/lel48/SierraChartData/";
futures_root = "ES";
futures_root_len = len(futures_root)
futures_codes= { 'H': 3, 'M': 6, 'U': 9, 'Z': 12 }
utc = ZoneInfo('UTC')
eastern = ZoneInfo('America/New_York')
SCDateTimeEpoch = datetime(1899, 12, 30, tzinfo=utc)


def read_sierra_chart_scid():
    start_time = datetime.now()

    files = glob.glob(datafile_dir + futures_root + "*.scid")
    for filename in files:
        process_scid_file(filename);

    end_time = datetime.now()
    print(f"read_sierra_chart_scid time = {(end_time - start_time)}")


def process_scid_file(path: str):
    filename = os.path.basename(path)
    print("processing filename=", filename)
    futures_code = filename[futures_root_len]
    if futures_code not in futures_codes:
        return;

    futures_two_digit_year_str = filename[futures_root_len+1:futures_root_len+3]
    try:
        futures_year = 2000 + int(futures_two_digit_year_str)
    except ValueError:
        return

    end_month = futures_codes[futures_code]
    start_month = end_month - 3
    start_year = end_year = futures_year
    if futures_code == 'H':
        start_month = 12
        start_year = end_year - 1
    elif futures_code == 'Z':
        end_month = 3;
        end_year = end_year + 1

    out_path = datafile_outdir + futures_root + futures_code + futures_two_digit_year_str + ".zip"

    # only keep ticks between start_date and end_date
    #est = ZoneInfo.ZoneInfo('America/New_York')
    start_dt = datetime(start_year, start_month, 9, 18, 0, 0, tzinfo=eastern)
    end_dt = datetime(end_year, end_month, 9, 18, 0, 0, tzinfo=eastern)

    file = open(path, 'rb')
    hdr_tuple = read_hdr(file)

    count = 0;
    while True:
        ir_tuple = read_ir(file)
        if ir_tuple is None:
            break
        count = count + 1

        dt = SCDateTimeEpoch + timedelta(microseconds=ir_tuple[0])
        # convert SCDateTime to Eastern datetime
        dt_et = dt.astimezone(eastern)

if (__name__ == '__main__'):

    #import sys
    #if len(sys.argv) > 1:
    #    print(fact(int(sys.argv[1])))
    read_sierra_chart_scid()