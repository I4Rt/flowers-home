def getDayWord(n):
    if n % 10 == 1:
        return 'день'
    elif 1 < n % 10 < 5:
        return 'дня'
    elif n % 10 > 4:
        return 'дней'
    raise Exception('Недопустимый формат дня')