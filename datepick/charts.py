import pygal

from .models import VacationHistory
from .views import *


class VacationChart():


            
    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = '올해 휴가 사용 현황'


    def get_data(self):

        data = {}
        for history in VacationHistory.objects.all():
            data[history.user] = history.total

        return data

    def generate(self):
        chart_data = self.get_data()

        for key,value in chart_data.items():
            self.chart.add(key,value)

        return self.chart.render(is_unicode= True)