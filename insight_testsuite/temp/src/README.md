# Run
There are two ways to run the code:

1. Run the `run.sh` script in the `h1b_statistics-master` directory, or
2. Run the `h1b_counting.py` script in this `src` directory.

# Customize parameters
You can change the following parameters in the **`h1b_counting.py`** script if you wish to customize your analysis:
- `K`: how many top elements to return.
- `FIELDS`: metrics of interest and corresponding possible field names in raw file. For example, `{'occupations': ['SOC_NAME', 'LCA_CASE_SOC_NAME'], 'states': ['WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE']}`.
- `CONDITIONS`: conditions to count values and corresponding possible field names. For example, `{'CERTIFIED': ['CASE_STATUS', 'STATUS']}`.
- `INPUT_FILE`: input filename. The filename should be consistent with the input file's name you want to analyze.
- `OUTPUT_FILE`: generic output filename. The filename must contain string 'K_COL-NAME'.