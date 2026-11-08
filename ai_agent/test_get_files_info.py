from functions.get_files_info import get_files_info
#from ai_agent import main


if __name__ == "__main__":
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))
    print(get_files_info("calculator", "main.py"))
