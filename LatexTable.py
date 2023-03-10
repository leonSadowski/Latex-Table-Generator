'''Create LaTeX tables using arrays with uncertainties
    Version 2.0
'''

import numpy as np 
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
from uncertainties import ufloat as uf
import os



class Table():

    def __init__(self, data, decimals, caption_input, texfile_name,  label_name, column_names, si_setup = 4.2, H_specifier = False):

        def get_tabledata(data, decimals):

            self.num_list = [[] for _ in range(len(data))]  #create list with n (number of arrays in data) 1D arrays (each one containing values in the form of \num{x(y)} later on)

            for list_index, (unp_array,  decimal) in enumerate(zip(data, decimals)):
                for nom_val, std_val in zip(noms(unp_array), stds(unp_array)):
                    if std_val != 0:                                                    #easy improvement to handle values w/o errors (avoid a+/-0)
                        error = str(f'{std_val:.{decimal}f}').replace('.','')
                        self.num_list[list_index].append(f'\\num{{{nom_val:.{decimal}f}({error})}}')
                    else: 
                        self.num_list[list_index].append(f'\\num{{{nom_val:.{decimal}f}}}')
                    

        def make_latextable(caption_input, texfile_name, label_name, column_names, si_setup = 4.2):
            '''Give caption as string-variable and column_names as array with columname-strings'''

            texfile = texfile_name    

            #create table head - file will be overwritten if already existent!
            with open(texfile, "w") as text_file: 
                if H_specifier == True:
                    print(f'\\begin{{table}}[H] \n \t \centering', file = text_file)
                else:
                    print(f'\\begin{{table}} \n \t \centering', file = text_file)
                print(f'\t \caption{{{caption_input}}}', file = text_file)
                print(f'\t \label{{{label_name}}}', file = text_file)
                print(f'\t \sisetup{{table-format={si_setup}}}', file = text_file)

            #check number of columns

            col = len(self.num_list)
            
            #check if correct number of column names is given (returns if not, warning)
            if col != len(column_names):
                print(f"\nWarning: Table '{texfile}': {len(column_names)} column captions given for {col} columns! - No output file produced\n")
                os.remove(texfile)
                return

            #determining numer of columns
            countS = 0  
            with open(texfile, "a") as text_file:
                print('\t \\begin{tabular}{', end = " ", file = text_file)
            while(countS < (col-1)):
                with open(texfile, "a") as text_file:
                    print('S ', end = " ", file = text_file)
                countS = countS + 1 
            if(countS == (col-1)):
                with open(texfile, "a") as text_file:
                    print('S}', file = text_file)


            with open(texfile, "a") as text_file:   
                print('\t \t \\toprule', file = text_file)

            #fiiling in of each column heading
            headcount = 0
            with open(texfile, "a") as text_file:
                print(f"\t \t", end = " ", file = text_file)
            for unit in column_names:
                if(headcount == (col-1)):
                    with open(texfile, "a") as text_file:
                        print(f"{{{unit}}} \\\ ", file = text_file)
                else:
                    with open(texfile, "a") as text_file:
                        print(f"{{{unit}}} & ", end = ' ', file = text_file)
                headcount = headcount + 1

            with open(texfile, "a") as text_file:
                print(f'\t \t \midrule', file = text_file)

            #filling in of values
            linecount = 0
            colcount = 0
            max_line_number = max([len(list_bla) for list_bla in self.num_list])
            while(linecount < max_line_number):      #algorithm runs as long as maximum number of lines of longest columnn not reached
                with open(texfile, "a") as text_file:
                    print(f'\t \t', end = " ", file = text_file)                                    
                while(colcount < (col-1)):
                    with open(texfile, "a") as text_file:
                        try:
                            print(self.num_list[colcount][linecount], ' & ', end = " ", file = text_file) 
                        except IndexError:      #exception occurs when linecount out of range (i.e. column with less lines than longest column of table)
                            print(' & ', end = " ", file = text_file)
                    colcount += 1
                if(colcount == (col-1)):
                    with open(texfile, "a") as text_file:
                        try:
                            print(self.num_list[colcount][linecount], ' \\\  ', file = text_file)  
                        except IndexError: 
                            print(' \\\  ', file = text_file)
                linecount +=1
                colcount = 0

            #table foot
            with open(texfile, "a") as text_file:
                print(f'\t \t \\bottomrule', file = text_file)
                print(f'\t \end{{tabular}}', file = text_file)
                print(f'\end{{table}}', file = text_file)

            
            print(f"\n"
                  f"Latex-Code saved in '{texfile}'.\n")
            

        get_tabledata(data, decimals)
        make_latextable(caption_input, texfile_name, label_name, column_names, si_setup = si_setup)

if __name__ == '__main__':

    #Example of application

    a = unp.uarray([1.000,2.200,3.400,4.500,5.590],[0.19782,0.02023,0.0030,0.40897,0.5768])
    b = unp.uarray([5,4,2,1],[5,4,2,1])
    c = np.array([1,2,3,4,5])

    data = [a,b,c]
    caption_input = 'A table with values including uncertainties.'
    column_names = [r'$E_\gamma \, / \, \mathrm{keV}$', 'Second column', 'third column']

    values = Table(data, decimals = [3,0,0], caption_input = caption_input, texfile_name = 'table.tex', \
                   label_name = 'tab:values', column_names = column_names, si_setup = 1.0, H_specifier = False)
