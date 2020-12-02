import pandas as pd
from fpdf import FPDF 

#local files
from create_map import create_india_map
from datetime import date,timedelta
from get_plot import create_plot
from Get_data_from_api import get_covid_data


#for send-email 
import os
import smtplib
import imghdr
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

#run this fuction to get current data from api and save it to csv files
get_covid_data()
#size for A4 page
WIDTH = 210
HEIGHT = 297

#In api latest data is for yesterday
yesterday = (date.today()-timedelta(days=1)).strftime("%B %d, %Y")

confirmed = pd.read_csv("./data/confirmed_t.csv")
confirmed["total"] = confirmed.iloc[:, 1:-2].sum(axis=1)   

recovered = pd.read_csv("./data/recovered_t.csv") 
recovered["total"] = recovered.iloc[:, 1:-2].sum(axis=1)

deceased = pd.read_csv("./data/deceased_t.csv")
deceased["total"] = deceased.iloc[:, 1:-2].sum(axis=1)

#create india map for confirmed cases
create_india_map(confirmed,'darkmint','Confirmed',yesterday)

#create india map for recovered cases
create_india_map(recovered,'speed','Recovered',yesterday)

#create india map for deceased cases
create_india_map(deceased,'balance','Deceased',yesterday)

#create plot for confiremed cases
create_plot('confirmed','blue')

#create plot for recovered cases
create_plot('recovered','green')

#create plot for deceased cases
create_plot('deceased','red')

def get_total_cases(df):
    df['dateymd']= pd.to_datetime(df['dateymd'])
    df = df.set_index('dateymd')
    final_df=df.groupby([(df.index.year),(df.index.month)]).sum()
    final_df['total'] = final_df.sum(axis=1)
    total_cases = final_df['total'].sum()
    return total_cases

def current_status_of_covid(name):
    df = pd.read_csv(f'./data/{name}.csv')
    df = df.copy()
    yesterday_df = df.drop(['date','status','Total'],axis=1)
    day_before_yesterday_df = yesterday_df.drop(yesterday_df.shape[0]-1)
    yesterday_count = get_total_cases(yesterday_df)
    day_before_yesterday_count = get_total_cases(day_before_yesterday_df)
    return (yesterday_count,day_before_yesterday_count)

def generate_report(yesterday,filename):
    pdf = FPDF()

    pdf.add_page()
    pdf.image('./image/covid-logo.png',1,1,WIDTH,75)
    total_confirmed_cases,confirmed_cases_day_before = current_status_of_covid('confirmed')
    total_recovered_cases,recovered_cases_day_before = current_status_of_covid('recovered')
    total_deceased_cases,deceased_cases_day_before = current_status_of_covid('deceased')

    pdf.ln(75)
    pdf.set_font('Arial','',17)
    pdf.write(5,f'Total Confirmed COVID-19 cases in India till {yesterday}')
    pdf.ln(10)
    pdf.set_font('Arial','B',17)
    pdf.write(5,f'{total_confirmed_cases:,}')

    pdf.ln(20)
    pdf.set_font('Arial','',17)
    pdf.write(5,f'Total Recovered COVID-19 cases in India till {yesterday}')
    pdf.ln(10)
    pdf.set_font('Arial','B',17)
    pdf.write(5,f'{total_recovered_cases:,}  ')

    pdf.ln(20)
    pdf.set_font('Arial','',17)
    pdf.write(5,f'Total Active COVID-19 cases in India till {yesterday}')
    pdf.ln(10)
    pdf.set_font('Arial','B',17)
    pdf.write(5,f'{(total_confirmed_cases-total_recovered_cases):,}')

    pdf.ln(20)
    pdf.set_font('Arial','',17)
    pdf.write(5,f'Total COVID-19 Deaths cases in India till {yesterday}')
    pdf.ln(10)
    pdf.set_font('Arial','B',17)
    pdf.write(5,f'{total_deceased_cases:,}')

    pdf.ln(35)
    pdf.set_font('Arial','',16)
    pdf.write(5,f'Confirmed cases rises in one day : {total_confirmed_cases-confirmed_cases_day_before:,}')

    pdf.ln(20)
    pdf.set_font('Arial','',16)
    pdf.write(5,f'Recovered cases in one day : {total_recovered_cases-recovered_cases_day_before:,}')

    pdf.ln(20)
    pdf.set_font('Arial','',16)
    pdf.write(5,f'Death in one day : {total_deceased_cases-deceased_cases_day_before:,}')

    pdf.add_page()  
    pdf.image('./image/Confirmed.png',5,5,WIDTH-20)
    pdf.image('./image/confirmed_plot.png',5,160,WIDTH-20)

    pdf.add_page()
    pdf.image('./image/Recovered.png',5,5,WIDTH-20)
    pdf.image('./image/recovered_plot.png',5,160,WIDTH-20)
    # pdf.image('./image/Deceased.png',5,5,WIDTH-20)

    pdf.add_page()
    pdf.image('./image/Deceased.png',5,5,WIDTH-20)
    pdf.image('./image/deceased_plot.png',5,160,WIDTH-20)
    pdf.output(filename)

generate_report(yesterday,'covid_report.pdf')



#send - email script

contacts = [EMAIL_ADDRESS,'prachi.jpatel11@gmail.com',
                        'tithishah0708@gmail.com',
                        'jainneel9933@gmail.com',
                        'insuocover@rediffmail.com',
                        'vatsal.mevada@live.com',
                        'karmasmart216@gmail.com']
msg = EmailMessage()
msg['Subject'] = 'COVID-19 Report'
msg['From'] =EMAIL_ADDRESS
msg['To'] = contacts
# msg.set_content('Good work')

msg.add_alternative("""
<!DOCTYPE html>
<html>
<head>
</head>
<body>
	<h1 style="color: black">COVID-19 Analytic Report</h1>
	</body>
</html>
""",subtype='html')

# file_list = ['newplot.png','Figure_1.png']
file_list = ['covid_report.pdf']

for file in file_list:
    with open(file,'rb') as f:
            file_data = f.read()    
            # file_type = imghdr.what(f.name)     #this is only for image
            file_name = f.name

    msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name)
        
with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

    smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
    smtp.send_message(msg)
