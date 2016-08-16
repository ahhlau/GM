import re
import os
import shutil

# 
def read(filename):
	with open(filename, 'r') as f:
		lines = filter(None, (line.rstrip() for line in f))
	
	# print lines

	text = []
	for i in lines:
		i = i.lstrip()
		if i[0] == '/':
			# a = i.replace("/* ----------------- ", '')
			# a = a.replace(" ----------------- */", '')
			# # print a
			# text.append(a)
			text.append(" ")
			# print text

		elif '   ' in i and 'description' not in i:
			a, b = i.split('   ')
			text.append(a)
			text.append(b)
		else:
			text.append(i)

	# print lines
	return text

# Read input
def inputFile(filename):
	inputs = []
	with open(filename, 'r') as f:
		lines = filter(None, (line.strip() for line in f))
	for i in lines:
		inputs.append(i)

	return inputs

# Returns a list of job names
def readJobs(filename):
	with open(filename, 'r') as f:
		lines = filter(None, (line.rstrip() for line in f))

	text = []
	job = ['update_job', 'insert_job', 'delete_job', 'delete_box']
	for i in lines:
		i = i.lstrip()
		if 'job_type' in i and 'job:' in i:
			a, b = i.split('job_type:')
			text.append(a.strip())
		else:
			for j in job:
				if j in i:
					text.append(i)
	f.close()

	return text

# Returns a list of all lines
def readFile(filename):
	with open(filename, 'r') as f:
		lines = filter(None, (line.rstrip() for line in f))

	text = []
	for i in lines:
		i = i.lstrip()
		if i[0] == '/':
			pass
		elif i[0] == '#':
			pass
		elif 'job_type' in i:
			a, b = i.split('job_type:')
			text.append(a.strip())
			text.append('job_type: ' + b.strip())
		else:
			text.append(i)
	f.close()

	return text

# Parses file to a list of jobs
def parseJobs(text):
	check = ['update_job', 'insert_job', 'delete_job', 'delete_box']
	job = []
	temp = []

	for i in range(len(text)-1):
		temp.append(text[i])
		for j in check:
			if j in text[i+1]:
				job.append(temp)
				temp = []
	temp.append(text[-1])
	job.append(temp)

	return job

# 
def readBack(filename):
	with open(filename, 'r') as f:
		lines = filter(None, (line.rstrip() for line in f))
	
	# print lines

	text = []
	for i in lines:
		i = i.lstrip()
		if i[0] == '/':
			# a = i.replace("/* ----------------- ", '')
			# a = a.replace(" ----------------- */", '')
			# # print a
			# text.append(a)
			# text.append(" ")
			pass
			# print text

		elif '   ' in i and 'description' not in i:
			a, b = i.split('   ')
			text.append(a)
			text.append(b)
		else:
			text.append(i)

	# print lines
	return text

# 
def jParse(text):
	job = []
	index = []
	for i in range(len(text)):
		if text[i] == ' ':
			index.append(i)
	index.append(len(text))
	# print index

	for i in range(len(index)-1):
		temp = []
		for j in range(len(text)):
			if j > index[i] and j < index[i+1]:
				temp.append(text[j])
				# print text[j]
		job.append(temp)
	# print job
	
	return job

# def valid(jtext):
# 	check = True
# 	failures = 0
# 	job = []
# 	num = 0
# 	checks = ['insert_job', 'update_job', 'delete_job', 'delete_box']
# 	# for i in jtext:
# 	# 	for j in range(len(text)):
# 	# 		for 
# 	for i in range(len(text)):
# 		if text[i] == ' ':
# 			# print text[i+1]
# 			a, b = text[i+1].split(": ")
# 			# print a
# 			if a in checks:
# 				num += 1
# 			if a not in checks:
# 				check = False
# 				failures += 1
# 				job.append(b)

# 	return num, check, failures, job

# def test(text):
# 	check = True
# 	failures = 0
# 	for i in text:
# 		if 'test' in i:
# 			check = False
# 			failures += 1

# 	# return check, failures

# Count jobs
def count(jtext):
	check = ['update_job', 'insert_job', 'delete_job', 'delete_box']
	job = [0, 0, 0, 0] 
	for i in jtext:
		for j in range(len(i)):
			for k in range(len(check)):
				if check[k] in i[j]:
					job[k] += 1

	return job

# Check valid delete jobs:
def deleteJobs(jtext):
	check = True
	failures = 0
	job = []
	for i in jtext:
		for j in range(len(i)):
			if 'delete_job:' in i[j]:
				if len(i) != 1:
					check = False
					failures += 1
					job.append(i)

	return [check, failures, job]

# Check if 'test' in file
def test(jtext):
	check = True
	failures = 0
	job = []
	for i in jtext:
		for j in range(len(i)):
			if 'test' in i[j]:
				check = False
				failures += 1
				a, b = i[0].split(":")
				b = b.strip()
				job.append(b)

	return [check, failures, job]

# Check status: on_ice are in insert_job
def ice(jtext):
	check = True
	failures = 0
	job = []
	for i in jtext:
		# print i
		if 'status: ON_ICE' in i or 'status: on_ice' in i:
			if 'insert_job' not in i[0]:
				check = False
				failures += 1
				a, b = i[0].split(":")
				b = b.strip()
				job.append(b)
				# print '#######################'
				# print i[0]

	return [check, failures, job]

# Check valid statuses
def status(jtext):
	check = True
	failures = 0
	job = []
	checks = ['FAILURE', 'INACTIVE', 'ON_HOLD', 'ON_ICE', 'ON_NOEXEC', 'SUCCESS', 'TERMINATED']
	for i in jtext:
		for j in range(len(i)):
			if 'status:' in i[j]:
				a, b = i[j].split(":")
				b = b.strip()
				if b not in checks:
					check = False
					failures += 1
					c, d = i[0].split(":")
					d = d.strip()
					job.append(d)

	return [check, failures, job]

# Check job name < 64 char
def jobName(jtext):
	check = True
	failures = 0
	job = []
	for i in jtext:
		# print i
		a, b = i[0].split(":")
		b = b.strip()
		if len(b) > 64 or ' ' in b:
			check = False
			failures += 1
			job.append(b)

	return [check, failures, job]

# Check valid owner
def owner(jtext):
	check = True
	failures = 0
	job = []
	for i in jtext:
		for j in range(len(i)):
			if 'owner:' in i[j]:
				a, b = i[j].split(":")
				b = b.strip()
				if b == 'Bautosys':
					if 'sendevent' not in i[j-2]:
						check = False
						failures += 1
						c, d = i[0].split(":")
						d = d.strip()
						job.append(d)

	return [check, failures, job]

# Check valid start_time
def startTimes(jtext):
	check = True
	failures = 0
	job = []
	pattern = re.compile('^"([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]"$|^$')
	for i in jtext:
		for j in range(len(i)):
			# print i
			if 'start_times:' in i[j]:
				# a, b = i[j].split(": ")
				a, b = i[j].split("times:")
				b = b.strip()
				if not pattern.match(b):
					check = False
					failures += 1
					c, d = i[0].split(":")
					d = d.strip()
					job.append(d)

	return [check, failures, job]

# Check valid start_min
def startMins(jtext):
	check = True
	failures = 0
	job = []
	pattern = re.compile('^[\d\d,]*\d\d$')
	for i in jtext:
		for j in range(len(i)):
			if 'start_mins:' in i[j]:
				a, b = i[j].split(":")
				b = b.strip()
				if not pattern.match(b):
					check = False
					failures += 1
					c, d = i[0].split(":")
					d = d.strip()
					job.append(d)

	return [check, failures, job]

# Check valid days_of_week
def daysOfWeek(jtext):
	check = True
	failures = 0
	job = []
	checks = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su', 'all', '']
	for i in jtext:
		for j in range(len(i)):
			if 'days_of_week:' in i[j]:
				a, b = i[j].split(":")
				b = b.strip()
				c = b.split(",")
				for k in c:
					if k not in checks:
						check = False
						failures += 1
						q, w = i[0].split(":")
						w = w.strip()
						job.append(w)

	return [check, failures, job]

# Check valid date_condition
def dateConditions(jtext):
	check = True
	failures = 0
	job = []
	for i in jtext:
		for j in range(len(i)):
			if 'date_conditions:' in i[j]:
				if 'date_conditions: 0' not in i[j]:
					week = False
					times = False
					mins = False
					calendar = False
					timesOrMins = False
					for k in range(len(i)):
						if 'days_of_week:' in i[k]:
							week = True 
						if 'start_times' in i[k]:
							times = True
						if 'start_mins' in i[k]:
							mins = True
						if 'run_calendar' in i[k]:
							calendar = True

					if times != mins:
						timeOrMins = True

					if not(week or timeOrMins) and calendar == False:
						check = False
						failures += 1
						a, b = i[0].split(":")
						b = b.strip()
						job.append(b)

					# if calendar == False and (week == False or timesOrMins == False):
					# 	check = False
					# 	failures += 1
					# 	a, b = i[0].split(": ")
					# 	job.append(b)

	return [check, failures, job]

# Return jobs with calendars
def calendar(jtext, changeID):
	# check = 'No'
	num = 0
	check = True
	failures = 0
	job = []
	for i in jtext:
		for j in range(len(i)):
			if 'run_calendar' in i[j]:
				# check = 'Yes'
				num += 1
				# a, b = i[0].split(":")
				# b = b.strip()
				# job.append(b)

				a, b = i[j].split(":")
				b = b.strip()
				b = b + '.txt'
				# print changeID
				# print b
				calName = os.path.join('.\\', changeID, b)
				# print calName
				if os.path.isfile(calName) != True:
					check = False
					failures += 1
					c, d = i[0].split(":")
					d = d.strip()
					job.append(d)
				else:
					with open(calName, 'r') as f:
						lines = filter(None, (line.rstrip() for line in f))

					for i in lines:
						i = i.lstrip()
						if i[0] == '/' or i[0] == '#':
							check = False
							failures += 1
							job.append(b)


	# return check, num, job
	return [check, failures, num, job]

# Check notification
def notification(jtext):
	check = True
	failures = 0
	job = []
	checks = ['send_notification', 'notification_msg', 'notification_emailaddress']
	for i in jtext:
		for j in range(len(i)):
			# a, b = i[j].split(": ")
			# if a in checks:
			# 	check = False
			# 	failures += 1
			# 	q, w = i[0].split(": ")
			# 	job.append(w)
			for k in checks:
				if k in i[j]:
					check = False
					failures += 1
					q, w = i[0].split(":")
					w = w.strip()
					job.append(w)

	return [check, failures, job]

# Returns list of machine name
def machine(jtext):
	mac = []
	for i in jtext:
		for j in range(len(i)):
			if 'machine:' in i[j]:
				a, b = i[j].split(":")
				b = b.strip()
				if b not in mac:
					mac.append(b)

	return mac

# Returns list of global variables
def globalVariable(jtext):
	gVar = []
	for i in jtext:
		for j in range(len(i)):
			if '$$' in i[j]:
				temp = i[j][i[j].find('$$')+1:i[j].find('/')]
				if temp not in gVar:
					gVar.append(temp)

	return gVar

# Check matching converse jobs in back
def compareJilBack(jil, back):
	check = True
	failures = 0
	job = []
	# print jil
	compareJil = jil[:]
	for i in range(len(compareJil)):
		# print i
		if 'delete_job' in compareJil[i]:
			compareJil[i] = compareJil[i].replace('delete_job', 'insert_job')
		if 'insert_job' in compareJil[i]:
			# print i
			# print '#'
			compareJil[i] = compareJil[i].replace('insert_job', 'delete_job')
	# if jil != back:
	# 	check = False
	# print "#####"
	# print compareJil
	# print back
	# print back
	for i in compareJil:
		if i not in back:
			check = False
			failures += 1
			job.append(i)

	return [check, failures, job]

# Check if update jobs have excessive attributes
def updateJobs(jil, back):
	check = True
	failures = 0
	job = []
	indexJil = []
	indexBack = []
	# for i in jil:
	# 	for j in range(len(i)):
	# 		if 'update_job' in i[j]:
	# 			for k in back:
	# 				for l in range(len(i)):
	# 					if i[0] == k[0]:
	# 						# print i
	# 						print k
	# 						indexJil.append(jil.index(i))
	# 						indexBack.append(back.index(k))

	for i in jil:
		if 'update_job' in i[0]:
			for k in back:
				if i[0] == k[0]:
					indexJil.append(jil.index(i))
					indexBack.append(back.index(k))

	for i in range(len(indexJil)):
		fail = False
		temp = [jil[indexJil[i]][0]]
		for j in range(2, len(jil[indexJil[i]])):
			# print jil[indexJil[i]][j]
			# print back[indexBack[i]][j]
			# if jil[indexJil[i]][j] == back[indexBack[i]][j]:
			if jil[indexJil[i]][j] in back[indexBack[i]]:
				# print jil[indexJil[i]][j]
				check = False
				fail = True
				temp.append(jil[indexJil[i]][j])


		if fail == True:
			failures += 1
		job.append(temp)

	# print indexJil
	# print indexBack

	return check, failures, job

def allChecks(textParse, textParseBack):
	passChecks = True
	fails = 0
	job = []
	output = []
	# allChecks = [jobCount, deleteJobs, deleteJobs, test, ice, status, jobName, owner, startTimes, startMins, daysOfWeek, dateConditions, calendar, notification, machine, globalVariable, updateJobs]
	allChecks = [jobCount]
	
	for f in allChecks:
		output.append(f(textParse, textParseBack))


def main():
	print 'hello'

	# jilFile = raw_input("Enter the name of the jil file: ")
	# parse = readFile(jilFile)
	changeID, jilName, backName = inputFile('input.txt')
	# print changeID
	parse = readFile(os.path.join('.\\', changeID, jilName))
	parseBack = readFile(os.path.join('.\\', changeID, backName))
	# parse = readFile(".\\test jils\\UU_EMAIL.txt")
	# print parse
	textParse = parseJobs(parse)
	textParseBack = parseJobs(parseBack)
	# print textParse

# Console testing
	jobCount = count(textParse)
	print jobCount[0], "update jobs,", jobCount[1], "insert jobs,", jobCount[2], "delete jobs,", jobCount[3], "delete boxes"
	print "Machine", machine(textParse)
	print "Global Variable", globalVariable(textParse)

	print "Delete jobs JIL", deleteJobs(textParse)
	print "Delete jobs Backout", deleteJobs(textParseBack)
	print "Test", test(textParse)
	print "Ice", ice(textParse)
	print "Status", status(textParse)
	print "Job Name", jobName(textParse)
	print "Owner", owner(textParse)
	print "Start Times", startTimes(textParse)
	print "Start Mins", startMins(textParse)
	print "Days of Week", daysOfWeek(textParse)
	print "Date Conditions", dateConditions(textParse)
	print "Calendar", calendar(textParse, changeID)
	print "Notification", notification(textParse)

	
	back = readJobs(os.path.join('.\\', changeID, backName))
	jil = readJobs(os.path.join('.\\', changeID, jilName))
	# print jil
	# print back
	print "Compare backout", compareJilBack(jil,back)

	print
	print
	print "Update jobs"
	print updateJobs(textParse, textParseBack)

	print
	print
	# allChecks(textParse, textParseBack)

# Checking
	passChecks = True
	fail = 0
	job = []
	jobs = {}
	output = []


	a1 = (count(textParse))
	a2 = (deleteJobs(textParse))
	a3 = (deleteJobs(textParseBack))
	a4 = (test(textParse))
	a5 = (ice(textParse))
	a6 = (status(textParse))
	a7 = (jobName(textParse))
	a8 = (owner(textParse))
	a9 = (startTimes(textParse))
	a10 = (startMins(textParse))
	a11 = (daysOfWeek(textParse))
	a12 = (dateConditions(textParse))
	a13 = (calendar(textParse, changeID))
	a14 = (notification(textParse))
	a15 = (updateJobs(textParse, textParseBack))

	a16 = (machine(textParse))
	a17 = (globalVariable(textParse))



	# a2 = [False, 2, ['asdf', 'qwerty']]
	# a10 = [False, 4,['1', '2', '3', '4']]
	# a14 = [False, 3, ['asdf', '2', '4']]



	output.append(a1)
	output.append(a2)
	output.append(a3)
	output.append(a4)
	output.append(a5)
	output.append(a6)
	output.append(a7)
	output.append(a8)
	output.append(a9)
	output.append(a10)
	output.append(a11)
	output.append(a12)
	output.append(a13)
	output.append(a14)
	output.append(a15)
	output.append(a16)
	output.append(a17)

	# output.append(count(textParse))
	# output.append(deleteJobs(textParse))
	# output.append(deleteJobs(textParseBack))
	# output.append(test(textParse))
	# output.append(ice(textParse))
	# output.append(status(textParse))
	# output.append(jobName(textParse))
	# output.append(owner(textParse))
	# output.append(startTimes(textParse))
	# output.append(startMins(textParse))
	# output.append(daysOfWeek(textParse))
	# output.append(dateConditions(textParse))
	# output.append(calendar(textParse, textParseBack))
	# output.append(notification(textParse))
	# output.append([False, 2, ["asdfasdf"]])
	# output.append([False, 2, ["asdfasdf"]])
	# output.append([False, 2, ["asdfeafe"]])
	# output.append(machine(textParse))
	# output.append(globalVariable(textParse))
	
	# print output

	for i in range(1, len(output)-3):
		# print output[i][0]
		if output[i][0] == False:
			passChecks = False
			fail += output[i][1]
			for j in output[i][-1]:
				if j not in job:
					job.append(j)
	# print
	print "Did files pass the syntax check:", passChecks
	print "Number of failures:", fail
	print "Jobs that failed:", job

	for i in job:
		jobs[i] = []

	# print jobs



	if a2[-1]:
		for j in a2[-1]:
			jobs.setdefault(j,[]).append("Delete job error in jil")

	if a3[-1]:
		for j in a3[-1]:
			jobs.setdefault(j,[]).append("Delete job error in backout")
	
	if a4[-1]:
		for j in a4[-1]:
			jobs.setdefault(j,[]).append("Test")

	if a5[-1]:
		for j in a5[-1]:
			jobs.setdefault(j,[]).append("ON_ICE should only be in insert jobs")

	if a6[-1]:
		for j in a6[-1]:
			jobs.setdefault(j,[]).append("Status attribute invalid")
	
	if a7[-1]:
		for j in a7[-1]:
			jobs.setdefault(j,[]).append("Job name > 64 chars or has space in it")

	if a8[-1]:
		for j in a8[-1]:
			jobs.setdefault(j,[]).append("Owner cannot be Bautosys")

	if a9[-1]:
		for j in a9[-1]:
			jobs.setdefault(j,[]).append("Start times invalid")
	
	if a10[-1]:
		for j in a10[-1]:
			jobs.setdefault(j,[]).append("Start mins invalid")

	if a11[-1]:
		for j in a11[-1]:
			jobs.setdefault(j,[]).append("Days of week invalid")

	if a12[-1]:
		for j in a12[-1]:
			jobs.setdefault(j,[]).append("Date conditions invalid")
	
	if a13[-1]:
		for j in a13[-1]:
			jobs.setdefault(j,[]).append("Calendar name error")

	if a14[-1]:
		for j in a14[-1]:
			jobs.setdefault(j,[]).append("Notifications are no longer implented. Delete notifications")

	# if a15[-1]:
	# 	for j in a15[-1]:
	# 		jobs.setdefault(j,[]).append("Update job error")
	
	# if a16[-1]:
	# 	for j in a16[-1]:
	# 		jobs.setdefault(j,[]).append("Delete job error")

	# print "Failures per job:", jobs
	print "Failures per job:"
	for i in job:
		if jobs[i]:
			print i, jobs[i]

# Writing to output file
	f = open('output.txt', 'w')
	f.write('hello\n')
	f.write("These jobs below have errors\n\n")
	for i in job:
		if jobs[i]:
			f.write(str(i))
			f.write("\n")
			for j in jobs[i]:
				f.write(str(j))
				f.write("\n")
			f.write("\n")
			# f.write("\n")

	f.write("\n\n")
	f.write("Update jobs should only have attributes that need to be updated\n")
	f.write("Please delete these attributes in the JIL file under these job names:\n\n")
	if a15[-1]:
		for i in a15[-1]:
			for j in i:
				f.write(str(j))
				f.write("\n")
			f.write("\n")
	f.close()

# Copy output file to change request folder
	shutil.copy2('output.txt', os.path.join('.\\', changeID))

# Writing data file
	f = open('data.txt', 'w')
	
	if jobCount[0] != 0:
		f.write(str(jobCount[0]))
		f.write(" update jobs")
	if jobCount[1] != 0:
		f.write(", ")
		f.write(str(jobCount[1]))
		f.write(" insert jobs")
	if jobCount[2] != 0:
		f.write(", ")
		f.write(str(jobCount[2]))
		f.write(" delete jobs")
	if jobCount[3] != 0:
		f.write(", ")
		f.write(str(jobCount[3]))
		f.write(" delete boxes")
	f.write("\n\n")

	jobUpdate = []
	jobDelete = []
	jobInsert = []
	boxDelete = []

	if a16:
		f.write("Machine\n")
		for i in a16:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	if a17:
		f.write("Global Variable\n")
		for i in a17:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	for i in textParse:
		a, b = i[0].split(":")
		b = b.strip()
		if 'update_job' in a:
			jobUpdate.append(b)
		elif 'delete_job' in a:
			jobDelete.append(b)
		elif 'insert_job' in a:
			jobInsert.append(b)
		elif 'boxDelete' in a:
			boxDelete.append(b)


	if jobDelete:
		f.write("Delete jobs\n")
		for i in jobDelete:
			f.write(str(i))
			f.write("\n")
		if jobInsert or jobUpdate or boxDelete:
			f.write("\n\n")
	
	if jobInsert:
		f.write("Insert jobs\n")
		for i in jobInsert:
			f.write(str(i))
			f.write("\n")
		if jobUpdate or boxDelete:
			f.write("\n\n")	

	if jobUpdate:
		f.write("Update jobs\n")
		for i in jobUpdate:
			f.write(str(i))
			f.write("\n")
		if boxDelete:
			f.write("\n\n")

	if boxDelete:
		f.write("Delete box\n")
		for i in boxDelete:
			f.write(str(i))
			f.write("\n")
	f.close()

# Copy data file in change request folder
	shutil.copy2('data.txt', os.path.join('.\\', changeID))


main()