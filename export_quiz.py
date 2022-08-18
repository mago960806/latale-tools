import xlrd
import csv
from pathlib import Path


TEMP_DIR = Path()
CSV_PATH = Path(TEMP_DIR) / "DATA/CSV"


workbook: xlrd.book.Book = xlrd.open_workbook("猜谜题库.xls")
worksheet: xlrd.sheet.Sheet = workbook.sheet_by_name("繁體")

answers = {}
quiz_id = 1
for index in range(worksheet.nrows):
    values = worksheet.row_values(index)
    if values[1] == "A:":
        answers[quiz_id] = int(values[2])
        quiz_id += 1

with open(CSV_PATH / "QUIZ_Q.csv", encoding="utf-8") as csv_file, open("QUIZ.txt", "w", encoding="gbk") as txt_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        question_id, question_text = row[0], row[2]
        question_answer = row[answers.get(int(question_id)) + 2]

        txt_file.write(f"{question_id}. {question_text}\n")
        txt_file.write(question_answer + "\n\n")
