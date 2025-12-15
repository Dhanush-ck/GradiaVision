import pdfplumber

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



        # print(data)

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

        # for i in subjects:
        #     print(i.values())


        for line in lines:
            if "Total Marks (%)" in line:
                data["total_percentage"] = line.split()[3]
                data["sgpa"] = line.split()[5]
                data["grade"] = line.split()[7]
                # print(line.split()[3])
                # print(line.split()[5])
                # print(line.split()[7])
            # if "CGPA" in line and "SGPA" in line:
            #     data["cgpa"] = line.split()[-1]
            #     # print(line.split()[-1])
            #     print(line)

        tables = page.extract_tables()
        data["cgpa"] = tables[1][2][-1]
        # print(tables[1][2][-1])

    for i, j in data.items():
        print(i, j)
    return data


def extract_marklist_data(pdf_path):
    data = {}

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]

        text = page.extract_text()

        lines = text.split("\n")

        for line in lines:
            if "Name" in line and "Course" not in line:
                data['name'] = line.split(":")[1].strip()

            elif "Reg No" in line:
                data['prn'] =  line.split(':')[1][:16].strip()
                data['regno'] = line.split(" ")[-1].strip()

            elif "Programme" in line:
                data['programme'] = line.split(":")[1].strip()

            elif "Semester :" in line:
                semester_text = line.split(":")[-1].strip()
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

    return data 