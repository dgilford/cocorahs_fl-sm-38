# CoCoRaHS nearby stations

This morning I played around with updating my CoCoRaHS code to calculate my station's distance to nearby stations, and plotting how many observations those stations have:
![[./_resources/CoCoRaHS_nearby_stations,_Fingerprints_Code.resources/image.png]]
Next I want to look at the correlations between these stations, but I don't know the best way to do this.  I need to isolate the same days of data for each (being aware that it is possible there could be more than one obs. per day at a given station!), then correlate their timeseries somehow. But how? Rain is such a sparse variable in time. Eventually I want to map these correlations and also show how correlated these are based on distance.

Maybe one way is to add white noise to the observations which are zero and compute R then? Also can plot a scatter of the non-zero observations to just get a visual idea and whether any biases or patterns emerge.
