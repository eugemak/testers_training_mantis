# -*- coding: utf-8 -*-
import pytest
import json
import os.path
import importlib
import jsonpickle
import ftputil
from fixture.application import Application

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        root_path = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(root_path, file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])

    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])

    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")


@pytest.fixture()
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    # fixture.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    # parser.addoption("--check_ui", action="store_true")


# хук для использования в качестве фикстуры имя модуля с тестовыми данными или json-файла
def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


# функция для загрузки данных из отдельного модуля
def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata


# функция для загрузки данных из json файла
def load_from_json(file):
    root_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root_path, "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())


#
# @pytest.fixture()
# def check_ui(request):
#     return request.config.getoption("--check_ui")


# @pytest.fixture(scope="session")
# def db(request):
#     db_config = load_config(request.config.getoption("--target"))['db']
#     dbfixture = DbFixture(host=db_config['host'], database=db_config['database'],
#                           user=db_config['user'], password=db_config['password'])
#
#     def fin():
#         dbfixture.destroy()
#
#     request.addfinalizer(fin)
#     return dbfixture
#
#
# @pytest.fixture(scope="session")
# def orm(request):
#     db_config = load_config(request.config.getoption("--target"))['db']
#     orm_fixture = ORMFixture(host=db_config['host'], name=db_config['database'],
#                              user=db_config['user'], password=db_config['password'])
#     return orm_fixture
