# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

#actual data to compare to
def summarise_model_results_capped(results, policy_count):
  # Actual results to compare against
  #-------------------------------------
  actual_all = 1056+6704+1052+345+101
  actual_1k  = 6704+1052+345+101
  actual_10k = 1052+345+101
  actual_20k = 345+101
  actual_50k = 101

  fit_actual = {
#      'Actual_Burn': [33.8, 15.4, 11.0, 9.5, np.nan],
      'Actual_Count' : [actual_1k,
                  actual_10k,
                  actual_20k,
                  actual_50k],
      'Threshold': [1000,10000,20000,50000],
  }
  pd_summary = pd.DataFrame.from_dict(fit_actual)
  pd_summary = pd_summary.set_index('Threshold')

  # Process model results
  #-------------------------------------

  pd_summary['Fitted_Count'] = [np.count_nonzero(results.loc[results['claim_value']>=1000])/policy_count*1e6,
                  np.count_nonzero(results.loc[results['claim_value']>=10000])/policy_count*1e6,
                  np.count_nonzero(results.loc[results['claim_value']>=20000])/policy_count*1e6,
                  np.count_nonzero(results.loc[results['claim_value']>=50000])/policy_count*1e6]

  pd_summary['Fitted_Severity'] = [
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=1000) & (results['claim_value']<10000)]),
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=10000) & (results['claim_value']<20000)]),
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=20000) & (results['claim_value']<50000)]),
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=50000)])]
  

  pd_summary['Fitted_Burn'] = pd_summary['Fitted_Count']*pd_summary['Fitted_Severity']/1e6
  #
  # get figure of results
  #
  
  figure = build_figure(pd_summary)
  
  return pd_summary, figure


#actual data to compare to
def summarise_model_results_excess(results,policy_count):
  # Actual results to compare against
  #-------------------------------------
  actual_100k = 34+12+5.4+3.5+2.3+2.0
  actual_250k = 12+5.4+3.5+2.3+2.0
  actual_500k = 5.4+3.5+2.3+2.0
  actual_1m = 3.5+2.3+2.0
  actual_2m = 2.3+2.0
  actual_5m = 2.0

  fit_actual = {
#      'Actual_Burn': [8.7, 7.2, 6.1, 8.6, 10.7, 33.2],
      'Actual_Count' : [actual_100k,
                  actual_250k,
                  actual_500k,
                  actual_1m,
                  actual_2m,
                  actual_5m],
      'Threshold': [100e3,250e3,500e3,1e6,2e6,5e6],
  }
  pd_summary = pd.DataFrame.from_dict(fit_actual)
  pd_summary = pd_summary.set_index('Threshold')

  # Process model results
  #-------------------------------------
  
  pd_summary['Fitted_Count'] = [np.count_nonzero(results.loc[results['claim_value']>=100e3])/policy_count*1e6,
                  np.count_nonzero(results.loc[results['claim_value']>=250e3])/policy_count*1e6,
                  np.count_nonzero(results.loc[results['claim_value']>=500e3])/policy_count*1e6,
                  np.count_nonzero(results.loc[results['claim_value']>=1e6])/policy_count*1e6,
                  np.count_nonzero(results.loc[results['claim_value']>=2e6])/policy_count*1e6,
                  np.count_nonzero(results.loc[results['claim_value']>=5e6])/policy_count*1e6]

  pd_summary['Fitted_Severity'] = [
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=100e3) & (results['claim_value']<250e3)]),
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=250e3) & (results['claim_value']<500e3)]),
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=500e3) & (results['claim_value']<1e6)]),
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=1e6) & (results['claim_value']<2e6)]),
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=2e6) & (results['claim_value']<5e6)]),
                                  np.mean(results['claim_value'].loc[(results['claim_value']>=5e6)])]

  pd_summary['Fitted_Burn'] = pd_summary['Fitted_Count']*pd_summary['Fitted_Severity']/1e6
  
  
  #
  # get figure of results
  #
  
  figure = build_figure(pd_summary)
  
  return pd_summary, figure

def build_figure(summary):
    
    fig_validation = go.Figure()
    fig_validation.add_trace(
        go.Line(
            y=summary['Actual_Count'],
            x=summary.index,
            name='Actual Claim Count'
    ))
    fig_validation.add_trace(
        go.Line(
            y=summary['Fitted_Count'],
            x=summary.index,
            name='Fitted Claim Count'
    ))
    
    fig_validation.update_layout(
        title="Severity Distribution",
        xaxis_title="Claim Threshold",
        yaxis_title="Number of Claims in Sample")

    return (fig_validation)