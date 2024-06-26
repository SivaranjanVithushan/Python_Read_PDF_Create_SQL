
import fitz  # PyMuPDF
import re

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    text = ""
    
    # Loop through each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    
    return text

# Extract text from the provided PDF
pdf_path = "/Users/vithushan/Desktop/python/ETC 4262 19 UP N.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

# Step 2: Parse Extracted Text
def parse_grades(text):
    course_code = None
    course_name = None
    grades = []
    lines = text.split('\n')
    index_no = None
    
    for line in lines:
      # Match course code
        if "Course Code" in line:
            match = re.search(r"Course Code\s*:\s*(\w+)", line)
            if match:
                course_code = match.group(1)
                
        # Match course name
        if "Course Name" in line:
            match = re.search(r"Course Name\s*:\s*(.*)", line)
            if match:
                course_name = match.group(1).strip()
                
        # Match index numbers
        match = re.match(r"(EGT/\d+/\d+)", line)
        if match:
            index_no = match.group(1)
        elif index_no:
            # Match full grade text including complex patterns
            grade_match = re.match(r"([A-F][+-]?|\([A-Za-z]+\)|[A-Za-z]+\([A-Z]+\)(?: & [A-Za-z]+\([A-Z]+\))?)", line)
            if grade_match:
                grade = line.strip()
                grades.append((index_no, grade))
                index_no = None  # Reset index_no after finding grade
    
    return course_code,course_name ,grades

course_code, course_name, grades = parse_grades(extracted_text)

# Step 3: Generate SQL Statements
def generate_sql_inserts(course_code, course_name, grades, table_name):
    sql_statements = []
    
    for index_no, grade in grades:
        sql = f"INSERT INTO {table_name} (course_code, course_name, index_no, grade) VALUES ('{course_code}', '{course_name}','{index_no}', '{grade}');"
        sql_statements.append(sql)
    
    return sql_statements

table_name = "student_grades"
sql_statements = generate_sql_inserts(course_code, course_name, grades, table_name)

# Output the SQL statements
for sql in sql_statements:
    print(sql)
