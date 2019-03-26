import re,jieba,datetime

def remove_punctuation(line, strip_all=True):
  if strip_all:
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
  else:
    punctuation = """，！？。＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏ """
    punctuation_en="""!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
    re_punctuation = "[{}]+".format(punctuation)
    re_punctuation_en = "[{}]+".format(punctuation_en)
    line = re.sub(re_punctuation, "", line)
    line=re.sub(re_punctuation_en,"",line)
  return line.strip()

def cutline(line):
    line=str(line)
    words=jieba.cut(line,cut_all=False)
    re=" ".join(words)
    return re

def get_stopwords(line):
    f=open(".\stopwords.txt")
    stopwords=[]
    for words in f:
        stopwords.append(words)
    final=[]
    for word in line:
        if word not in stopwords:
            final.append(word)
    finalString="".join(final)
    f.close()
    return finalString

def clean_time_text(text):
    text=text.replace("三十一", "31").replace("三十", "30")
    text =text.replace("二十一", "21").replace("二十二", "22").replace("二十三", "23").replace("二十四", "24").replace("二十五", "25").replace(
        "二十六", "26").replace("二十七", "27").replace("二十八", "28").replace("二十九", "29").replace("二十", "20")
    text =text.replace("十一","11").replace("十二","12").replace("十三","13").replace("十四","14").replace("十五","15").replace("十六","16").replace("十七","17").replace("十八","18").replace("十九","19").replace("十","10")
    text =text.replace("一","1").replace("二","2").replace("两","2").replace("三","3").replace("四","4").replace("五","5").replace("六","6").replace("七","7").replace("八","8").replace("九","9")
    text =text.replace("一刻","15分").replace("半","30分").replace(":","点")
    text =text.replace("今天",datetime.datetime.now().strftime("%Y")+"年"+datetime.datetime.now().strftime("%m")+"月"+datetime.datetime.now().strftime("%d")+"日").replace("明天",((datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y"))+"年"+((datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%m"))+"月"+((datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%d"))+"日").replace("后天",((datetime.datetime.now()+datetime.timedelta(days=2)).strftime("%Y"))+"年"+((datetime.datetime.now()+datetime.timedelta(days=2)).strftime("%m"))+"月"+((datetime.datetime.now()+datetime.timedelta(days=2)).strftime("%d"))+"日")
    if len(re.findall(re.compile((r"([\u4E00-\u9FA5]*|[0-9]*)上午([\u4E00-\u9FA5]*|[0-9]*)点")), text))>0:
        text = text.replace("上午", "")
    if len(re.findall(re.compile((r"([\u4E00-\u9FA5]*|[0-9]*)下午([\u4E00-\u9FA5]*|[0-9]*)点")), text))>0:
        if int(text[text.find("下午")+2:text.find("点")])<=12:
            a=int(text.find("下午") + 2)
            b=str(int(text[text.find("下午") + 2:text.find("点")]) + 12)
            text=sub_index(text,a,b)
            text = text.replace("下午", " ")
        elif int(text[text.find("下午")+2:text.find("点")])>=13:
            text = text.replace("下午", "")
    if (len(re.findall(re.compile((r"([\u4E00-\u9FA5]*|[0-9]*)上午([\u4E00-\u9FA5]*|[0-9]*)点")), text))==0)&(len(re.findall(re.compile((r"([\u4E00-\u9FA5]*|[0-9]*)上午([\u4E00-\u9FA5]*|[0-9]*)")), text))>0):
        text = text.replace("上午", " 10点")
    if (len(re.findall(re.compile((r"([\u4E00-\u9FA5]*|[0-9]*)下午([\u4E00-\u9FA5]*|[0-9]*)点")), text)) == 0) & (
            len(re.findall(re.compile((r"([\u4E00-\u9FA5]*|[0-9]*)下午([\u4E00-\u9FA5]*|[0-9]*)")), text)) > 0):
        text = text.replace("下午", " 16点")
    return text

def sub_index(string,location,word):
    new=[]
    for s in string:
        new.append(s)
    new[location]=word
    return "".join(new)



# text="2019年3月26日下午"
# text=clean_time_text(text)
# print(text)




