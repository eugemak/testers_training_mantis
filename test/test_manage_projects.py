import random
import string
from model.manage_projects_m import Project


def test_create_project(app):
    app.session.login("administrator", "root")

    # фунция для создания случайной последовательности значений
    def random_string(prefix, maxlen):
        symbols = string.ascii_letters + string.digits
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

    # Определяем новый проект
    project = Project(name=random_string("name", 20), description=random_string("description", 10))

    # Получаем список проектов
    old_list = app.manage_projects.get_projects_list()

    # Создаём проект
    app.manage_projects.create_project(project)

    # Получаем обновленный список проектов
    new_list = app.manage_projects.get_projects_list()

    # Добавляем к старому списку новый проект
    old_list.append(project)

    assert sorted(old_list, key=Project.project_id_or_max) == sorted(new_list, key=Project.project_id_or_max)


def test_delete_project(app):
    app.session.login("administrator", "root")

    # фунция для создания случайной последовательности значений
    def random_string(prefix, maxlen):
        symbols = string.ascii_letters + string.digits
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

    # Определяем новый проект
    project = Project(name=random_string("name", 20), description=random_string("description", 10))

    # Получаем список проектов
    if len(app.manage_projects.get_projects_list()) == 0:
        app.manage_projects.create_project(project)

    # Получаем список проектов
    old_list = app.manage_projects.get_projects_list()

    # Удаляем первый по списку проект
    app.manage_projects.delete_first_project()

    # Получаем обновленный список проектов
    new_list = app.manage_projects.get_projects_list()

    # Убираем из старого списка удалённый проект
    old_list.remove(project)

    assert sorted(old_list, key=Project.project_id_or_max) == sorted(new_list, key=Project.project_id_or_max)


def test_create_project_via_soap(app):
    username = "administrator"
    password = "root"
    app.session.login(username, password)

    parced_old_list = soap_projects_list(app, password, username)

    # фунция для создания случайной последовательности значений
    def random_string(prefix, maxlen):
        symbols = string.ascii_letters + string.digits
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

    project = Project(name=random_string("name", 20), description=random_string("description", 10))

    # Создаём проект
    app.manage_projects.create_project(project)

    parced_new_list = soap_projects_list(app, password, username)
    parced_old_list.append(project)

    assert sorted(parced_old_list, key=Project.project_id_or_max) == sorted(parced_new_list, key=Project.project_id_or_max)


def test_delete_project_via_soap(app):
    username = "administrator"
    password = "root"
    app.session.login(username, password)

    # фунция для создания случайной последовательности значений
    def random_string(prefix, maxlen):
        symbols = string.ascii_letters + string.digits
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

    # Определяем новый проект
    project = Project(name=random_string("name", 20), description=random_string("description", 10))

    parced_old_list = soap_projects_list(app, password, username)

    # Проверяем, есть ли проекты вообще. Добавляем при необходимости
    if len(parced_old_list) == 0:
        app.manage_projects.create_project(project)

    # Получаем список проектов
    parced_old_list = soap_projects_list(app, password, username)

    # Удаляем первый по списку проект
    app.manage_projects.delete_first_project()

    # Получаем обновленный список проектов
    parced_new_list = soap_projects_list(app, password, username)

    # Убираем из старого списка удалённый проект
    parced_old_list.remove(project)

    assert sorted(parced_old_list, key=Project.project_id_or_max) == sorted(parced_new_list, key=Project.project_id_or_max)


def soap_projects_list(app, password, username):
    # Получаем список проектов
    unparsed_list = app.soap.get_projects_list(username, password)
    assert unparsed_list

    parced_old_list = app.manage_projects.get_projects_list_from_soap(unparsed_list)
    assert parced_old_list

    return parced_old_list
