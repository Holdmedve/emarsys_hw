import re

class InvalidTimeFormat(Exception):
    pass

class InvalidTimeValue(Exception):
    pass

class InvalidTurnaroundValue(Exception):
    pass


def ValidateTime(time):
    rule = '[0-9]+:[0-9]+-[A-Z]{2}-[a-z,A-Z]+$'
    if not re.match(rule, time):
        raise InvalidTimeFormat

    splitTime = re.split(':|-', time)

    hour = int(splitTime[0])
    if hour < 1 or hour > 12:
        raise InvalidTimeValue
    
    min = int(splitTime[1])
    if min < 0 or min > 59:
        raise InvalidTimeValue

    dayPeriod = splitTime[2]
    if dayPeriod not in ['AM', 'PM']:
        raise InvalidTimeValue

    if dayPeriod == 'AM':
        if hour == 12 or hour < 9:
            raise InvalidTimeValue
    elif dayPeriod == 'PM':
        if hour < 12 and hour > 5:
            raise InvalidTimeValue
        elif hour == 5 and min != 0:
            raise InvalidTimeValue

    day = splitTime[3]
    if day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        raise InvalidTimeValue

    return (hour, min, dayPeriod, day)


def ValidateTurnaround(turnaround):
    if not turnaround.isdecimal():
        raise InvalidTurnaroundValue
    
    turnaround = int(turnaround)
    # one week or longer turnaround can't be displayed with this program
    if turnaround < 1 or turnaround > 39:
        raise InvalidTurnaroundValue

    return turnaround

def Convert12to24format(hour, dayPeriod):
    if dayPeriod == 'PM' and hour != 12:
        hour += 12

    return hour

def Convert24to12format(hour):
    dayPeriod = ''
    if hour < 12:
        dayPeriod = 'AM'
    else:
        dayPeriod = 'PM'
        if hour > 12:
            hour = hour - 12

    return (hour, dayPeriod)
       
def CalculateDueDay(day, deltaDay):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    dayIdx = days.index(day)
    
    dueDayIdx = dayIdx + deltaDay
    dueDay = days[dueDayIdx % 5]

    return dueDay


def CalculateDueDate(time, turnaround):
    fallbackDueDate = (0, 0, '', '')

    hour, min, dayPeriod, day = fallbackDueDate
    try:
        hour, min, dayPeriod, day = ValidateTime(time)
    except InvalidTimeValue or InvalidTimeFormat:
        return fallbackDueDate

    try:
        turnaround = ValidateTurnaround(turnaround)
    except InvalidTurnaroundValue:
        return fallbackDueDate

    hour = Convert12to24format(hour, dayPeriod)

    deltaDay = turnaround // 8
    turnaround -= deltaDay * 8

    hour += turnaround
    if hour >= 17:
        deltaDay += 1
        hour = 9 + (hour - 17)

    hour, dayPeriod = Convert24to12format(hour)
    dueDay = CalculateDueDay(day, deltaDay)
    
    return (hour, min, dayPeriod, dueDay)

