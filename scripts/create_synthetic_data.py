import os
import json
import pandas as pd

os.makedirs("data/csv", exist_ok=True)
os.makedirs("data/json", exist_ok=True)
os.makedirs("data/metadata", exist_ok=True)
os.makedirs("data/permissions", exist_ok=True)
os.makedirs("data/pdfs", exist_ok=True)
os.makedirs("indexes", exist_ok=True)

employees = pd.DataFrame([
    {"emp_id": "E001", "name": "Aarav Sharma", "dept": "HR", "salary_band": "L3", "location": "Mumbai"},
    {"emp_id": "E002", "name": "Riya Mehta", "dept": "Finance", "salary_band": "L2", "location": "Pune"},
    {"emp_id": "E003", "name": "Kabir Khan", "dept": "Security", "salary_band": "L4", "location": "Bengaluru"}
])

finance = pd.DataFrame([
    {"report_id": "F001", "quarter": "Q1", "cost_center": "IT", "amount": 250000},
    {"report_id": "F002", "quarter": "Q2", "cost_center": "HR", "amount": 120000},
    {"report_id": "F003", "quarter": "Q2", "cost_center": "Security", "amount": 310000}
])

incidents = pd.DataFrame([
    {"incident_id": "INC001", "severity": "high", "system": "email", "status": "open"},
    {"incident_id": "INC002", "severity": "medium", "system": "vpn", "status": "closed"},
    {"incident_id": "INC003", "severity": "high", "system": "database", "status": "investigating"}
])

employees.to_csv("data/csv/employees.csv", index=False)
finance.to_csv("data/csv/finance.csv", index=False)
incidents.to_csv("data/csv/incidents.csv", index=False)

logs = [
    {"event_id": "L001", "event_type": "login_failure", "user": "emp23", "severity": "medium"},
    {"event_id": "L002", "event_type": "data_export", "user": "fin12", "severity": "high"},
    {"event_id": "L003", "event_type": "privilege_escalation", "user": "sec99", "severity": "critical"}
]
with open("data/json/security_logs.json", "w", encoding="utf-8") as f:
    json.dump(logs, f, indent=2)

policy_text = """
HR Policy Document

Employees are eligible for 18 annual leave days.
Remote work requires manager approval.
Salary details are confidential and restricted to authorized HR personnel.
Managers may access summary employee policy information but not confidential salary records.
"""

with open("data/pdfs/hr_policy.txt", "w", encoding="utf-8") as f:
    f.write(policy_text)

metadata = pd.DataFrame([
    {"doc_id": "DOC001", "title": "HR Policy", "source_type": "pdf", "department": "HR", "sensitivity": "internal", "allowed_roles": "HR,Manager", "location": "data/pdfs/hr_policy.txt"},
    {"doc_id": "DOC002", "title": "Finance Report", "source_type": "csv", "department": "Finance", "sensitivity": "confidential", "allowed_roles": "Finance,Manager", "location": "data/csv/finance.csv"},
    {"doc_id": "DOC003", "title": "Security Logs", "source_type": "json", "department": "Security", "sensitivity": "restricted", "allowed_roles": "Security", "location": "data/json/security_logs.json"},
    {"doc_id": "DOC004", "title": "Employee Records", "source_type": "csv", "department": "HR", "sensitivity": "confidential", "allowed_roles": "HR", "location": "data/csv/employees.csv"},
    {"doc_id": "DOC005", "title": "Incident Register", "source_type": "csv", "department": "Security", "sensitivity": "internal", "allowed_roles": "Security,Manager", "location": "data/csv/incidents.csv"}
])
metadata.to_csv("data/metadata/documents.csv", index=False)

users = pd.DataFrame([
    {"user_id": "u_hr_1", "role": "HR", "department": "HR"},
    {"user_id": "u_fin_1", "role": "Finance", "department": "Finance"},
    {"user_id": "u_sec_1", "role": "Security", "department": "Security"},
    {"user_id": "u_mgr_1", "role": "Manager", "department": "Management"}
])
users.to_csv("data/permissions/users.csv", index=False)

print("Free synthetic enterprise dataset created.")