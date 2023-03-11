#!/usr/bin/python
# encoding: utf-8
import functools
import os
import re
from xml.etree import ElementTree

from Feedback import Feedback
import sys


class Project:

    def __init__(self, name, path, time=0):
        self.name = name
        self.path = path
        self.time = time


def searchWorkspaces():
    workSpaceStr = os.getenv("WORK_SPACE")
    workSpaces = workSpaceStr.split(";")

    for workSpace in workSpaces:
        search(workSpace)


def search(workspace):
    """
    搜索工作空间里的所有Java文件夹
    @param workspace: 工作空间路径 举例:/users/admin/workspace
    """
    files = os.listdir(workspace)
    for file in files:
        fullpath = workspace + "/" + file
        if isJavaDir(fullpath) and re.search(arg, file.lower()):
            projects.append(Project(file, fullpath))


def isJavaDir(path):
    """
    判断当前目录是否是Java文件夹。
    判断依据：如果文件夹里含有pom.xml文件，判断是，否则不是
    @param path:
    @return:
    """
    if os.path.isdir(path):
        tempFiles = os.listdir(path)
        for tempFile in tempFiles:
            if tempFile == "pom.xml":
                return True
    return False


def recentProject():
    prefix = "~/Library/Application Support/JetBrains/"
    suffix = "/options/recentProjects.xml"
    prefix = os.path.expanduser(prefix)
    files2 = os.listdir(prefix)
    path = prefix + findExactPath(files2) + suffix
    tree = ElementTree.parse(path)

    eles = tree.findall("./component/")
    # lastOpenProject(eles)

    otherProjects(eles)


def addProject(project):
    fb.add_item(project.name, project.path, project.path)


def lastOpenProject(options):
    for o in options:
        if o.get("name") == 'lastOpenedProject':
            path = os.path.expanduser(o.get('value').replace("$USER_HOME$", "~"))
            name = path.split("/")[-1]
            fb.add_item(name, path)


def otherProjects(options):
    for o in options:
        if o.get("name") == 'additionalInfo':
            entries = o.findall("map/entry")
            for entry in entries:
                parseEntry(entry)


def parseEntry(entry):
    path = os.path.expanduser(entry.get('key').replace("$USER_HOME$", "~"))
    name = path.split("/")[-1]
    time = 0
    options = entry.findall("value/RecentProjectMetaInfo/option")
    for o in options:
        if o.get("name") == "activationTimestamp":
            time = o.get("value")
    projects.append(Project(name, path, int(time)))


def findExactPath(files):
    opFiles = []
    for file in files:
        if file.startswith("IntelliJIdea"):
            opFiles.append(file)
    opFiles.sort(reverse=True)
    return opFiles[0]


def sortFun(p1, p2):
    if p1.time < p2.time:
        return -1
    elif p1.time > p2.time:
        return 1
    else:
        if p1.name < p2.name:
            return 1
        elif p1.name > p2.name:
            return -1
        else:
            return 0


if __name__ == '__main__':
    arg = ''
    fb = Feedback()
    projects = []

    if len(sys.argv) < 2:
        recentProject()
    else:
        arg = sys.argv[1].lower()
        searchWorkspaces()

    projects.sort(key=functools.cmp_to_key(sortFun), reverse=True)
    projects = projects[0:9]
    for p in projects:
        addProject(p)

    if fb.isEmpty():
        fb.add_item("找不到项目:" + arg, "找不到这个项目，请确认输入没有错🙅‍♂️!", valid="no")

    print(fb)
