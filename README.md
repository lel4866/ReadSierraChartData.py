# ReadSierraChartScidPy
Python 3.9 version of program to Read Sierra Chart(tm) SCID stock/futures binary data files

This program reads Sierra Chart .scid files from C:/SierraChart/Data directory and writes zipped, filtered CSV files to the local SierraChartData directory.
Filenames must start with the futures root 'ES' (in capitals) and end with the extension 'scid' (in lower case)
On my machine this is at C:/Users/larry/SierraChartData. I have a private GitHub repo named SierraChartData which also has this data

Unlike each .scid file, which contains tick data for the entire contract, 
the written CSV files only contain at most 1 tick per second starting from the 1800 ET on the 9th of the first active month to 1800 ET on the 9th of the expiration month,
a total of 3 months. For each day, there is data from 6pm ET through 4:30pm ET of the following day...the current hours (as of 8/5/2021) of the CME futures contracts.
For each week, there is data from 6pm ET Sunday through 4:30pm ET Friday.
Each tick is written in the form: iso-datetime,price For example: 2021-06-09T18:00:01-04:00,4213.00
The following header is written before any data: ISODateTime,Close

Each input file name is of the form {futures prefix}{futures month code}{2 digit year}{maybe other stuff}.scid, where {futures prefix is capitalized.
It is a binary file whose format is specified in Sierra Chart documentation. Basically each file consists of a header and a number of data records. I have copied the
header files in this repo from the Sierra Chart directory.

# Future work:
wite program to convert these csv file to centered range bars. So, the following sequence of prices:

101.25, 101.00, 101.25, 101.50, 101.75, 101.50, 101.75, 102.00, 102.25, 101.75, 101.50


would become just: 101.25, 101.75, 102.25, 101.75 

# Programming comments:
So...I programmed this in C++, C#, and Python 3.9...and was pleasantly surprised that Python was just as fast...