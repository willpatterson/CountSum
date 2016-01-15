********
CountSum
********

**Requires:** Python 3

CountSum is a small python application used to sum and filter the contents of genetic count files. 
CountSum can preform a stand-alone sum operation or a sum operation with a choice of filter.

Filters:
========

1. **zero**      -- Filter if a gene count has a value of zero in any summed count pair.
2. **average**   -- Filter if the average count value of all congruent genes across all files is under a specified threshold.
3. **less_than** -- Filter if the total sum of all congruent genes across all files is under a specified threshold.

Installation: 
=============
::

    $> git clone https://github.com/willpatterson/count_sum.git
    $> cd count_sum
    $> python setup.py install

Usage: 
======
::

    $> csum {-h} {operation} /path/to/count/files {threshold} {-d} {-h}

**Count File Directory Structure:**
For CountSum to process your count files, all count file pairs to be summed need to be in their own directories. To filter all of the summed pairs at once, place the directories containing pairs into one master directory to pass into CountSum. Any subdirectory containing more than two files will be discounted. See the chart below for reference:

::

    master 
    | 
    ++-Subdir_1 
    |   | 
    |   +-Count_file_1 
    |   +-Count_file_2
    |
    ++-Subdir_2
    |   |
    |   +-Count_file_1.1
    |   +-Count_file_2.1


Examples:
=========
::

    $> csum sum /path/to/countfiles ##Sums files
    $> csum average /path/to/countfiles 6 -d ##This will sum your files and filter out average values lower than 6
    $> csum average /path/to/countfiles 6 ##This will sum your files, and set all averages under 6 to 0

    $> csum -h ##Tells you the operations available 
    $> csum {operation} -h ##Gives you information about an operation's commands

