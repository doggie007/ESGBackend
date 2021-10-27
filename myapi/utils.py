import requests
import json
from bs4 import BeautifulSoup
from random import choice


from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction
from azure.core.credentials import AzureKeyCredential

class Scraper:
    def __init__(self) -> None:
        self.user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        ]

    def scrape_yahoo(self,ticker="none"):
        url = f'http://finance.yahoo.com/quote/{ticker}/sustainability?p={ticker}'
        
        headers = { 'User-Agent': choice(self.user_agent_list)} 
        try:
            web_data = requests.get(url,headers=headers)
        except:
            return None
        if web_data.status_code != 200:
            return None
        soup = BeautifulSoup(web_data.text, 'html.parser')
        try:
            total_esg_score = soup.find("div",{"class":"Fz(36px) Fw(600) D(ib) Mend(5px)"}).text
            percentile = soup.find("span",{"class":"Bdstarts(s) Bdstartw(0.5px) Pstart(10px) Bdc($seperatorColor) Fz(12px) smartphone_Bd(n) Fw(500)"}).text
            separate_scores = soup.findAll("div",{"class":"D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)"})
            environment_score = separate_scores[0].text
            social_score = separate_scores[1].text
            governance_score = separate_scores[2].text
            return {"yahoo_total_score":total_esg_score,"yahoo_percentile":percentile,"yahoo_total_rating":self.calculate_rating(float(total_esg_score)),"yahoo_e":environment_score,"yahoo_s":social_score,"yahoo_g":governance_score}
        except:
            return None

    def calculate_rating(self,score):
        if score <= 10:
            return "Negligible"
        elif score <= 20:
            return "Low"
        elif score <= 30:
            return "Medium"
        elif score <= 40:
            return "High"
        else:
            return "Severe"
    
    def call_api(self,ticker="none"):
        url = "https://esg-environmental-social-governance-data.p.rapidapi.com/search"

        querystring = {"q":ticker}

        headers = {
            'x-rapidapi-host': "esg-environmental-social-governance-data.p.rapidapi.com",
            'x-rapidapi-key': "32bede5644mshba3ea132aabc097p1a3728jsn1ed47cce2ead"
            }

        response = requests.request("GET", url, headers=headers, params=querystring).text
        if response == "[]":
            return None
        data = json.loads(response)[0]
        results = {"api_total_grade":data.get("total_grade"),"api_total_level":data.get("total_level"),"api_egrade":data.get("environment_grade"),"api_elevel":data.get("environment_level"),"api_sgrade":data.get("social_grade"),"api_slevel":data.get("social_level"),"api_ggrade":data.get("governance_grade"),"api_glevel":data.get("governance_level")}
        return results


    def scrape_sustainable(self,company):
        # requires full name of company

        # requires all lowercase and slugified
        company = company.lower().replace(' ','-')

        url = f"https://www.sustainable.com/companies/{company}"
        headers = { 'User-Agent': choice(self.user_agent_list)} 
        try:
            web_data = requests.get(url,headers=headers)
        except:
            return None
        if web_data.status_code != 200:
            return None
        soup = BeautifulSoup(web_data.text, 'html.parser')
        overall_score = soup.find("span",{"class":"text-5xl font-bold text-mono text-black"}).text
        ranks = soup.findAll("span",{"class":"text-5xl font-bold text-mono text-black inline-flex"})
        overall_rank, industry_rank = ranks[0].text, ranks[1].text
        out_of = soup.findAll("span",{"class":"ml-2 text-lg font-medium text-gray-400"})
        _, total_out_of, industry_out_of = out_of[0].text[2:], out_of[1].text[2:], out_of[2].text[2:]
        esg = soup.findAll("span",{"class":"text-2xl text-gray-800 text-mono"})
        score_e = esg[0].text
        score_s = esg[1].text
        score_g = esg[2].text
        env_rank = esg[3].text.split()[0]
        social_rank = esg[4].text.split()[0]
        gov_rank = esg[5].text.split()[0]
        result = {"sust_overall_score":overall_score,"sust_overall_rank":overall_rank, "sust_total_out_of":total_out_of,"sust_e":score_e,"sust_s":score_s,"sust_g":score_g,"sust_industry_rank":industry_rank,"sust_industry_out_of":industry_out_of,"sust_erank":env_rank,"sust_srank":social_rank,"sust_grank":gov_rank}
        return result




class AzureAPI:

    def __init__(self) -> None:
        self.key = "39dcefbbc05b4660916903493091f5fa"
        self.endpoint = "https://sentiment-esg.cognitiveservices.azure.com/"
    
    # authentication
    def authenticate_client(self):
        ta_credential = AzureKeyCredential(self.key)
        text_analytics_client = TextAnalyticsClient(
                endpoint=self.endpoint, 
                credential=ta_credential)
        return text_analytics_client

    # sentiment analysis returns sentiment, positive, neutral, negative
    def sentiment_analysis(self, document):
        client = self.authenticate_client()

        document = [document]
        response = client.analyze_sentiment(documents=document)[0]
        # print(response)
        # print("Document Sentiment: {}".format(response.sentiment))
        # print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        #     response.confidence_scores.positive,
        #     response.confidence_scores.neutral,
        #     response.confidence_scores.negative,
        # ))
        # # print(response)
        return {"sentiment":response.sentiment,"positive":response.confidence_scores.positive,"neutral":response.confidence_scores.neutral,"negative":response.confidence_scores.negative}
     # print(sentiment_analysis_example(client))



    def extractive_summarization(self, document):
        client = self.authenticate_client()
        document = [document]

        poller = client.begin_analyze_actions(
            document,
            actions=[
                ExtractSummaryAction()
            ],
        )

        document_results = poller.result()
        for result in document_results:
            extract_summary_result = result[0]  # first document, first result
            if extract_summary_result.is_error:
                print("...Is an error with code '{}' and message '{}'".format(
                    extract_summary_result.code, extract_summary_result.message
                ))
                return None
            else:
                return {"summary":" ".join([sentence.text for sentence in extract_summary_result.sentences])}
    