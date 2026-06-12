import pytest


def _pytest_major_version():
    return int(pytest.__version__.split('.', 1)[0])


def _is_test_yaml_file(path):
    if hasattr(path, "suffix"):
        return path.suffix == ".yml" and path.name.startswith("test")
    return path.ext == ".yml" and path.basename.startswith("test")


def _node_path(node):
    if hasattr(node, "path"):
        return node.path
    return node.fspath


if _pytest_major_version() >= 7:
    def pytest_collect_file(parent, file_path):
        if _is_test_yaml_file(file_path):
            return YamlFile.from_parent(parent, path=file_path)
else:
    def pytest_collect_file(parent, path):
        if _is_test_yaml_file(path):
            return YamlFile.from_parent(parent, fspath=path)


class YamlFile(pytest.File):
    def collect(self):
        f = _node_path(self).open()
        for line in f.readlines():
            yield YamlItem.from_parent(self, name=line.strip(), spec="xxx")
        f.close()

class YamlItem(pytest.Item):
    def __init__(self, name, parent, spec):
        super(YamlItem, self).__init__(name, parent)
        self.spec = spec

    def runtest(self):
        pass

    def reportinfo(self):
        return _node_path(self), 0, "usecase: %s" % self.name
