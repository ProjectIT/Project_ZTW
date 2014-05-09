from datetime import timezone
from random import choice
from django.utils.datetime_safe import datetime
from projects.models import Project, User, Task, TaskComment, File, PersonInProject

def __generateRandomDate():
	return datetime.date()
# default_timezone = timezone.get_default_timezone()
# value = timezone.make_naive(value, default_timezone)
# return value

def create_stub_user():
	first_names = ["Amelia", "Ava", "Mia", "Lily", "Olivia", "Ruby", "Seren", "Evie", "Ella", "Grace", "Emily", "Jacob",
				   "Oliver", "Riley", "Jack", "Alfie", "Harry", "Charlie", "Dylan", "William", "Mason"]
	last_names = ["Brown", "Johnson", "Jones", "Khan", "Lewis", "Patel", "Roberts", "Smith", "Taylor", "Thomas",
				  "Williams"]
	u = User()
	u.name = choice(first_names)
	u.lastName = choice(last_names)
	u.email = u.lastName + "50@gmail.com"
	u.login = u.name + "50"
	u.password = u.name
	isFemale = first_names.index(u.name) <= first_names.index("Emily")
	u.gender = "Female" if isFemale else "Male"
	u.birthdate = __generateRandomDate()
	u.registerDate = __generateRandomDate()
	u.modifiedDate = __generateRandomDate()
	u.lastLoginDate = __generateRandomDate()


def create_stub_project(createdBy):
	p = Project()
	p.name = "Project A"
	p.complete = 80
	p.description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed condimentum vel neque eget iaculis. Mauris placerat consectetur leo eget tempus. Nullam porta lacinia metus, in laoreet lectus cursus a. Praesent condimentum ligula vitae tellus vehicula, non sodales lectus ultricies. Sed nunc nisi, pulvinar eget pulvinar nec, posuere sed arcu. Vivamus et lacus ut est facilisis faucibus at quis ligula. Aliquam scelerisque dolor lorem, ut blandit libero dapibus id. Duis risus felis, mattis nec consequat non, pellentesque a sem. Maecenas at neque ut enim fermentum vulputate. Vivamus non auctor enim. Fusce sollicitudin ullamcorper massa, at posuere libero commodo sed. Nullam pharetra, diam et ultrices fermentum, tortor felis tincidunt risus, id condimentum nibh leo eu nisl. Cras leo ante, blandit ac bibendum eu, volutpat id nulla."
	p.created = __generateRandomDate()
	p.createdBy = createdBy
	p.modifiedDate = __generateRandomDate()

def create_stub_task(projectId, createdBy, personResponsible):
	t = Task()
	t.projectId = projectId
	t.personResponsible = personResponsible
	t.title = "Task A"
	t.type = choice(Task.TASK_TYPES)[1]
	t.status = choice(Task.TASK_STATUS)[1]  #"Open"
	t.deadline = __generateRandomDate()
	t.description = "Duis eget facilisis libero. Morbi eu gravida elit. Phasellus nec tempus nunc. Nullam vehicula dolor fringilla nulla pharetra scelerisque. Proin eu massa eu ligula fringilla congue eu nec odio. Aliquam dictum vestibulum urna, eu elementum massa convallis quis. Proin vehicula viverra elit, sed pretium diam porta ac. Vestibulum quis turpis sed magna luctus mattis. Aenean et placerat urna, ac convallis metus. Etiam lectus ante, venenatis et bibendum congue, convallis et velit. In nulla purus, ultricies ac tincidunt et, lacinia non risus."
	t.created = __generateRandomDate()
	t.createdBy = createdBy
	t.modified = __generateRandomDate()

def create_stub_task_comment(taskId, createdBy):
	tc = TaskComment()
	tc.taskId = taskId
	tc.text = "Praesent risus ipsum, faucibus vitae ipsum nec, scelerisque ultricies risus. Integer porttitor, lacus ut ullamcorper ullamcorper, turpis velit imperdiet ipsum, et ultricies ligula elit in libero. Quisque nec turpis diam. Praesent cursus nulla in libero euismod, a adipiscing urna auctor. Quisque congue lacinia vulputate"
	tc.created = __generateRandomDate()
	tc.createdBy = createdBy

def create_stub_file(createdBy, projectId=None, taskId=None, ):
	f = File()
	f.taskId = taskId
	f.projectId = projectId
	f.type = choice(File.FILE_TYPE)[1]
	f.path = ""
	f.created = __generateRandomDate()
	f.createdBy = createdBy

def create_stub_person_in_project(projectId, userId, createdBy):
	pip = PersonInProject()
	pip.projectId = projectId
	pip.userId = userId
	pip.role = choice(PersonInProject.PERSON_ROLE)[1]
	pip.created = __generateRandomDate()
	pip.createdBy = createdBy