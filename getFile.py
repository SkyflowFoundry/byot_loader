import os
from fileFinder import file_selector  # type: ignore

def getFile(file_type, script_directory):
    selected_file_name, selected_file_path = file_selector(file_type, script_directory)

    # Get input csv file 
    if selected_file_name and selected_file_path:
        # Retrieve directory and file name
        selected_directory = os.path.dirname(selected_file_path)
        fullFile = os.path.join(selected_directory, selected_file_name)

        # Set working directory to the directory containing the selected file
        os.chdir(selected_directory)
        #print(fullFile)
        return fullFile, selected_directory

#Testing only....
#testFileName = getFile('getFile Testing')
#print (testFileName)