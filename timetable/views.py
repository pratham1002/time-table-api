import xlrd
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET']) 
def CourseData(request):

    course_number=request.GET['course_number']

    loc=("timetable.xlsx")
    wb=xlrd.open_workbook(loc)
    sheet=wb.sheet_by_index(0)

    lectures=[]
    practicals=[]
    tutorials=[]
    section_number=0
    instructors=[]
    row_number=0

    for i in range(sheet.nrows):

        if sheet.cell_value(i,1).lower() == course_number.lower() :
            
            for j in range(sheet.nrows):

                if j == 0:
                    row_number= i
                    instructors.append(sheet.cell_value(i+j,9))
                    try:
                        instructors.append(int(sheet.cell_value(i+j,10)))
                    except :
                        instructors.append(sheet.cell_value(i+j,10))
                    instructors.append(sheet.cell_value(i+j,7))
                    section_number = section_number + 1
                    continue

                elif len(str(sheet.cell_value(i+j,1))):
                    lectures.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                    break

                elif len(str(sheet.cell_value(i+j,2))):
                    lectures.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )

                    instructors=[]
                    section_number=0

                    if sheet.cell_value(i+j,2) == "Tutorial":

                        for k in range(sheet.nrows):
                            if k == 0:
                                row_number=i+j+k
                                instructors.append(sheet.cell_value(i+j+k,9))
                                try:
                                    instructors.append(int(sheet.cell_value(i+j+k,10)))
                                except :
                                    instructors.append(sheet.cell_value(i+j+k,10))
                                instructors.append(sheet.cell_value(i+j+k,7))
                                section_number = section_number + 1
                                continue

                            elif len(str(sheet.cell_value(i+j+k,1))):
                                tutorials.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                                break

                            elif len(str(sheet.cell_value(i+j+k,6))):
                                tutorials.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                                instructors=[]
                                section_number = section_number + 1
                                row_number=i+j+k
                                instructors.append(sheet.cell_value(i+j+k,9))
                                try:
                                    instructors.append(int(sheet.cell_value(i+j+k,10)))
                                except:
                                    instructors.append(sheet.cell_value(i+j+k,10))
                                instructors.append(sheet.cell_value(i+j+k,7))

                            else:
                                instructors.append(sheet.cell_value(i+j+k,7))
                        break

                    if sheet.cell_value(i+j,2) == "Practical":

                        for k in range(sheet.nrows):
                            if k == 0:
                                row_number=i+j+k
                                instructors.append(sheet.cell_value(i+j+k,9))
                                try:
                                    instructors.append(int(sheet.cell_value(i+j+k,10)))
                                except :
                                    instructors.append(sheet.cell_value(i+j+k,10))
                                instructors.append(sheet.cell_value(i+j+k,7))
                                section_number = section_number + 1
                                continue

                            elif len(str(sheet.cell_value(i+j+k,1))):
                                practicals.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                                break

                            elif len(str(sheet.cell_value(i+j+k,6))):
                                practicals.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                                instructors=[]
                                section_number = section_number + 1
                                row_number=i+j+k
                                instructors.append(sheet.cell_value(i + j + k, 9))
                                try:
                                    instructors.append(int(sheet.cell_value(i+j+k,10)))
                                except: 
                                    instructors.append(sheet.cell_value(i+j+k,10))
                                instructors.append(sheet.cell_value(i+j+k,7))

                            else:
                                instructors.append(sheet.cell_value(i+j+k,7))
                        break

                elif len(str(sheet.cell_value(i+j,6))):
                    lectures.append(str(section_number) + ', ' + ', '.join([str(elem) for elem in instructors]) )
                    instructors=[]
                    section_number = section_number + 1
                    row_number=i+j
                    instructors.append(sheet.cell_value(i+j,9))
                    try:
                        instructors.append(int(sheet.cell_value(i+j,10)))
                    except :
                        instructors.append(sheet.cell_value(i+j,10))
                    instructors.append(sheet.cell_value(i+j,7))

                
                else:
                    instructors.append(sheet.cell_value(i+j,7))

            break
    return Response({ "Course_Number":course_number, "lectures":lectures, "practicals": practicals, "tutorials": tutorials, })


