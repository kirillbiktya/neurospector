from setuptools import setup, find_packages
from config import VERSION, DEV
from pip._internal.req import parse_requirements


def increase_build_num():
    with open("build_num", "r") as f:
        build_num = f.read()
        print(build_num)
        build_num = str(int(build_num) + 1)
    with open("build_num", "w") as f:
        f.write(build_num)
    return build_num


install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.requirement) for ir in install_reqs]

if DEV:
    v = VERSION + ".dev" + increase_build_num()
else:
    v = VERSION

setup(
    name='neurospector',
    version=v,
    install_requires=reqs,
    packages=find_packages(exclude=("terraform", "scripts")),
    platforms="linux-x64_84"
)
