from datetime import datetime
import locale
import re
locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')


def xpath(path):
    def decorator(f):
        def wrapper(listing):
            data = listing.xpath(f'./{path}/text()')
            if data:
                return f(data[0])
            return f('')
        return wrapper
    return decorator


def keep_digits(text):
    text = re.sub(r'[^\d,]', '', text.strip())
    text = text.replace(',', '.')
    if not text:
        return None
    return float(text)


@xpath('/div[1]/h2/span[2]')
def address_floor(text):
    return text.strip().split(',') + [None, None]


def address(listing):
    return address_floor(listing)[0]


def floor(listing):
    data = address_floor(listing)[1]
    if data:
        return keep_digits(data)
    return None


@xpath('/div[1]/div/span[2]')
def area(text):
    return text.strip()


@xpath('/div[2]/div/div[2]')
def rent(text):
    return keep_digits(text)


@xpath('/div[3]/div[1]/span')
def price(text):
    return keep_digits(text)


@xpath('/div[3]/div[2]/div[1]')
def date(text):
    d = text.replace('Såld', '').strip()
    if not d:
        return None
    return datetime.strptime(d, '%d %B %Y')


@xpath('/div[3]/div[2]/div[2]')
def kr_sqm(text):
    return keep_digits(text)


@xpath('/div[4]')
def change(text):
    return keep_digits(text)


@xpath('/div[2]/div/div[1]')
def sqm_rooms(text):
    def floats(text):
        for x in text.split():
            try:
                yield float(x)
            except:
                pass
    data = list(floats(text)) + [None, None]
    return {'sqm': data[0], 'rooms': data[1]}


def sqm(listing):
    return sqm_rooms(listing)['sqm']


def rooms(listing):
    return sqm_rooms(listing)['rooms']
