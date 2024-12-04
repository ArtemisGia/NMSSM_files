import re
class NMSSMFileHandler:
    ''' Designed to read and update the values of the NMSSM parameters in NMSSMTools'''
    def __init__(self, filename):
        self.filename = filename

    # def update_nmssm_params(self, LAM, kappa, tanb):
    #     try:
    #         found_extpar = False
    #         found_minpar = False
    #         # Step 1: Read the file into a list of lines
    #         with open(self.filename, 'r') as file1:
    #             rows = file1.readlines()

    #         # Step 2: Open the file for writing (this will overwrite the file content)
    #         with open(self.filename, 'w') as file:
    #             for i in range(len(rows)):
    #                 row = rows[i]

    #                 # Step 3: Extract the leading whitespace from the row
    #                 leading_whitespace = row[:len(row) - len(row.lstrip())]

    #                 # Remove the leading whitespace and split the row into columns
    #                 row_parts = row.strip().split()
    #                 if "BLOCK MINPAR" in row:
    #                     found_minpar = True
                        
    #                 if found_minpar and len(row_parts) > 3:
    #                     if row_parts[0] == '3':
    #                         row_parts[1] = f"{tanb:.1E}" 
    #                         row = leading_whitespace + ' '.join(row) + '\n'                     
                    
    #                 if "BLOCK EXTPAR" in row:
    #                     found_extpar = True
                    
    #                 # Check if there are at least 3 parts (flag, value, comment)
    #                 if found_extpar and len(row_parts) >= 3:
                        
    #                     if row_parts[0] == '61':
                           
    #                         original_value_start = row.find(row_parts[1])
    #                         original_value_end = original_value_start + len(row_parts[1])

                            
    #                         spacing_before_value = row[:original_value_start]
    #                         spacing_after_value = row[original_value_end:]

                            
    #                         new_value = f"{LAM:.4E}"  # Scientific notation (optional)

    #                         # Format the new row with the same spacing
    #                         row = f"{spacing_before_value}{new_value}{spacing_after_value}"
                            
    #                     if row_parts[0] == '62':
                           
    #                         original_value_start = row.find(row_parts[1])
    #                         original_value_end = original_value_start + len(row_parts[1])

                            
    #                         spacing_before_value = row[:original_value_start]
    #                         spacing_after_value = row[original_value_end:]

                            
    #                         new_value = f"{kappa:.6E}"  # Scientific notation (optional)

    #                         # Format the new row with the same spacing
    #                         row = f"{spacing_before_value}{new_value}{spacing_after_value}"
                            
    #                 # Write the updated or unchanged row to the file
    #                 file.write(row)

    #         print(f"File '{self.filename}' successfully updated with LAM={LAM}")

    #     except Exception as e:
    #         print(f"An error occurred: {e}")

   

    def update_nmssm_params(self, LAM, kappa, tanb, At, Ak, mA ):
        try:
            found_extpar = False
            found_minpar = False
            # Step 1: Read the file into a list of lines
            with open(self.filename, 'r') as file1:
                rows = file1.readlines()
    
            # Step 2: Open the file for writing (this will overwrite the file content)
            with open(self.filename, 'w') as file:
                for i in range(len(rows)):
                    row = rows[i]
    
                    # Step 3: Extract the leading whitespace from the row
                    leading_whitespace = row[:len(row) - len(row.lstrip())]
    
                    # Remove the leading whitespace and split the row into columns
                    row_parts = row.strip().split()
                    
                    # Check if we are in the "BLOCK MINPAR" section
                    if "BLOCK MINPAR" in row:
                        found_minpar = True
                    
                    # If in "BLOCK MINPAR" and the row has more than 3 parts
                    if found_minpar and len(row_parts) > 3:
                        if row_parts[3] == 'TANB':
                            # Replace the value of tanb (2nd element in this case)
                            row_parts[1] = f"{tanb:.1E}"  # Update with tanb value
                            row = leading_whitespace + ' '.join(row_parts) + '\n'
                    
                    # Check if we are in the "BLOCK EXTPAR" section
                    if "BLOCK EXTPAR" in row:
                        found_extpar = True
                    
                    # If in "BLOCK EXTPAR" and the row has at least 3 parts
                    if found_extpar and len(row_parts) >= 3:
                        # For parameter 61 (LAM) replacement
                        if row_parts[0] == '61':
                            row_parts[1] = f"{LAM:.4E}"  # Update with LAM value
                            row = leading_whitespace + ' '.join(row_parts) + '\n'
                        
                        # For parameter 62 (kappa) replacement
                        if row_parts[0] == '62':
                            row_parts[1] = f"{kappa:.4E}"  # Update with kappa value
                            row = leading_whitespace + ' '.join(row_parts) + '\n'

                        # For parameter 64 (AKAPPA) replacement 
                        if row_parts[0] == '64':
                            row_parts[1] = f"{Ak:.4E}"  # Update with LAM value
                            row = leading_whitespace + ' '.join(row_parts) + '\n'

                        # For parameter 124 (mA) replacement 
                        if row_parts[0] == '124':
                            row_parts[1] = f"{mA:.4E}"  # Update with LAM value
                            row = leading_whitespace + ' '.join(row_parts) + '\n'

                        # For parameter AU3
                        if row_parts[0] == '11':
                            row_parts[1] = f"{At:.2E}"  
                            row = leading_whitespace + ' '.join(row_parts) + '\n'

                        # For parameter AD3
                        if row_parts[0] == '12':
                            row_parts[1] = f"{At:.2E}"  
                            row = leading_whitespace + ' '.join(row_parts) + '\n'

                        # For parameter AE3
                        if row_parts[0] == '13':
                            row_parts[1] = f"{At:.2E}"  
                            row = leading_whitespace + ' '.join(row_parts) + '\n'

                        # # For parameter 65 mueff
                        # if row_parts[0] == '65':
                        #     row_parts[1] = f"{mu:.4E}"  # Update with kappa value
                        #     row = leading_whitespace + ' '.join(row_parts) + '\n'

                    
                    # Write the updated or unchanged row to the file
                    file.write(row)
    
            print(f"File '{self.filename}' successfully updated with LAM={LAM}, kappa={kappa}, tanb={tanb}")
    
        except Exception as e:
            print(f"An error occurred: {e}")


    def find_higgs_mass(self, spectr):
        higgs25 = None
        higgs35 = None
        higgs45 = None
        found_mass_block = False

        try:
            # Open the file for reading
            with open(spectr, 'r') as file:
                for line in file:
                    # Check for the "Block MASS" line
                    if "BLOCK MASS" in line:
                        found_mass_block = True
                        continue  # Move to the next line after "Block MASS"
                    
                    # After finding "Block MASS", search for the row that starts with '25'
                    if found_mass_block and line.strip().startswith('25'):
                        # Split the line by spaces and take the second entry (the value)
                        parts = line.split()
                        if len(parts) > 1:
                            # Save the second entry in the list (index 1)
                            higgs25 = float(parts[1])
                            
                    if found_mass_block and line.strip().startswith('35'):
                        # Split the line by spaces and take the second entry (the value)
                        parts = line.split()
                        if len(parts) > 1:
                            # Save the second entry in the list (index 1)
                            higgs35 = float(parts[1])
                            
                    if found_mass_block and line.strip().startswith('45'):
                        # Split the line by spaces and take the second entry (the value)
                        parts = line.split()
                        if len(parts) > 1:
                            # Save the second entry in the list (index 1)
                            higgs45 = float(parts[1])
                            
                    if higgs25 is not None and higgs35 is not None and higgs45 is not None:
                        break
                    
            return [higgs25, higgs35, higgs45]

        except Exception as e:
            print(f"An error occurred: {e}")
            return [higgs25, higgs35, higgs45]


    def find_mixing_terms(self, filename2):
    # Initialize an empty 3x3 matrix
        mixing_matrix = [[None for _ in range(3)] for _ in range(3)]
        found_mixing_block = False
    
        try:
            # Open the file for reading
            with open(filename2, 'r') as file:
                for line in file:
                    # Check for the "Block NMHMIX" line
                    if "BLOCK NMHMIX" in line:
                        found_mixing_block = True
                        continue
                    if found_mixing_block:
                        parts = line.split()
                        if len(parts) > 3:
                            # Get the row and column indices (convert from 1-based to 0-based)
                            i = int(parts[0]) - 1
                            j = int(parts[1]) - 1
                            # Get the matrix value
                            value = float(parts[2])
                            # Store the value in the correct position in the matrix
                            mixing_matrix[i][j] = value
    
                        # Stop after reading the entire 3x3 matrix
                        if all(all(row is not None for row in col) for col in mixing_matrix):
                            break
    
            return mixing_matrix  # Return the full 3x3 matrix
    
        except Exception as e:
            print(f"An error occurred: {e}")
            return mixing_matrix  # Return the matrix even if it's incomplete


    def find_higgs_error(self, spectr):
        
        ''' Function to find and save the uncertainties from the CP even Higgs mass calculations. 
        The order is lightest - second lightest - heaviest CP even Higgs eigenstate '''
        
        higgs_errors = []
        found_error_block = False
    
        try:
            # Open the file for reading
            with open(spectr, 'r') as file:
                for line in file:
                    if "BLOCK DMASS" in line:
                        found_error_block = True
                        continue 
                    if found_error_block:
                        parts = line.split()
                        if len(parts) < 2:
                            continue
                        if parts[1] == '#':
                            higgs_errors.append(float(parts[0]))
                        if len(higgs_errors) == 3:
                            break
            return higgs_errors
    
        except Exception as e:
            print(f"An error occured: {e}")
            return [None, None, None]
            
                            
