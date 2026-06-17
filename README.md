
# Intelligence Task Manager

## System description

יחידת מודיעין בשם ShadowNet זקוקה למערכת לניהול סוכנים ומשימות. מטרת הפרוייקט (נכון להיום): לבנות את שכבת הנתונים המלאה — חיבור ל-MySQL, יצירת טבלאות, ומחלקות OOP לניהול הנתונים

## Folder structure

intelligence-task-manager/
├── database/
│ ├── db_connection.py
│ ├── agent_db.py
│ └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore

## Table structure

### Table agents

- id, INT, AUTO_INCREMENT, PRIMARY KEY NOT MULL
- name, VARCHAR(50) NOT MULL
- specialty, VARCHAR(50) NOT MULL
- is_active, BOOLEAN DEFAULT TRUE NOT MULL
- completed_missions, INT DEFAULT 0 NOT MULL
- failed_missions, INT DEFAULT 0 NOT MULL
- agent_rank, ENUM / VARCHAR(50), NOT MULL

### Table missions

- id, INT, AUTO_INCREMENT, PRIMARY KEY NOT MULL
- title, VARCHAR(50) NOT MULL
- description, TEXT NOT MULL
- location, VARCHAR(50) NOT MULL
- difficulty, INT NOT MULL (1-10)
- importance, INT NOT MULL (1-10)
- status, VARCHAR(50) NOT MULL 
- risk_level, VARCHAR(50) DEFAULT NEW NOT MULL
- assigned_agent_id, INT 

## Explanation of the MissionDB, AgentDB, DBConnection classes — DB, and what each method does

### DBConnection

תפקידה המרכזי של המחלקה הוא לנהל ישירות את החיבור למסד הנתונים - כל מה שלא קשור לפונקציונליות של הפקוייקט אלא לחיבור ויצירה.

מחזירה חיבור פעיל ל - MySQL() (מסד הנתונים) ()connection_get
יוצרת את db_Intelligence אם לא קיים ()database_create
יוצרת את שתי הטבלאות אם לא קיימות ()tables_crea

### AgentDB

- create_agent(data), יוצרת סוכן חדש ומחזירה את האובייקט של הסוכן
- get_all_agents(), מחזירה רשימת כל הסוכנים
- get_agent_by_id(),
- update_agent(id, data),
- deactivate_agent(id), מגדירה מצב סוכן ללא פעיל
- increment_completed(id), מעדכן את כמות המשימות שהושלמו
- increment_failed(id), מעדכן את כמות המשימות שנכשלו
- get_agent_performance(id), מחזירה מילון עם המפתחות האלו:
completed, failed, total, success_rate
- count_active_agents() מחזירה את מספר הסוכנים הפעילים

### MissionDB

- create_mission(data), יצירת משימה חדשה ומחזירה את כל האובייקט
- get_all_missions(), יצירת משימה חדשה ומחזירה את כל האובייקט
- get_mission_by_id(id), מחזירה משימה אחת לפי ID או None
- assign_mission(m_id, a_id), משייכת משימה לסוכן
- update_mission_status(id, status), משמשת לכל שינויי סטטוס
- get_open_missions_by_agent(id), מחזירה משימות ASSIGNED/IN_PROGRESS של סוכן 
- count_all_missions(), סה"כ משימות
- count_by_status(status), סופרת לפי סטטוס מסויים
- count_open_missions(), סופרת משימות פתוחות
- count_critical_missions() סופרת משימות CRITICAL
- get_top_agent(), הסוכן עם completed_missions הגבוה ביותר 




## System rules

1. rank must be Commander / Senior / Junior any some value else = error
2. difficulty and importance must be between 1 and 10 else = error
3. level_risk is calculated automatically when a task is created — the user does not submit it.
4. An agent with False=active_is cannot accept tasks.
5. An agent cannot have more than 3 open tasks (PROGRESS_IN / ASSIGNED) at the same time.
6. If level_risk=CRITICAL — only an agent with the rank of Commander can accept the mission.
7. Only a task with a status of NEW can be assigned. After assignment: status=ASSIGNED.
8. You can only start a task with the ASSIGNED status. After: PROGRESS_IN=status.
9. Only a task can be completed. PROGRESS_IN and changed to completed or failed status.
10. Only a task with a status of NEW or ASSIGNED can be canceled — otherwise an error.

## Running instructions

כדי שהמערכת תרוץ כדרוש תחילה עליך ליצור קונטיינר בדוקר עי הרצת הפקודה הזו בשורת הפקודה:

```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```
לאחר מכן יש ליצור תיקיה חדשה בשם הפרוייקט ולבודד את סביבת העבודה ע"י הרצת פקודות אלה בשורת הפקודה:

```bash
python -m venv .venv
cd .venv/Scripts
/activate
```

אחר כך יש להתקין את כל הספריות הנדרשות כדלהלן:

```bash
pip install mysql.connector-python
pip install fastapi uvicorn
pip install logging
```
לאחר מכן יש להוריד את הפרוייקט מגיטהאב (ואם צריך יש לחלץ אותם), להעביר את הקבצים לתיקייה שייצרת.

לאחר שהכל נעשה יש לוודא שהחיבור בין המערכת למסד הנתונים טוב ויציב

ולאחר מכן בכדי שהשרת יתחיל לרוץ יש להריץ בשורת הפקודה את הפקודה הבאה:

```bash
uvicorn main:app --reload
```

אחרי שהשרת עלה יש אפשרות להיכנס ישר דרך גוגל עם כתובת מדוייקת ויש אפשרות להוסיף לאחר כתובת הלוקלית את הטקסט הבא:
/docs
כך שתוכל לראות את הדברים בצורה ויזואלית יפה ומסודרת
