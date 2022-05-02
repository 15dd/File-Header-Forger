FilePath = " "   # 引号内填文件地址,例如 "C:\\Admin" ,注意:一定要用双斜杠
with open(FilePath,"rb+") as rawFile:
    rawFile.seek(0)   # 括号内填需覆盖内容的起始位置,默认从0开始
    rawFile.write(b"PK") # 引号内填需要覆盖的内容,内容默认采用ASCII编码填写,之后自动以数值的形式写入文件前几个字节中
                         # 默认为自动转换成zip的格式
                         # 以转化为zip格式为例:zip的文件头为十六进制的"504b0304",其对应的ASCII编码为"PK",将此填入引号内即可

# 2022/5/2 21:38 Edited by cyh128
# version 1.0





