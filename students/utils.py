import pdfplumber
import re

def extract_marklist_data_normal(pdf_path):
    data = {}

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]

        text = page.extract_text()

        lines = text.split("\n")

        for line in lines:
            if "Name" in line:
                data['name'] = line.split(":")[1].strip()

            elif "Reg No" in line:
                data['regno'] = line.split(" ")[-1].strip()

            elif "Programme" in line:
                data['programme'] = line.split(":")[1].strip()

            elif "Semester :" in line:
                semester_text = line.split(":")[1].strip()
                if "First" in semester_text:
                    data['semester'] = 1
                elif "Second" in semester_text:
                    data['semester'] = 2
                elif "Third" in semester_text:
                    data['semester'] = 3
                elif "Fourth" in semester_text:
                    data['semester'] = 4
                elif "Fifth" in semester_text:
                    data['semester'] = 5
                elif "Sixth" in semester_text:
                    data['semester'] = 6

        table = page.extract_table()

        subjects = []

        i = 0
        for row in table[1:]:
            if row[0] is None:
                continue

            if "Total" in row[0] :
                continue

            subject = {
                "course_code": "".join(row[0].split('\n')),
                "course_title": " ".join(row[1].split('\n')) if row[1] is not None else row[1],
                "credit": int(row[3]) if row[3] is not None else row[3],
                "max_mark": int(row[4]) if row[4] is not None else row[4],
                "ce": int(row[5]) if row[5] is not None else row[5],
                "ese": int(row[6]) if row[6] is not None else row[6],
                "total": int(row[7]) if row[7] is not None else row[7],
                "gp": float(row[8]) if row[8] is not None else row[8],
                "grade": row[9],
                "cp": float(row[10]) if row[10] is not None else row[10],
                "result": row[11],
            }
  
            if None not in subject.values():
                subjects.append(subject)

        data["subjects"] = subjects

        for line in lines:
            if "Total Marks (%)" in line:
                data["total_percentage"] = line.split()[3]
                data["sgpa"] = line.split()[5]
                data["grade"] = line.split()[7]

        tables = page.extract_tables()
        data["cgpa"] = tables[1][2][-1]

    for i, j in data.items():
        print(i, j)
    return data


def extract_marklist_data_fyugp(pdf_path):
    data = {}

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]

        text = page.extract_text()

        lines = [l.strip() for l in text.split("\n") if l.strip()]

        for line in lines:
            if 'UNIVERSITY' in line:
                data['university'] = line.strip()
                
            if "Name" in line and "Course" not in line:
                data['name'] = line.split(":")[1].strip()

            elif "Reg No" in line:
                data['prn'] =  line.split(':')[1][:16].strip()
                data['regno'] = line.split(" ")[-1].strip()

            elif "Programme" in line:
                data['programme'] = line.split(":")[1].strip()

            elif "Semester:" in line:
                semester_text = line.split(":")[-1].strip()
                if "FIRST" in semester_text:
                    data['semester'] = 1
                elif "SECOND" in semester_text:
                    data['semester'] = 2
                elif "THIRD" in semester_text:
                    data['semester'] = 3
                elif "FOURTH" in semester_text:
                    data['semester'] = 4
                elif "FIFTH" in semester_text:
                    data['semester'] = 5
                elif "SIXTH" in semester_text:
                    data['semester'] = 6

        table = page.extract_table()

        i = 2
        filtered_table = []
        while i < len(table):
            count = 0
            for j in table[i]:
                if j == None:
                    count = count + 1
                    
            if count > 9 and not table[i][0].startswith('SGPA'):
                i = i + 1
                continue
            
            filtered_table.append(table[i])
            i = i + 1

        i = 0
        subjects = []
        while i < len(filtered_table)-2:
            subject = {}
            subject['code'] = filtered_table[i][0]
            subject['name'] = filtered_table[i][1]
            subject['credit'] = int(filtered_table[i][3])
            subject['max'] = {}
            subject['TH'] = {}
            subject['TH']['max'] = {}
            subject['TH']['awarded'] = {}
            subject['TH']['max']['cca'] = check_data(filtered_table[i][4])
            subject['TH']['max']['ese'] = check_data(filtered_table[i][5])
            subject['max']['total'] = check_data(filtered_table[i][6])
            subject['TH']['awarded']['cca'] = check_data(filtered_table[i][7])
            subject['TH']['awarded']['ese'] = check_data(filtered_table[i][8])
            subject['max']['awarded']= check_data(filtered_table[i][9])
            if i != len(filtered_table)-3:
                if filtered_table[i+1][0] == None:
                    subject['PR'] = {}
                    subject['PR']['max'] = {}
                    subject['PR']['awarded'] = {}
                    subject['PR']['max']['cca'] = check_data(filtered_table[i+1][4])
                    subject['PR']['max']['ese'] = check_data(filtered_table[i+1][5])
                    subject['PR']['awarded']['cca'] = check_data(filtered_table[i+1][7])
                    subject['PR']['awarded']['ese'] = check_data(filtered_table[i+1][8])

                    subject['gp'] = int(filtered_table[i][10])
                    subject['grade'] = filtered_table[i][11]
                    subject['cp'] = int(filtered_table[i][12])
                    subject['result'] = filtered_table[i][13]
                    subjects.append(subject)
                    i = i + 2
                    continue
            subjects.append(subject)
            i = i + 1
        data['subjects'] = subjects
        data['total'] = {}
        data['total']['credit'] = filtered_table[-2][3]
        data['total']['max'] = filtered_table[-2][6]
        data['total']['awarded'] = filtered_table[-2][9]
        data['total']['cp'] = filtered_table[-2][12]
        data['sgpa'] = float(filtered_table[-1][0].split(':')[1].strip()[0:4])
    return data 

def check_data(digital_data):
    if digital_data.isdigit():
        return int(digital_data)
    else:
        return 0

