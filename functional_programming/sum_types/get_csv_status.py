from enum import Enum
from typing import Any


class CSVExportStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    SUCCESS = 3
    FAILURE = 4


RawCSVData = list[list[object]]
PreparedCSVData = list[list[str]]
CSVStatusResult = tuple[str, PreparedCSVData | str]

# Don't touch above this line
def PENDING(csvData: list[list[object]]) -> tuple[str, list[list[str]]]:
    conv_list = []
    for object in csvData:
        element_string = [str(element) for element in object]
        conv_list.append(element_string)
    return ("Pending...", conv_list)


def PROCESSING(csvData: list[list[str]]) -> tuple[str, list[list[str]] | str]:
    conv_list = []
    for list in csvData:
        element_str = ",".join(element for element in list)
        conv_list.append(element_str)
    conv_str = "\n".join(conv_list)
    return ("Processing...", conv_str)


def SUCCESS(csvData):
    return ("Success!", csvData)


def FAILURE(csvData):
    temp = PENDING(csvData)
    temp = PROCESSING(temp[1])
    return ("Unknown error, retrying...", temp[1])


def get_csv_status(status: CSVExportStatus, data: Any) -> CSVStatusResult:
    match(status):
        case CSVExportStatus.PENDING:
            return PENDING(data)
        case CSVExportStatus.PROCESSING:
            return PROCESSING(data)
        case CSVExportStatus.SUCCESS:
            return SUCCESS(data)
        case CSVExportStatus.FAILURE:
            return FAILURE(data)
        case _:
            raise Exception("unknown export status")
