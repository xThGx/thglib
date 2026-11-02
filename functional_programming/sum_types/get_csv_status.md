# Sum Types Practice

Doc2Doc should be able to prepare and export a CSV file of whatever data you input. CSV (Comma-Separated Values) is a ubiquitous text format that allows for information to be structured in a table. There is usually a header row, followed by data rows. Within rows, items are separated by commas.

## Assignment

Complete the get_csv_status function. It should use a match statement to select the correct response depending on the status of the export operation. Create functions to handle each operation as follows:

    PENDING: return a tuple with the string "Pending..." and the raw table data converted from a list of lists of anything, to a prepared list of lists of strings.
        Try to use nested map functions to convert the data items into strings.
        Remember to convert from a map object back into a list.
    PROCESSING: return a tuple with the string "Processing..." and the prepared list of lists of strings converted to one CSV-formatted string.
        For each list of strings, combine the strings with join with commas in between to form a row.
        For each row string, combine the strings with join with newlines ("\n") in between to form a table.
    SUCCESS: return a tuple with the string "Success!" and the data as-is.
    FAILURE: return a tuple with the string "Unknown error, retrying..." and the data after it's been prepared and processed into a CSV string, by combining the steps for PENDING and PROCESSING.
    For any other status, raise an Exception:

    unknown export status

## Tip

It's better if you try this challenge without using loops for practice, but you may use loops.
