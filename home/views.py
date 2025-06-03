from django.shortcuts import render
from django.views.generic import View

class IndexClassBaseView(View):
    def get(self,reqeust):
        return render(reqeust,'index.html')
