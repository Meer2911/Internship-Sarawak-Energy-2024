import re
import pandas as pd
import inflect

# functions used to check for the information in the shapes (position id, name etc)
def categoriseGrades(clean_block):
    grade_identifiers = ["NE1", "NE2", "NE3", "NE4", "NE5", "NE6", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
                         "SG1", "SG2", "SG3", "SG4", "SG5", "NE1*", "NE2*", "NE3*", "NE4*", "NE5*", "NE6*", "E1*", "E2*", "E3*", "E4*", "E5*", "E6*", "E7*", "E8*", 
                         "SG1*", "SG2*", "SG3*", "SG4*", "SG5*"]
    
    primary_identifiers = ["NE1*", "NE2*", "NE3*", "NE4*", "NE5*", "NE6*", "E1*", "E2*", "E3*", "E4*", "E5*", "E6*", "E7*", "E8*", 
                         "SG1*", "SG2*", "SG3*", "SG4*", "SG5*"]
    
    # Split the clean block into words
    words = re.split(r'\s+|/', clean_block)

    print(words)

    input("Press Enter to continue...")

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
    job_grade = job_grade.replace("*", "")
    salary_grade = salary_grade.replace("*", "")

    # print("Job grade:", job_grade)
    # print("Salary grade:", salary_grade)
    
    return job_grade, salary_grade

def checkExactMatch(target, clean_block):
    clean_words = clean_block.split()
    target_words = target.split()

    if "Senior" in target_words:
        if ("Sr" in clean_words and "Senior" not in clean_words):
            clean_words.append("Senior")
    
    if "Ak" in target_words:
        if ("Ak." in clean_words and "Ak" not in clean_words):
            clean_words.append("Ak")

    print("Clean words:", clean_words)
    print("Target words:", target_words)
    input("Press Enter to continue...")
    return all(word in clean_words for word in target_words)

def removeUnwantedParentheses(text):
    # Define a regex pattern to match text inside parentheses
    parentheses_pattern = re.compile(r'\((.*?)\)')

    def replacer(match):
        return ''  # Remove the text inside parentheses

    # Substitute the matches using the replacer function
    return re.sub(parentheses_pattern, replacer, text).strip()

# using regex, get information to check for data reconciliation
def prepDataForValidation(position_title_raw, job_role_raw, salary_scale_raw):
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

def isRomanNumeral(word):
    return re.match(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X)$", word) is not None

def pluralisePositionTitle(title):
    words = title.split()

    if len(words) < 2:
        p = inflect.engine()
        return p.plural(title)

    # Identify the word to be pluralized (the last word that is not a Roman numeral)
    last_non_roman_index = len(words) - 1
    for i in range(len(words) - 1, -1, -1):
        if not isRomanNumeral(words[i]):
            last_non_roman_index = i
            break

    # Pluralize the identified word
    p = inflect.engine()
    words[last_non_roman_index] = p.plural(words[last_non_roman_index])
    
    # Reassemble the title
    pluralized_title = ' '.join(words)
    
    return pluralized_title

def checkPositionData(text, df):
    # Split the text by double newlines if there are multiple blocks
    text_blocks = text.split('\n\n')
    
    # Initialize a list to hold all errors
    all_errors = []
    # Process each block of text separately
    for block in text_blocks:
        clean_block = removeUnwantedParentheses(block)

        clean_block = clean_block.strip()
        
        # Extract the position id from the cleaned block
        position_id_match = re.findall(r'\d{8}', clean_block)

        if not position_id_match:
            all_errors.append(f"No position ID found in block:\n{block}")
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
                        print(f"All data found in text block")
                    else:
                        all_errors.append(f"Position ID {position_id} should be vacant")
                    continue
                
                position_row = position_row.iloc[0]
                
                # Extract attributes
                position_title_raw = position_row['Position Title']
                job_role_raw = position_row['Job Role']
                formal_name = position_row['Incumbent(s) Formal Name']
                salary_scale_raw = position_row['Incumbent(s) Pay Scale Level']
                
                position_title, job_role_prefix, job_role_number, job_role, salary_scale = prepDataForValidation(position_title_raw, job_role_raw, salary_scale_raw)

                if salary_scale is None:
                    all_errors.append(f"Salary scale pattern not found in '{salary_scale_raw}'")
                    continue
                
                # Check whether each attribute is in the cleaned block
                errors = []
                
                job_grade, salary_grade = categoriseGrades(person)
                
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
                plural_position_title = pluralisePositionTitle(position_title)
                
                try: 
                    if not checkExactMatch(plural_position_title, person):
                        if not checkExactMatch(position_title, person):
                            errors.append(f"Position title '{position_title}' incorrect")
                    if not checkExactMatch(job_role, job_grade):
                        errors.append(f"Job role '{job_role}' incorrect")
                    if not checkExactMatch(formal_name, person):
                        errors.append(f"Formal name '{formal_name}' incorrect")
                    if not checkExactMatch(salary_scale, salary_grade):
                        errors.append(f"Salary grade '{salary_grade}' incorrect")
                        errors.append("Please double check the salary grade in the text block (if not, probably is contractor, vacant, or specialist position)")            
                except:
                    continue
                
                # Collect errors for the block
                if errors:
                    errors.append(person + "\n")
                    all_errors.extend(errors)
                else:
                    print(f"All data found in text block")
                
                # Print all collected errors
                if all_errors:
                    for error in all_errors:
                        print(error)

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
                else:
                    all_errors.append(f"Position ID {position_id} should be vacant")
                continue
            
            position_row = position_row.iloc[0]
            
            # Extract attributes
            position_title_raw = position_row['Position Title']
            job_role_raw = position_row['Job Role']
            formal_name = position_row['Incumbent(s) Formal Name']
            salary_scale_raw = position_row['Incumbent(s) Pay Scale Level']
            
            position_title, job_role_prefix, job_role_number, job_role, salary_scale = prepDataForValidation(position_title_raw, job_role_raw, salary_scale_raw)
            
            if salary_scale is None:
                all_errors.append(f"Salary scale pattern not found in '{salary_scale_raw}'")
                continue
            
            # Check whether each attribute is in the cleaned block
            errors = []
            
            job_grade, salary_grade = categoriseGrades(clean_block)
            
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

                print("Clean block:", clean_block)
            except:
                pass

            
            try: 
                if not checkExactMatch(position_title, clean_block):
                    errors.append(f"Position title '{position_title}' incorrect")
                if not checkExactMatch(job_role, job_grade):
                    errors.append(f"Job role '{job_role}' incorrect")
                if not checkExactMatch(formal_name, clean_block):
                    errors.append(f"Formal name '{formal_name}' incorrect")
                if not checkExactMatch(salary_scale, salary_grade):
                    errors.append(f"Salary grade '{salary_grade}' incorrect")
                    errors.append("Please double check the salary grade in the text block (if not, probably is contractor, vacant, or specialist position)")            
            except:
                continue
            
            # Collect errors for the block
            if errors:
                errors.append(block + "\n")
                all_errors.extend(errors)
            else:
                print(f"All data found in text block")
    

    # # Print all collected errors
    # if all_errors:
    #     for error in all_errors:
    #         print(error)

# Load the dataframe
df = pd.read_excel('D:\DataManagementSystem\PositionList(19Jun2024)_v1.0.xlsx', skiprows=1)
df.columns = df.iloc[0]
df = df[1:]

# Sample text     
text = '1 Senior Executive - I*/II- E3*/E4\n50001793 Bettina Anak Kantu - E3\n'

checkPositionData(text, df)