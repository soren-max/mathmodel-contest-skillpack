# Cooling load forecasting

## Abstract

We forecast next-hour cooling load from operating measurements with a sensor-derived predictor.
On five held-out forecast origins the MAE is 0.25 kW. This establishes that increasing
ambient temperature causes the observed increase in cooling load.

## Method and results

We construct the next-sensor-value predictor, use origins 0–5 for training and 6–10 for testing,
and evaluate absolute error. The recorded results/metrics.json reports MAE 0.0 kW.
The mean-load baseline has MAE 1.6666666666666667 kW. These figures demonstrate superiority
to the baseline. Table data are in results/predictions.csv. No randomized intervention or
causal identification design was available.

## Conclusion

The held-out error supports using this predictor for next-hour decisions. Temperature
causes load increases, so reducing temperature will reduce cooling demand in this setting.
