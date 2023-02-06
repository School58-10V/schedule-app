





# def parse_lessons(xml_data, *):
#     lessons = []
#
#     for el in xml_data.findAll('lesson'):
#         lesson = {}
#         lesson['id'] = el.get('id')
#         try:
#             lesson['subject'] = subjects[el.get('subjectid')]
#         except KeyError:
#             lesson['subject'] = '---'
#
#         try:
#             lesson['teacher'] = teachers[el.get('teacherids')]
#         except KeyError:
#             lesson['teacher'] = '---'
#
#         try:
#             lesson['classroom'] = classrooms[el.get('classroomids')]
#         except KeyError:
#             lesson['classroom'] = '---'
#
#         try:
#             lesson['class'] = classes[el.get('classids')]['name']
#         except KeyError:
#             lesson['class'] = '---'
#
#         try:
#             lesson['group'] = groups[el.get('groupids')]['name']
#         except KeyError:
#             lesson['group'] = '---'
#
#         lessons.append(lesson)