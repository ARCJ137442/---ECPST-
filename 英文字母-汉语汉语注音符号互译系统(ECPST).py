'''英文字母-汉语汉语注音符号互译 (English-Chinese Phonetic Symbol Translation,ECPST)
原理：基于单元的逐字符扫描互译
主函数：ECPST
'''
# 内部模块
import sys # 系统输入
import os # 系统

# 外部模块
import pyperclip # 剪贴板
from 字符串处理程序通用模块 import * # 子模块

# Core Module
# 核心互译对照表
LANG_DICTORY={
    'b':'ㄅ','p':'ㄆ','m':'ㄇ','f':'ㄈ',
    'd':'ㄉ','t':'ㄊ','n':'ㄋ','l':'ㄌ',
    'g':'ㄍ','k':'ㄎ','h':'ㄏ',
    'j':'ㄐ','q':'ㄑ','x':'ㄒ',
    'zh':'ㄓ','ch':'ㄔ','sh':'ㄕ','r':'ㄖ',
    'z':'ㄗ','c':'ㄘ','s':'ㄙ',
    'i':'ㄧ','u':'ㄨ','ü':'ㄩ',
    'a':'ㄚ','o':'ㄛ','e':'ㄜ','ê':'ㄝ',
    'ai':'ㄞ','ei':'ㄟ','ao':'ㄠ','ou':'ㄡ',
    'an':'ㄢ','en':'ㄣ','ang':'ㄤ','eng':'ㄥ',
    'er':'ㄦ',
    'v':'ㄪ','ng':'ㄫ','gn':'ㄬ', # 某些设备/窗口无法显示
    'w':'^ㄨ','y':'^ㄧ'}

CONFIG_FORMAT_EN='''Configuration code format descriptions:
1. Each character is treated as a value
2. Character in '0-_' and space are false, others are true
3. Three-digit corresponding table :(old Chinese pronunciation is replaced with Chinese characters enabled by initials, and compound phonetic symbols are disabled)
Notes:
1. To distinguish 'w' and 'y' from 'i' and 'u', a '^' will be added before each corresponding Chinese phonetic symbols
2. This system is case insensitive to English
'''
CONFIG_FORMAT_CN='''配置代码格式说明：
一、每个字符视为一个值
二、字符'0-_'和空格为假，其余为真
三、位数对应表：（老国音用声母启用汉字替代，禁用复合注音）
注：
一、为与'i'、'u'区分，'w'、'y'对应的汉语汉语注音符号前用一'^'表示
二、本系统对英文不区分大小写
'''

# 主函数
def ECPST(context:str,oldReplace:bool=False,disableComplex:bool=False) -> str:
    '''输入内容及配置，自动将英文字母与汉语注音符号相互翻译'''
    currentDictory=LANG_DICTORY
    # 替换老国音符号（存在无法显示问题）
    if oldReplace:
        LANG_DICTORY['v']='万'
        LANG_DICTORY['ng']='兀'
        LANG_DICTORY['gn']='广'
    # 生成逆向字典并合成为最终字典
    currentDictory.update({k:v for v,k in currentDictory.items()}) # 使用字典推导式反转字典
    return translateStrByDic(context=context,dictory=currentDictory,singleCharacter=disableComplex)

# 针对单元的翻译
def translateUnit(unitStr:str,dict:dict) -> str:
    if unitStr in dict: return dict[unitStr] # 有对应则返回互译后的值
    else: return unitStr # 否则直接返回

# 子函数：按照字典翻译
def translateStrByDic(context:str,dictory:dict,singleCharacter:bool=False) -> str:
    '''根据字典自动替换字符串内字符并返回新字符'''
    # 获取最长单元的长度
    maxUnitLength=max([len(i) for i in dictory.keys()])
    # 单字符逐字翻译
    if singleCharacter or maxUnitLength==1:
        return ''.join([translateUnit(unitStr=x,dict=dictory) for x in context])
    # 包括多字符的翻译，多字符优先匹配
    result=''
    i=0
    while i<len(context):
        for j in range(maxUnitLength,0,-1): # 反向从长到短遍历
            #if i+j>=len(context): continue # 忽略超过长度的遍历
            unit=context[i:i+j] # 不包括i+j
            # 最后的单字处理：忽略不能翻译的字符
            if j==1 or unit in dictory:
                if j==1:
                    result+=translateUnit(unitStr=unit,dict=dictory)
                else:
                    result+=dictory[unit]
                i+=j # 读写头右移至i+j
                break
    return result

# 主函数面向输入的重写
def onceHandleECPST(context:str,configFormat:str) -> None:
    try:
        result=ECPST(context=context.lower(),
            oldReplace=getBoolConfigInStr(format=configFormat,index=0),
            disableComplex=getBoolConfigInStr(format=configFormat,index=1)
        ) # 读取文本与配置，返回结果
        print(result)
        pyperclip.copy(result)
        print(gsbl(en='The analysis results have been copied to the clipboard',zh='互译结果已复制到剪贴板'))
        os.system("pause")
    except BaseException as error: catchExcept(error,context,"main->")

# Main Function
try:
    print(gsbl(en='<========English-Chinese Phonetic Symbol Translation System (ECPST)========>',
               zh='<========英文字母-汉语汉语注音符号互译系统 (ECPST)========>'
              ))
    #Function Main
    if __name__=='__main__':
        if len(sys.argv)>1:
            try:
                inc=inputBL(en=CONFIG_FORMAT_EN+'Config Code Format: ',zh=CONFIG_FORMAT_CN+'配置代码格式：')
                for path in sys.argv[1:]:
                    try:
                        context=readFile(path)
                        onceHandleECPST(context=context,configFormat=inc)
                    except BaseException as error: catchExcept(error,context,"main->")
            except BaseException as error: catchExcept(error,context,"main->")
        else:
            while True:
                inp=inputBL(en='Please input a text: ',zh='请输入文本：')
                inc=inputBL(en=CONFIG_FORMAT_EN+'Config Code Format: ',zh=CONFIG_FORMAT_CN+'配置代码格式：')
                try:
                    onceHandleECPST(inp,configFormat=inc)
                except BaseException as error:
                    catchExcept(error,inp,"main->")
except BaseException as e:
    printExcept(e,"main->")
