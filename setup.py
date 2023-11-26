from setuptools import setup

setup(name='clean_folder',
      version='1',
      description='This code automatically organizes files in a specified directory based on their types and categories. It uses predefined dictionaries for classifying files into groups such as images, videos, documents, audio, archives, and others. Additionally, it includes functions for normalizing file names, handling duplicates, moving files to appropriate folders, and searching for files in the specified directory.',
      url='https://github.com/Nyambevos/Sorter_for_files',
      author='Nuambevos',
      author_email='ruslan.bilokoniuk@gmail.com',
      license='MIT',
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']})