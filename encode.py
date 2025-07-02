def int_to_base62(n: int) -> str:
    if n == 0:
        return '0'
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    base = 62
    result = ''
    while n > 0:
        n, rem = divmod(n, base)
        result = chars[rem] + result
    return result

#thank`s for Kotazz and Mishanya