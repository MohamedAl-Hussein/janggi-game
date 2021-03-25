from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Gaming',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Engine',
    version='0.0.1',
    description='Janggi game engine.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Mohamed Al-Hussein',
    author_email='mohamed.n.al.hussein@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='janggi',
    packages=find_packages(),
    install_requires=['']
)
