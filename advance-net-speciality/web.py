import csv
import re

def fix_csv(input_file, output_file):
    headers = ['question', 'ans1', 'ans2', 'ans3', 'ans4', 'ans5', 'ans6', 'correct_ans', 'check_radio', 'topic', 'domain', 'explanation']

    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
        
        # Write the header row
        writer.writerow(headers)
        
        # Skip the original header row
        next(reader, None)
        
        current_row = []
        for row in reader:
            if row and row[0].strip().startswith("NEW QUESTION"):
                if current_row:
                    process_row(current_row, writer)
                current_row = row
            elif row:  # Only extend if the row is not empty
                current_row.extend(row)
        
        # Process the last question
        if current_row:
            process_row(current_row, writer)

def process_row(row, writer):
    # Combine all fields into a single string
    full_text = ' '.join(str(field) for field in row if field)
    
    # Extract question and answers
    question_match = re.search(r'NEW QUESTION \d+(.*?)(?=A\.|$)', full_text, re.DOTALL)
    question = question_match.group(1).strip() if question_match else ''
    
    answers = re.findall(r'([A-F]\. .*?)(?=[A-F]\.|Answer:|$)', full_text, re.DOTALL)
    answers = [ans.strip() for ans in answers]
    
    # Extract correct answer
    correct_ans_match = re.search(r'Answer: ([A-F])', full_text)
    correct_ans = correct_ans_match.group(1) if correct_ans_match else ''
    
    # Convert correct answer to a number between 1 and 6
    correct_ans_num = ord(correct_ans) - ord('A') + 1 if correct_ans else 0
    correct_ans_num = str(correct_ans_num) if 1 <= correct_ans_num <= 6 else ''
    
    # Extract explanation
    explanation_match = re.search(r'Explanation:(.*)', full_text, re.DOTALL)
    explanation = explanation_match.group(1).strip() if explanation_match else ''
    
    # Determine if it's a single-answer or multiple-answer question
    check_radio = 'radio' if len(re.findall(r'Answer: [A-F]', full_text)) == 1 else 'check'
    
    # Prepare the row
    new_row = [question] + answers + [''] * (6 - len(answers))  # Pad answers to 6
    new_row.append(correct_ans_num)
    new_row.append(check_radio)
    new_row.extend(['', '', explanation])  # Add empty topic and domain, then explanation
    
    # Ensure the row has exactly 12 fields
    new_row = new_row[:12]
    if len(new_row) < 12:
        new_row.extend([''] * (12 - len(new_row)))
    
    writer.writerow(new_row)

# Usage
input_file = 'advance.csv'
output_file = 'advance_fixed.csv'
fix_csv(input_file, output_file)

print("CSV file processing completed successfully.")