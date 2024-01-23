class Utils:
    @classmethod
    def file_to_string(cls, file_name: str):
        with open(file_name, "r", encoding="utf-8") as input_file:
            return "".join(input_file.readlines())

    @classmethod
    def string_to_file(cls, file_name: str, string: str):
        with open(file_name, "w", encoding="utf-8") as output_file:
            output_file.write(string)