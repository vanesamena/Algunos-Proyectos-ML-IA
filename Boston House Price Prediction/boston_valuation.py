from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np


# Gather data

boston_dataset = load_boston()
data=pd.DataFrame(data=boston_dataset.data, columns=boston_dataset.feature_names)

features=data.drop(['INDUS','AGE'],axis=1)

# Transform to log values
log_prices=np.log(boston_dataset.target)
target=pd.DataFrame(log_prices,columns=['PRICE'])

# Defining variables
ZILLOW_MEDIAN_PRICE = 739.18  # Price to April 2022 - Check in https://www.zillow.com/boston-ma/home-values/
SCALE_FACTOR=ZILLOW_MEDIAN_PRICE/np.median(boston_dataset.target)

CRIM_IDX=0
ZN_IDX=1
CHAS_IDX=2
RM_IDX=4
PTRATIO_IDX=8

property_stats=features.mean().values.reshape(1,11)

regr=LinearRegression().fit(features,target) # all thetas
fitted_vals=regr.predict(features) # all us predictions

#Calculate MSE and RMSE

MSE = mean_squared_error(target,fitted_vals)
RMSE = np.sqrt(MSE)
#the unit are log dollar prices in 000s

def get_log_estimate(nr_rooms,
                    students_per_classroom,
                    next_to_river=False,
                    high_confidence=True):
    
    #Configure property
    property_stats[0][RM_IDX]=nr_rooms
    property_stats[0][PTRATIO_IDX]=students_per_classroom
    
    if next_to_river:
         property_stats[0][CHAS_IDX]=1
    else:
         property_stats[0][CHAS_IDX]=0
    
    #make prediction
    log_estimate = regr.predict(property_stats)[0][0]
    
    #Calc Range
    if high_confidence: #we calculate the 95%
        upper_bound = log_estimate + 2*RMSE
        lower_bound = log_estimate - 2*RMSE
        interval = 95
    else:    #we calculate 68% oly 1 standart desviation or one sigma
        upper_bound = log_estimate + RMSE
        lower_bound = log_estimate - RMSE
        interval = 68
        
    return log_estimate, upper_bound, lower_bound, interval



def get_dollar_estimate(rm, ptratio,chas=False,large_range=True):
    """Estimate the price of a property in Boston.
    
    Keyword arguments:
    rm -- number of rooms in the property
    ptratio -- number of students per teacher in the classroom for the school in the area
    chas -- True if the property is next to the river, False otherwise
    large_range -- True for 95% prediction interval, False for 68% interval
    """
    
    
    if rm<1 or ptratio<1 or ptratio>50:
        return 'That is unrealistic. Try again'
    
    
    
    log_est,upper,lower,conf = get_log_estimate(nr_rooms=rm,
                                                students_per_classroom=ptratio, 
                                                next_to_river=chas,
                                                high_confidence=large_range )

    # Converto to today's dollars 
    dollar_est=np.e**log_est*1000*SCALE_FACTOR
    upper_bound_prices=np.e**upper*1000*SCALE_FACTOR
    lower_bound_prices=np.e**lower*1000*SCALE_FACTOR

    # Round the dollar values to nearest thousand

    round_est=np.around(dollar_est,-3)
    round_upper=np.around(upper_bound_prices,-3)
    round_lower=np.around(lower_bound_prices,-3)

    print(f'The estimated property value is: {round_est}')
    print(f'At {conf}% confidence the valuation range is:')
    print(f'USD {round_lower} at the lower end to USD {round_upper} at the high end.')



