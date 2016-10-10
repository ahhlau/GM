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
	dup = []
	job = ['update_job', 'insert_job', 'delete_job', 'delete_box']
	for i in lines:
		i = i.strip()
		if 'job_type' in i and 'job:' in i:
			a, b = i.split('job_type:')
			text.append(a.strip())
		else:
			for j in job:
				if j in i:
					if j not in text:
						text.append(i)
					else:
						print "Duplicate job names:", i
						dup.append(i)
						text.append(i)
	f.close()

	return text

# Returns a list of all lines
def readFile(filename):
	with open(filename, 'r') as f:
		lines = filter(None, (line.rstrip() for line in f))

	text = []
	dup = []
	dupe = []
	for i in lines:
		i = i.strip()
		if i[0] == '/':
			pass
		elif i[0] == '#':
			pass
		elif 'job_type' in i and 'job:' in i:
			a, b = i.split('job_type:')
			if a.strip() in text:
				dup.append(a.strip())
				# print a.strip()
			text.append(a.strip())
			text.append('job_type: ' + b.strip())
		else:
			if 'job:' in i and i in text:
				dup.append(i)
			text.append(i)
	f.close()

	if dup:
		dupe.append(False)
		dupe.append(len(dup))
		dupe.append(dup)
	else:
		dupe.append(True)
		dupe.append(0)
		dupe.append(dup)
	# print dupe

	return text, dupe

# Parses file to a list of jobs
def parseJobs(text):
	check = ['update_job', 'insert_job', 'delete_job', 'delete_box']
	job = []
	temp = []
	dup = []

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

def correctInputs(text):
	check = True
	failures = 0
	lines = []
	lineNum = []
	for i in text:
		if not (i[0] == '#' or (i[:1] == '/*' and i[-2:] == '*/') or ':' in i):
			check = False
			failures += 1
			lines.append(i)
			lineNum.append(text.index(i)+1)

	return [check, failures, lineNum, lines]

def valid(jtext):
	checks = ['update_job', 'insert_job', 'delete_job', 'delete_box']
	check = True
	failures = 0
	job = []
	for i in jtext:
		a, b = i[0].split(":")
		a = a.strip()
		# print a
		if a not in checks:
			check = False
			failures += 1
			job.append(i[0])

	return [check, failures, job]

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
			if 'test' in i[j] or 'TEST' in i[j] or 'Test' in i[j]:
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
	pattern = re.compile('^"(([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9],\s?)*([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]"$|^$')
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
	pattern = re.compile('^([0-5][0-9],\s?)*[0-5][0-9]$|^$')
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


	return [check, failures, job]

# Return jobs with calendars
def calendar(jtext, changeID):
	# check = 'No'
	num = 0
	check = True
	failures = 0
	job = []
	cal = ['Calendar Name:']
	calCountJobs = ['Mulitple Calendars:']
	for i in jtext:
		calCount = 0
		for j in range(len(i)):
			if 'run_calendar' in i[j]:
				# check = 'Yes'
				num += 1
				# a, b = i[0].split(":")
				# b = b.strip()
				# job.append(b)

				a, b = i[j].split(":")
				b = b.strip()
				if b not in cal:
					cal.append(b)
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
			if 'calendar' in i[j]:
				calCount += 1
		if calCount > 1:
			check = False
			failures += 1
			a, b = i[0].split(":")
			b = b.strip()
			calCountJobs.append(b)


	# return check, num, job
	return [check, failures, num, cal, calCountJobs, job]

# Check notification
def notification(jtext):
	check = True
	failures = 0
	job = []
	checks = ['send_notification', 'notification_msg', 'notification_emailaddress']
	for i in jtext:
		for j in range(len(i)):
			for k in checks:
				if k in i[j]:
					if 'send_notification: n' in i[j]:
						pass
					else:
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
				temp = i[j][i[j].find('$$')+3:i[j].find('}')]
				if temp not in gVar:
					gVar.append(temp)

	return gVar

# if jobs are deleted then inserted, they should be update jobs
def deleteInsert(jtext):
	check = True
	failures = 0
	job = []
	delJobs = []
	inJobs = []
	for i in jtext:
		if 'delete_job' in i[0]:
			a, b = i[0].split(':')
			b = b.strip()
			delJobs.append(b)
		if 'insert_job' in i[0]:
			a, b = i[0].split(':')
			b = b.strip()
			inJobs.append(b)
	for i in delJobs:
		if i in inJobs:
			check = False
			failures += 1
			job.append(i)

	return [check, failures, job]

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
			# print compareJil[i]
			compareJil[i] = compareJil[i].replace('delete_job', 'insert_job')
			# print compareJil[i]
			# print
		elif 'insert_job' in compareJil[i]:
			# print compareJil[i]
			# print '#'
			compareJil[i] = compareJil[i].replace('insert_job', 'delete_job')
			# print compareJil[i]
			# print
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
	jobJil = []
	jobBack = []
	indexJil = []
	indexBack = []
	attributes = []
	attributesB = []

	for i in jil:
		if 'update_job' in i[0]:
			for k in back:
				if i[0] == k[0]:
					indexJil.append(jil.index(i))
					indexBack.append(back.index(k))

	for i in range(len(indexJil)):
		fail = False
		tempJil = [jil[indexJil[i]][0]]
		tempBack = [back[indexBack[i]][0]]
		jobAttribute = [jil[indexJil[i]][0]]
		backAttribute = [back[indexBack[i]][0]]
		# check for uniqueness of update jobs
		for j in range(1, len(jil[indexJil[i]])):
			# print jil[indexJil[i]][j]
			# print back[indexBack[i]][j]
			# if jil[indexJil[i]][j] == back[indexBack[i]][j]:
			# print jil[indexJil[i]][j]


			try:
				a, b = jil[indexJil[i]][j].split(": ")
			except:
				a, b = jil[indexJil[i]][j].split(":")
			jobAttribute.append(a.strip())
			if jil[indexJil[i]][j] in back[indexBack[i]]:
				# print jil[indexJil[i]][j]
				check = False
				fail = True
				tempJil.append(jil[indexJil[i]][j])
		attributes.append(jobAttribute)
		# check if attributes in back does not exist in jil
		for j in range(1, len(back[indexBack[i]])):
			try:
				a, b = back[indexBack[i]][j].split(": ")
			except:
				a, b = back[indexBack[i]][j].split(":")
			backAttribute.append(a.strip())
			# if back[indexBack[i]][j] not in jil[indexJil[i]]:
			# 	check = False
			# 	fail = True
			# 	tempBack.append(back[indexBack[i]][j])
		attributesB.append(backAttribute)

		if fail == True:
			failures += 1
		jobJil.append(tempJil)
		jobBack.append(tempBack)

	# print indexJil
	# print indexBack
	# print attributes
	# print attributesB
	# print

	existinJILandnotBack = []
	existinBackandnotJIL = []
	for i in range(len(attributes)):
		# check if attributes in JIL are not in back
		temp = [attributes[i][0]]
		for j in attributes[i]:
			if j not in attributesB[i]:
				temp.append(j)
		existinJILandnotBack.append(temp)
		# check if attributes in back are not in JIL
		temp = [attributesB[i][0]]
		for j in attributesB[i]:
			if j not in attributes[i]:
				temp.append(j)
		existinBackandnotJIL.append(temp)

	# print existinJILandnotBack
	# print existinBackandnotJIL


	return [check, failures, existinJILandnotBack, existinBackandnotJIL, jobJil, jobBack]

def asms(jil):
	check = True
	failures = 0
	job = []
	temp = []
	for i in jil:
		a, b = i.split(":")
		b = b.strip()
		c = re.search(r"-(\d)*-", b)
		asmsNum = re.sub(r"-", "", c.group())
		# print asmsNum
		if asmsNum not in temp:
			temp.append(asmsNum)
			job.append(i)
	if len(temp) != 1:
		check = False
		failures = len(job)
		return [check, failures, job] 
	else:
		return [check, failures, []]

def insertJobs(jtext):
	check = True
	failures = 0
	job = []
	appFail = 0
	appJob = []
	groupFail = 0
	groupJob = []
	alarmFail = 0
	alarmJob = []
	def application(iJob):
		a = 0
		fail = 0
		for i in iJob:
			# print i
			if "application: mon-batch-" in i:
				a += 1
		# print a
		if a != 1:
			fail += 1
			b, c = iJob[0].split(":")
			c = c.strip()
			return [fail, c]
		else:
			return [fail, []]

	def group(iJob):
		a = 0
		check = ['P2', 'P3', 'P4']
		fail = 0
		for i in iJob:
			if 'group:' in i:
				b, c = i.split(":")
				# print c.strip()
				if c.strip() in check:
					a += 1
				# print a
		if a != 1:
			fail += 1
			b, c = iJob[0].split(":")
			c = c.strip()
			return [fail, c]
		else:
			return [fail, []]

	def alarm(iJob):
		a = 0
		check = ['y', 'n']
		fail = 0
		for i in iJob:
			if 'alarm_if_fail:' in i:
				b, c = i.split(":")
				if c.strip() in check:
					a += 1
		if a != 1:
			fail += 1
			b, c = iJob[0].split(":")
			c = c.strip()
			return [fail, c]
		else:
			return [fail, []]

	for i in jtext:
		if 'insert_job' in i[0]:
			a = application(i)
			b = group(i)
			c = alarm(i)
			appFail += a[0]
			if a[1]:
				appJob.append(a[1])
			groupFail += b[0]
			if b[0]:
				groupJob.append(b[1])
			alarmFail += c[0]
			if c[0]:
				alarmJob.append(c[1])
	failures = appFail + groupFail + alarmFail

	if failures != 0:
		check = False
	for i in appJob:
		job.append(i)
	for i in groupJob:
		job.append(i)
	for i in alarmJob:
		job.append(i)

	# print '####'
	# print job
	# print	


  	job = uniqueList(job)
	

	return [check, failures, job, [appFail, appJob], [groupFail, groupJob], [alarmFail, alarmJob]]

def uniqueList(seq):
	seen = set()
	return [x for x in seq if x not in seen and not seen.add(x)]

def main():
	print 'hello'

	# jilFile = raw_input("Enter the name of the jil file: ")
	# parse = readFile(jilFile)
	changeID, jilName, backName = inputFile('input.txt')
	changeID = changeID.strip()
	jilName = jilName.strip()
	backName = backName.strip()
	# print changeID
	parse, jilDupe = readFile(os.path.join('.\\', changeID, jilName))
	parseBack, backDupe = readFile(os.path.join('.\\', changeID, backName))
	# parse = readFile(".\\test jils\\UU_EMAIL.txt")
	# print parse
	textParse = parseJobs(parse)
	textParseBack = parseJobs(parseBack)
	# print textParse
	# print jilDupe

# Console testing
	jobCount = count(textParse)
	print jobCount[0], "update jobs,", jobCount[1], "insert jobs,", jobCount[2], "delete jobs,", jobCount[3], "delete boxes"
	print "Machine", machine(textParse)
	print "Global Variable", globalVariable(textParse)
	print "Correct Inputs JIL", correctInputs(parse)
	print "Correct Inputs Back", correctInputs(parseBack)
	print "Valid", valid(textParse)
	print "Jil duplicate jobs", jilDupe
	print "Backout duplicate jobs", backDupe
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
	print "Delete / Insert", deleteInsert(textParse)

	
	back = readJobs(os.path.join('.\\', changeID, backName))
	jil = readJobs(os.path.join('.\\', changeID, jilName))

	
	print "ASMS JIL", asms(jil)
	print "ASMS Backout", asms(back)
	print "Compare backout", compareJilBack(jil, back)

	print
	print
	print "Update jobs"
	print updateJobs(textParse, textParseBack)

	print
	print
	print "Insert jobs"
	print insertJobs(textParse)
	print
	print

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
	a15 = (valid(textParse))


	a16 = (updateJobs(textParse, textParseBack))

	a17 = (machine(textParse))
	a18 = (globalVariable(textParse))

	a19 = (compareJilBack(jil, back))
	a20 = (jilDupe)
	a21 = (backDupe)
	a22 = (asms(jil))
	a23 = (asms(back))
	a24 = (deleteInsert(textParse))
	a25 = (correctInputs(parse))
	a26 = (correctInputs(parseBack))

	a27 = (insertJobs(textParse))

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
	output.append(a18)
	output.append(a19)
	output.append(a20)
	output.append(a21)
	output.append(a22)
	output.append(a23)
	output.append(a24)
	output.append(a25)
	output.append(a26)
	output.append(a27)

# Add total of failures and jobs
	# print output[22]
	for i in range(1, len(output)-11):
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

	# for i in job:
	# 	print jobs[i]
	# 	jobs[i] = []


	if a2[-1]:
		for j in a2[-1]:
			jobs.setdefault(j,[]).append("Delete job error in jil")

	if a3[-1]:
		for j in a3[-1]:
			jobs.setdefault(j,[]).append("Delete job error in backout")
	
	if a4[-1]:
		for j in a4[-1]:
			jobs.setdefault(j,[]).append("'Test' should not be in JIL")

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
			jobs.setdefault(j,[]).append("Notifications are no longer implemented. Delete notifications")

	if a15[-1]:
		for j in a15[-1]:
			jobs.setdefault(j,[]).append("Invalid job")
	
	# if a16[-1]:
	# 	for j in a16[-1]:
	# 		jobs.setdefault(j,[]).append("Delete job error")

	# print "Failures per job:", jobs
	print "Failures per job:"
	# print job
	for i in job:
		if jobs[i]:
			print i, jobs[i]

# Writing to output file
	f = open('output.txt', 'w')
	f.write('hello\n\n')
	f.write("We are reviewing your change request prior to sending it to CAB approval. Some items need to be clarified and/or reviewed and fixed. Please see my  comments below and reply back to me with corrections/responses. Your request will be on hold meanwhile.\n\n\n")
	# Duplicate jobs in JIL
	if jilDupe[-1]:
		f.write("These jobs below are duplicated in the JIL:\n")
		for i in jilDupe[-1]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n\n")

	# Duplicate jobs in Backout
	if backDupe[-1]:
		f.write("These jobs below are duplicated in the Backout JIL:\n")
		for i in backDupe[-1]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n\n")

	# Syntax errors
	if job:
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
		f.write("\n")
	else:
		f.write("No syntax errors\n\n\n")

	if len(a13[-2]) > 1:
		# f.write("Calendar Name\n")
		for i in a13[-2]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")


	if a19[-1]:
		f.write("Backout JIL jobs do not mirror JIL\n")
		f.write("Each insert_job in the jil has to have a mirrored delete_job in the backout and vice versa. Each update_job should also have a mirrored update_job in the backout to revert changes.\n")
		f.write("Please add the following jobs in the backout:\n\n")
		for i in a19[-1]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n\n")
	else:
		f.write("No backout errors\n\n\n")

	if a24[-1]:
		f.write("The job below were deleted and then inserted. These jobs should be combined to update_jobs\n")
		f.write("Please rewrite these jobs as update_jobs\n\n")
		for i in a24[-1]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	if a16[-2]:
		f.write("Update jobs should only have attributes that need to be updated\n")
		f.write("Please delete these attributes in the JIL and Backout files under these job names:\n\n")
		for i in a16[-2]:
			for j in i:
				f.write(str(j))
				f.write("\n")
			f.write("\n\n")
	else:
		f.write("No update_job JIL errors\n\n\n")
	if a16[-1]:
		f.write("Update jobs should only have attributes that need to be updated\n")
		f.write("Please delete these attributes in the Backout files under these job names:\n\n")
		for i in a16[-1]:
			for j in i:
				f.write(str(j))
				f.write("\n")
			f.write("\n\n")
	else:
		f.write("No update_job Backout errors\n\n\n")

	if a16[2]:
		f.write("These attributes exist in JIL and not in Backout\n")
		f.write("Please include these attributes in the Backout as well\n\n")
		for i in a16[2]:
			for j in i:
				f.write(str(j))
				f.write("\n")
			f.write("\n\n")
	else:
		f.write("Nothing exists in JIL and not Backout")

	if a16[3]:
		f.write("These attributes exist in Backout and not in JIL\n")
		f.write("Please include these attributes in the Backout as well\n\n")
		for i in a16[3]:
			for j in i:
				f.write(str(j))
				f.write("\n")
			f.write("\n\n")
	else:
		f.write("Nothing exists in Backout and not in JIL")

	if a20[-1]:
		f.write("JIL has duplicate jobs:\n")
		for i in a20[-1]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	if a21[-1]:
		f.write("Backout has duplicate jobs:\n")
		for i in a21[-1]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	if a22[-1]:
		f.write("JIL has more than one ASMS number:\n")
		f.write("JIL file should only have jobs with one unique ASMS number\n")
		for i in a22[-1]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	if a23[-1]:
		f.write("Backout has more than one ASMS number:\n")
		f.write("Backout file should only have one unique ASMS number\n")
		for i in a23[-1]:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	if a25[-1]:
		f.write("Incorrect input in JIL\n")
		f.write("Comments should start with '#' or be surrounded by '/*' and '*/'\n")
		for i in range(len(a25[-1])):
			f.write("Line number ")
			f.write(str(a25[-2][i]))
			f.write(" : ")
			f.write(str(a25[-1]))
			f.write("\n")
		f.write("\n\n")

	if a26[-1]:
		f.write("Incorrect input in Backout\n")
		f.write("Comments should start with '#' or be surrounded by '/*' and '*/'\n")
		for i in range(len(a26[-1])):
			f.write("Line number ")
			f.write(str(a26[-2][i]))
			f.write(" : ")
			f.write(str(a26[-1]))
			f.write("\n")
		f.write("\n\n")

	if a27[2]:
		f.write("As of 10/10/2016, all insert jobs should have 'application', 'group', and 'alarm_if_fail' attributes\n")
		f.write("Please add the attributes below for the following jobs:\n\n")

		if a27[3][1]:
			f.write("application - the batch monitoring configuration item that should be assigned incidient fialures from the job, format is mon-batch-<application CI>-prod in most cases\n")
			f.write("'application' attributes should be in the following insert jobs:\n")
			for i in a27[3][1]:
				f.write(str(i))
				f.write("\n")
			f.write("\n\n")
		if a27[4][1]:
			f.write("group - the priority that should be assigned to the incident ticket.  Valid values are P2, P3, or P4\n")
			f.write("'group' attributes should be in the following insert jobs:\n")
			for i in a27[3][1]:
				f.write(str(i))
				f.write("\n")
			f.write("\n\n")
		if a27[5][1]:
			f.write("alarm_if_fail - should be y if an alert is to be sent on failure, or n if an alert is not to be sent\n")
			f.write("'alarm_if_fail' attributes should be in the following insert jobs:\n")
			for i in a27[4][1]:
				f.write(str(i))
				f.write("\n")

	f.close()

# Copy output file to change request folder
	shutil.copy2('output.txt', os.path.join('.\\', changeID))

# Writing data file
	f = open('data.txt', 'w')

	
	if jobCount[0] != 0:
		f.write(str(jobCount[0]))
		f.write(" update jobs")
		comma = False
		for i in jobCount[1:]:
			if i != 0:
				comma = True
		if comma == True:
			f.write(', ')

	if jobCount[1] != 0:
		f.write(str(jobCount[1]))
		f.write(" insert jobs")
		comma = False
		for i in jobCount[2:]:
			if i != 0:
				comma = True
		if comma == True:
			f.write(', ')
	
	if jobCount[2] != 0:
		f.write(str(jobCount[2]))
		f.write(" delete jobs")
		comma = False
		for i in jobCount[3:]:
			if i != 0:
				comma = True
		if comma == True:
			f.write(', ')
	
	if jobCount[3] != 0:
		f.write(str(jobCount[3]))
		f.write(" delete boxes")
	f.write("\n\n\n")

	jobUpdate = []
	jobDelete = []
	jobInsert = []
	boxDelete = []

	if a17:
		f.write("Machine\n")
		for i in a17:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	if a18:
		f.write("Global Variable\n")
		for i in a18:
			f.write(str(i))
			f.write("\n")
		f.write("\n\n")

	if len(a13[-3]) > 1:
		# f.write("Calendar Name\n")
		for i in a13[-3]:
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
		elif 'delete_box' in a:
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

	f.write("\n\n")
	f.write("The job(s) below could not be verified as successfully tested in Pre-Prod or Dev. Can you send me confirmation that testing was done, or can you perform a test using Autosys Dev and reply back to us once that is complete. We can only go through with the change if the test is done in one of the Autosys lower environments.\n")

	f.write("\n\n")
	f.write("No Autosys alert notification needed as job rule mask already exists\n\n\n")
	f.write("An alert notification task to the Autosys team IS REQUIRED")
	f.close()

# Copy data file in change request folder
	shutil.copy2('data.txt', os.path.join('.\\', changeID))


# Copy jil file from change request folder to parent folder
	shutil.copy2(os.path.join('.\\', changeID, jilName), '.')
	shutil.move(jilName, 'inputJil.txt')

# Copy backout file from change request folder to parent folder
	shutil.copy2(os.path.join('.\\', changeID, backName), '.')
	shutil.move(backName, 'backoutJIL.txt')


main()
