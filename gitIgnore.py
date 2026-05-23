import os
import re
import argparse


def is_there_gitignore(project_dir):
    return ".gitignore" in os.listdir(project_dir)


def get_gitignore_lines(project_dir):
    lines = []
    gitignore_path = os.path.join(project_dir, ".gitignore")

    #читаем все строки из .gitignore
    with open(gitignore_path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "" or line[0] == "#":
                continue
            lines.append(line)

    return lines


def file_matches_rule(relative_path, rule):
    if rule[0] == "*":
        regex_rule = rule.replace(".", r"\.")
        regex_rule = regex_rule.replace("*", ".*")
        return re.search(regex_rule + "$", relative_path) is not None

    return relative_path == rule


def make_output_path(project_name, relative_path):
    if "/" not in relative_path:
        return relative_path

    return project_name + "/" + relative_path


def get_ignored_files(project_dir):
    if not is_there_gitignore(project_dir):
        return []

    result = []
    rules = get_gitignore_lines(project_dir)
    project_name = os.path.basename(os.path.abspath(project_dir))

    #обходим все файлы
    for root, dirs, files in os.walk(project_dir):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(full_path, project_dir)
            relative_path = relative_path.replace("\\", "/")

            for rule in rules:
                if file_matches_rule(relative_path, rule):
                    output_path = make_output_path(project_name, relative_path)
                    result.append(
                        f"{output_path} ignored by expression {rule}"
                    )
                    break

    return result


def main():
    parser = argparse.ArgumentParser(description="Проверка ignored файлов.")
    parser.add_argument("--project_dir", required=True)
    args = parser.parse_args()

    project_dir = args.project_dir

    if not os.path.isdir(project_dir):
        raise Exception(f"Error: {project_dir} is not a valid directory.")

    ignored_files = get_ignored_files(project_dir)

    print("Ignored files:")
    for file in ignored_files:
        print(file)


if __name__ == "__main__":
    main()