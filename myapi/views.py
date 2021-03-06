from django.http.response import Http404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from .utils import Scraper, AzureAPI
from .serializers import YahooSerializer, EnterpriseSerializer ,SustainableSerializer, SentimentSerializer, SummarySerializer, WordSerializer


class ESGView(views.APIView):
    def get(self, request):
        # print("hello")
        ticker = self.request.query_params.get("ticker")
        company = self.request.query_params.get("company")
        # print(ticker,company)
        # if not ticker or not company:
        #     return Http404("Type in")
        scrape = Scraper()
        yahoo = scrape.scrape_yahoo(ticker)
        enterprise = scrape.call_api(ticker)
        sustainable = scrape.scrape_sustainable(company)
        if yahoo:
            yahoo = YahooSerializer(yahoo).data
        if enterprise:
            enterprise = EnterpriseSerializer(enterprise).data
        if sustainable:
            sustainable = SustainableSerializer(sustainable).data
        response = {
            'yahoo': yahoo,
            'enterprise': enterprise,
            'sustainable': sustainable
        } 
        return Response(response)

class AzureAnalysis(views.APIView):
    def get(self,request):
        document = self.request.query_params.get("document")
        lines = self.request.query_params.get("lines")
        try:
            lines = int(lines)
            if not (0 < lines < 21):
                lines = 3
        except:
            lines = 3
        azure = AzureAPI()

        summary = azure.extractive_summarization(document, lines)
        
        if summary:
            summary = SummarySerializer(summary).data
        else:
            return Http404("Data entered is invalid")

        response = {
            'summary': summary
        }
        return Response(response)