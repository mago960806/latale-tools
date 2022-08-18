from multiprocessing.connection import answer_challenge
import xlrd

workbook: xlrd.book.Book = xlrd.open_workbook("猜谜题库.xls")
worksheet: xlrd.sheet.Sheet = workbook.sheet_by_name("繁體")
# for index in range(worksheet.nrows):
#     print(worksheet.row(index))
data = {}
quiz_id = 1
for index in range(worksheet.nrows):
    values = worksheet.row_values(index)
    if values[1] == "A:":
        data[quiz_id] = int(values[2])
        quiz_id += 1

for a in data.values():
    print(a)
