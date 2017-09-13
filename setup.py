import sys
import setuptools

if not (0x030500f0 <= sys.hexversion < 0x040000a0):
    raise Exception('requires Python >=3.5, <4.0')

package_name, *_ = setuptools.find_packages()
setuptools.setup(
    name=package_name,
    version='1.0.0',
    license='MIT',
    author='thewizardplusplus',
    author_email='thewizardplusplus@yandex.ru',
    url='https://github.com/thewizardplusplus/' + package_name,
    packages=[package_name],
    install_requires=[
        'termcolor >=1.1.0, <2.0',
        'python-dotenv >=0.7.1, <1.0',
        'admitad >=1.1.1, <2.0',
        'Jinja2 >=2.9.6, <3.0',
    ],
    python_requires='>=3.5, <4.0',
    entry_points={'console_scripts': ['{0} = {0}:main'.format(package_name)]},
)
