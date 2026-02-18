import pdfplumber

def extract_attendace_data(regno_column, attendance_column,pdf_path):
    regno_column -= 1
    attendance_column -=1
    data = []

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]

        table = page.extract_table()
        cleaned_data = []
        for row in table[2:]:
            record = []
            for i in row:
                if i is not None:
                    record.append(i)
            cleaned_data.append(record)

        for i in cleaned_data:
            # if float(i[attendance_column]) < 75:
            #     print(f"Regno - {i[regno_column]}, Attendance - {i[attendance_column]}")
            individual_data = {}
            individual_data['regno'] = i[regno_column][:8]+'0'+i[regno_column][8:]
            individual_data['attendance'] = float(i[attendance_column])
            data.append(individual_data)

        return data