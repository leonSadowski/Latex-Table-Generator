'''Create LaTeX tables using arrays with uncertainties

    Version 1.5

'''

import numpy as np 
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
from uncertainties import ufloat as uf
import os



class Table():

    def __init__(self, data, decimals, caption_input, texfile_name,  label_name, column_names, si_setup = 4.2, H_specifier = False):

        txtfile_name = 'temp.txt'

        def get_tabledata(data, decimals):

            data_numpy_arrays = []  #list of 2D numpy arrays (array[0] = noms, array[1] = stds in each case)

            num_list = []  #create list with n (number of arrays in data) 1D arrays (each one containing values in the form of \num{x(y)})
            c = 0
            while c < len(data):
                num_list.append([])
                c += 1


            for unp_array, list_index, decimal in zip(data,np.arange(0, len(data)), decimals) :
                for nom_val, std_val in zip(noms(unp_array), stds(unp_array)):
                    error = str(f'{std_val:.{decimal}f}').replace('.','')
                    num_list[list_index].append(f'\\num{{{nom_val:.{decimal}f}({error})}}')
            

            np.savetxt(f'{txtfile_name}', np.array(num_list).T, fmt='%s', delimiter = '\t') #save data in temporary .txt file



        def make_latextable(caption_input, texfile_name, label_name, column_names, si_setup = 4.2):
            '''Give caption as string-variable and column_names as array with columname-strings'''

            #needs to be cleaned up (name of texfile / texile_name)
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
            col = len(np.genfromtxt(txtfile_name, unpack = True, dtype = str)) 
            

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
            count = 0
            colcount = 0
            while(colcount < len(np.genfromtxt(txtfile_name, unpack = True, dtype = str)[0])):      #ACHTUNG: Es wird geprüft, wie viele Elemente das erste Array der genfromtxt arrays hat ([0])
                with open(texfile, "a") as text_file:
                    print(f'\t \t', end = " ", file = text_file)                                      # -> nur unproblematisch solange alle spalten über die gleiche zeilenanzahl verfügen!!
                while(count < (col-1)):
                    with open(texfile, "a") as text_file:
                        print(np.genfromtxt(txtfile_name, unpack = True, dtype = str)[count][colcount], ' & ', end = " ", file = text_file) 
                    count = count + 1
                if(count == (col-1)):
                    with open(texfile, "a") as text_file:
                        print(np.genfromtxt(txtfile_name, unpack = True, dtype = str)[count][colcount], ' \\\  ', file = text_file)   #ein \n vor ', file = rausgenommen - jetzt keine freien zeilen mehr in tex-datei
                colcount = colcount + 1
                count = 0

            #table foot
            with open(texfile, "a") as text_file:
                print(f'\t \t \\bottomrule', file = text_file)
                print(f'\t \end{{tabular}}', file = text_file)
                print(f'\end{{table}}', file = text_file)

            
            print(f"\n"
                  f"Latex-Code saved in '{texfile}'.\n")
            

        get_tabledata(data, decimals)
        make_latextable(caption_input, texfile_name, label_name, column_names, si_setup = si_setup)
        os.remove('temp.txt')





if __name__ == '__main__':

    #Example of application

    a = unp.uarray([1.000,2.200,3.400,4.500,5.590],[0.19782,0.02023,0.0030,0.40897,0.5768])
    b = unp.uarray([5,4,3,2,1],[5,4,3,2,1])

    data = [a,b]
    caption_input = 'A table with values including uncertainties.'
    column_names = [r'$E_\gamma \, / \, \mathrm{keV}$', 'Second column']

    values = Table(data, decimals = [3,0], caption_input = caption_input, texfile_name = 'table.tex', \
                   label_name = 'tab:values', column_names = column_names, si_setup = 1.0, H_specifier = False)