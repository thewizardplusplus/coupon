import sys
import setuptools

if not (0x030500f0 <= sys.hexversion < 0x040000a0):
    raise Exception('requires Python >=3.5, <4.0')

packages = setuptools.find_packages()
package_name = packages[0]
setuptools.setup(
    name=package_name,
    version='1.1.0',
    license='MIT',
    author='thewizardplusplus',
    author_email='thewizardplusplus@yandex.ru',
    url='https://github.com/thewizardplusplus/' + package_name,
    packages=packages,
    install_requires=[
        'termcolor >=1.1.0, <2.0',
        'python-dotenv >=0.7.1, <1.0',
        'admitad >=1.1.1, <2.0',
        'ply >=3.10, <4.0',
        'requests >=2.18.1, <3.0',
        'Jinja2 >=2.9.6, <3.0',
    ],
    python_requires='>=3.5, <4.0',
    entry_points={'console_scripts': ['{0} = {0}:main'.format(package_name)]},
)
