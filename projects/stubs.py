from random import choice, randint

from django.utils.datetime_safe import datetime

from projects.models import Project, User, Task, TaskComment, File, PersonInProject


def __createExampleProject():
	# just for testing
	project_creator = create_stub_user()
	p = create_stub_project(project_creator)
	p.tasks = [create_stub_task(p, project_creator, create_stub_user()) for _ in range(4)]
	p.people = [create_stub_user() for _ in range(4)]
	p.files = [create_stub_file(project_creator,projectId=p) for _ in range(4)]
	return p

def __createExampleTask():
	# just for testing
	project_creator = create_stub_user()
	t = create_stub_task( __createExampleProject(), create_stub_user(),create_stub_user())
	t.files = [create_stub_file(project_creator,taskId=t) for _ in range(4)]
	t.comments = [ create_stub_task_comment(t,project_creator) for _ in range(4)]
	return t

def __generateRandomDate():
	#return datetime.date()
	myStr = "2011-10-01 15:26"
	return datetime.strptime(myStr, "%Y-%m-%d %H:%M")
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
	u.avatarPath = "stub_imgs/avatar2.jpg"
	u.id = 11100 + randint(0, 99)
	return u


def create_stub_project(createdBy):
	p = Project()
	p.name = "Project A"
	p.complete = randint(0, 20) * 5
	p.description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed condimentum vel neque eget iaculis. Mauris placerat consectetur leo eget tempus. Nullam porta lacinia metus, in laoreet lectus cursus a. Praesent condimentum ligula vitae tellus vehicula, non sodales lectus ultricies. Sed nunc nisi, pulvinar eget pulvinar nec, posuere sed arcu. Vivamus et lacus ut est facilisis faucibus at quis ligula. Aliquam scelerisque dolor lorem, ut blandit libero dapibus id. Duis risus felis, mattis nec consequat non, pellentesque a sem. Maecenas at neque ut enim fermentum vulputate. Vivamus non auctor enim. Fusce sollicitudin ullamcorper massa, at posuere libero commodo sed. Nullam pharetra, diam et ultrices fermentum, tortor felis tincidunt risus, id condimentum nibh leo eu nisl. Cras leo ante, blandit ac bibendum eu, volutpat id nulla."
	p.created = __generateRandomDate()
	p.createdBy = createdBy
	p.modifiedDate = __generateRandomDate()
	p.id = 22200 + randint(0, 99)
	return p

def create_stub_task(projectId, createdBy, personResponsible):
	t = Task()
	t.projectId = projectId
	t.personResponsible = personResponsible
	t.title = "Task A"
	t.type = choice(Task.TASK_TYPES)
	t.status = choice(Task.TASK_STATUS)[1]  #"Open"
	t.deadline = __generateRandomDate()
	t.description = "Duis eget facilisis libero. Morbi eu gravida elit. Phasellus nec tempus nunc. Nullam vehicula dolor fringilla nulla pharetra scelerisque. Proin eu massa eu ligula fringilla congue eu nec odio. Aliquam dictum vestibulum urna, eu elementum massa convallis quis. Proin vehicula viverra elit, sed pretium diam porta ac. Vestibulum quis turpis sed magna luctus mattis. Aenean et placerat urna, ac convallis metus. Etiam lectus ante, venenatis et bibendum congue, convallis et velit. In nulla purus, ultricies ac tincidunt et, lacinia non risus."
	t.created = __generateRandomDate()
	t.createdBy = createdBy
	t.modified = __generateRandomDate()
	t.id = 33300 + randint(0, 99)
	return t

def create_stub_task_comment(taskId, createdBy):
	tc = TaskComment()
	tc.taskId = taskId
	tc.text = "Praesent risus ipsum, faucibus vitae ipsum nec, scelerisque ultricies risus. Integer porttitor, lacus ut ullamcorper ullamcorper, turpis velit imperdiet ipsum, et ultricies ligula elit in libero. Quisque nec turpis diam. Praesent cursus nulla in libero euismod, a adipiscing urna auctor. Quisque congue lacinia vulputate"
	tc.created = __generateRandomDate()
	tc.createdBy = createdBy
	return tc

def create_stub_file(createdBy, projectId=None, taskId=None, ):
	f = File()
	f.taskId = taskId
	f.projectId = projectId
	f.type = choice(File.FILE_TYPE)[1]
	f.path.name = "avatar2.jpg"  # TODO not working
	# f.path.name = django.core.files.File("avatar2.jpg")
	f.created = __generateRandomDate()
	f.createdBy = createdBy
	f.id = 55500 + randint(0, 99)
	return f

def create_stub_person_in_project(projectId, userId, createdBy):
	pip = PersonInProject()
	pip.projectId = projectId
	pip.userId = userId
	pip.role = choice(PersonInProject.PERSON_ROLE)[1]
	pip.created = __generateRandomDate()
	pip.createdBy = createdBy
	pip.id = 66600 + randint(0, 99)
	return pip