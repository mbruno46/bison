from setuptools import setup

VERSION = (0, 2, 1)

def version():
    v = ".".join(str(v) for v in VERSION)
    cnt = f'__version__ = "{v}" \n__version_full__ = __version__'
    with open('bison/version.py', 'w') as f:
        f.write(cnt)
    with open('bison/VERSION','w') as f:
        f.write(f'v{v}')
    return v

setup(
    name='bison',
    version=version(),
    packages=find_packages(include=['bison*']),
)
