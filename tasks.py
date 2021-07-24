from invoke import task
from pathlib import Path
from typing import List
from enum import Enum


HOME = Path.home()

class Direction(str, Enum):
    UP = "up"
    DOWN = "down"

@task(name="list")
def list_(c):
    c.run("inv --list")


def _construct_compose(compose_files: List[str], direction: Direction, detached: bool):
    assert direction in Direction._value2member_map_

    cmd = "docker-compose "
    cmd += " ".join([f"-f {file}" for file in compose_files])
    cmd += " " + direction
    if detached and direction == Direction.UP:
        cmd += " -d"

    return cmd

def _updown(c, direction: Direction):
    assert direction in Direction._value2member_map_

    cmd = _construct_compose([HOME / "GeneralMisc" / "docker-compose.yml"], direction, True)
    c.run(cmd)

    with c.cd(HOME / "jeppe.science"):
        c.run("./" + direction)

@task
def up(c):
    _updown(c, "up")

@task
def down(c):
    _updown(c, "down")
