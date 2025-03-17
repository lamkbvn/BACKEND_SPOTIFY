def clean_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line.replace("\x00", ""))  # Xóa ký tự null nếu có

clean_file("requirements.txt")
clean_file("installed_packages.txt")
