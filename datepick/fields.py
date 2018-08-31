# from django import forms
#
# class SpecialForm(forms.TextInput):
#     def __init__(self, data_list, name, *args, **kwargs):
#         super(SpecialForm, self).__init__(*args, **kwargs)
#         self._name = name
#         self._list = data_list
#         self.attrs.update({'list': 'list__%s' % self._name})
#
#     def render(self, name, value, attrs=None):
#         text_html = super(SpecialForm, self).render(name, value, attrs=attrs)
#         data_list = '<datalist id="list__%s">' % self._name
#         for item in self._list:
#             data_list += '<option value="%s">' % item
#         data_list += '</datalist>'
#
#         return (text_html + data_list)