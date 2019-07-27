# -*- encoding: utf-8 -*-

def nations_():
    for line in open("chinese_nations.txt"):
        line = line.strip()
        if len(line) > 2:
            yield line[:-1]
        yield line

nations = list(nations_())
nations.sort(reverse=True)

def province_names(name):
    if name.endswith('市'):
        return [name, name.rstrip('市')]
    elif name.endswith('省'):
        return [name, name.rstrip('省')]
    elif name == '内蒙古自治区':
        return [name, '内蒙古省', '内蒙古', '内蒙']
    elif name == '广西壮族自治区':
        return [name, '广西自治区', '广西省', '广西']
    elif name == '西藏自治区':
        return [name, '西藏省', '西藏']
    elif name == '新疆维吾尔自治区':
        return [name,'新疆维吾尔族自治区', '新疆自治区', '新疆省', '新疆']
    return [name]

def _zhou(name):
    x = name.rstrip('自治州')
    for i in nations: x = x.replace(i,"")
    ret = [name,x+"自治州",x+"州",x+"市",x]
    if name == '克孜勒苏柯尔克孜自治州': ret.append("克州")
    elif name == '巴音郭楞蒙古自治州': ret.append("巴州")
    elif name == '博尔塔拉蒙古自治州': ret.append("博州")
    return ret

def city_names(name):
    if name.endswith('市'):
        ret = [name, name.rstrip('市')]
        if name == '呼和浩特市': ret.append('呼市')
        return ret
    elif name.endswith('盟'):
        return [name, name.rstrip('盟')]
    elif name.endswith("自治州"):
        return _zhou(name)
    elif name.endswith("地区"):
        return [name, name.rstrip("地区")]
    return [name]

# TODO: 高新技术产业开发区
county_suffix = ['新区', '矿区','区', '县', '市', '现代产业园', '行政委员会', '管委会']
def county_names(name):
    if len(name) <= 2: return [name] # 赵县
    if name.endswith('自治县'):
        x = name[:-3]
        for i in nations: x = x.replace(i,"")
        if len(x) == 0: return [name]
        ret = [name,x+"自治县",x+"县",x]
        return ret    
    for suffix in county_suffix:
        if name.endswith(suffix):
            return [name, name[:-len(suffix)]]
    if name.endswith('自治旗'):
        x = name[:-len('自治旗')]
        return [name, x+'旗', x]
    elif name.endswith('旗'):
        return [name, name.rstrip('旗')]
    elif name == '保定白沟新城':
        return [name, '白沟']
    elif name.endswith('群岛'):
        return [name, name.rstrip('群岛')]
    elif name == '中沙群岛的岛礁及其海域':
        return [name, '中沙群岛', '中沙']
    return [name]

town_suffix = ['镇', '乡', '街道办事处', '街道', '地区办事处']
def town_names(name):
    for suffix in town_suffix:
        if name.endswith(suffix):
            return [name, name[:-len(suffix)]]
    return [name]

def village_names(name):
    ss = ["村委会","村民委员会","社区村委会","嘎查","嘎查村","嘎查村委员会"]
    for s in ss:
        if name.endswith(s):
            x = name[:-len(s)]
            if x.endswith('村'):
                return [name, x, x.rstrip('村')]
            else:
                return [name, x+'村', x]

    ss = ["社区居委会","社区居民委员会","居民委员会","居委会","社区","社区委员会","社区居委","社区居民委会"]
    for s in ss:
        if name.endswith(s):
            x = name[:-len(s)]
            return [name, x+'社区', x+"小区", x]

    ss = ["生活区","工作区","工业园","工业区"]
    for s in ss:
        if name.endswith(s):
            x = name[:-len(s)]
            return [name, x]
    return [name]

def names(f, name):
    return globals().get('%s_names' % f)(name)

if __name__ == "__main__":
    for line in open("addr.txt"):
        item = line.strip().split("\t")
        print("%s\t%s\t%s"%(item[0],item[1],names(item[0], item[2])))
