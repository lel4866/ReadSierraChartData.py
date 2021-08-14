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
import zipfile
import multiprocessing as mp

from ScidStructs import read_hdr, read_ir

datafile_dir = "C:\\SierraChart\\Data\\";
datafile_outdir = "C:\\Users\\lel48\\SierraChartData\\";
futures_root = "ES";
futures_root_len = len(futures_root)
futures_codes= { 'H': 3, 'M': 6, 'U': 9, 'Z': 12 }
utc = ZoneInfo('UTC')
eastern = ZoneInfo('America/New_York')
SCDateTimeEpoch = datetime(1899, 12, 30, tzinfo=utc)


def read_sierra_chart_scid():
    start_time = datetime.now()

    files = glob.glob(datafile_dir + futures_root + "*.scid")
    pool = mp.Pool(mp.cpu_count())
    pool.map(process_scid_file, files)

    end_time = datetime.now()
    print(f"read_sierra_chart_scid time = {(end_time - start_time)}")


def process_scid_file(path: str):
    filename = os.path.basename(path)
    print("processing filename=", filename)
    futures_code = filename[futures_root_len].upper()
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

    out_fn_base = futures_root + futures_code + futures_two_digit_year_str
    out_path = datafile_outdir + out_fn_base
    out_path_csv = out_path + ".csv"
    out_path_zip = out_fn_base + ".zip"
    out_path_filename = out_fn_base + ".csv"
    os.chdir(datafile_outdir)

    # only keep ticks between start_date and end_date (the 3 months of "active" data)
    start_dt = datetime(start_year, start_month, 9, 18, 0, 0, tzinfo=eastern)
    end_dt = datetime(end_year, end_month, 9, 18, 0, 0, tzinfo=eastern)

    with open(path, 'rb') as file:
        # make sure we can read header
        hdr_tuple = read_hdr(file)

        with open(out_path_filename, 'w') as outfile:
            # write header
            outfile.write('ISODateTime,Close\n')

            count = 0;
            prev_ts = start_dt.timestamp()
            while True:
                # read an scid tick record into a tuple
                ir_tuple = read_ir(file)
                if ir_tuple is None:
                    break
                count = count + 1

                # convert SCDateTime (UTC) to Python datetime in America/New_York time zone
                dt = SCDateTimeEpoch + timedelta(microseconds=ir_tuple[0])
                dt_et = dt.astimezone(eastern)

                # only keep ticks between specified start and end date/times...that is, for the 3 "active" months
                if dt_et < start_dt:
                    continue
                if dt_et >= end_dt:
                    break

                # only keep 1 tick for each second
                tt = dt_et.timetuple()
                ts = dt_et.timestamp()
                if ts == prev_ts:
                    continue
                prev_ts = ts

                # convert tick tuple to string
                outfile.write(f"{dt_et.isoformat(timespec='seconds')},{ir_tuple[1]:.2f}\n")
    
    # convert csv to zip, delete csv
    with zipfile.ZipFile(out_path_zip, 'w') as zip:
        zip.write(out_path_filename)
        os.remove(out_path_csv)


if (__name__ == '__main__'):

    #import sys
    #if len(sys.argv) > 1:
    #    print(fact(int(sys.argv[1])))
    read_sierra_chart_scid()