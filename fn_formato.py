def formatNumber(number, decimals, espanol=True):
    if type(number) != int and type(number) != float:
        return number
 
    d={'.':',', ',':'.'}
    return ''.join(d.get(s, s) for s in f"{number:,.{decimals}f}") \
        if espanol \
        else f"{number:,.{decimals}f}"