def loadl(s: list) -> dict:
    """
    :param s: 줄들을 받아옵니다
    :return: dict 타입으로 재귀적으로 노드륿 돌려줍니다. PART{} PART{} 같이 같은 노드가 여러 개 있을 경우 Key로 PART, 값으로 [{},{}]을 담아 줍니다.
    """
    dic = {}
    c = 0
    n = 0
    for i in range(len(s)):
        if "{" in s[i]:
            if c == 0:
                n = i
            c += 1
        elif "}" in s[i]:
            c -= 1
            if c == 0:
                u = s[n - 1].strip()
                if dic.get(u) is None:
                    dic[u] = []
                dic[u].append(loadl(s[n + 1:i - 1]))
        elif ("=" in s[i]) and c == 0:
            d = s[i].split("=")
            dic[d[0].strip()] = d[1].strip()
        i += 1
    return dic


def loads(ln: str) -> dict:
    """
    :param ln: 줄들을 받아옵니다
    :return: dict 타입으로 재귀적으로 노드륿 돌려줍니다. PART{} PART{} 같이 같은 노드가 여러 개 있을 경우 Key로 PART, 값으로 [{},{}]을 담아 줍니다.
    """
    s = ln.split("\n")
    return loadl(s)


def dumpl(ln: dict) -> list:
    """
    :param ln: 재귀적으로 구성된 노드를 받아옵니다
    :return: 다시 KSP 파일 형식으로 구성해서 예쁘게 들여쓴 후 줄별 list로 돌려줍니다
    """
    r = _rdumps(ln)
    c = 0
    for i in range(len(r)):
        if "}" in r[i]:
            c -= 1
        r[i] = "    " * c + r[i]
        if "{" in r[i]:
            c += 1
    return r


def dumps(ln: dict) -> str:
    """
    :param ln: 재귀적으로 구성된 노드를 받아옵니다
    :return: 다시 KSP 파일 형식으로 구성해서 예쁘게 들여쓴 후 str로 돌려줍니다
    """
    return '\n'.join(dumpl(ln))


def _rdumps(ln: dict):
    """
    :param ln: 재귀적으로 구성된 노드를 받아옵니다
    :return: 다시 KSP 파일 형식으로 구성해서 들여쓰지 않고 줄별 list로 돌려줍니다
    """
    s = []
    for k, v in ln.items():
        if str(type(v)) == str(type([])):
            s.append(k)
            s.append("{")
            for t in v:
                s += _rdumps(t)
            s.append("}")
        else:
            s.append(k + " = " + v)
    return s