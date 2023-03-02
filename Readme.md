Python module to generate LaTeX tables using uncertainties.unumpy uarrays (uncertainties package © 2010–2016, Eric O. LEBIGOT) or numpy.arrays for values without uncertainty.

This module allows to create tables of values with uncertainties, that are saved in a .tex-file.
The uncertainties will be displayed in the .tex-table via '\num{x(y)}' when an error is given, else '\num{x}'.

Update notes 2.0:
Removed Restrictions (different lines for each column possible, only one column possible, no temporary txt file necessary)

CAVE:
.tex-files will be overwritten if already existent! 




Example of application:

from LatexTable import Table 

data = [a, b]   #where a and b are arrays with uncertainties, e.g a = unumpy.uarray([1, 2, 3, 4],[0.1, 0.2, 0.3, 0.4]), the use of numpy arrays or unumpy with errors equal to zero will result in value displayed without error

caption_input = 'A table with values including uncertainties.'
column_names = ['First column' , 'Second column']

table = Table(data, decimals = [3 , 0], caption_input = caption_input, texfile_name = 'table.tex', label_name = 'tab:values', column_names = column_names, si_setup = 1.0, H_specifier = False)

Parameters:

 - data: List of arrays with uncertainties
 - decimals: List of significant decimals for each column
 - caption_input: String for the caption of the table
 - texfile_name: Name of the designated .tex-file for the table
 - label_name: Label for the table 
 - column_names: List, containing strings for the headings of each column
 - si_setup: Specifying of siuntix setup, default set to 4.2
 - H_specifier: Bool, if True '[ H ]' is included for table positioning

An example table can be created by executing the python file as main.

The table object does not have any other methods or attributes, initializing it will result in saving the table in the .tex-file.















