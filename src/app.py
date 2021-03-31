import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from time import sleep

# Function definition for data load
@st.cache
def data_load(path):
  data = pd.read_csv(path)
  sleep(3)
  return data

# Function definition to create the comparison charts
def comparison_chart(data, causa_mortis, estado='Brasil'):
  # Data processing to prepare the chart figure
  if estado == 'Brasil':
      deaths_by_type_2019 = data[0].groupby('tipo_doenca')['total'].sum()
      deaths_by_type_2020 = data[1].groupby('tipo_doenca')['total'].sum()
      deaths_by_type_2021 = data[2].groupby('tipo_doenca')['total'].sum()
      if(causa_mortis == 'COVID'):
          selection_2019 = 0
      else:
          selection_2019 = int(deaths_by_type_2019.loc[causa_mortis])

      selection_2020 = int(deaths_by_type_2020.loc[causa_mortis])
      selection_2021 = int(deaths_by_type_2021.loc[causa_mortis])
  else:
      deaths_by_type_2019 = data[0].groupby(['uf', 'tipo_doenca'])['total'].sum()
      deaths_by_type_2020 = data[1].groupby(['uf', 'tipo_doenca'])['total'].sum()
      deaths_by_type_2021 = data[2].groupby(['uf', 'tipo_doenca'])['total'].sum()

      if(causa_mortis == 'COVID'):
          selection_2019 = 0
      else:
          selection_2019 = int(deaths_by_type_2019.loc[estado, causa_mortis])

      selection_2020 = int(deaths_by_type_2020.loc[estado, causa_mortis])
      selection_2021 = int(deaths_by_type_2021.loc[estado, causa_mortis])

  selection_by_causa_mortis = [selection_2019, selection_2020, selection_2021]
  
  death_df = pd.DataFrame({'Total': selection_by_causa_mortis,
      'Year': [2019, 2020, 2021]})

  # Preparing the chart figure
  chart_figure, ax = plt.subplots()
  ax = sns.barplot(x='Year', y='Total', data=death_df)
  ax.set_title(f'Deaths due to {causa_mortis} in {estado}')
  # ax.set_size(8,6)
  
  return chart_figure

# Function definition: main function 
def main():

  # Reading data from the csv files
  data_2019 = data_load('data/obitos-2019.csv')
  data_2020 = data_load('data/obitos-2020.csv')
  data_2021 = data_load('data/obitos-2021.csv')
  all_data = [data_2019, data_2020, data_2021]
  data_to_show = { '2019': 0, '2020': 1, '2021': 2}

  # Creates the list of values for user selection
  causa_mortis_list = data_2021['tipo_doenca'].unique()
  state_list = np.append(data_2021['uf'].unique(), 'Brasil')

  # Receive user input for causa mortis and state
  causa_mortis = st.sidebar.selectbox('Select the causa mortis', causa_mortis_list)
  selected_state = st.sidebar.selectbox('Select the state', state_list)

  # Call function to prepare data to display
  deaths_by_type_figure = comparison_chart(all_data, causa_mortis, selected_state)

  # Inserting visual elements on the screen
  st.title('COVID-19 analysis')
  st.markdown('Number of deaths in Brazil or in a brazilian state per year')

  # Display chart
  st.pyplot(deaths_by_type_figure)

  # Displaying the data on the screen
  show_data = st.sidebar.selectbox('Show source data', [False, True])
  if(show_data):
    selected_year = st.sidebar.selectbox('Select data period', ['2019', '2020', '2021'])
    st.dataframe(all_data[data_to_show[selected_year]])
    st.text('Add source data here')

if __name__ == "__main__":
  main()