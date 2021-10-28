from rest_framework import serializers

class YahooSerializer(serializers.Serializer):
   yahoo_total_score = serializers.CharField()
   yahoo_percentile = serializers.CharField()
   yahoo_total_rating = serializers.CharField()
   yahoo_e = serializers.CharField()
   yahoo_s = serializers.CharField()
   yahoo_g = serializers.CharField()

class EnterpriseSerializer(serializers.Serializer):
    api_total_grade = serializers.CharField()
    api_total_level = serializers.CharField()
    api_egrade = serializers.CharField()
    api_elevel = serializers.CharField()
    api_sgrade = serializers.CharField()
    api_slevel = serializers.CharField()
    api_ggrade = serializers.CharField()
    api_glevel = serializers.CharField()

class SustainableSerializer(serializers.Serializer):
    sust_overall_score = serializers.CharField()
    sust_overall_rank = serializers.CharField()
    sust_total_out_of =serializers.CharField()
    sust_e = serializers.CharField()
    sust_s = serializers.CharField()
    sust_g = serializers.CharField()
    sust_industry_rank = serializers.CharField()
    sust_industry_out_of = serializers.CharField()
    sust_erank = serializers.CharField()
    sust_srank = serializers.CharField()
    sust_grank = serializers.CharField()

class SentimentSerializer(serializers.Serializer):
    sentiment = serializers.CharField()
    positive = serializers.CharField()
    neutral = serializers.CharField()
    negative = serializers.CharField()

class SummarySerializer(serializers.Serializer):
    summary = serializers.CharField()

class WordSerializer(serializers.Serializer):
    word = serializers.CharField()
    url = serializers.CharField() or None