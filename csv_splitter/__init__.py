import os
import csv
import uuid

def get_new_file_name(output_dir,file_num):
    slug = str(uuid.uuid4())
    return os.path.abspath(os.path.join(output_dir,
                                    '{0}{1}.csv'.format(str(file_num), slug)))

def write_collected_to_file(collected_rows, header, path_target):
    with open(path_target, 'w', newline='') as csv_output:
        writer = csv.writer(csv_output, delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL,
                            lineterminator='\n')
        if header:
            writer.writerow(header)
        for output_row in collected_rows:
            writer.writerow(output_row)

def split(origin_file, max_row, output_dir='./', got_header=0, populete_header=0):
    if not((type(max_row) is int) and max_row > 0):
        raise Exception('max_row must be an integer greater than zero')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(origin_file, 'r', newline='') as csv_input:
        reader = csv.reader(csv_input, delimiter=',', quotechar='"', doublequote = False)

        if got_header:
            header = reader.__next__()
            if not(populete_header):
                header = None
        else:
            header = None

        row_num = 0
        collected_rows = []
        output_files = []

        for row in reader:
            need_new_file = not((row_num+1) % max_row)
            collected_rows.append(row)
            if need_new_file:
                file_num = row_num//max_row
                path_target = get_new_file_name(output_dir, file_num)
                write_collected_to_file(collected_rows, header, path_target)
                output_files.append(path_target)
                collected_rows = []
            row_num+=1
        if collected_rows:
            file_num = row_num//max_row
            path_target = get_new_file_name(output_dir, file_num)
            write_collected_to_file(collected_rows, header, path_target)
            output_files.append(path_target)
    return output_files

# files = split('tmp.csv', max_row=25, output_dir='./tmp/', got_header=1, populete_header=1)
# print(files)
