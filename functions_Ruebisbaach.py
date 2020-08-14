import matplotlib.pyplot as plt
import scipy.stats as sp
import numpy as np
import pandas as pd

def height_to_intensity(data,duration):
    intensity_mmhr = data/duration
    return intensity_mmhr


def Gumbelfit_EM(data, return_periods, plot_fig):
    '''
     Fitting Gumbel using the Method of Moments estimates - make this a function?
     Obtaining Fiting Parameters (Mean, Standard Deviation (S),
     Shape Parameter (Alpha), and Scale Parameter (u).
     See also De Paola et al. (2014). Intensity-Duration-Frequency (IDF) rainfall curves, for data series and climate projection in African cities 
     
     input:
         data - selected columns of a pandas dataframe
         return_periods - selected return periods in years
         plot_fig - set to 1 to activate figure plotting
     output:
         parameters - parameters of the Gumbel distribution
         values - a DataFrame with x and corresponding Exceedance Probability
         x_T - Rainfall Intensity estimates at the corresponding return period
    '''
#data = intensity_mmhr.loc[:,dur]

    m = len(data)
    Mean = data.mean(axis = 0)
    Std    = data.std(axis = 0)
    u = 1.282/Std
    v = Mean-0.45*Std
    
    x = np.arange(0, data.max() * 1.5, 0.1) #, 0:0.1:max(data)*1.5
    p_cum = np.exp(-np.exp(-u*(x-v)))
    p_inv_cum = 1 - p_cum
    
    x_T = (-1/u)*np.log(-np.log(1-(1./np.array(return_periods)))) + v

    parameters = dict()
    parameters['location'] = u
    parameters['scale'] = v
    
    values = pd.DataFrame(index=x, columns=['Exceedance_prob'], data = p_inv_cum)
    values.index.name = 'x'
    
    if plot_fig == 1:
        plt.figure()
        plt.title('CDF and ICDF Data')
        plt.plot(x, p_cum, '-.k', label = 'CDF')
        plt.plot(x, p_inv_cum, '-.r', label = 'ICDF')      
        
        plt.legend()
        plt.xlabel('Rainfall (mm/hr)')
        plt.ylabel('Probability')
        
        plt.plot(x_T, np.exp(-np.exp(-u*(x_T-v))), '*k')
        plt.plot(x_T, 1-np.exp(-np.exp(-u*(x_T-v))), '*r')
        plt.ylim(0,1)
        plt.show()
        
        
        plt.figure()
        plt.title('Return Period - semilog')
        plt.semilogx(1./p_inv_cum, x, '-.r')
        plt.semilogx(return_periods, x_T, '*r')
        plt.grid()
        plt.ylabel('Rainfall Intensity (mm/hr)')
        plt.xlabel('Return Period (yrs)')

    return parameters, values , x_T

def Gumbel_evfit(data, return_periods, plot_fig):
    '''
     Fitting Gumbel parameters using maximum likelihood estimators from
     scipy package: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gumbel_r.html
    
     input:
         data - selected columns of a pandas dataframe
         return_periods - selected return periods in years
         plot_fig - set to 1 to activate figure plotting
     output:
         parameters - parameters of the Gumbel distribution
         values - a DataFrame with x and corresponding Exceedance Probability
         x_T - Rainfall Intensity estimates at the corresponding return period
    '''
    parameters = dict()

    loc, scale = sp.gumbel_r.fit(data.values)
    parameters['location'] = loc
    parameters['scale'] = scale
    
    x = np.arange(0, data.max() * 1.5, 0.1) #, 0:0.1:max(data)*1.5
    p_cum = sp.gumbel_r.cdf(x, loc = loc, scale = scale)
    p_inv_cum = sp.gumbel_r.sf(x, loc = loc, scale = scale)
    
    values = pd.DataFrame(index=x, columns=['Exceedance_prob'], data = p_inv_cum)
    values.index.name = 'x' 
    
    x_T = sp.gumbel_r.isf(1/np.array(return_periods), loc = loc, scale = scale)
    
    if plot_fig == 1:
        plt.figure()
        plt.title('CDF and ICDF Data')
        plt.plot(x, p_cum, '-.k', label = 'CDF')
        plt.plot(x, p_inv_cum, '-.r', label = 'ICDF')      
        
        plt.legend()
        plt.xlabel('Rainfall (mm/hr)')
        plt.ylabel('Probability')
        
        plt.plot(x_T, sp.gumbel_r.cdf(x_T, loc = loc, scale = scale), '*k')
        plt.plot(x_T, sp.gumbel_r.sf(x_T, loc = loc, scale = scale), '*r')
        plt.ylim(0,1)
        plt.show()        
        
        plt.figure()
        plt.title('Return Period - semilog')
        plt.semilogx(1./p_inv_cum, x, '-.r')
        plt.semilogx(return_periods, x_T, '*r')
        plt.grid()
        plt.ylabel('Rainfall Intensity (mm/hr)')
        plt.xlabel('Return Period (yrs)')   
    
    return parameters, values , x_T

def empirical_T(data, plot_fig):
    '''
    We calculate the empirical return period
    input:
         data - selected columns of a pandas dataframe
         plot_fig - set to 1 to activate figure plotting
     output:
         data - a DataFrame with the calculate empirical return periods
    '''
    
    emp_T = pd.DataFrame(data = data)
    emp_T.sort_values(by=emp_T.columns[0], ascending = False, inplace = True)
    emp_T.loc[:,'rank'] = emp_T.iloc[:,0].rank(ascending = False)
    emp_T.loc[:,'exc_prob'] = emp_T.loc[:,'rank'] / (len(emp_T) + 1 )
    emp_T.loc[:,'return period (yrs)'] = 1/emp_T.loc[:,'exc_prob']

    if plot_fig == 1:    
        # plt.figure()
        # plt.title('Empirical return periods')
        # plt.plot(emp_T.loc[:,'return period (yrs)'], emp_T.iloc[:,0], 'ok')
        # plt.xlabel('Return Periods (yrs)')
        # plt.ylabel('Rainfall Intensity (mm/hr)')
        
        plt.figure()
        plt.title('Empirical return periods')
        plt.semilogx(emp_T.loc[:,'return period (yrs)'], emp_T.iloc[:,0], 'ok')
        plt.xlabel('Return Periods (yrs)')
        plt.ylabel('Rainfall Intensity (mm/hr)')

    return emp_T
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    