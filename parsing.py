# Written by Naomi Zarrilli
# Used for parsing information from Boston's 2019 payroll report.
# CSV source: Employee Earnings Report 2019, https://data.boston.gov/dataset/employee-earnings-report

import csv
from collections import defaultdict
import statistics

def parse():
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

	education_total_employee_count = 0
	education_full_time_employee_count = 0
	education_job_titles = defaultdict(int)
	education_salary_total = 0.0
	education_overtime_total = 0.0
	education_salaries = []
	teacher_salaries = []

	bpd_total_employee_count = 0
	bpd_full_time_employee_count = 0
	bdp_job_titles = defaultdict(int)
	bpd_salary_total = 0.0
	bpd_overtime_total = 0.0
	bpd_salaries = []
	police_officer_salaries = []
	miniumum_wage_full_time_salary = 12 * 40 * 52 # $12 minimum hourly wage times 40 hour week times 52 weeks

	with open('boston_payroll_data.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		headers = reader.fieldnames
		for row in reader:
			employee_earnings = float(row["TOTAL EARNINGS"].replace(',', ''))
			# for BPS departments, some departments are just titled the school's name, while others are titled something like "BPS [school name]" or "BPS Transportation"
			if row["DEPARTMENT_NAME"] in education_departments or row["DEPARTMENT_NAME"].startswith("BPS"):
				education_total_employee_count += 1
				# only include full time employees as part time salary data ends up skewing numbers to make salaries seem lower
				if employee_earnings >= miniumum_wage_full_time_salary:
					education_full_time_employee_count += 1
					education_job_titles[row["TITLE"]] += 1
					# "-" indicates a null value
					if row["TOTAL EARNINGS"] != "-":
						education_salaries.append(employee_earnings)
						education_salary_total += employee_earnings
						if row["TITLE"].lower() == "teacher":
							teacher_salaries.append(employee_earnings)
					if row[" OVERTIME "].strip() != "-":
						education_overtime_total += float(row[" OVERTIME "].replace(',', ''))
			# unlike BPS department, there was no variation for BPD department titles
			if row["DEPARTMENT_NAME"] == "Boston Police Department":
				bpd_total_employee_count += 1
				# only include full time employees as part time salary data ends up skewing numbers to make salaries seem lower
				if employee_earnings >= miniumum_wage_full_time_salary:
					bpd_full_time_employee_count += 1
					bdp_job_titles[row["TITLE"]] += 1
					# "-" indicates a null value
					if row["TOTAL EARNINGS"] != "-":
						bpd_salary_total += float(employee_earnings)
						bpd_salaries.append(employee_earnings)
						if row["TITLE"].lower() == "police officer":
							police_officer_salaries.append(employee_earnings)
					if row[" OVERTIME "].strip() != "-":
						bpd_overtime_total += float(row[" OVERTIME "].replace(',', ''))

	education_salaries.sort(reverse=True)
	bpd_salaries.sort(reverse=True)
	teacher_salaries.sort(reverse=True)
	police_officer_salaries.sort(reverse=True)
	print("Total education employees {}".format(education_total_employee_count))
	print("Total full time education employees {}".format(education_full_time_employee_count))
	print("Education Salary total {}".format(education_salary_total))
	print("Education Overtime total {}".format(education_overtime_total))
	print("Median full time education salary {}".format(statistics.median(education_salaries)))
	print("Education job titles {}".format(education_job_titles))
	print("Top education ten salaries {}".format(education_salaries[:9]))
	print("Sum of top 10 education salaries {}".format(sum(education_salaries[:9])))
	print("Top 10 teacher salaries {}".format(teacher_salaries[:9]))
	print("Sum of all teacher salaries {}".format(sum(teacher_salaries)))
	print("Total teachers {}".format(len(teacher_salaries)))
	print("Median full time teacher salary {}".format(statistics.median(teacher_salaries)))
	print("----")
	print("Total BPD employees {}".format(bpd_total_employee_count))
	print("Total full time BPD employees {}".format(bpd_full_time_employee_count))
	print("BPD Salary total {}".format(bpd_salary_total))
	print("BPD Overtime total {}".format(bpd_overtime_total))
	print("Median full time BPD salary {}".format(statistics.median(bpd_salaries)))
	print("Top ten salaries {}".format(bpd_salaries[:9]))
	print("Sum of top 10 salaries {}".format(sum(bpd_salaries[:9])))
	print("Top 10 police officer salaries {}".format(police_officer_salaries[:9]))
	print("Sum of top 10 police officer salaries {}".format(sum(police_officer_salaries[:9])))
	print("Sum of all police offcier salaries {}".format(sum(police_officer_salaries)))
	print("Total police officers {}".format(len(police_officer_salaries)))
	print("Median full time police officer salary {}".format(statistics.median(police_officer_salaries)))
	normalize_bpd_titles(bdp_job_titles)

def normalize_bpd_titles(bdp_job_titles):
	# Trying to categorize BPD job titles
	normalized_titles = defaultdict(int)
	for title in bdp_job_titles.keys():
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
	print("BPD job titles {}".format(normalized_titles.keys()))

parse()