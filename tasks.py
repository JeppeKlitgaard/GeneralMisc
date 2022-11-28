from invoke import task
from pathlib import Path
from typing import List
from enum import Enum

HOME = Path.home()
GENERAL_MISC = HOME / "GeneralMisc"

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

    # Traefik
    cmd = _construct_compose([GENERAL_MISC / "traefik" / "docker-compose.yml"], direction, True)
    c.run(cmd)

    # Portainer
    cmd = _construct_compose([GENERAL_MISC / "portainer" / "docker-compose.yml"], direction, True)
    c.run(cmd)

    # Tiny Tiny RSS
    cmd = _construct_compose([GENERAL_MISC / "ttrss" / "docker-compose.yml"], direction, True)
    c.run(cmd)

    # Wallabag
    cmd = _construct_compose([GENERAL_MISC / "wallabag" / "docker-compose.yml"], direction, True)
    c.run(cmd)

    # Homer
    cmd = _construct_compose([GENERAL_MISC / "homer" / "docker-compose.yml"], direction, True)
    c.run(cmd)

    # jeppe.science website:
    # - remark42 comments
    # - umami analytics
    with c.cd(HOME / "jeppe.science"):
        c.run(f"./run_docker prod {direction}")

@task
def up(c):
    _updown(c, "up")

@task
def down(c):
    _updown(c, "down")
