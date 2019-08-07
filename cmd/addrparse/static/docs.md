# 常识智能组件 - 文本地址解析🏡

文本地址解析服务接口精准解析地址信息，标准化各部分地址信息区段，输出标准结构的地址信息。目前提供五级地址查询服务，基于权威五级地址库，可根据原始地址查询出标准五级地址，或对已有非标准地址进行清洗、结构化、纠错和补全。

权威五级地址库来源于国家统计局网站，提供了中国省市县乡村5级地址的标准名称和对应的统计用区划代码和城乡划分代码。

数据抓取和清洗的程序请参见如下地址：[https://github.com/liuzl/china-address-code](https://github.com/liuzl/china-address-code)

权威五级地址库是tsv格式的文本文件，第一列是区划代码，第二列是地址名称。其中地址类型根据区划代码的位数进行区分：省级2位、市级4位、县级6位、乡级9位、村级12位。

标准地址解析服务是基于权威五级地址库，采用语义解析技术进行实现的。

### HTTP请求

`POST https://semantics.work/addr/api`

### 请求参数

参数 | 描述
--------- | -------
`text` | `字符串`，用户输入的待解析地址文本，UTF-8编码 

### 状态码说明

status | 说明
--------- | -------
`ok` | 查找成功
`fail` | 失败，此时`message`保存错误信息

### 返回信息说明

字段 | 说明 
--- | ---
`message`|结构化地址信息

### 返回数据应答样例

输入数据：`邢台石家庄村北京海淀`

```json
{
   "status":"ok",
   "message":[
      {
         "level":"village",
         "address":[
            {
               "code":"130523101218",
               "province":"河北省",
               "city":"邢台市",
               "county":"内丘县",
               "town":"大孟村镇",
               "village":"石家庄村委会"
            },
            {
               "code":"130524100203",
               "province":"河北省",
               "city":"邢台市",
               "county":"柏乡县",
               "town":"柏乡镇",
               "village":"石家庄村委会"
            },
            {
               "code":"130534105225",
               "province":"河北省",
               "city":"邢台市",
               "county":"清河县",
               "town":"坝营镇",
               "village":"石家庄村委会"
            },
            {
               "code":"130581101213",
               "province":"河北省",
               "city":"邢台市",
               "county":"南宫市",
               "town":"大高村镇",
               "village":"石家庄村委会"
            }
         ],
         "start":0,
         "end":18,
         "text":"邢台石家庄村",
         "length":18
      },
      {
         "level":"county",
         "address":[
            {
               "code":"110108",
               "province":"北京市",
               "city":"市辖区",
               "county":"海淀区"
            }
         ],
         "start":18,
         "end":30,
         "text":"北京海淀",
         "length":12
      }
   ]
}
```