from . import jalali

def persian_numbers_converter(mystr):
    numbers = {
        "0" : "۰",
        "1" : "۱",
        "2" : "۲",
        "3" : "۳",
        "4" : "۴",
        "5" : "۵",
        "6" : "۶",
        "7" : "۷",
        "8" : "۸",
        "9" : "۹",
    }

    for e, p in numbers.items():
        mystr = mystr.replace(e, p)
    return mystr

def jalali_converter(time):
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    output = "{}/{}/{}".format(
        time_to_tuple[0],
        time_to_tuple[1],
        time_to_tuple[2],
        )

    return persian_numbers_converter(output)
