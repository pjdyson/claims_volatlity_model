# -*- coding: utf-8 -*-



import pandas as pd
import numpy as np
import scipy.stats as sps

import plotly.graph_objects as go

################################
# Custom functions


def generate_portfolio(policy_count, frequency, shape, scale, max_lim):
  # Calculate number of claims and the size of each claim for given frequency-severity parameters
  number_of_claims = np.random.poisson(frequency*policy_count)
  claim_store = pd.DataFrame({'claim_number':list(range(1, number_of_claims+1))})
  dist_full = sps.pareto.rvs(b=shape, loc=0, scale=scale, size=int(number_of_claims*2)+1)
  dist_limited = list(filter(lambda x: x < max_lim, dist_full))[:number_of_claims]
  claim_store['claim_value'] = dist_limited
  return claim_store.set_index('claim_number')

def generate_array_of_portfolios(policy_count, frequency, claims_shape, claims_scale, claims_max_lim, number_in_array):
    # For a given policy yesr exposure, run a set number of sample portfolios
    array_of_sample_sums = []
    for x in range(1, number_in_array+1, 1):
        claim_sample = generate_portfolio(policy_count, frequency, claims_shape, claims_scale, claims_max_lim)
        sample_claim_sum = np.sum(claim_sample['claim_value'])
        array_of_sample_sums.append(sample_claim_sum)
    return array_of_sample_sums


def run_sample_model(max_policy_count, no_samples,policy_frequency,
                  claims_shape, claims_scale, claims_max_lim):
  # Run the model for no_samples, for 20 different policy counts (up to maximum)
  sample_groups = int(max_policy_count/20)
  list_of_sample_sizes = list(range(sample_groups,max_policy_count+1, sample_groups))
  results = pd.DataFrame(columns=list_of_sample_sizes)
  for sample_size in list_of_sample_sizes:
      results[sample_size] = generate_array_of_portfolios(sample_size, policy_frequency, claims_shape, claims_scale, claims_max_lim, no_samples)
  #format the table for use
  #results_melt = results.melt(var_name='Policy Exposure', value_name='Claim Total')  
  #results_melt['Burn Cost'] = results_melt['Claim Total']/results_melt['Policy Exposure']  
  return results


def produce_charts(results_df):
    median = results_df.median()
    sum_data = {'Median':median,
                '10th':results_df.quantile(0.10)-median,
                '25th':results_df.quantile(0.25)-median,
                '75th':results_df.quantile(0.75)-median,
                '90th':results_df.quantile(0.90)-median}
    
    results_summary = pd.DataFrame(sum_data).reset_index().rename({'index':'Policy_Count'}, axis='columns')
    results_summary['10thBC'] = results_summary['10th']/results_summary['Policy_Count']
    results_summary['25thBC'] = results_summary['25th']/results_summary['Policy_Count']
    results_summary['75thBC'] = results_summary['75th']/results_summary['Policy_Count']
    results_summary['90thBC'] = results_summary['90th']/results_summary['Policy_Count']

    # Plot Results
    figure = go.Figure()
    figure.add_trace(
        go.Line(
            y=results_summary['10thBC'],
            x=results_summary['Policy_Count'],
            name='10th Percentile'
    ))
    
    figure.add_trace(
        go.Line(
            y=results_summary['25thBC'],
            x=results_summary['Policy_Count'],
            name='25th Percentile'
    ))
    figure.add_trace(
        go.Line(
            y=results_summary['75thBC'],
            x=results_summary['Policy_Count'],
            name='75th Percentile'
    ))
    figure.add_trace(
        go.Line(
            y=results_summary['90thBC'],
            x=results_summary['Policy_Count'],
            name='90th Percentile'
    ))
    
    min_bc = np.min(results_summary['10thBC'])
    max_bc = np.max(results_summary['90thBC'])
    figure.add_shape(dict(type="line",x0=15000,y0=min_bc,x1=15000,y1=max_bc,line=dict(color="Red",width=3)))
    figure.add_shape(dict(type="line",x0=35000,y0=min_bc,x1=35000,y1=max_bc,line=dict(color="RoyalBlue",width=3)))
    figure.add_shape(dict(type="line",x0=65000,y0=min_bc,x1=65000,y1=max_bc,line=dict(color="RoyalBlue",width=3)))

    figure.update_layout(
        title="Plot Title",
        xaxis_title="Policy Exposure (Years)",
        yaxis_title="Movement in Burn Cost",
        annotations=[
        dict(x=15000,y=max_bc, xref="x", yref="y", text="Class B", showarrow=False, ax=0, ay=50 ),
        dict(x=35000,y=max_bc, text="Class A", showarrow=False, ax=0, ay=50 ),
        dict(x=65000,y=max_bc, text="Class A (Max Exposure)", showarrow=False, ax=0, ay=50 )
        ]
        )
    
    return figure
