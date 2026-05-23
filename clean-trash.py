import os
import time
import argparse
import logging


logger = logging.getLogger("clean_trash")


def set_logger():
    logging.basicConfig(
        filename="clean_trash.log",
        level=logging.INFO,
        format="%(asctime)s %(message)s"
    )


def get_age(path):
    return time.time() - os.path.getmtime(path)


def delete_old_files(trash_folder_path, age_thr):
    #удаляем старые файлы
    for root, dirs, files in os.walk(trash_folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_age = get_age(file_path)

            if file_age > age_thr:
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")


def delete_empty_folders(trash_folder_path):
    for root, dirs, files in os.walk(trash_folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)

            if len(os.listdir(dir_path)) == 0:
                os.rmdir(dir_path)
                logger.info(f"Deleted folder: {dir_path}")


def clean_trash(trash_folder_path, age_thr):
    delete_old_files(trash_folder_path, age_thr)
    delete_empty_folders(trash_folder_path)


def main():
    parser = argparse.ArgumentParser(description="Очистка умной корзины.")
    parser.add_argument("--trash_folder_path", required=True)
    parser.add_argument("--age_thr", required=True)
    args = parser.parse_args()

    trash_folder_path = args.trash_folder_path
    age_thr = int(args.age_thr)

    if not os.path.isdir(trash_folder_path):
        raise Exception(f"Error: {trash_folder_path} is not a valid directory.")

    set_logger()
    logger.info("Started")

    clean_trash(trash_folder_path, age_thr)
    time.sleep(1)
    clean_trash(trash_folder_path, age_thr)

    logger.info("Finished")


if __name__ == "__main__":
    main()
