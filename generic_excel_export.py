"""
This piece of code shows two different aproachs to deliver excel from through
Python/Django
The first approach is a generic Class Based View (CBV) class that gives a CSV
file.

The second approach delivers a Json file for a AJAX request. This way, you can
handle errors on the front end.
"""

from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render


class get_excel(TemplateView):

    def get_colum_names():
        """ The returning list must contains the name for the columns in order """
        column_names = ["col 1", "col 2", "col n"]
        return column_names

    def get_data():
        """
        Wherever your data is, get, bundle and return.
        It must be a list of strings (comma separated). Each string is the row
        containing the cells separated by comma.
        """
        your_data = []
        your_data.append("row_1", "row_2", "row_n")
        return your_data

    def post(self):
            your_data = self.get_data()

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

            t = loader.get_template('exportacao/csv.txt')

            column_names = self.get_colum_names()
            column_names = ";".join(cn for cn in column_names)

            """
            Include the BOM (byte order mark) and its done.
            Excel will recognise the output data as UTF-8 encoding.
            """
            column_names = u'\ufeff'.encode('utf8') + column_names

            c = Context({'column_names': column_names,
                         'data': self.your_data
                        })

            response.write(t.render(c))
            return response
