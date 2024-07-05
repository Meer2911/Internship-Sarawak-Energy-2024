import pandas as pd
import tkinter as tk
from tkinter import filedialog
from vsdx import VisioFile
import re
import atexit
import signal
import sys
import inflect

class ListWithListener(list):
    def __init__(self, *args, callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def append(self, item):
        super().append(item)
        if self.callback:
            self.callback(item)

class ExcelProcessor:
    def __init__(self):
        self.listOfExcelFile = ListWithListener(callback=self.onAppendToListOfExcelFile)
        self.listofOriginalDataFrames = ListWithListener(callback=self.onAppendToListOfOriginalDataframes)
        self.listOfDisplayedDataFrames = ListWithListener(callback=self.onAppendToListOfDisplayedDataframes)
        
        # debug variables
        self.kolek = 0
        self.wong = 0

        # for pay scale and designation
        self.listOfPayScaleAndDesignationInconsistencyIDs = []
        self.listOfPayScaleAndDesignationNoRomanIDs = []
        self.listOfPayScaleAndDesignationNoMatchIDs = []


        # for position title and job role
        self.listOfPositionTitleAndJobRoleInconsistencyIDs = []
        self.listOfPositionTitleAndJobRoleNoRomanIDs = []
        self.listOfPositionTitleAndJobRoleNoMatchIDs = []
    
    def cleanup(self):
        self.listOfExcelFile.clear()

        # Clear the DataFrames in listofOriginalDataFrames
        for df in self.listofOriginalDataFrames:
            if df is not None:
                df.drop(df.index, inplace=True)
        
        # Clear the DataFrames in listOfDisplayedDataFrames
        for df in self.listOfDisplayedDataFrames:
            if df is not None:
                df.drop(df.index, inplace=True)
        
        self.listofOriginalDataFrames.clear()
        self.listOfDisplayedDataFrames.clear()

    # callback methods (listeners for list)
    def onAppendToListOfExcelFile(self, item):
        return

    def onAppendToListOfOriginalDataframes(self, item):
        # cross check on the data within the dataframe everytime a new dataframe is added
        item_processed = item.apply(self.processRow, axis=1)
        print("Correct:", self.kolek)
        print("Wrong:", self.wong)
        return item_processed

    def onAppendToListOfDisplayedDataframes(self, item):
        return
    
    # adjust based on format from excel file (extracted from database)
    def createDataframe(self, excel_file_path):
        # Read the Excel file, skipping first 2 rows
        df = pd.read_excel(excel_file_path, skiprows=1)
        # Set the 3rd row as column headers
        df.columns = df.iloc[0]
        # Start DataFrame from 4th row
        df = df[1:]

        return df

    # open Excel file and read the data into a DataFrame
    def openExcelFile(self):
        # Open file dialog to select Excel file
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        excel_file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xlsx")])

        root.destroy()
        if excel_file_path:
            self.listOfExcelFile.append(excel_file_path)
            df = self.createDataframe(excel_file_path)

            df.columns = df.columns.str.strip()
            self.listofOriginalDataFrames.append(df)
            self.listOfDisplayedDataFrames.append(df)

            return excel_file_path 
        else:
            print("No excel file selected.")

    # open Visio file and return file path
    def openVisioFile(self):
        # Open file dialog to select Visio file
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        visio_file_path = filedialog.askopenfilename(title="Select Visio File", filetypes=[("Visio files", "*.vsdx")])

        root.destroy()
        if visio_file_path:
            return visio_file_path
        else:
            print("No visio file selected.")
            return None
    
    # pay scale (reference) and designation (checking)
    def processPayScaleAndDesignation(self, row):
        # Check if the column 'Incumbent(s) Pay Scale Level' is NaN or None
        if pd.isnull(row['Incumbent(s) Pay Scale Level']):
            self.kolek += 1
            return True

        # Convert the column value to string
        incumbent_pay_scale_level = str(row['Incumbent(s) Pay Scale Level'])

        # Updated regex pattern to recognize the specified formats
        grade_pattern = r'MYS/Sarawak/SEB/([^/]+)/([^/]+)(?:/[^/]+)?'

        # Extract grade and additional info using regex
        match = re.search(grade_pattern, incumbent_pay_scale_level)
        if match:
            salary_grade = match.group(1) 
            grade_number_match = re.match(r'([A-Za-z]+)(\d+)', salary_grade)

            if grade_number_match:
                grade_prefix = grade_number_match.group(1)  # 'E', 'NE', etc.
                grade_number = grade_number_match.group(2)  # '1', '5', etc.

                # Extract current title
                current_title = row['Incumbent(s) Designation']
                manager_title = re.search(r'^Manager\b', current_title)
                senior_manager_title = re.search(r'^Senior Manager\b', current_title)
                project_director_title = re.search(r'^Project Director\b', current_title)
                assistant_manager_title = re.search(r'^Assistant Manager\b', current_title)
                assistant_general_manager_title = re.search(r'^Assistant General Manager\b', current_title)

                # get roman numeral from current title
                roman_numeral = re.search(r'\b(I|II)\b', current_title)
                if roman_numeral:
                    if (str(roman_numeral.group()) == "II" and senior_manager_title and (grade_prefix == "E" and grade_number == "7")):
                        self.kolek += 1
                        return True
                    elif (str(roman_numeral.group()) == "I" and (grade_number == "1" or grade_number == "3" or grade_number == "5" or (grade_prefix == "E" and grade_number == "6"))):
                        self.kolek += 1
                        return True
                    elif(str(roman_numeral.group()) == "II" and (grade_number == "2" or grade_number == "4"or grade_number == "7")):
                        self.kolek += 1
                        return True
                    elif(str(roman_numeral.group()) == "II" and grade_prefix == "NE"):
                        self.kolek += 1
                        return True
                    
                    else:
                        print("Possible inconsistency found (pay scale and designation): ", str(row['Position ID']) + " " + current_title + " " + str(grade_number_match.group()))
                        self.wong += 1

                        self.listOfPayScaleAndDesignationInconsistencyIDs.append(row['Position ID'])
                        return False
                else:
                    if manager_title and (grade_prefix == "E" and grade_number == "5"):
                        self.kolek += 1
                        return True
                    elif senior_manager_title and (grade_prefix == "E" and grade_number == "6"): 
                        self.kolek += 1
                        return True
                    elif project_director_title and (grade_prefix == "E" and grade_number == "8"):
                        self.kolek += 1
                        return True
                    elif assistant_manager_title and (grade_prefix == "E" and grade_number == "4"):
                        self.kolek += 1
                        return True
                    elif assistant_general_manager_title and (grade_prefix == "E" and grade_number == "8"):
                        self.kolek += 1
                        return True
                    else: 
                        print("No roman numeral found (pay scale and designation): ", str(row['Position ID']) + " " + current_title + " " + str(grade_number_match.group()))
                        self.kolek += 1 

                        self.listOfPayScaleAndDesignationNoRomanIDs.append(row['Position ID'])
                        return False
        
        else:
            print("No match found for pattern (pay scale and designation): ", incumbent_pay_scale_level)
            
            self.listOfPayScaleAndDesignationNoMatchIDs.append(row['Position ID'])
            return False

        return True
    
    # position title (reference) and job role
    def processPositionTitleAndJobRole(self, row):
        # position title (extracting roman numeral)
        position_title = str(row['Position Title'])
        roman_numeral_pattern = r'\b(I|II)\b'
        senior_manager_title = re.search(r'^Senior Manager\b', position_title) # E6 (might have roman)
        assistant_manager_title = re.search(r'^Assistant Manager\b', position_title) # E4
        assistant_general_manager_title = re.search(r'^Assistant General Manager\b', position_title) # E4
        manager_title = re.search(r'^Manager\b', position_title) # E5
        project_director_title = re.search(r'^Project Director\b', position_title) # E8
        roman_numeral = re.search(roman_numeral_pattern, position_title)

        # job role (extracting grade)
        job_role = row['Job Role']
        job_role_pattern = r'^([^\d]+)(\d)'
        job_role_match = re.search(job_role_pattern, job_role)
        
        if job_role_match:
            job_role_prefix = job_role_match.group(1) # 'E', 'NE', etc.
            job_role_number = job_role_match.group(2) # '1', '5', etc.
            
            if roman_numeral and job_role_match:
                if (str(senior_manager_title) and (str(job_role_prefix) == "E") and (str(job_role_number) == "7") and (str(roman_numeral.group()) == "II")):
                    return True
                elif (str(senior_manager_title) and (str(job_role_prefix) == "E") and (str(job_role_number) == "6") and (str(roman_numeral.group()) == "I")):
                    return True
                elif (str(manager_title) and (str(job_role_prefix) == "E") and (str(job_role_number) == "5") and (str(roman_numeral.group()) == "I")):
                    return True
                elif (str(roman_numeral.group()) == "I" and (str(job_role_number) == "1" or str(job_role_number) == "3" or str(job_role_number) == "5")):
                    return True
                elif (str(roman_numeral.group()) == "II" and (str(job_role_number) == "2" or str(job_role_number) == "4" or str(job_role_number) == "6")):
                    return True
                else:
                    print("Possble inconsistency found (position title and job role): " + str(row['Position ID']) + " " + row['Position Title'] + " " + row['Job Role'])
                    self.kolek -= 1
                    self.wong += 1

                    self.listOfPositionTitleAndJobRoleInconsistencyIDs.append(row['Position ID'])
                    return False
            else:
                if (str(manager_title) and (str(job_role_prefix) == "E") and (str(job_role_number) == "5")):
                    return True
                elif (str(assistant_manager_title) and (str(job_role_prefix) == "E") and (str(job_role_number) == "4")):
                    return True
                elif (str(assistant_general_manager_title) and (str(job_role_prefix) == "E") and (str(job_role_number) == "8")):
                    return True
                elif (str(project_director_title) and (str(job_role_prefix) == "E") and (str(job_role_number) == "8")):
                    return True
                else:
                    print("No roman numeral found (job role and title): " + str(row['Position ID']) + " " + row['Position Title'] + " " + row['Job Role'])
                    self.kolek -= 1
                    self.wong += 1

                    self.listOfPositionTitleAndJobRoleNoRomanIDs.append(row['Position ID'])
                    return False
        else:
            print("No match found for pattern: (job role): " + str(row['Position ID']) + " " + row['Position Title'] + " " + row['Job Role'])
            self.kolek -= 1
            self.wong += 1

            self.listOfPositionTitleAndJobRoleNoMatchIDs.append(row['Position ID'])
            return False              

    # reconcile data in each row (from excel file) for 
    def processRow(self, row):
        if self.processPayScaleAndDesignation(row) and self.processPositionTitleAndJobRole(row):
            return row
        else:
            return None

    # TODO: check the text in the org chart against the data in the DataFrame    
    def checkOrgChartText(self, df, positionID, text):
        row = df[df['Position ID'] == positionID]
        
        # when row is empty or when have missing values
        if row.empty or row.isnull().values.any():
            return ["Row not found in DataFrame or missing values"]
        
        row = row.iloc[0]
        
        position_id = str(row['Position ID'])
        position_title = str(row['Position Title'])
        job_role = str(row['Job Role'])
        formal_name = str(row['Incumbent(s) Formal Name'])
        designation = str(row['Incumbent(s) Designation'])
        
        pay_scale_level_raw = row['Incumbent(s) Pay Scale Level']
        grade_pattern = r'MYS/Sarawak/SEB/([^/]+)/([^/]+)(?:/[^/]+)?'
        match = re.search(grade_pattern, pay_scale_level_raw)
        
        errors = []

        # Split the text into segments based on double newline
        segments = text.split('\n\n')
        
        # Check each segment for the required information
        for segment in segments:
            segment_errors = []
            
            if position_id not in segment:
                segment_errors.append(f"Position ID '{position_id}' not found in segment")
            if position_title not in segment:
                segment_errors.append(f"Position Title '{position_title}' not found in segment")
            if job_role not in segment:
                segment_errors.append(f"Job Role '{job_role}' not found in segment")
            if formal_name not in segment:
                segment_errors.append(f"Incumbent's Formal Name '{formal_name}' not found in segment")
            if designation not in segment:
                segment_errors.append(f"Incumbent's Designation '{designation}' not found in segment")
            
            if match:
                salary_grade = match.group(1)
                grade_number_match = re.match(r'([A-Za-z]+)(\d+)', salary_grade)
                pay_scale_level = grade_number_match.group(0) if grade_number_match else None
                
                if pay_scale_level not in segment:
                    segment_errors.append(f"Pay Scale Level '{pay_scale_level}' not found in segment")
            else:
                segment_errors.append("Pay Scale Level pattern not matched in segment")

            # If there are no errors in this segment, return success
            if not segment_errors:
                return ["All information is correct in this segment"]
            
            # Otherwise, collect the errors for this segment
            errors.extend(segment_errors)
        
        # If no segment matched all information, return the collected errors
        return errors
        
    # TODO: process Visio and Excel file, make comparison for cross validation
    def processVisioFile(self, visio_file_path, excel_file_path):
        # Depth First Search for traversing shapes (find relationship)
        def print_connected_shapes_dfs(shape_id):
            # print(shape_connections)

            if shape_id in processed_shapes:
                return
            processed_shapes.add(shape_id)
            
            for conn_shape_id in shape_connections.get(shape_id, []):
                if conn_shape_id not in processed_shapes:
                    for shape_info in shapes_with_text:
                        # print(shape_info) # add regex here to cross check with the excel file
                        if shape_info[0] == conn_shape_id:
                            print("Connected Shape ID:", conn_shape_id)
                            print("Shape Info:", shape_info)
                            print()
                            print_connected_shapes_dfs(conn_shape_id)

        try:
            df = self.createDataframe(excel_file_path)

            # Extract all unique values from the DataFrame
            unique_departments = set(df['Department'].unique())
            # unique_divisions = set(df['Division'].unique())
            # unique_sections = set(df['Section'].unique())
            # unique_units = set(df['Unit'].unique())

            with VisioFile(visio_file_path) as vis:
                for page_number, page in enumerate(vis.pages, start=1):
                    print(f"=============================== Page {page_number} - {page.name} ===============================")

                    # Collect all shapes with their text and connections
                    shapes_with_text = []
                    shape_connections = {}
                    for shape in page.child_shapes:
                        if shape.text and shape.connected_shapes:
                            shape_id = shape.ID
                            # do validation when position ID is found in the text
                            if re.search(r'\b\d{8}\b', shape.text):
                                try:
                                    text = shape.text
                                    lines = text.splitlines()
                                    cleaned_lines = [line.strip() for line in lines]
                                    text = '\n'.join(cleaned_lines)
                                    self.checkPositionData(text, df)
                                    print("=====================================")
                                except Exception as e:
                                    print(f"Error checking position data")
                                    print(e)
                                    pass
                            # print(shape_id)
                            # print(shape.text)
                            # print(shape)

                            # TODO: make it so that it only extract text colours when going through information (not information for departments, division etc)
                            # try:
                            #     self.extractTextColors(shape)
                            # except Exception as e:
                            #     print(f"Unable to extract colors from shape, please check manually")
                            #     print("Shape is with text:", shape.text)
                            
                            # position_id_pattern = r'\b\d+\b'
                            # position_id_match = re.search(position_id_pattern, shape.text)
                            # if position_id_match:
                            #     position_id = position_id_match.group(0)                        
                            #     try:
                            #         errors = self.checkOrgChartText(df, position_id, shape.text) # fix here crap (need figure out the logic to check the correct row, maybe through position id?)
                            #         for error in errors:
                            #             print(f"{error}")
                            #         print("=====================================")
                            #     except Exception as e:
                            #         print("Error checking org chart text")
                            #         print(e)
                            #         print("=====================================")
                            # else:
                            #     print("Position ID not found in shape text")
                            
                            shapes_with_text.append((shape_id, shape.text))
                            connected_ids = [conn_shape.ID for conn_shape in shape.connected_shapes]
                        if connected_ids:
                            shape_connections[shape_id] = connected_ids
                        

                    # Set to track processed shapes
                    processed_shapes = set()

                    # find the topmost shape which has corresponding 'Department' from dataframe
                    topmost_shape_id = None
                    for shape_info in shapes_with_text:
                        if any(department in shape_info[1] for department in unique_departments):
                            topmost_shape_id = shape_info[0]
                            # print(shape_info)
                            break

                    if topmost_shape_id is not None:
                        print_connected_shapes_dfs(topmost_shape_id)

                        # Print total number of shapes processed
                        print(f"Total shapes: {len(shapes_with_text)}")
                        print(f"Total shapes processed: {len(processed_shapes)}")
                        
                        input("Press Enter to continue to next page...")
                    
        except Exception as e:
            print(f"Error processing Visio file: {e}")
            print("Ensure the visio file is of correct format (.vsdx, NOT .vsd) and not corrupted.")
    
    # TODO: based on updated dataframe, save the file
    def saveExcelFile(self):
        return
    
    # extract text the unique text colors from the text inside the shape
    def extractTextColors(self, shape):
        # get text color(s) from shape.text to check the text color
        shape.get_text_colors()

        # from the list, get unique elements that have #
        colors = [color for color in shape.get_text_colors() if '#' in color]

        # filter the list to get the color that are unique
        unique_colors = []
        if colors != []:
            unique_colors = list(set(colors))

        return unique_colors

    # functions used to check for the information in the shapes (position id, name etc)
    def categoriseGrades(self, clean_block):
        grade_identifiers = ["NE1", "NE2", "NE3", "NE4", "NE5", "NE6", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
                            "SG1", "SG2", "SG3", "SG4", "SG5", "NE1*", "NE2*", "NE3*", "NE4*", "NE5*", "NE6*", "E1*", "E2*", "E3*", "E4*", "E5*", "E6*", "E7*", "E8*", 
                            "SG1*", "SG2*", "SG3*", "SG4*", "SG5*"]
        
        primary_identifiers = ["NE1*", "NE2*", "NE3*", "NE4*", "NE5*", "NE6*", "E1*", "E2*", "E3*", "E4*", "E5*", "E6*", "E7*", "E8*", 
                            "SG1*", "SG2*", "SG3*", "SG4*", "SG5*"]
        
        # Split the clean block into words
        words = re.split(r'\s+|/', clean_block)

        job_grade = None
        salary_grade = None

        possible_grades = [word for word in words if word in grade_identifiers]

        if (len(possible_grades) == 2):
            job_grade = possible_grades[0]
            salary_grade = possible_grades[1]
        elif (len(possible_grades) == 3 or len(possible_grades) == 4):
            for i in range(min(len(possible_grades), 2)):
                if possible_grades[i] in primary_identifiers:
                    job_grade = possible_grades[i]
                    break
            
            # Assign remaining grades as salary grade
            salary_grade = possible_grades[-1]

        # remove stars from job grade and salary grade
        try:
            job_grade = job_grade.replace("*", "")
            salary_grade = salary_grade.replace("*", "")
        except:
            pass

        # print("Job grade:", job_grade)
        # print("Salary grade:", salary_grade)
        return job_grade, salary_grade

    def checkExactMatch(self, target, clean_block):
        clean_words = clean_block.split()
        target_words = target.split()

        # possible short form for 'Senior'
        if "Senior" in target_words:
            if ("Sr" in clean_words and "Senior" not in clean_words):
                clean_words.append("Senior")

        if "Ak" in target_words:
            if ("Ak." in clean_words and "Ak" not in clean_words):
                clean_words.append("Ak")

        # print("Clean words:", clean_words)
        # print("Target words:", target_words)
        return all(word in clean_words for word in target_words)

    def removeUnwantedParentheses(self, text):
        # Define a regex pattern to match text inside parentheses
        parentheses_pattern = re.compile(r'\((.*?)\)')

        def replacer(match):
            return ''  # Remove the text inside parentheses

        # Substitute the matches using the replacer function
        return re.sub(parentheses_pattern, replacer, text).strip()

    # using regex, get information to check for data reconciliation
    def prepDataForValidation(self, position_title_raw, job_role_raw, salary_scale_raw):
        position_title = re.sub(r'\(.*?\)', '', position_title_raw).strip()

        job_role_pattern = r'^([^\d]+)(\d)'
        job_role_match = re.search(job_role_pattern, job_role_raw)

        job_role_prefix = job_role_match.group(1) # 'E', 'NE', etc.
        job_role_number = job_role_match.group(2) # '1', '5', etc.
        job_role = job_role_prefix + job_role_number

        grade_pattern = r'MYS/Sarawak/SEB/([^/]+)/([^/]+)(?:/[^/]+)?'
        salary_scale_match = re.search(grade_pattern, salary_scale_raw)
        if not salary_scale_match:
            salary_scale = None
        else:
            salary_scale = salary_scale_match.group(1)

        return position_title, job_role_prefix, job_role_number, job_role, salary_scale

    def isRomanNumeral(self, word):
        return re.match(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)$", word) is not None

    # to determine plural form of position title
    def pluralisePositionTitle(self, title):
        words = title.split()
    
        if len(words) < 2:
            p = inflect.engine()
            return p.plural(title)

        # Identify the word to be pluralized (the last word that is not a Roman numeral)
        last_non_roman_index = len(words) - 1
        for i in range(len(words) - 1, -1, -1):
            if not self.isRomanNumeral(words[i]):
                last_non_roman_index = i
                break

        # Pluralize the identified word
        p = inflect.engine()
        words[last_non_roman_index] = p.plural(words[last_non_roman_index])
        
        # Reassemble the title
        pluralized_title = ' '.join(words)
        
        return pluralized_title

    def checkPositionData(self, text, df):
        # Split the text by double newlines if there are multiple blocks
        text_blocks = text.split('\n\n')
        
        # Initialize a list to hold all errors
        all_errors = []
        # Process each block of text separately
        for block in text_blocks:
            clean_block = self.removeUnwantedParentheses(block)

            # remove spacing / white spaces
            clean_block = clean_block.strip()
            
            # Extract the position id from the cleaned block
            position_id_match = re.findall(r'\d{8}', clean_block)

            # save all text shape into txt file (debugging purposes)
            with open("text.txt", "a") as f:
                f.write(str(clean_block) + "\n" + "=====================================\n")

            if not position_id_match:
                all_errors.append(f"No position ID found in block:\n{block}\n")
                continue

            if len(position_id_match) > 1:
                initial_line = clean_block.split("\n")[0]
                pattern = r'\n(?=\d{8})'
                split_blocks = re.split(pattern, clean_block[len(initial_line):].strip())
                final_blocks = [initial_line + '\n' + block.strip() for block in split_blocks if block.strip()]

                for person in final_blocks:
                    # pattern to find position id
                    position_id_pattern = r'\d{8}'
                    position_id_match = re.search(position_id_pattern, person)

                    position_id = position_id_match.group(0)
            
                    # Check for corresponding row in the dataframe
                    position_row = df[df['Position ID'] == int(position_id)]
                    
                    if position_row.empty:
                        all_errors.append(f"Position ID: {position_id} not found in excel file")
                        continue
                    
                    # validation if position is vacant
                    if position_row['Incumbent(s) Formal Name'].isnull().all():
                        if ("Vacant" in person or "vacant" in person):
                            print(f"All data found in text block" + position_id)
                            return
                        else:
                            all_errors.append(f"Position ID {position_id} should be vacant")
                        continue
                    
                    position_row = position_row.iloc[0]
                    
                    # Extract attributes
                    position_title_raw = position_row['Position Title']
                    job_role_raw = position_row['Job Role']
                    formal_name = position_row['Incumbent(s) Formal Name']
                    salary_scale_raw = position_row['Incumbent(s) Pay Scale Level']
                    
                    position_title, job_role_prefix, job_role_number, job_role, salary_scale = self.prepDataForValidation(position_title_raw, job_role_raw, salary_scale_raw)

                    if salary_scale is None:
                        all_errors.append(f"Salary scale pattern not found in '{salary_scale_raw}'")
                        continue
                    
                    # Check whether each attribute is in the cleaned block
                    errors = []
                    
                    job_grade, salary_grade = self.categoriseGrades(person)
                    
                    try:
                        if "I/II*" in person:
                            person = person.replace("I/II*", "II")
                        elif "I/ II*" in person:
                            person = person.replace("I/ II*", "II")
                        elif "I*/II" in person:
                            person = person.replace("I*/II", "I")
                        elif "I*/ II" in person:
                            person = person.replace("I*/ II", "I")
                        else:
                            pass
                    except:
                        pass

                    # add plural form for position title
                    plural_position_title = self.pluralisePositionTitle(position_title)

                    try:
                        if not self.checkExactMatch(plural_position_title, person):
                            if not self.checkExactMatch(position_title, person):
                                errors.append(f"Position title '{position_title}' incorrect")
                        if not self.checkExactMatch(job_role, job_grade):
                            errors.append(f"Job role '{job_role}' incorrect")
                        if not self.checkExactMatch(formal_name, person):
                            errors.append(f"Formal name '{formal_name}' incorrect")
                        if not self.checkExactMatch(salary_scale, salary_grade):
                            errors.append(f"Salary grade '{salary_grade}' incorrect")
                            errors.append("Please double check the salary grade in the text block (if not, probably is contractor, vacant, or specialist position)")            
                    except:
                        continue

                    # Collect errors for the block
                    if errors:
                        errors.append(person + "\n")
                        all_errors.extend(errors)
                        print(f"Errors found in text block")
                    else:
                        print(f"All data found in text block" + position_id)
            else:
                position_id = position_id_match[0]
                
                # Check for corresponding row in the dataframe
                position_row = df[df['Position ID'] == int(position_id)]
                
                if position_row.empty:
                    all_errors.append(f"Position ID: {position_id} not found in excel file")
                    continue
                
                # validation if position is vacant
                if position_row['Incumbent(s) Formal Name'].isnull().all():
                    if ("Vacant" in clean_block or "vacant" in clean_block):
                        print(f"All data found in text block")
                        return
                    else:
                        all_errors.append(f"Position ID {position_id} should be vacant")
                    continue
                
                position_row = position_row.iloc[0]
                
                # Extract attributes
                position_title_raw = position_row['Position Title']
                job_role_raw = position_row['Job Role']
                formal_name = position_row['Incumbent(s) Formal Name']
                salary_scale_raw = position_row['Incumbent(s) Pay Scale Level']
                
                position_title, job_role_prefix, job_role_number, job_role, salary_scale = self.prepDataForValidation(position_title_raw, job_role_raw, salary_scale_raw)
                
                if salary_scale is None:
                    all_errors.append(f"Salary scale pattern not found in '{salary_scale_raw}'")
                    continue
                
                # Check whether each attribute is in the cleaned block
                errors = []
                
                job_grade, salary_grade = self.categoriseGrades(clean_block)
                
                try:
                    if "I/II*" in clean_block:
                        clean_block = clean_block.replace("I/II*", "II")
                    elif "I/ II*" in clean_block:
                        clean_block = clean_block.replace("I/ II*", "II")
                    elif "I*/II" in clean_block:
                        clean_block = clean_block.replace("I*/II", "I")
                    elif "I*/ II" in clean_block:
                        clean_block = clean_block.replace("I*/ II", "I")
                    else:
                        pass
                except:
                    pass

                try: 
                    if not self.checkExactMatch(position_title, clean_block):
                        errors.append(f"Position title '{position_title}' incorrect")
                    if not self.checkExactMatch(job_role, job_grade):
                        errors.append(f"Job role '{job_role}' incorrect")
                    if not self.checkExactMatch(formal_name, clean_block):
                        errors.append(f"Formal name '{formal_name}' incorrect")
                    if not self.checkExactMatch(salary_scale, salary_grade):
                        errors.append(f"Salary grade '{salary_grade}' incorrect")
                        errors.append("Please double check the salary grade in the text block (if not, probably is contractor, vacant, or specialist position)")            
                except:
                    continue

                # Collect errors for the block
                if errors:
                    errors.append(clean_block + "\n")
                    all_errors.extend(errors)
                    print(f"Errors found in text block")
                else:
                    print(f"All data found in text block" + position_id)
        
        # Print all collected errors
        if all_errors:
            for error in all_errors:
                print(error)

    def main(self):
        # TODO: main loop to ask for user input (test, will need to update to GUI later)
        while True:
            print("1. Open Excel File")
            print("2. Process and compare Visio and Excel File")
            print("3. Exit")
            choice = input("Enter choice: ")
            if choice == "1":
                self.openExcelFile()

                print("\nPay scale and designation inconsistencies:")
                print("Total IDs with inconsistencies:", len(self.listOfPayScaleAndDesignationInconsistencyIDs))
                print("Total IDs with no roman numerals:", len(self.listOfPayScaleAndDesignationNoRomanIDs))
                print("Total IDs with no matches:", len(self.listOfPayScaleAndDesignationNoMatchIDs))

                print("\nPosition title and job role inconsistencies:")
                print("Total IDs with inconsistencies:", len(self.listOfPositionTitleAndJobRoleInconsistencyIDs))
                print("Total IDs with no roman numerals:", len(self.listOfPositionTitleAndJobRoleNoRomanIDs))
                print("Total IDs with no matches:", len(self.listOfPositionTitleAndJobRoleNoMatchIDs))

            elif choice == "2":
                # open and save file names
                excel_file_path = self.openExcelFile()
                visio_file_path = self.openVisioFile()
                if visio_file_path and excel_file_path:
                        self.processVisioFile(visio_file_path, excel_file_path)
                        # remove the latest excel file from the list
                        self.listOfExcelFile.pop()
                        self.listofOriginalDataFrames.pop()
                        self.listOfDisplayedDataFrames.pop()
                else:
                    print("No files selected.")
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    # initialise processor and register cleanup function to call upon exit
    processor = ExcelProcessor()
    atexit.register(processor.cleanup)

    def signalHandler(sig, frame):
        processor.cleanup()
        sys.exit(0)

    # signal handler
    signal.signal(signal.SIGINT, signalHandler)

    try:
        processor.main()
    except SystemExit:
        pass
    except:
        processor.cleanup()
        raise