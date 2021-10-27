from django.http.response import Http404
from rest_framework import views
from rest_framework.response import Response

from .utils import Scraper, AzureAPI
from .serializers import YahooSerializer, EnterpriseSerializer ,SustainableSerializer, SentimentSerializer, SummarySerializer

class ESGView(views.APIView):
    def get(self, request):
        ticker = self.request.query_params.get("ticker")
        company = self.request.query_params.get("company")
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
        azure = AzureAPI()
        sentiment = azure.sentiment_analysis(document)
        summary = azure.extractive_summarization(document)
        if sentiment:
            sentiment = SentimentSerializer(sentiment).data
        if summary:
            summary = SummarySerializer(summary).data
        response = {
            'sentiment': sentiment,
            'summary': summary
        }
        return Response(response)