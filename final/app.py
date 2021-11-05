def find_top_confirmed(n = 15):
    import pandas as pd
    corona_df=pd.read_csv("owid-covid-latest.csv")
    by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'new_cases']]
    cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return cdf

cdf=find_top_confirmed()
pairs=[(country,confirmed) for country,confirmed in zip(cdf.index,cdf['Confirmed'])]


import folium
import pandas as pd
corona_df = pd.read_csv("owid-covid-latest.csv")
corona_df=corona_df[['Lat','Long_','Country_Region','last_updated_date','Confirmed', 'new_cases', 'Deaths', 'new_deaths' ,'new_tests','Tests', 'positive_rate','tests_per_case','total_vaccinations','people_vaccinated','people_fully_vaccinated','population','median_age','aged_65_older','gdp_per_capita','extreme_poverty']]
corona_df=corona_df.dropna()

m=folium.Map(location=[34.223334,-82.461707],
            tiles='Stamen toner',
            zoom_start=8)

def circle_maker(x):
    popup_text='<div> <b><h5>Country_Region:{}</h5></b> <b>Last Updated Date</b> : {} <br> <b>Confirmed cases:</b>{} <br> <b> New cases :</b> {} <br> <b> Deaths :</b> {} <br> <b>New Deaths : </b> {} <br> <b> Tests :</b> {} <br> <b>New Tests :</b> {} <br> <b> Positive Rate :</b> {} <br> <b> Tests Per Case :</b> {} <br> <b> Total Vaccinations :</b> {} <br> <b> People Vaccinated :</b> {} <br>  <b>People Fully Vaccinated :</b> {} <br> <b> Population :</b> {} <br> <b> Median Age :</b> {} <br>  <b>Aged 65 and older :</b> {} <br> <b> GDP Per Capita : </b> {} <br> <b> Extreme Poverty : </b> {} </div>'.format(x[2] , x[3] ,x[4],x[5],x[6],x[7],x[9],x[8],x[10],x[11],x[12],x[13],x[14],x[15],x[16],x[17],x[18],x[19])
    test = folium.Html(popup_text, script=True)
    popup = folium.Popup(test, max_width=300,min_width=300)
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[4]//20),
                 color="red",
                 popup=popup).add_to(m)
corona_df.apply(lambda x:circle_maker(x),axis=1)

html_map=m._repr_html_()
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)

if __name__=="__main__":
    app.run(debug=True)