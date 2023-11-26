import sys
import shutil
from pathlib import Path

# Dictionary defining file categories based on their extensions
TYPE_FILE = {
    "images": ('JPEG', 'PNG', 'JPG', 'SVG'),
    "video": ('AVI', 'MP4', 'MOV', 'MKV'),
    "documents": ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    "audio": ('MP3', 'OGG', 'WAV', 'AMR'),
    "archives": ('ZIP', 'GZ', 'TAR'),
    "other": ()
}

# Character mapping for transliterating Cyrillic characters to Latin characters
MAP = {
    ord('А'): 'A',      ord('а'): 'a',
    ord('Б'): 'B',      ord('б'): 'b',
    ord('В'): 'V',      ord('в'): 'v',
    ord('Г'): 'G',      ord('г'): 'g',
    ord('Ґ'): 'G',      ord('ґ'): 'g',
    ord('Д'): 'D',      ord('д'): 'd',
    ord('Е'): 'E',      ord('е'): 'e',
    ord('Є'): 'Ye',     ord('є'): 'ye',
    ord('Ё'): 'Yo',     ord('ё'): 'yo',
    ord('Ж'): 'Zh',     ord('ж'): 'zh',
    ord('З'): 'Z',      ord('з'): 'z',
    ord('И'): 'I',      ord('и'): 'i',
    ord('І'): 'I',      ord('і'): 'i',
    ord('Ї'): 'Yi',     ord('ї'): 'yi',
    ord('Й'): 'Y',      ord('й'): 'y',
    ord('К'): 'K',      ord('к'): 'k',
    ord('Л'): 'L',      ord('л'): 'l',
    ord('М'): 'M',      ord('м'): 'm',
    ord('Н'): 'N',      ord('н'): 'n',
    ord('О'): 'O',      ord('о'): 'o',
    ord('П'): 'P',      ord('п'): 'p',
    ord('Р'): 'R',      ord('р'): 'r',
    ord('С'): 'S',      ord('с'): 's',
    ord('Т'): 'T',      ord('т'): 't',
    ord('У'): 'U',      ord('у'): 'u',
    ord('Ф'): 'F',      ord('ф'): 'f',
    ord('Х'): 'Kh',     ord('х'): 'kh',
    ord('Ц'): 'Ts',     ord('ц'): 'ts',
    ord('Ч'): 'Ch',     ord('ч'): 'ch',
    ord('Ш'): 'Sh',     ord('ш'): 'sh',
    ord('Щ'): 'Shch',   ord('щ'): 'shch',
    ord('Ъ'): '',       ord('ъ'): '',
    ord('Ы'): 'Y',      ord('ы'): 'y',
    ord('Ь'): '',       ord('ь'): '',
    ord('Э'): 'E',      ord('э'): 'e',
    ord('Ю'): 'Yu',     ord('ю'): 'yu',
    ord('Я'): 'Ya',     ord('я'): 'ya'
    }



def normalize(text):
    """Normalize the input text by replacing non-alphanumeric characters with underscores
       and applying Cyrillic to Latin transliteration."""
    
    # Initialize an empty string to store the normalized text
    new_text = ""

    # Iterate through each character in the input text
    for char in text:
        # Replace non-alphanumeric characters with underscores, keep alphanumeric characters unchanged
        if not char.isalnum():
            new_text += "_"
        else:
            new_text += char

    # Use the translate method to apply additional character mapping for transliteration
    return new_text.translate(MAP)


def add_folder(path, name_folder):
    """ The add_folder function creates a subfolder with a specified name (name_folder)
        within a given path (path). It returns a Path object representing the created or 
        existing subfolder. If the subfolder does not already exist, it is created using 
        the mkdir method. """

    # Create a Path object representing the target subfolder
    p = Path(path, name_folder)
    
    # Check if the subfolder doesn't exist, and if not, create it
    if not p.exists():
        p.mkdir()

    # Return the Path object representing the created or existing subfolder
    return p
        

def move_files(path, sorted_paths):
    """ The move_files function processes a dictionary of sorted file paths (sorted_paths) 
        and moves them to appropriate folders based on their categories. It handles file naming, 
        duplicates, and special treatment for archives. The function utilizes the add_folder 
        and normalize functions, and it makes use of the shutil and pathlib modules for file 
        operations. """

    # Iterate through each category and its associated file paths in the sorted dictionary
    for name_folder, file_paths in sorted_paths.items():
        # Create the target directory based on the category
        target_directory = add_folder(path, name_folder)

        # Iterate through each file path in the current category
        for file_path in file_paths:
            # Initialize variables for file naming and duplicate handling
            name_file = None
            duplicate = 0

            # Determine the file name based on the category
            if name_folder == "other":
                name_file = file_path.stem
            else:
                name_file = normalize(file_path.stem)

            # Handle duplicates by appending a number to the file name
            while True:
                if duplicate == 1:
                    name_file += "_1"
                elif duplicate > 1:
                    # Correcting a typo in the original code ('==' instead of '+=')
                    name_file = name_file[:name_file.rfind("_") + 1] + str(duplicate)

                # Check if a file with the current name already exists in the target directory
                if Path(target_directory, f"{name_file}{'' if name_folder == 'archives' else file_path.suffix}").exists():
                    duplicate += 1
                    continue

                break

            # Handle archive files by extracting them or moving them to the 'other' category on failure
            if name_folder == "archives":
                try:
                    shutil.unpack_archive(file_path, Path(target_directory, name_file))
                    file_path.unlink()
                    continue
                except:
                    print(f"Failed to extract {name_file} archive")
                    shutil.move(file_path, Path(add_folder(path, "other"), file_path.name))
                    continue

            # Move the file to the target directory with the correct name and extension
            shutil.move(file_path, Path(target_directory, f"{name_file}{file_path.suffix}"))


def sorted_paths_by_file_types(list_file):
    """ The sorted_paths_by_file_types function takes a list of file paths (list_file) 
        and categorizes them based on predefined file types and their extensions (TYPE_FILE). 
        It returns a dictionary where keys represent file types, and values are lists of 
        paths belonging to each type. Files with extensions not matching any predefined type 
        are categorized under 'other'. """

    # Initialize an empty dictionary to store sorted file paths
    sorted_lists = {}

    # Iterate through each file path in the input list
    for path in list_file:
        # Iterate through predefined file types and their extensions
        for key, value in TYPE_FILE.items():
            # Check if the file's suffix (extension) matches any of the predefined extensions
            if path.suffix.lstrip(".").upper() in value:
                # If a match is found, add the path to the corresponding list in the dictionary
                if not key in sorted_lists:
                    sorted_lists[key] = []
                sorted_lists[key].append(path)
                break
        else:
            # If no match is found, add the path to the 'other' category in the dictionary
            if not 'other' in sorted_lists:
                sorted_lists['other'] = []
            sorted_lists['other'].append(path)

    # Return the dictionary containing sorted file paths
    return sorted_lists


def search_files(path_folder=Path(), ignore_folder=True):
    """ The search_files function recursively explores a specified directory (path_folder).
        It identifies files, excluding hidden ones, and optionally skips directories listed
        in TYPE_FILE when the ignore_folder parameter is set to True. The function returns
        a list of paths for the located files."""

    # Initialize an empty list to store the paths of found files
    list_files = []

    # Iterate through the entries in the specified folder
    for path in path_folder.iterdir():
        # Skip hidden files or folders (those starting with ".")
        if path.name[0] == ".":
            continue

        # Check if the current entry is a directory
        if path.is_dir():
            # If the directory name is in TYPE_FILE and ignore_folder is True, skip it
            if str(path.stem) in TYPE_FILE:
                if ignore_folder:
                    continue
            # Recursively call the search_files function for subdirectories
            list_files += search_files(path_folder=path, ignore_folder=False)
            continue

        # If the entry is a file, add its path to the list
        list_files.append(path)

    # Return the list of found file paths
    return list_files       
            

def checking_argument(path):
    """ The checking_argument function takes a path as an argument, 
    converts it to a Path object, and then checks if it exists and 
    corresponds to a directory. If the path is valid, it returns 
    the Path object; otherwise, it prints an error message and exits 
    the program. """

    # Convert the input path to a Path object
    p = Path(path)
    
    # Check if the path exists and is a directory
    if p.exists() and p.is_dir():
        # If the path is valid, return the Path object
        return p
    else:
        # If the path is not valid, print an error message and exit the program
        print(f"The folder address is incorrect: ({path})")
        exit()


def main():
    # Retrieve the path from the command line arguments and validate it
    PATH = checking_argument(sys.argv[1])
    
    # Search for files in the specified directory
    print("Search for files...")
    list_of_file_paths = search_files(PATH)
    number_of_files = len(list_of_file_paths)

    # Process the found files if there are any
    if number_of_files > 0:
        print(f"Found {number_of_files} {'file' if number_of_files == 1 else 'files'}")

        # Sort the found files into categories
        sorted_paths_list = sorted_paths_by_file_types(list_of_file_paths)
        for group_name, files_paths in sorted_paths_list.items():
            print(f"-> {group_name}: {len(files_paths)} {'file' if len(files_paths) == 1 else 'files'}")
    
        # Move the sorted files to their respective folders
        move_files(PATH, sorted_paths_list)

    else:
        print("No files found to sort")

    
    # Remove empty directories, excluding  sorting-created directories
    for path in PATH.iterdir():
        if not path.name in TYPE_FILE:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
 
            
if __name__ == "__main__":
    main()