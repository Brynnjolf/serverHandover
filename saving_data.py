from main.models import *
from django.core.files.storage import default_storage
from datetime import datetime
import json

def save_json_data(payload):
    payloadJSON = json.loads(payload)
    for scrapeDate, scrapeData in payloadJSON.items():
        for companyKey, companyValue in scrapeData.items():
            if companyKey != 'Date':
                companyModel = Company(ticker= companyKey, name= companyValue['Summary']['Name'], sector= companyValue['Profile']['\nBusiness Description\n'])
                companyModel.save()
                #print(companyKey, companyValue['Summary']['Name'], companyValue['Profile']['\nBusiness Description\n'])
                for companyDataKey, companyDataValue in companyValue.items():
                    if companyDataKey == "Summary":
                        summaryList = []
                        summaryList.append(
                            Summary(
                                ticker_date = companyKey + scrapeDate.replace('/','-'),
                                ticker = companyModel,
                                date = datetime.strftime(datetime.now(), "%Y-%m-%d") + " 00:00:00+1200",
                                market_cap = companyDataValue['Market Cap'],
                                risk = companyDataValue['Risk'],
                                debt_equity_index = companyDataValue['Debt Equity Index'],
                                net_dividend_yield_index = companyDataValue['Net Dividend Yield Index'],
                                sharpe_ratio_index = companyDataValue['Sharpe Ratio Index'],
                                return_on_equity_index = companyDataValue['Return on Equity Index'],
                                score = companyDataValue['Score']*100,
                            )
                        )
                        # print(summaryKey, summaryValue)
                        Summary.objects.bulk_create(summaryList, ignore_conflicts = True)
                        print("Saved summary information for ", companyKey)
                    if companyDataKey == "Directors":
                        directorList = []
                        for directorName, roleName in companyDataValue.items():
                            # print(directorName, roleName)
                            directorList.append(
                                Directors(
                                    name_date = directorName + scrapeDate.replace('/','-'),
                                    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "+1200",
                                    ticker = companyModel,
                                    director_name = directorName,
                                    director_role = roleName
                                )
                            )
                        Directors.objects.bulk_create(directorList, ignore_conflicts = True)
                        print("Saved director information for ", companyKey)
                    if companyDataKey == "Ratio":
                        ratioList = []
                        ratioList.append(
                            Ratios(
                                ticker_date = companyKey + scrapeDate.replace('/','-'),
                                date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "+1200",
                                ticker = companyModel,
                                ePS = companyDataValue['EPS'],
                                nTA = companyDataValue['NTA'],
                                net_DPS = companyDataValue['Net DPS'],
                                gross_DPS = companyDataValue['Gross DPS'],
                                beta_Value = companyDataValue['Beta Value'],
                                price_NTA = companyDataValue['Price/NTA'],
                                net_Yield = companyDataValue['Net Yield'],
                                gross_Yield = companyDataValue['Gross Yield'],
                                sharpe = companyDataValue['Sharpe Ratio'],
                                debt_Equity = companyDataValue['Debt Equity'],
                                return_On_Equity = companyDataValue['Return on Equity']
                            )
                        )
                        Ratios.objects.bulk_create(ratioList, ignore_conflicts=True)
                        print("Saved ratio data for ", companyKey)

                    if companyDataKey == "FinancialProfile":
                        # print(companyDataValue['Year'])
                        for statementKey, statementValue in companyDataValue['Data'].items():
                            
                            # print(statementKey)
                            pass
                    if companyDataKey == "Profile":
                        profileList = []
                        # print(profileKey, profileValue)
                        profileList.append(
                            CompanyProfile(
                                ticker_date = companyKey + scrapeDate.replace('/','-'),
                                ticker = companyModel,
                                    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "+1200",
                                overview = companyDataValue['\nOverview\n'],
                                performance = companyDataValue['\nPerformance\n'],
                                outlook = companyDataValue['\nOutlook\n'],
                                description = companyDataValue['\nBusiness Description\n']
                            )
                        )
                        CompanyProfile.objects.bulk_create(profileList, ignore_conflicts= True)
                        print("Saved profile data for ", companyKey)
                    if companyDataKey == "HistoricalPrices":
                        priceList = []
                        for date, priceData in companyDataValue.items():
                            # print(date, priceData)
                            # print(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
                            priceList.append(
                                Price(
                                    ticker_date = companyKey + date,
                                    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "+1200",
                                    ticker = companyModel,
                                    price = priceData['Last'],
                                    capital_adjusted = priceData['Capital Adjusted'],
                                    volume_traded = priceData['Volume Traded'],
                                    value_traded = priceData['Dollar Value Traded'],
                                    number_of_trades = priceData['Trades'],
                                    price_change = priceData['Change']))
                        Price.objects.bulk_create(priceList, ignore_conflicts= True)
                        print("Saved price data for ", companyKey)
                    if companyDataKey == "HistoricalDividends":
                        divList = []
                        for date, dividend in companyDataValue.items():
                            # print(date, dividend)
                            divList.append(
                                Dividends(
                                    ticker_date = companyKey + date,
                                    date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "+1200",
                                    ticker = companyModel,
                                    dividends = dividend))
                        Dividends.objects.bulk_create(divList, ignore_conflicts= True)
                        print("Saved dividend data for ", companyKey)

def save_files(files):
    for file in files.values():
        if default_storage.exists(file.name):
            default_storage.delete(file.name)
        file_name = default_storage.save(file.name, file)
        print("Saved uploaded file to: " + default_storage.url(file_name))