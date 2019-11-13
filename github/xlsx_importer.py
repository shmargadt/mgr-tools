import datetime
import xlsxwriter


def open_xlsx_file_and_return_workbook():
  """Create a workbook with current time name

    Returns:
        workbook (workbook): workbook object for writing excel files.
  """
  now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
  output_file_name = "trello_status-{0}.xlsx".format(now)
  workbook = xlsxwriter.Workbook(output_file_name)
  return workbook

def write_to_xlsx(worksheet, board_name, fieldnames, data, first_row_index, options):
  """Write trello data into xlsx file

    Parameters:
        worksheet (worksheet): current worksheet object for writing.
        board_name (string): Trello board name using as title of each board.
        fieldnames (array): Headers of the columns of the file.
        data (dict): All the data to be written using keys as columns of file.
        first_row_index(int): Index of first row of data to be written
        options(dict): Options for worksheet

    Returns:
        row_index (int): End index of the data.
                         Current row of next data to be written
  """
  # Make Title for table
  row_index = first_row_index+1
  cells_range = "A{0}:D{0}".format(row_index)
  worksheet.merge_range(cells_range, board_name, options['merge_format'])

  # Make Headers for table
  ordered_list = ['members', 'column', 'name', 'url']
  for header in ordered_list:
      col = ordered_list.index(header) 
      worksheet.write(row_index,col,header) 

  # Iterate over the data and write it out row by row.
  row_index+=1
  for datum in data:
    cell_options = {}
    if datum['column'].find("Sprint")  > -1 or datum['column'].find("To Do")  > -1:
      cell_options = options['red']
    if datum['column'].find("Done") > -1:
      cell_options = options['green']
    if datum['column'].find("Doing") > -1:
      cell_options = options['yellow']
    for header in ordered_list:
      col=ordered_list.index(header)
      cell = datum[header]

      # Spilt members column values
      if not col: 
        cell = ', '.join(cell)
      worksheet.write(row_index, col, cell, cell_options)
    row_index+=1
  row_index+=1
  return row_index


def close_xlsx_file(workbook):
  """Close the workbook

    Parameters:
       workbook (workbook): workbook object for writing excel files.

    Returns:
        workbook (workbook): workbook object for writing excel files.
  """
  workbook.close()
  return workbook

