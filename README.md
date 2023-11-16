This script serves as a tool for organizing files, categorizing them, and moving them based on their types. 
Let's go through the main components of the code:

File Type Definitions:
TYPE_FILE is a dictionary that defines categories for different file types based on their extensions 
(e.g., images, videos, documents, audio, archives, and other). The file extensions associated with 
each category are listed as tuples.

Cyrillic to Latin Transliteration:
The MAP dictionary is used for transliterating Cyrillic characters to Latin characters. 
This is often useful for creating readable filenames.

Normalization Function:
The normalize function takes a text input, replaces non-alphanumeric characters with underscores, 
and applies transliteration.

Functions for Working with Folders and Files:
add_folder: Creates a subfolder with a specified name within a given path. Returns a Path object representing 
the created or existing subfolder.
move_files: Processes a dictionary of sorted file paths and moves them to appropriate folders based on their categories. 
Utilizes the add_folder and normalize functions, and makes use of the shutil and pathlib modules for file operations.
sorted_paths_by_file_types: Takes a list of file paths and categorizes them based on predefined file types and their extensions (TYPE_FILE). 
Returns a dictionary where keys represent file types, and values are lists of paths belonging to each type.

File Search Function:
search_files: Recursively explores a specified directory, identifies files excluding hidden ones, and optionally skips directories listed 
in TYPE_FILE when the ignore_folder parameter is set to True. Returns a list of paths for the located files.

Argument Checking and Main Function:
checking_argument: Takes a path as an argument, converts it to a Path object, and then checks if it exists and corresponds to a directory. 
If the path is valid, it returns the Path object; otherwise, it prints an error message and exits the program.
main: The main function, called when the script is run. Retrieves the path from the command line arguments, performs a search for files, 
sorts them, and moves them to their respective folders. Also removes empty directories, excluding sorting-created directories.
