import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        curPath = os.getcwd()
        #print(f"the current file path is: {curPath}")
        workDirAbs = os.path.abspath(working_directory)
        #print(f"the working directory is: {workDirAbs}")
        targetDir = os.path.normpath(os.path.join(workDirAbs, directory))
        #print(f"the target directory will be: {targetDir}")
        validDir = os.path.commonpath([workDirAbs, targetDir]) == workDirAbs
        #print(f"the entered directory is: {'valid' if validDir else 'invalid'}")
        if not validDir:
            #print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        record = os.listdir(targetDir)
        #print(record)
        # ['pkg', 'main.py', 'tests.py']
        newList = []
        newStr = ""
        for item in record:
            try:
                itemPath = os.path.join(targetDir, item)
            except Exception as e:
                return f"Error: {e}"
            try:
                file_size = os.path.getsize(itemPath)
            except Exception as e:
                return f"Error: {e}"
            try:
                is_dir = os.path.isdir(itemPath)
            except Exception as e:
                return f"Error: {e}"
            formatted_string = f"{item}: file_size={file_size} bytes, is_dir={is_dir}"
            newList.append(formatted_string)
            newStr = "\n".join(newList)

        #print(newList)
        #print(newStr)
        return newStr

        if not os.path.isdir(directory):
            #print(f'Error: "{directory}" is not a directory')
            return f'Error: "{directory}" is not a directory'

        #print(f'Success: "{directory}" is within the working directory')
        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        #print(e)
        return f"{e}"

# # print(help(os.path))
# curPath = os.getcwd()
# # print(curPath)
# workDir = 'workspace'
# directory = 'bob'
# # absPath = os.path.abspath(curPath)
# workDirAbsPath = os.path.abspath(workDir)
# targetDir = os.path.normpath(os.path.join(workDirAbsPath, directory))
# print(targetDir)
# validDir = os.path.commonpath([workDirAbsPath, targetDir]) == workDirAbsPath
# print(validDir)
# if not validDir:
#     print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
# if validDir:
#     print(f'WTF why is it still working? wit "{directory}"')

if __name__ == "__main__":
    
    get_files_info("calculator", ".")
    # get_files_info("calculator", "/bin")
    # get_files_info("calculator", "../")
    # get_files_info("calculator", "main.py")
