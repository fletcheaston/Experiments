import re
from dataclasses import dataclass, field

from fastapi import APIRouter, Body

router = APIRouter(tags=["2022 - Day 7: No Space Left On Device"])


DOCUMENT_EXAMPLE = [
    "$ cd /",
    "$ ls",
    "dir a",
    "14848514 b.txt",
    "8504156 c.dat",
    "dir d",
    "$ cd a",
    "$ ls",
    "dir e",
    "29116 f",
    "2557 g",
    "62596 h.lst",
    "$ cd e",
    "$ ls",
    "584 i",
    "$ cd ..",
    "$ cd ..",
    "$ cd d",
    "$ ls",
    "4060174 j",
    "8033020 d.log",
    "5626152 d.ext",
    "7214296 k",
]


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


@dataclass
class File:
    name: str
    size: int

    def __str__(self) -> str:
        return f"{self.name} - {self.size}"


@dataclass
class Filesystem:
    root_directory: Directory
    current_directory: Directory

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
        return []


@router.post("/part-1")
async def year_2022_day_7_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    directory = Directory(name="/")
    filesystem = Filesystem(
        root_directory=directory,
        current_directory=directory,
    )

    total = 0

    # Iterate over lines
    for line in document:
        filesystem.feed_line(line)

    return total


@router.post("/part-2")
async def year_2022_day_7_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for line in document:
        pass

    return total
