from datasets import load_dataset
import pandas as pd

### Measurements by cell ###
measurements_by_cell = load_dataset('CelfAI/COOPER','measurements_by_cell')

measurements_by_cell_data_train = measurements_by_cell['train'].to_pandas()
measurements_by_cell_data_test = measurements_by_cell['test'].to_pandas()
measurements_by_cell_data = pd.concat([measurements_by_cell_data_train, measurements_by_cell_data_test])

### Topology ###
topology = load_dataset('CelfAI/COOPER','topology')
topology_data = topology['main'].to_pandas()



### Performance indicators meanings ###
performance_indicators_meanings = load_dataset('CelfAI/COOPER','performance_indicators_meanings')
performance_indicators_meanings_data = performance_indicators_meanings['main'].to_pandas()

#### Optionally Join Measurements by cell and Topology ###
all_data = pd.merge(measurements_by_cell_data, topology_data, on='LocalCellName', how='left')
pm_columns=[x for x in measurements_by_cell_data.columns.tolist() if x not in ['LocalCellName', 'datetime']]

mean_by_cell= measurements_by_cell_data.groupby('LocalCellName')[pm_columns].mean().reset_index()
min_by_cell= measurements_by_cell_data.groupby('LocalCellName')[pm_columns].min().reset_index()

mean_by_band= all_data.groupby('Band')[pm_columns].mean().reset_index()
mean_by_site= all_data.groupby('SiteLabel')[pm_columns].mean().reset_index()
    

