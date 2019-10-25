from django.db import models

# Create your models here.
# Company model
class Company(models.Model):
    ticker = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length = 50)
    sector = models.CharField(max_length = 255)

class Summary(models.Model):
    ticker_date = models.CharField(max_length=13, primary_key=True)
    date = models.DateTimeField('Date Scraped')
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    market_cap = models.BigIntegerField()
    risk = models.DecimalField(decimal_places = 2, max_digits = 5)
    debt_equity_index = models.DecimalField(decimal_places = 2, max_digits = 5)
    net_dividend_yield_index = models.DecimalField(decimal_places = 2, max_digits = 5)
    sharpe_ratio_index = models.DecimalField(decimal_places = 2, max_digits = 5)
    return_on_equity_index = models.DecimalField(decimal_places = 2, max_digits = 5)
    score = models.SmallIntegerField()

class Directors(models.Model):
    date = models.DateTimeField('Date Scraped')
    name_date = models.CharField(max_length=99, primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    director_name = models.CharField(max_length=100)
    director_role = models.CharField(max_length=100)

class Dividends(models.Model):
    ticker_date = models.CharField(max_length=13, primary_key=True)
    date = models.DateTimeField('Date Scraped')
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    dividends = models.FloatField()

class Ratios(models.Model):
    ticker_date = models.CharField(max_length=13, primary_key=True)
    date = models.DateTimeField('Date Scraped')
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    ePS = models.FloatField()
    nTA = models.FloatField()
    net_DPS = models.FloatField()
    gross_DPS = models.FloatField()
    beta_Value = models.FloatField()
    price_NTA = models.FloatField()
    net_Yield = models.FloatField()
    gross_Yield = models.FloatField()
    sharpe = models.FloatField()
    debt_Equity = models.FloatField()
    return_On_Equity = models.FloatField()

class IncomeStatement(models.Model):
    year = models.DateTimeField('Date Scraped')
    ticker_year = models.CharField(max_length=7, primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    sales_revenue = models.FloatField()
    investment_revenue = models.FloatField()
    total_core_revenue = models.FloatField()
    EBITDA = models.FloatField()
    depreciation = models.FloatField()
    EBIT = models.FloatField()
    interest_expense = models.FloatField()
    PBT = models.FloatField()
    income_tax_expense = models.FloatField()
    continuing_operations = models.FloatField()
    MIE = models.FloatField()
    net_income = models.FloatField()
    basic_eps = models.FloatField()
    diluted_eps = models.FloatField()

class Price(models.Model):
    date = models.DateTimeField('Date Scraped')
    ticker_date = models.CharField(max_length=13, primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    price = models.FloatField()
    capital_adjusted = models.FloatField()
    volume_traded = models.FloatField()
    value_traded = models.FloatField()
    number_of_trades = models.FloatField()
    price_change = models.FloatField()

class CompanyProfile(models.Model):
    date = models.DateTimeField('Date Scraped')
    ticker_date = models.CharField(max_length=13, primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    overview = models.TextField()
    performance = models.TextField()
    outlook = models.TextField()
    description = models.TextField()

class CashTable(models.Model):
    year = models.DateTimeField('Date Scraped')
    ticker_year = models.CharField(max_length=7, primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    operating = models.FloatField()
    investing = models.FloatField()
    finance = models.FloatField()
    net_change = models.FloatField()

class Equity(models.Model):
    year = models.DateTimeField('Date Scraped')
    ticker_year = models.CharField(max_length=7, primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    paid_in_capital = models.FloatField()
    reatained_earnings = models.FloatField()
    minority_interest = models.FloatField()
    other_equity = models.FloatField()
    total_equity = models.FloatField()

class Liabilities(models.Model):
    year = models.DateTimeField('Date Scraped')
    ticker_year = models.CharField(max_length=7, primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    payables = models.FloatField()
    current_debt = models.FloatField()
    current_liabilities = models.FloatField()
    long_term_debt = models.FloatField()
    deferred_tax_liabilities = models.FloatField()
    other_NC_liabilities = models.FloatField()
    NC_liability = models.FloatField()
    total_liability = models.FloatField()

class Assets(models.Model):
    year = models.DateTimeField('Date Scraped')
    ticker_year = models.CharField(max_length=7, primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    cash_equity = models.FloatField()
    NTR = models.FloatField()
    current_inventory = models.FloatField()
    other_CA = models.FloatField()
    PPE = models.FloatField()
    intangible_assests = models.FloatField()
    LT_investments = models.FloatField()
    LT_deferred_assets = models.FloatField()
    other_NCA = models.FloatField()
    current_assets = models.FloatField()
    NC_assets = models.FloatField()
    total_assets = models.FloatField()

class Score(models.Model):
    date = models.DateTimeField('Date Scraped', primary_key=True)
    ticker = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="ticker")
    score = models.FloatField()


# Storing company filters
class Filter(models.Model):
    risk = models.CharField(max_length=20)
    index = models.CharField(max_length=20)
    blacklist = models.TextField()