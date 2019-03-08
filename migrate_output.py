import os


def split_dirname(dirname):
    s = dirname.replace("-", "/")
    s = s.replace(".", "/")
    s = s.replace(":", "")
    return s


def dirlist():
    directories = [d for d in os.listdir("output") if d.startswith("2")]
    return directories


def main(output_directory, city):
    new_root_path = os.path.join(output_directory, city)
    for directory in dirlist():
        old_path = os.path.join(OUTPUT_DIRECTORY, directory)
        new_path = os.path.join(new_root_path, split_dirname(directory))
        os.renames(old_path, new_path)


if __name__ == "__main__":
    OUTPUT_DIRECTORY = "output"
    CITY = "vancouver"
    main(OUTPUT_DIRECTORY, CITY)
