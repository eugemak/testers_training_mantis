
from model.manage_projects_m import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def go_to_manage_project_page(self):
        wd = self.app.wd
        url = self.app.base_url + '/my_view_page.php'
        wd.get(url)
        wd.find_element_by_link_text("Manage").click()
        if wd.current_url.endswith("/manage_overview_page.php") and len(wd.find_elements_by_name("password")) > 0:
            wd.find_element_by_name("password").click()
            wd.find_element_by_name("password").clear()
            wd.find_element_by_name("password").send_keys("root")
            wd.find_element_by_css_selector('input[type="submit"]').click()
        wd.find_element_by_link_text("Manage Projects").click()

    def create_project(self, project):
        wd = self.app.wd
        self.go_to_manage_project_page()
        self.init_new_project()
        self.fill_new_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        wd.find_element_by_link_text("Proceed").click()
        self.users_cache = None

    def init_new_project(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()

    def fill_new_project_form(self, project):
        self.change_field("name", project.name)
        self.change_field("description", project.description)

    def change_field(self, group_field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(group_field_name).click()
            wd.find_element_by_name(group_field_name).clear()
            wd.find_element_by_name(group_field_name).send_keys(text)

    def open_first_project(self):
        wd = self.app.wd
        wd.find_element_by_css_selector("tr.row-1 > td > a").click()

    def confirm_delete_project(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()

    def delete_first_project(self):
        wd = self.app.wd
        self.go_to_manage_project_page()
        self.open_first_project()
        self.confirm_delete_project()
        self.users_cache = None

    users_cache = None

    def get_projects_from_table(self):
        wd = self.app.wd
        self.go_to_manage_project_page()
        self.users_cache = []
        projects_list = wd.find_elements_by_xpath("//table[3]/tbody/tr")[2:]
        for item in projects_list:
            href = item.find_element_by_tag_name("td").find_element_by_tag_name("a").get_attribute("href")
            project_id = href.replace('http://localhost/mantisbt-1.2.20/manage_proj_edit_page.php?project_id=', '')
            cells = item.find_elements_by_tag_name("td")
            name_field = cells[0].text
            description_field = cells[4].text
            self.users_cache.append(Project(project_id=project_id, name=name_field, description=description_field))

    def get_projects_list(self):
        if self.users_cache is None:
            self.get_projects_from_table()
        return list(self.users_cache)

    def get_projects_list_from_soap(self, unparsed_list):
        parsed_list = []
        for item in unparsed_list:
            project_id = item.id
            name = item.name
            description = item.description
            parsed_list.append(Project(project_id=project_id, name=name, description=description))
        return parsed_list
