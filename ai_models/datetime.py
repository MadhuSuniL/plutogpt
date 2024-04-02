from datetime import datetime
from pytz import timezone
import random, calendar
from ai_utils.keywords import date_formats, time_formats
days_list = calendar.day_name[0:]

class DateTime:
    
    def get_date(self, tz=None, format='24h'):
        tz = tz or 'UTC'
        tz_obj = timezone(tz)
        now = datetime.now(tz=tz_obj)
        date_format = random.choice(date_formats)
        if format == '12h':
            date_format = date_format.replace('HH', 'hh')
        return now.strftime(date_format)
    
    def get_time(self, tz=None, format='24h'):
        tz = tz or 'UTC'
        tz_obj = timezone(tz)
        now = datetime.now(tz=tz_obj)
        time_format = random.choice(time_formats)
        if format == '12h':
            time_format = time_format.replace('HH', 'hh')
        return now.strftime(time_format)
    
    def get_datetime(self, tz=None, date_format='24h', time_format='24h'):
        tz = tz or 'UTC'
        tz_obj = timezone(tz)
        now = datetime.now(tz=tz_obj)
        if date_format == '12h':
            date_format = random.choice(date_formats).replace('HH', 'hh')
        else:
            date_format = random.choice(date_formats)
        if time_format == '12h':
            time_format = random.choice(time_formats).replace('HH', 'hh')
        else:
            time_format = random.choice(time_formats)
        return now.strftime(f"{date_format} {time_format}")

    def get_calender(self, year = datetime.now().date().year, month = datetime.now().date().month):
        cal = calendar.HTMLCalendar()
        html_code = cal.formatmonth(year, month).replace('border="0"', 'border="1"').replace('cellpadding="0"', 'cellpadding="2"').replace('class="month"', 'class="font-bold"').replace('colspan="7"', 'colspan="7" style="text-align:center;" ')
        return html_code

    def get_weekday(self, year = datetime.now().date().year, month = datetime.now().date().month, day = datetime.now().date().day):
        weekday = calendar.weekday(int(year), int(month), int(day))
        return f'The week day for <b>{year}-{month}-{day}</b> is <b class="text-2xl">{days_list[weekday]}</b>' 
    
    def get_difference_between_dates(self, date1, date2):
        return f"differnece between <b>{date1.strftime(random.choice(date_formats))}</b> and <b>{date2.strftime(random.choice(date_formats))}</b> is <b class='text-2xl'>{str(date1 - date2).replace('-', '').split(',')[0]}</b>"
    
    def get_next_day(self, day):        
        weekday = days_list.index(day.title())
        today = datetime.date.today()
        days_until_weekday = (weekday - today.weekday() + 7) % 7
        if days_until_weekday == 0:
            next_weekday = today + datetime.timedelta(days=days_until_weekday+7)
            return f"The next <b>{calendar.day_name[weekday]}</b> is on <b class='text-2xl'>{next_weekday}</b>"
        elif days_until_weekday == 1:
            next_weekday = today + datetime.timedelta(days=days_until_weekday) 
            return f"The next <b>{calendar.day_name[weekday]}</b> is on <b class='text-2xl'>{next_weekday} (Tomorrow)</b>"         
        elif days_until_weekday == 2:
            next_weekday = today + datetime.timedelta(days=days_until_weekday) 
            return f"The next <b>{calendar.day_name[weekday]}</b> is on <b class='text-2xl'>{next_weekday} (Day after tomorrow)</b>"
        else:
            next_weekday = today + datetime.timedelta(days=days_until_weekday) 
            return f"The next <b>{calendar.day_name[weekday]}</b> is on <b class='text-2xl'>{next_weekday}</b>"
    
    def get_days_till(self, target_date):
        today = datetime.date.today()
        days_until = (target_date - today).days
        return (f"There are <b class='text-2xl'>{days_until}</b> days until <b>{target_date}</b>")                 

    def get_week_no(self, date = datetime.date.today()):
        year, week_num, day_of_week = date.isocalendar()
        return(f"The current week number is <b class='text-2xl'>{week_num}</b>")
    
    def is_leap_year(self, year):
        try:
            if calendar.isleap(year):
                return(f"<b>{year}</b> is <b class='text-2xl'>a leap year</b>")
            else:
                return(f"<b>{year}</b> is <b class='text-2xl'> not a leap year</b>")        
        except:
            return 'If you are trying to find the specific year is leap year or not, Please inlcude the year'
    
            
            