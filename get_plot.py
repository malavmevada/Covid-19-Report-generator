import pandas as pd
import matplotlib.pyplot as plt
from datetime import date,timedelta
plt.style.use('seaborn')
yesterday = (date.today()-timedelta(days=1)).strftime("%B %d, %Y")

def create_final_df(name):
    df = pd.read_csv(f'./data/{name}.csv')
    name = df.copy()
    name = name.drop(['date','status','Total'],axis=1)
    name['dateymd']= pd.to_datetime(name['dateymd'])
    name = name.set_index('dateymd')
    final_df=name.groupby([(name.index.year),(name.index.month)]).sum()
    final_df['total'] = final_df.mean(axis=1)
    final_df.rename(index={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',7:'July',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'},inplace=True)
    final_df['months'] = final_df.index.map(lambda x :x[1])
    return final_df

def create_plot(name,color):
    final_df=create_final_df(name)
    fig = plt.figure(figsize=(8,5))
    plt.plot(final_df['months'],final_df['total'],color=color)   
    plt.xlabel('Months')
    plt.ylabel(f'Covid  {name}  Counts')
    if name == 'deceased':
        plt.title(f'Covid-19 Deaths in India till {yesterday}')
        plt.legend(['Deaths'])
    else:
        plt.title(f'Covid-19 {name} cases in india till {yesterday}')
        plt.legend([f'{name}'])
    fig.savefig(f"./image/{name}_plot.png",dpi=100)
    # plt.show()

