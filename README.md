# claims_volatlity_model

- This is a frequency-severity model for individual claims, to test/demonstrate the impact of policy volume on ultimate claim volatility
- The main file 'analysis.py' shows how the model can be calibrated for motor-bodily-injury claims from the IFoA thrid-party working party paper [IFOA TPWP](https://www.actuaries.org.uk/practice-areas/general-insurance/research-working-parties/third-party)
- 'Model_validation.py' contains the functions which are used to test the fit of the severity distribution
- 'Model_volatility.py' contains the model functions
  - __generate portfolio:__  creates a single ultimate from x policies by generating a random number of claims (poisson) and the severity (pareto, truncated) of claims from the given parameters.
  - __generate array of portfolios:__ runs 'generate portfolio' y number of times against the same number of policies to get the volatility at a particular policy volume
  - __run sample model:__ Run 'generate array of portfolios' for 20 buckets between zero and 'max policy count' to show how the volatility changes at different policy volumes.
  - produce charts: plots the output from 'run sample model' using plotly
  
If you have any questions or indded suggestions, please feel free to drop me a message here [Peter Dyson](https://www.linkedin.com/in/pjdyson/)
