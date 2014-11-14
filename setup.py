from setuptools import setup

with open('requirements.txt') as requirements_file:
    REQUIREMENTS = requirements_file.readlines()

setup(
    name='rapidfeedback',
    version='0.0.2',
    description='Distributed system for delivering rapid haptic feedback to developers, e.g. in case of Jenkins failures',
    author='Johannes Ebke',
    author_email='johannes@ebke.org',
    classifiers=[
        'Programming Language :: Python :: 3.3'
    ],
    url='https://github.com/JohannesEbke/rapidfeedback',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'missilecontrol = missilecontrol:run',
            'missilesite = missilesite:run'
        ]
    }
)
