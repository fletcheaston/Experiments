import re
from dataclasses import dataclass, field
from pathlib import Path

import pytest


@dataclass
class Directory:
    name: str

    parent: "Directory | None" = None

    files: dict[str, "File"] = field(default_factory=dict)
    directories: dict[str, "Directory"] = field(default_factory=dict)

    @property
    def size(self) -> int:
        files_size = sum([file.size for file in self.files.values()])
        directories_size = sum(
            [directory.size for directory in self.directories.values()]
        )

        return files_size + directories_size

    @property
    def all_directories(self) -> list["Directory"]:
        directories: list["Directory"] = [self]

        for directory in self.directories.values():
            directories.append(directory)

            directories += directory.all_directories

        return directories

    def upsert_file(self, file: "File") -> None:
        if file.name not in self.files:
            self.files[file.name] = file

    def upsert_directory(self, name: str) -> None:
        if name not in self.directories:
            self.directories[name] = Directory(
                name=name,
                parent=self,
            )

    def get_directory(self, name: str) -> "Directory":
        return self.directories[name]

    def directories_smaller_than(self, size: int) -> list["Directory"]:
        directories: list["Directory"] = []

        for directory in self.directories.values():
            if directory.size <= size:
                directories.append(directory)

            directories += directory.directories_smaller_than(size)

        return directories


@dataclass
class File:
    name: str
    size: int


@dataclass
class Filesystem:
    root_directory: Directory
    current_directory: Directory

    @property
    def all_directories(self) -> list[Directory]:
        directories: list[Directory] = [self.root_directory]

        directories += self.root_directory.all_directories

        return directories

    @property
    def size(self) -> int:
        return self.root_directory.size

    def feed_line(self, line: str) -> None:
        if match := re.search(r"\$ cd (.+)", line):
            name = match.groups()[0]

            match name:
                case "/":
                    self.current_directory = self.root_directory

                case "..":
                    self.current_directory = self.current_directory.parent

                case _:
                    self.current_directory.upsert_directory(name=name)
                    self.current_directory = self.current_directory.get_directory(
                        name=name
                    )

        elif match := re.search(r"dir (.+)", line):
            name = match.groups()[0]
            self.current_directory.upsert_directory(name=name)

        elif match := re.search(r"(\d+) (.+)", line):
            size, name = match.groups()
            file = File(
                name=name,
                size=int(size),
            )
            self.current_directory.upsert_file(file)

    def directories_smaller_than(self, size: int) -> list[Directory]:
        assert self.root_directory.size > size

        return self.root_directory.directories_smaller_than(size)


def part_1(document: list[str]) -> int:
    root = Directory(name="/")
    filesystem = Filesystem(
        root_directory=root,
        current_directory=root,
    )

    for line in document:
        filesystem.feed_line(line)

    return sum(
        [directory.size for directory in filesystem.directories_smaller_than(100000)]
    )


def part_2(document: list[str]) -> int:
    total_disk_size = 70000000
    needed_unused_disk_size = 30000000

    root = Directory(name="/")
    filesystem = Filesystem(
        root_directory=root,
        current_directory=root,
    )

    for line in document:
        filesystem.feed_line(line)

    # Basic math to get the minimum disk size needed to be freed
    occupied_disk_size = filesystem.size
    unused_disk_size = total_disk_size - occupied_disk_size
    minimum_disk_size_needed = needed_unused_disk_size - unused_disk_size

    # Iterate over all directories, ordered by size (ascending)
    # Get the smallest directory that's over (or equal to) the minimum free size
    directories = sorted(filesystem.all_directories, key=lambda x: x.size)

    for directory in directories:
        if directory.size >= minimum_disk_size_needed:
            return directory.size


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 95437),
        ("input.txt", 1390824),
    ],
)
def test_part_1(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 24933642),
        ("input.txt", 7490863),
    ],
)
def test_part_2(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
