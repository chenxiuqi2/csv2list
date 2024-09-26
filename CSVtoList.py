class CSVToTextList:
    """
    将CSV文件中某一列的数据提取为TEXT_LIST，并添加一个多行文本输出，适配CR Cycle Text节点和CR TextList节点。
    安装chardet库
    pip install chardet
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        返回定义节点输入字段的字典。
        """
        return {
            "required": {
                "csv_file_path": ("STRING", {"default": "输入CSV文件的路径", "multiline": False}),
                "column_name": ("STRING", {"default": "输入要提取的列名", "multiline": False}),
            }
        }

    # 输出类型：第一个是 TEXT_LIST，第二个是 STRING，用于兼容不同的节点
    RETURN_TYPES = ("TEXT_LIST", "STRING")
    RETURN_NAMES = ("文本列表", "多行文本")

    FUNCTION = "extract_column_to_text_list_and_string"

    CATEGORY = "CSV 处理"

    def extract_column_to_text_list_and_string(self, csv_file_path, column_name):
        """
        读取CSV文件并提取指定列，生成TEXT_LIST和多行文本，适配CR Cycle Text节点和CR TextList节点。
        """
        import csv
        import chardet

        text_list = []
        multiline_text = ""
        
        # 自动检测文件编码
        with open(csv_file_path, 'rb') as f:
            result = chardet.detect(f.read())
            detected_encoding = result['encoding']

        try:
            # 打开CSV文件并使用检测到的编码读取，再将其转换为UTF-8
            with open(csv_file_path, newline='', encoding=detected_encoding) as csvfile:
                csv_reader = csv.DictReader(csvfile)
                
                # 遍历CSV文件的每一行，提取指定列的值，并将其存入列表
                for row in csv_reader:
                    if column_name in row:
                        item = row[column_name]
                        text_list.append(item)  # 直接输出文本，适配 TEXT_LIST
                        multiline_text += item + "\n"  # 同时生成多行文本
                    else:
                        raise ValueError(f"CSV文件中找不到列 {column_name}。")
        except Exception as e:
            return (f"错误: {str(e)}",)

        # 返回文本列表和多行文本
        return (text_list, multiline_text.strip())


NODE_CLASS_MAPPINGS = {
    "CSVToTextList": CSVToTextList
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "CSVToTextList": "CSV 列转TEXT_LIST和多行文本"
}
