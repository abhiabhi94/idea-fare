import unicodedata
from datetime import timedelta

from django.template import Context, Template
from django.utils import timezone

from ideas.templatetags.cool_num import cool_num
from ideas.templatetags.cool_timesince import cool_timesince
from tests.base import TestBase


class TestTemplateTags(TestBase):
    def compare_strs(self, s1, s2):
        def NFD(s):
            return unicodedata.normalize('NFD', s)

        return NFD(s1) == NFD(s2)

    def test_define(self):
        data = 'data'
        context = Context({
            'data': data
        })
        Template(
            '{% load define %}'
            '{% define data as var %}'
            ).render(context)
        self.assertEqual(context['var'], data)

    def test_cool_num(self):
        num = 123
        expected = '123'

        self.assertEqual(cool_num(num), expected)

        # test for hundreds(K)
        num = 123_4
        expected = '1.23K'
        self.assertEqual(cool_num(num), expected)

        # test for precision
        num = 123_456
        expected = '123.456K'
        self.assertEqual(cool_num(num, 3), expected)

        # test for million
        num = 123_445_789
        expected = '123.45M'
        self.assertEqual(cool_num(num), expected)

    def test_cool_timesince(self):
        request = 'abcd'
        self.compare_strs(cool_timesince(request), request)

        now = timezone.now()
        minute = now.minute
        hour = now.hour
        day = now.day
        month = now.month
        response = 'Just now'

        # test Just now
        self.compare_strs(cool_timesince(now), response)

        # test minutes
        request = now - timedelta(minutes=minute)
        self.compare_strs(cool_timesince(request), f'{minute} minutes ago')

        # test hours
        request = now - timedelta(hours=hour)
        self.compare_strs(cool_timesince(request), f'{hour} hours ago')

        # test days
        request = now - timedelta(days=day)
        self.compare_strs(cool_timesince(request), f'{day} hours ago')

        # test months
        del_month = 2
        try:
            request = now.replace(month=month-del_month)
        except ValueError:  # happens when day is 31, previous months might not have that day
            request = now.replace(month=month-del_month, day=28)
        self.compare_strs(cool_timesince(request), f'{del_month} months ago')
