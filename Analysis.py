
import pandas as pd
import numpy as np
import scipy.stats as sps

import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

import model_volatility
import model_validation

#%%
################################
# Calibration
claim_capped_frequency = 9258/1e6
claim_capped_shape =  0.8  # alpha
claim_capped_scale =  1000.0      # beta
claim_capped_max_lim = 100000     # maximum

################################
# Calibration

claim_excess_frequency = 59/1e6
claim_excess_shape =  0.8       # alpha
claim_excess_scale =  100000.0  # beta
claim_excess_max_lim = 30000000 # maximum


#%% Validation

#run a single portfolio
policy_count_validation = 2e6
single_capped_result = model_volatility.generate_portfolio(policy_count_validation, claim_capped_frequency, claim_capped_shape, claim_capped_scale, claim_capped_max_lim)
single_excess_result = model_volatility.generate_portfolio(policy_count_validation, claim_excess_frequency, claim_excess_shape, claim_excess_scale, claim_excess_max_lim)

summary_capped, fig_capped = model_validation.summarise_model_results_capped(single_capped_result, policy_count_validation)
summary_excess, fig_excess = model_validation.summarise_model_results_excess(single_excess_result, policy_count_validation)


plot(fig_capped,filename="validation_capped.html")
plot(fig_excess,filename="validation_excess.html")


#%% Run a single policy count models

policy_counts_to_run = [15000,35000,65000]
#policy_counts_to_run = [35000]
sample_portfolios = 10000

pct_list = [10,25,50,75,90]
results_capped = pd.DataFrame({'Percentile':pct_list})
results_excess = pd.DataFrame({'Percentile':pct_list})
results_capped['Loss_layer'] = 'Capped'
results_excess['Loss_layer'] = 'Excess'

for policycount in policy_counts_to_run:
    print('Running: ' + '{:,.0f}'.format(policycount), 'Capped')
    point_model_capped = model_volatility.generate_array_of_portfolios(policy_count=policycount, 
                                                  frequency=claim_capped_frequency, 
                                                  claims_shape=claim_capped_shape, 
                                                  claims_scale=claim_capped_scale, 
                                                  claims_max_lim=claim_capped_max_lim, 
                                                  number_in_array=sample_portfolios,
                                                  )

    print('Running: ' + '{:,.0f}'.format(policycount), 'Excess')
    point_model_excess = model_volatility.generate_array_of_portfolios(policy_count=policycount, 
                                                  frequency=claim_excess_frequency, 
                                                  claims_shape=claim_excess_shape, 
                                                  claims_scale=claim_excess_scale, 
                                                  claims_max_lim=claim_excess_max_lim, 
                                                  number_in_array=sample_portfolios,
                                                  )

    results_capped[policycount] = results_capped['Percentile'].apply(lambda x: np.percentile(point_model_capped, x)-np.percentile(point_model_capped, 50))
    results_excess[policycount] = results_excess['Percentile'].apply(lambda x: np.percentile(point_model_excess, x)-np.percentile(point_model_excess, 50))



#%%

results = pd.concat([results_capped, results_excess])
results_melt = results.melt(id_vars=['Percentile','Loss_layer'], var_name='Policy Count', value_name='Value')

results_melt.to_csv('output_all.csv')


#%%
#
#Full model
#
#%% Run the model

max_policy_count = 150000
no_samples = 5000

results_capped = model_volatility.run_sample_model(
     max_policy_count = int(max_policy_count),
     no_samples = no_samples,
     policy_frequency = claim_capped_frequency,
     claims_shape = claim_capped_shape,
     claims_scale = claim_capped_scale,
     claims_max_lim = claim_capped_max_lim)

results_excess = model_volatility.run_sample_model(
     max_policy_count = int(max_policy_count),
     no_samples = no_samples,
     policy_frequency = claim_excess_frequency,
     claims_shape = claim_excess_shape,
     claims_scale = claim_excess_scale,
     claims_max_lim = claim_excess_max_lim)

#%% Summarise Results


figure_capped = model_volatility.produce_charts(results_capped)
plot(figure_capped, filename='fullmodel_capped.html')


figure_excess = model_volatility.produce_charts(results_excess)
plot(figure_excess, filename='fullmodel_excess.html')




