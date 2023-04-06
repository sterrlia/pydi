import importlib
from typing import List
from pydi.config import BuildScheme, Config
from pydi.container import Container
from pathlib import Path


def import_all(root: str, dirpath: str):
    if root.endswith("/") and dirpath.startswith("/"):
        root = root[:-1]
    elif not (root.endswith("/") or dirpath.startswith("/")):
        root = root + "/"
    globalpath = root + dirpath

    for path in Path(globalpath).glob("*"):
        name = path.name

        new_dirpath = dirpath + "/" + name
        if name.endswith(".py") and not name.endswith("__init__.py"):
            module_name = new_dirpath[:-3].replace("/", ".")
            if module_name.startswith('.'):
                module_name = module_name[1:]

            yield module_name
            importlib.import_module(module_name)

        if path.is_dir():
            yield from import_all(root, new_dirpath)


class AbstractKernel:
    def boot(self) -> Container:
        raise NotImplementedError

    def shutdown(self):
        raise NotImplementedError


class DefaultKernel(AbstractKernel):
    def __init__(
        self,
        project_dir: str,
        index_dir: str,
        config: Config,
        build_schemes: List[BuildScheme],
    ):
        self.project_dir = project_dir
        self.index_dir = index_dir
        self.build_schemes = build_schemes
        self.config = config

    def boot(self) -> Container:
        print("Booting kernel...")

        for module_name in import_all(self.project_dir, self.index_dir):
            print(module_name)

        container = Container(config=self.config, build_schemes=self.build_schemes)

        print("done")
        return container

    def shutdown(self):
        print("shutdown...")
        print("done")
