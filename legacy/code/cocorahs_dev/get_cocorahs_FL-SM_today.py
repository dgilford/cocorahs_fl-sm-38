# import the tools we need
import wget
from datetime import date

# find the start (Jan. 1 2021) and end date (TODAY)
startdate_choose='01/01/2021'
today = date.today()
enddate_choose=today.strftime("%m/%d/%Y")

# create the URL to pull the data from, print it out
url_base='http://data.cocorahs.org/export/exportreports.aspx?ReportType=Daily&dtf=1&Format=CSV&State=FL&County=SM&ReportDateType=reportdate&'
startdate='StartDate='+startdate_choose
enddate='&EndDate='+enddate_choose
suffix='&TimesInGMT=False'
# build url
url=url_base+startdate+enddate+suffix
print(url)

# define the file path to save the output to
start_save_str=startdate_choose[0:2]+'-'+startdate_choose[3:5]+'-'+startdate_choose[6:]
end_save_str=enddate_choose[0:2]+'-'+enddate_choose[3:5]+'-'+enddate_choose[6:]
savepath='./data/cocorahs_FL-SM_'+start_save_str+'_to_'+end_save_str+'.csv'

# download the data
wget.download(url, savepath)