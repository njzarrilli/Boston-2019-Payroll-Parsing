# Written by Naomi Zarrilli
# June 7, 2020
# Data sources: 
# CSV: https://data.boston.gov/dataset/employee-earnings-report
# Budget info: https://www.boston.gov/sites/default/files/file/2020/04/V3%2012-%2021%20R%20Public-Safety-Cabinet.pdf
# Budget info: https://www.boston.gov/sites/default/files/file/2020/04/V2%2006-%2021%20R%20Education-Cabinet.pdf

import csv
from collections import defaultdict

print "here"
education_departments = ["Achievement Gap", "Alighieri Montessori School", "Curley K-8", 
"Dorchester Academy", "Dudley St. Neighborhood School", "Early Learning Services", 
"East Boston EEC", "Edison K-8", "Eliot K-8", "English Language Learn", "Frederick Pilot Middle", 
"Gardner Pilot Academy", "Greater Egleston High", "Green Academy", "Greenwood, S K-8", "Haley Pilot", 
"Haynes EEC", "Henderson Elementary", "Hernandez K-8", "Higginson/Lewis K-8", 
"HPEC: Com Acd Science & Health", "Hurley K-8", "Jackson/Mann K-8", "Kennedy, EM Health Academy", 
"Kennedy, JF Elementary", "Kennedy, PJ Elementary", "Kilmer K-8", "King K-8", "Lyndon K-8", "Lyon K-8", 
"Lyon Pilot High 9-12", "Margarita Muniz Academy", "Mattahunt Elementary School", "Mildred Avenue K-8", 
"Mission Hill K-8", "Newcomers Academy", "P. A. Shaw Elementary", "Perry K-8", "Quincy Upper School", 
"Roosevelt K-8", "Superintendent", "Student Support Svc", "Teaching & Learning", "Tech Boston Academy",
"Tobin K-8", "Umana Middle", "Unified Student Svc", "UP Academy Dorchester", "UP Academy Holland",
"Warren/Prescott K-8", "West Roxbury Academy", "Young Achievers K-8"]

education_employee_count = 0
education_job_titles = defaultdict(int)
education_salary_total = 0.0
education_overtime_total = 0.0
education_salaries = []
teacher_salaries = []

bpd_employee_count = 0
bdp_job_titles = defaultdict(int)
bpd_salary_total = 0.0
bpd_overtime_total = 0.0
bpd_salaries = []
police_officer_salries = []

print "Starting parsing"

with open('boston_payroll_data.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	headers = reader.fieldnames
	for row in reader:
		if row["DEPARTMENT_NAME"] in education_departments or row["DEPARTMENT_NAME"].startswith("BPS"):
			education_employee_count += 1
			education_job_titles[row["TITLE"]] += 1
			education_salaries.append(float(row["TOTAL EARNINGS"].replace(',', '')))
			if row["TOTAL EARNINGS"] != "-":
				education_salary_total += float(row["TOTAL EARNINGS"].replace(',', ''))
			if row[" OVERTIME "].strip() != "-":
				education_overtime_total += float(row[" OVERTIME "].replace(',', ''))
			if row["TITLE"].lower() == "teacher":
				teacher_salaries.append(float(row["TOTAL EARNINGS"].replace(',', '')))

		if row["DEPARTMENT_NAME"] == "Boston Police Department":
			bpd_employee_count += 1
			bdp_job_titles[row["TITLE"]] += 1
			bpd_salaries.append(float(row["TOTAL EARNINGS"].replace(',', '')))
			if row["TOTAL EARNINGS"] != "-":
				bpd_salary_total += float(row["TOTAL EARNINGS"].replace(',', ''))
			if row[" OVERTIME "].strip() != "-":
				bpd_overtime_total += float(row[" OVERTIME "].replace(',', ''))
			if row["TITLE"].lower() == "police officer":
				police_officer_salries.append(float(row["TOTAL EARNINGS"].replace(',', '')))

education_salaries.sort(reverse = True)
bpd_salaries.sort(reverse = True)
teacher_salaries.sort(reverse=True)
police_officer_salries.sort(reverse=True)
print "Total education employees {}".format(education_employee_count)
print "Education Salary total {}".format(education_salary_total)
print "Education Overtime total {}".format(education_overtime_total)
#print "Education job titles {}".format(education_job_titles)
print "Top education ten salaries {}".format(education_salaries[:9])
print "Sum of top 10 education salaries {}".format(sum(education_salaries[:9]))
print "Top 10 teacher salaries {}".format(teacher_salaries[:9])
print "Sum of all teacher salaries {}".format(sum(teacher_salaries))
print "Total teachers {}".format(len(teacher_salaries))
print "----"
print "Total BPD employees {}".format(bpd_employee_count)
print "BPD Salary total {}".format(bpd_salary_total)
print "BPD Overtime total {}".format(bpd_overtime_total)
print "Top ten salaries {}".format(bpd_salaries[:9])
print "Sum of top 10 salaries {}".format(sum(bpd_salaries[:9]))
print "Top 10 police officer salaries {}".format(police_officer_salries[:9])
print "Sum of top 10 police officer salaries {}".format(sum(police_officer_salries[:9]))
print "Sum of all police offcier salaries {}".format(sum(police_officer_salries))
print "Total police officers {}".format(len(police_officer_salries))
# print "Education job titles {}".format(bdp_job_titles.keys())

normalized_titles = defaultdict(int)
# print bdp_job_titles
cleaned_titles = [s.replace("'", "") for s in bdp_job_titles.keys()]

for title in bdp_job_titles.keys():
	if title.lower() == "police officer":
		print "here"
	if "officer" in title.lower() or "offc" in title.lower() or "police officer" in title.lower():
		normalized_titles["police_officer"] += 1
	elif "lieutenant" in title.lower() or "lieut" in title.lower():
		normalized_titles["lieutenant"] += 1
	elif "analyst" in title.lower() or "anl" in title.lower():
		normalized_titles["analyst"] += 1
	elif "sergeant" in title.lower():
		normalized_titles["sergeant"] += 1
	elif "sec" in title.lower():
		normalized_titles["secretary"] += 1
	elif "admin asst" in title.lower() or "asst (administration)" in title.lower():
		normalized_titles["admin_asst"] += 1
	elif "criminalist" in title.lower():
		normalized_titles["criminalist"] += 1
	elif "accountant" in title.lower():
		normalized_titles["accountant"] += 1
	elif "captain" in title.lower():
		normalized_titles["captain"] += 1
	elif "commissioner" in title.lower():
		normalized_titles["commissioner"] += 1
	elif "maint" in title.lower():
		normalized_titles["maintenance"] += 1
	elif "clerk" in title.lower():
		normalized_titles["clerk"] += 1
	elif "custodian" in title.lower():
		normalized_titles["custodian"] += 1
	elif "data proc" in title.lower():
		normalized_titles["data_proc"] += 1
	elif "dispatcher" in title.lower():
		normalized_titles["dispatcher"] += 1
	elif "tech" in title.lower():
		normalized_titles["tech"] += 1
	else:
		normalized_titles[title] += 1
# print normalized_titles.keys()
