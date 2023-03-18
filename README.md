# toggl2jirapython script to for keeping track of time to Jira from Toggl
It is useful to use when you work with private Jira server wich is available only from your device but you prefer to check you time with TooglThis script groups toggl notes by jira key, summing up the elapsed time and adds in Jira one entry for each task in one day
To make everything works as well you must start you toggl notes with jira issue key (for example: RFT-3687 Some work)

Validations:
+ **Issue <> does not have a Jira number** each toggl note must start with jira issue key
+ **Task duration cannot be less than 1 minute** toggl note must be longer than one munute
+ **Task duration cannot exceed 8 hours** 
+ **the task has no tags** each toggl note must have one tag (if enable reqtag arg)
+ **the task has no project:** each toggl note must belongs to one project (if enable reqproject arg)


Explanation of script arguments:
+ **--since** the date since make report, like 2023-03-10
+ **--until** the date until make report, like 2023-03-18
+ **--action** Use CHECK mode to validate your toggl notes and WRITE to correct and write you time report to Jira (default = WRITE)
+ **--validate** If you want to correct you time tracking (add missing time) up to full work day (8 hours) you should set Y in this arg
+ **--max_dur_exclude_code** disable max time control (8 hours) for long jira keys which are set in this arg and separated by semicolon, like "MIS-9;MIS-7"
+ **--exclude_validate** set days to exclude time correction (if you user validate arg) like 2023-02-23;2023-02-24
+ **--reqtag** require to validate tag of toggl note (default False)
+ **--reqproject** require to validate project of toggl note (default False)

EXAMPLE:
```python app/main.py --validate Y --max_dur_exclude_code "MIS-9;MIS-7" --exclude_validate "2023-02-23;2023-02-24" --since 2023-03-10 --until 2023-03-18```

 You should create .env file in the root user folder (~) and set this variables in it:
+ **TOOGL_API_TOKEN** toggle token (you can find it inside you toggl pref)
+ **JIRA_URL** = jira server url
+ **JIRA_LOGIN** = jira login
+ **JIRA_PSWD** = jira password

install venv and requirements please run ```sh ./install.sh```