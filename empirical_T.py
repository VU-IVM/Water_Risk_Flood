def empirical_T(data, plot_fig):
#We calculate the empirical return period

	p = data.sort(reverse=True)
	r = data.len()
	r(p) = r
	data[:,2] = pd.DataFrame.transpose(r)
	data[:,3] = data[:,2]/(pd.DataFrame.shape(data,1)+1)
	data[:,4] = 1/data[:,3]

	if plot_fig == 1:
	
		df.plot(title='Empirical return periods', data[:,4], data[:,1], x='Return Periods (yrs)', y='Rainfall Intnsity (mm/hr)')
    
		df.plot(title='Empirical return periods 2', data[:,4], data[:,1], logx=True, x='Return Periods (yrs)', y='Rainfall Intensity (mm/hr)')
		return
	return