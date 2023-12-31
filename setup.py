from setuptools import setup, find_packages

setup(
    name='gameboyEmu',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/Kajacat/chip8Emu',
    license='MIT',
    author='Kasimir van Rijn',
    description='A Chip8 emulator written in Python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='chip8 emulator',
    install_requires=[
    ],
    python_requires='>=3.12',
)
