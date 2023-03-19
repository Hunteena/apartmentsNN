import datetime


def get_reserved_dates(bookings: list) -> dict:
    reserved = {}
    for booking in bookings:
        d = booking.dateFrom
        dates = [str(d)]
        while d < booking.dateTo:
            d += datetime.timedelta(days=1)
            dates.append(str(d))
        # print(dates)
        if reserved.get(booking.apartment.id):
            reserved[booking.apartment.id] += dates
        else:
            reserved[booking.apartment.id] = dates
        # print(reserved[booking.apartment.id])
    return reserved
