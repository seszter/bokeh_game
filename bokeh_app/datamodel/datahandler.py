import pandas as pd
import geopandas
import numpy as np
import pandas_bokeh



class DataModel():
    def __init__(self, PATH_DATA):
        self.lucknum = 0
        self.byear = 1961
        self.country = 'Norway'
        world = geopandas.read_file(
            geopandas.datasets.get_path('naturalearth_lowres')
        )
        world.replace({'United States of America': 'United States',
                       'Russia': 'Russian Federation'}, inplace=True)
        self.world = world
        self.tab1Data = pd.read_csv(PATH_DATA/'bokeh_data.csv')
        df = pd.read_csv(PATH_DATA/'df_toplot.csv')
        df['year_corrected'] = np.where(df.indicator.isin(['born_male', 'expected_to_survive_age65', 'urban']),
                                        df['Year'], df['Year'] - 20)
        yaxismap = {'born_male': 8,
                    'expected_to_survive_age65': 6,
                    'emplyoed': 4,
                    'urban': 7,
                    'not_obese_adult': 2,
                    'not_alcoholic_adult': 0,
                    'user_internet_adult': 1,
                    'attended_secondary_school_adult': 3}
        df['yaxis'] = df['indicator'].map(yaxismap)
        self.tab2Data = df
        self.labelsmap = {
                        'Be a male': 8,
                         'Can expect to live for 65 years': 6,
                         'Have a job': 4,
                         'Live in an urban area': 7,
                         "Not being obese": 2,
                         "Don't have a drinking problem": 0,
                         'Have access to internet': 1,
                         "Attended secondary school": 3
                        }

    def return_luck(self):
        return self.lucknum

    def return_byear(self):
        return self.byear

    def return_country(self):
        return self.country

    def return_tab1Data(self):
        return self.tab1Data

    def return_tab2Data(self):
        return self.tab2Data

    def return_world(self):
        return self.world

    def change_luck(self):
        self.lucknum = np.random.randint(0,100)

    def return_labelsmap(self):
        return self.labelsmap

    def draw_country(self, byear):
        randrow = self.tab1Data[(self.tab1Data.Year == int(byear)) &
                                (self.tab1Data['indicator'] == 'Population, total')].sample(weights='val')
        allpop = self.tab1Data[(self.tab1Data.Year==int(byear)) &
                               (self.tab1Data['indicator'] == 'Population, total')]['val'].sum()
        cpop = randrow['val'].iloc[0]
        self.country = randrow['country'].iloc[0]
        return self.country, round(cpop*100/allpop,2)

    def change_byear(self, byear):
        self.byear = byear

    def return_country_data(self):
        temp = self.tab2Data[self.tab2Data.country == self.country].copy()
        temp['color'] = np.where(temp['val'] >= self.lucknum, '#ACCD33', '#FFC45F')
        data = {}
        for year in temp.year_corrected.tolist():
            df_year = temp[temp.year_corrected == year][['yaxis', 'val', 'valper2', 'color']]
            data[year] = df_year.to_dict('series')
        return data