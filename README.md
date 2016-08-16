# GM
##Setup: 
	- Extract files into the same directory as your change request ID folders. File structure should look something like this:
		/Change requests
			-> syntax.py
			-> input.txt
			-> readme.md
			-> C100225114
				-> [jil]
				-> [backout]
			-> C123456789
				-> [jil]
				-> [backout]
	- Open input.txt
	- Paste the CHANGE REQUEST ID in the first row
	- Paste the JIL NAME and the extension in the second row
	- Paste the BACKOUT NAME and the extension in the third row
	- should look something like this:
		C100225114
		PC1 - FI-00204_FI-00178_FI-00179 change.txt
		PC1 - FI-00204_FI-00178_FI-00179 change - backout.txt

##Install Python:
	- https://www.python.org/downloads/release/python-2710/
	- download Windows x86 MSI installer
	- run the file to install python
	- we need to set path to python now:
		- click the windows home button
		- right click computer -> Properties
		- Advanced system settings 
		- Environment Variables...
		- under System variables, scroll to and click on Path
		- Edit...
		- in Variable value, scroll to the very end and add this:
			;C:\Python27\;C:\Python27\Scripts\
		- OK -> OK -> OK

##How to run this:
### Method 1
- double click syntax.py
### Method 2
	- navigate to your change request folder in which test.py resides
	- right click -> Properties
	- copy Location
	- OK
	- launch Windows PowerShell
	- type:
		cd "[location]"
		- basically paste your clipboard into [location]
		- you can do this by right clicking
		- should look something like this: 
			cd "C:\Users\TZKTF0\Documents\W\Change Requests"
	- type:
		python syntax.py
	- Enter

##What this program does:
	- Once you hit enter, the console will display some information. This is just a quick view. 
		- First section are the tests/checks that are run. 
			- Test [did it past the test? True/False, num of failures, which jobs failed]
		- Second section compares update jobs in the JIL and Backout. If they have the same same attributes, it creates a fail and lists out the job and which attributes are shared in the JIL and Backout. Update jobs should only have attributes that are unique, thus they should be different in the JIL and Backout
		- Third section is a summary of the jobs that failed (this does not take into account the uniqueness of update job attributes)
	- 2 files are created in the directory: output.txt, data.txt
		- output.txt lists the jobs that failed and update jobs that are not unique
		- data.txt lists Machine Name, Global Variable, and list of jobs
	- output.txt and data.txt copies are made in the Change Request ID folders
