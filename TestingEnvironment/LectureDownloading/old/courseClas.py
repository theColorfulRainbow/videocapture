

class Course(object):

	'''
	course = {'sectionId': 'c699d9cd-8907-4873-b5cf-98ed1544a81e', 'sectionName': 'Analogue Circuits 2 (ELEE080162017-8SV1SEM1)', 
	'lessonCount': 15, 'courseId': 'e01f4a6c-2967-41c0-943d-e00cb151ad48', 'courseCode': 'ELEE08016', 
	'courseName': 'Analogue Circuits 2', 'termId': '1b4d0f5b-9a93-48eb-8be8-42965853a047'}
	courseTerm = 2017-2018
	'''
	def __init__(sectionId, sectionName, lessonCount, courseId, courseCode, courseName, termId, courseTerm):
		self.sectionId = sectionId  
		self.sectionName = sectionName 
		self.lessonCount = lessonCount 
		self.courseId = courseId
		self.courseCode = courseCode
		self.courseName  = courseName 
		self.termId = termId
		self.courseTerm = courseTerm

	