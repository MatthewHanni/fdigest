from hashlib import sha512
import datetime
import csv
import os
import pathlib


def walk_dir(source_path):
    """
    Returns a list of tuples (file root dir, file name) for each file contained within the source_path

            Parameters:
                    source_path (str): Drive letter path or directory with which should be indexed


            Returns:
                    filename_dir_list (list): List of tuples. Each tuple contains a root directory and a file name
    """
    filename_dir_list = []
    for root, dirs, files in os.walk(source_path):
        print(f'Walking directory...Found {len(filename_dir_list)} source files.')
        for name in files:
            filename_dir_list.append((root, name))
    return filename_dir_list


def get_sha512_hash(file_path):
    """
    Returns the SHA512 hash of the file located at file_path

            Parameters:
                    file_path (str): Path to a file


            Returns:
                    hasher_hexdigest (str): Hexidecimal SHA512 hash digest for the file
    """
    block_size = 65536
    hasher = sha512()
    with open(file_path, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    hasher_hexdigest = hasher.hexdigest()
    return hasher_hexdigest


def get_source_path():
    """
    Prompts the user for the source drive or directory for which a digest will be generated

            Returns:
                    source_path (str): Path supplied by the user, validated by the script
    """
    while True:
        source_path = input(
            'Enter the path for which a digest should be created (e.g. "C:", "P:\homework do not open"): ')
        if not os.path.exists(source_path):
            print('Path does not exist. Please try again.')
            continue
        if not os.path.isdir(source_path):
            print('Path is not directory. Please try again.')
            continue
        return source_path


def process_record(filename_dir_record):
    file_dir = filename_dir_record[0]
    file_name = filename_dir_record[1]
    file_path = os.path.join(file_dir, file_name)

    digest_record = {}
    digest_record['file_path'] = file_path
    digest_record['file_name'] = file_name
    digest_record['file_dir'] = file_dir
    digest_record['file_extension'] = pathlib.Path(file_path).suffix
    digest_record['file_size'] = float(str(os.path.getsize(file_path)))
    digest_record['file_creation_time'] = str(datetime.datetime.utcfromtimestamp(os.path.getctime(file_path)))
    digest_record['last_modification_time'] = str(datetime.datetime.utcfromtimestamp(os.path.getmtime(file_path)))
    digest_record['sha512_hash'] = get_sha512_hash(file_path=file_path)
    return digest_record


def write_digest(digest_rows_dictlist):
    run_timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    digest_csv = f'fdigest--{run_timestamp}.csv'
    fieldnames = ["file_path", "file_name", "file_dir", "file_extension", "file_size", "file_creation_time",
                  "last_modification_time", "sha512_hash"]
    with open(digest_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(digest_rows_dictlist)


def main():
    source_path = get_source_path()
    filename_dir_list = walk_dir(source_path=source_path)
    digest_rows_dictlist = []
    i = 0
    for filename_dir_record in filename_dir_list:
        print(
            f'{datetime.datetime.now()}\tProcessing {i + 1}:{len(filename_dir_list)}\t'
            f'{os.path.join(filename_dir_record[0], filename_dir_record[1])}')
        digest_record = process_record(filename_dir_record)
        digest_rows_dictlist.append(digest_record)
    write_digest(digest_rows_dictlist=digest_rows_dictlist)


if __name__ == "__main__":
    main()
