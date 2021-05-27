from bs4 import BeautifulSoup as bs
from bs4.element import Tag
import csv
import requests
import os


URL = "https://myprojects.sharepoint.com/teams/gpols/_api"   # Your API
# URL = "http://localhost:8000/_api"     # For testing

PROJECT_FILEPATH = "ProjectData.csv"
ASSIGNMENTS_FILEPATH = "Assignments.csv"
TASKS_FILEPATH = "Tasks.csv"

CWD = os.getcwd()


def to_dict(tags: list):
    result = {}
    for tag in tags:
        result[tag.name] = tag.get_text()
    return result


def get_data_from_bs(bs_data):
    all_raw_data = bs_data.find_all("properties")
    return (to_dict(tag for tag in raw if type(tag) is Tag) for raw in all_raw_data)


def get_data_from_url(url: str):
    print(f"Get data from url: {url}")
    res = requests.get(url)
    if res.status_code == 200:
        print("200 OK")
        return res.text
    else:
        raise Exception(f"Request failed. Status: {res.status_code}: {res.text}")


def main():
    project_file = open(PROJECT_FILEPATH, 'w+', newline='')
    assignments_file = open(ASSIGNMENTS_FILEPATH, 'w+', newline='')
    tasks_file = open(TASKS_FILEPATH, 'w+', newline='')
    project_dict_writer = None
    assignments_dict_writer = None
    tasks_dict_writer = None

    try:
        bs_project_data = bs(get_data_from_url(f"{URL}/ProjectData"), "lxml-xml")
        all_projects_data = get_data_from_bs(bs_project_data)

        for project in all_projects_data:
            if not project_dict_writer:
                project_dict_writer = csv.DictWriter(project_file, project.keys())
                project_dict_writer.writeheader()
                project_dict_writer.writerow(project)
            else:
                project_dict_writer.writerow(project)

            project_id = project.get("ProjectId")

            bs_assignment_data = bs(get_data_from_url(f"{URL}/ProjectData/Projects(guid'{project_id}')/Assignments"), "lxml-xml")
            all_assignment_data = get_data_from_bs(bs_assignment_data)

            for assignment in all_assignment_data:
                if not assignments_dict_writer:
                    assignments_dict_writer = csv.DictWriter(assignments_file, assignment.keys())
                    assignments_dict_writer.writeheader()
                    assignments_dict_writer.writerow(assignment)
                else:
                    assignments_dict_writer.writerow(assignment)

            bs_task_data = bs(get_data_from_url(f"{URL}/ProjectData/Projects(guid'{project_id}')/Tasks"), "lxml-xml")
            all_task_data = get_data_from_bs(bs_task_data)

            for task in all_task_data:
                if not tasks_dict_writer:
                    tasks_dict_writer = csv.DictWriter(tasks_file, task.keys())
                    tasks_dict_writer.writeheader()
                    tasks_dict_writer.writerow(task)
                else:
                    tasks_dict_writer.writerow(task)
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        project_file.close()
        assignments_file.close()
        tasks_file.close()

    print(f"Generated {CWD}/{PROJECT_FILEPATH}")
    print(f"Generated {CWD}/{ASSIGNMENTS_FILEPATH}")
    print(f"Generated {CWD}/{TASKS_FILEPATH}")


if __name__ == "__main__":
    main()