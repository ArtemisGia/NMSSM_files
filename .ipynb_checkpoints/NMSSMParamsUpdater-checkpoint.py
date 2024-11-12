import numpy as np 

class NMSSMParamsUpdater:
    ''' This class can be used to modify the run files for NMSSMCalc and NMSSMCalcEW '''
    def __init__(self, filename, vev):
        self.filename = filename
        self.vev = vev
        

    def update_params(self, LAM, kappa, dimensionful_param, mu, mA, mW, beta):
        try:
            # Read the file into a list of lines
            with open(self.filename, 'r') as file1:
                rows = file1.readlines()

            # pen the file for writing (this will overwrite the file content)
            with open(self.filename, 'w') as file:
                for i in range(len(rows)):
                    row = rows[i]

                    # Extract the leading whitespace from the row
                    leading_whitespace = row[:len(row) - len(row.lstrip())]

                    # Remove the leading whitespace and split the row into columns
                    row_parts = row.split()

                    # Check if there are at least 3 parts (flag, value, comment)
                    if len(row_parts) >= 3:
                        # Check if the row starts with '61' or '62'
                        if row_parts[0] == '61':
                            # Find the exact position of the second value
                            original_value_start = row.find(row_parts[1])
                            original_value_end = original_value_start + len(row_parts[1])

                            # Preserve the exact spacing and formatting
                            spacing_before_value = row[:original_value_start]
                            spacing_after_value = row[original_value_end:]

                            # Replace the second entry (the value) with the new LAM value
                            new_value = f"{LAM:.6E}"  # Scientific notation (optional)

                            # Format the new row with the same spacing
                            row = f"{spacing_before_value}{new_value}{spacing_after_value}"
                            
                        if row_parts[0] == '62':
                            # Find the exact position of the second value
                            original_value_start = row.find(row_parts[1])
                            original_value_end = original_value_start + len(row_parts[1])

                            # Preserve the exact spacing and formatting
                            spacing_before_value = row[:original_value_start]
                            spacing_after_value = row[original_value_end:]

                            # Replace the second entry (the value) with the new LAM value
                            new_value = f"{kappa:.6E}"  # Scientific notation (optional)

                            # Format the new row with the same spacing
                            row = f"{spacing_before_value}{new_value}{spacing_after_value}"
                        
                       
                        if row_parts[0] == dimensionful_param:
                            
                            original_value_start = row.find(row_parts[1])
                            original_value_end = original_value_start + len(row_parts[1])
                            
                            spacing_before_value = row[:original_value_start]
                            spacing_after_value = row[original_value_end:]
                            
                            if dimensionful_param == '27':
                                ## From 2.29 in 0910.1785 I get the expression for mHpm
                                mHpm = np.sqrt(mA**2 + mW**2 - self.vev**2 * LAM**2)
                                new_value = f"{mHpm:.6E}"  # Scientific notation 
                                
                            elif dimensionful_param == '63':
                                ## From 6 in 2206.04618 I get the expression for A_lambda -- Where I have assumed that κ=λ
                                Alam = ( mA**2 * np.sin(beta)*np.cos(beta)) / mu -  kappa * self.vev 
                                new_value = f"{Alam:.6E}"  # Scientific notation 
                           
                            row = f"{spacing_before_value}{new_value}{spacing_after_value}"

                    # Write the updated or unchanged row to the file
                    file.write(row)

            print(f"File '{self.filename}' successfully updated with LAM={LAM}")
            return Alam if dimensionful_param == '63' else mHpm
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
            

    def find_higgs_mass(self, filename2):
        mass_value = None
        found_mass_block = False

        try:
            # Open the file for reading
            with open(filename2, 'r') as file:
                for line in file:
                    # Check for the "Block MASS" line
                    if "Block MASS" in line:
                        found_mass_block = True
                        continue  # Move to the next line after "Block MASS"

                    # After finding "Block MASS", search for the row that starts with '25'
                    if found_mass_block and line.strip().startswith('25'):
                        # Split the line by spaces and take the second entry (the value)
                        parts = line.split()
                        if len(parts) > 1:
                            # Save the second entry in the list (index 1)
                            mass_value = float(parts[1])
                        break  # Exit the loop after finding the first "25" row

            return mass_value

        except Exception as e:
            print(f"An error occurred: {e}")
            return mass_value

    def find_mixing_terms(self, filename2):      
        ZH11 = None
        ZH12 = None
        ZH13 = None
        found_mixing_block = False

        try:
            # Open the file for reading
            with open(filename2, 'r') as file:
                for line in file:
                    # Check for the "Block NMHMIX" line
                    if "Block NMHMIX" in line:
                        found_mixing_block = True
                        continue
                    if found_mixing_block:
                        parts = line.split()
                        if len(parts) > 4 and parts[4] == 'ZH(1,1)':
                            ZH11 = float(parts[2])
                            continue
                        if len(parts) > 4 and parts[4] == 'ZH(1,2)':
                            ZH12 = float(parts[2])
                            continue
                        if len(parts) > 4 and parts[4] == 'ZH(1,3)':
                            ZH13 = float(parts[2])
                            continue
                        break 

            return [ZH11, ZH12, ZH13]

        except Exception as e:
            print(f"An error occurred: {e}")
            return [ZH11, ZH12, ZH13]