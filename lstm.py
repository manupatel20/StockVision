# -*- coding: utf-8 -*-
"""lstm

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BN0WhV4qAzEwDNWKVnNjeABPkCuHA06v
"""

# https://www.kaggle.com/code/thebrownviking20/intro-to-recurrent-neural-networks-lstm-gru/notebook

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional
from keras.optimizers import SGD
import math
from sklearn.metrics import mean_squared_error

# Some functions to help out with
def plot_predictions(test,predicted):
    plt.plot(test, color='red',label='Real Apple Stock Price')
    plt.plot(predicted, color='blue',label='Predicted Apple Stock Price')
    plt.title('Apple Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Apple Stock Price')
    plt.legend()
    plt.show()

def return_rmse(test,predicted):
    rmse = math.sqrt(mean_squared_error(test, predicted))
    print("The root mean squared error is {}.".format(rmse))

# from google.colab import drive
# drive.mount('/content/drive')
# dataset = pd.read_csv('/content/drive/MyDrive/CE Sem 6/SDP/Project_Sample_2/IBM_2006-01-01_to_2018-01-01.csv', index_col='Date', parse_dates=['Date'])
dataset = pd.read_csv('./AAPL.csv', index_col='Date', parse_dates=['Date'])
# dataset = pd.merge(dataset1, dataset2)
print(dataset.head())
print(dataset.info())

# Checking for missing values
training_set = dataset[:'2021'].iloc[:,1:2].values
test_set = dataset['2022':].iloc[:,1:2].values

# We have chosen 'High' attribute for prices. Let's see what it looks like
dataset["High"][:'2021'].plot(figsize=(16,4),legend=True)
dataset["High"]['2022':].plot(figsize=(16,4),legend=True)
plt.legend(['Training set (Before 2022)','Test set (2022 and beyond)'])
plt.title('Apple stock price')
plt.show()

# Scaling the training set
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)
test_set_scaled = sc.fit_transform(test_set)

# print(training_set)
# print(test_set)

# Since LSTMs store long term memory state, we create a data structure with 60 timesteps and 1 output
# So for each element of training set, we have 60 previous training set elements 
X_train = []
y_train = []
# for i in range(60,200):
#   X_train.append(training_set_scaled[i-60:i,0])
#   y_train.append(training_set_scaled[i,0])
y_train = training_set_scaled[:,0]
X_train, y_train = np.array(training_set_scaled), np.array(y_train)

# Reshaping X_train for efficient modelling
X_train = np.reshape(X_train, (X_train.shape[0],X_train.shape[1],1))

# The LSTM architecture
regressor = Sequential()

# First LSTM layer with Dropout regularisation
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1],1)))
regressor.add(Dropout(0.2))

# Second LSTM layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# Third LSTM layer
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))

# Fourth LSTM layer
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))

# The output layer
regressor.add(Dense(units=1))

# Compiling the RNN
regressor.compile(optimizer='rmsprop',loss='mean_squared_error')

# Fitting to the training set
regressor.fit(X_train,y_train,epochs=50,batch_size=32)

# X_train.head()
# X_train.info()
print("Size of array: ", X_train.size)
print("Shape of array: ", X_train.shape)

# Now to get the test set ready in a similar way as the training set.
# The following has been done so first 60 entires of test set have 60 previous values which is impossible to get unless we take the whole 
# 'High' attribute data for processing
# dataset_total = pd.concat((dataset["High"][:'2021'],dataset["High"]['2022':]),axis=0)
# inputs = dataset_total[len(dataset_total)-len(test_set) - 60:].values
inputs = test_set
inputs = inputs.reshape(-1,1)
inputs  = sc.transform(inputs)

# Preparing X_test and predicting the prices
# X_test = inputs[]
# for i in range(60,200):
#     X_test.append(inputs[i-60:i,0])
X_test = np.array(inputs)
X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Visualizing the results for LSTM
plot_predictions(test_set,predicted_stock_price)

# print(test_set)
# print(predicted_stock_price.head())

# Evaluating our model
return_rmse(test_set,predicted_stock_price)

# # The GRU architecture
# regressorGRU = Sequential()

# # First GRU layer with Dropout regularisation
# regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
# regressorGRU.add(Dropout(0.2))


# # Second GRU layer
# regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
# regressorGRU.add(Dropout(0.2))


# # Third GRU layer
# regressorGRU.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
# regressorGRU.add(Dropout(0.2))


# # Fourth GRU layer
# regressorGRU.add(GRU(units=50, activation='tanh'))
# regressorGRU.add(Dropout(0.2))


# # The output layer
# regressorGRU.add(Dense(units=1))

# # Compiling the RNN
# regressorGRU.compile(optimizer=SGD(learning_rate=0.01, decay=1e-7, momentum=0.9, nesterov=False),loss='mean_squared_error')

# # Fitting to the training set
# regressorGRU.fit(X_train,y_train,epochs=50,batch_size=150)

# # Preparing X_test and predicting the prices
# # X_test = test_set_scaled
# # # for i in range(60,311):
# # #     X_test.append(inputs[i-60:i,0])
# # X_test = np.array(X_test)
# inputs = test_set
# inputs = inputs.reshape(-1,1)
# inputs  = sc.transform(inputs)

# # Preparing X_test and predicting the prices
# # X_test = inputs[]
# # for i in range(60,200):
# #     X_test.append(inputs[i-60:i,0])
# X_test = np.array(inputs)
# X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
# GRU_predicted_stock_price = regressorGRU.predict(X_test)
# GRU_predicted_stock_price = sc.inverse_transform(GRU_predicted_stock_price)

# # Visualizing the results for GRU
# plot_predictions(test_set,GRU_predicted_stock_price)

# # Evaluating GRU
# return_rmse(test_set,GRU_predicted_stock_price)

# regressor1 = Sequential()

# # First LSTM layer
# regressor1.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1],1)))
# regressor1.add(Dropout(0.2))

# # Second LSTM layer
# regressor1.add(LSTM(units=50, return_sequences=True))
# regressor1.add(Dropout(0.2))

# # Third LSTM layer
# regressor1.add(LSTM(units=50, return_sequences=True))
# regressor1.add(Dropout(0.2))

# # First GRU layer with Dropout regularisation
# regressor1.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
# regressor1.add(Dropout(0.2))


# # Second GRU layer
# regressor1.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
# regressor1.add(Dropout(0.2))


# # Third GRU layer
# regressor1.add(GRU(units=50, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
# regressor1.add(Dropout(0.2))

# # The output layer
# regressor1.add(Dense(units=1))

# # Compiling the RNN
# regressor1.compile(optimizer=SGD(lr=0.01, decay=1e-7, momentum=0.9, nesterov=False),loss='mean_squared_error')

# # Fitting to the training set
# regressor1.fit(X_train,y_train,epochs=100,batch_size=50)

# dataset_total = pd.concat((dataset["High"][:'2021'],dataset["High"]['2022':]),axis=0)
# inputs = dataset_total[len(dataset_total)-len(test_set) - 60:].values
# inputs = inputs.reshape(-1,1)
# inputs  = sc.transform(inputs)

# X_test = test_set
# # for i in range(60,311):
# #   X_test.append(inputs[i-60:i,0])
# X_test = np.array(X_test)
# X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
# predicted_stock_price = regressor.predict(X_test)
# predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# plot_predictions(test_set,predicted_stock_price)

# # Evaluating our model
# return_rmse(test_set,predicted_stock_price)

# # model = create_model()
# regressor1.save('lstm-gru-mix.h5') 
# regressor.save('lstm.h5')
# regressorGRU.save('gru.h5')

# !pip install pyyaml h5py

# import os

# import tensorflow as tf
# from tensorflow import keras

# new_model = tf.keras.models.load_model('lstm.h5')

# # Show the model architecture
# new_model.summary()

"""Save MOdel"""

# import pickle

# data={"modelLstm" : regressor}
# with open ('saved_lstm.pkl','wb') as file:
#   data=pickle.dump(data,file)

# import pickle

# data={"modelGru" : regressorGRU}
# with open ('saved_gru.pkl','wb') as file:
#   data=pickle.dump(data,file)

# import pickle

# data={"modelCombined" : regressor1}
# with open ('saved_combined.pkl','wb') as file:
#   data=pickle.dump(data,file)

"""# **IMP implementation**"""

# import time
# import datetime
# import pandas as pd

# ticker1='TSLA'
# ticker2='BAC'
# period1 = int(time.mktime(datetime.datetime(2012, 1, 1, 23, 59).timetuple())) # year,month,date, hour, min
# period2 = int(time.mktime(datetime.datetime(2022, 12, 31, 23, 59).timetuple()))
# interval = '1d'
# ticker3='AAPL'
# ticker4='MDB'
# ticker5='UBER'



# query_string1 = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker1}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
# query_string2 = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker2}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
# query_string3 = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker3}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
# query_string4 = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker4}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
# query_string5 = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker5}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'


# df1 = pd.read_csv(query_string1)
# df1.insert(loc=0,
#           column='Company',
#           value=ticker1)

# df2 = pd.read_csv(query_string2)
# df2.insert(loc=0,
#           column='Company',
#           value=ticker2)

# df3 = pd.read_csv(query_string3)
# df3.insert(loc=0,
#           column='Company',
#           value=ticker3)

# df4 = pd.read_csv(query_string4)
# df4.insert(loc=0,
#           column='Company',
#           value=ticker4)

# df5 = pd.read_csv(query_string5)
# df5.insert(loc=0,
#           column='Company',
#           value=ticker5)

# frames = [df1, df2, df3, df4, df5]
  
# result_df = pd.concat(frames)
# print(result_df)
# result_df.to_csv('dataset.csv')

# dataset=pd.read_csv('dataset.csv',  index_col='Date', parse_dates=['Date'])
# dataset.pop(dataset.columns[0])
# print(dataset)
# training_set = dataset[:'2021'].iloc[:,1:2].values
# test_set = dataset['2022':].iloc[:,1:2].values

# print(training_set)

# from google.colab import drive
# drive.mount('/content/drive')

# # result_df["High"]['TSLA'].plot(figsize=(16,4),legend=True)
# # result_df["High"]['BAC'].plot(figsize=(16,4),legend=True)
# # plt.legend(['TSLA','BAC'])
# # plt.title('stock price')
# # plt.show()

# dataset["High"][:'2021'].plot(figsize=(16,4),legend=True)
# dataset["High"]['2022':].plot(figsize=(16,4),legend=True)
# plt.legend(['Training set (Before 2022)','Test set (2022 and beyond)'])
# plt.title('stock price')
# plt.show()

# sc = MinMaxScaler(feature_range=(0,1))
# training_set_scaled = sc.fit_transform(training_set)
# test_set_scaled = sc.fit_transform(test_set)

# X_train = []
# y_train = []
# # for i in range(60,200):
# #   X_train.append(training_set_scaled[i-60:i,0])
# #   y_train.append(training_set_scaled[i,0])
# y_train = training_set_scaled[:,0]
# X_train, y_train = np.array(training_set_scaled), np.array(y_train)

# # Reshaping X_train for efficient modelling
# X_train = np.reshape(X_train, (X_train.shape[0],X_train.shape[1],1))

# # The LSTM architecture
# regressor = Sequential()

# # First LSTM layer with Dropout regularisation
# regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1],1)))
# regressor.add(Dropout(0.2))

# # Second LSTM layer
# regressor.add(LSTM(units=50, return_sequences=True))
# regressor.add(Dropout(0.2))

# # Third LSTM layer
# regressor.add(LSTM(units=50, return_sequences=True))
# regressor.add(Dropout(0.2))

# # Fourth LSTM layer
# regressor.add(LSTM(units=50))
# regressor.add(Dropout(0.2))

# # The output layer
# regressor.add(Dense(units=1))

# # Compiling the RNN
# regressor.compile(optimizer='rmsprop',loss='mean_squared_error')

# # Fitting to the training set
# regressor.fit(X_train,y_train,epochs=50,batch_size=32)

# print("Size of array: ", X_train.size)
# print("Shape of array: ", X_train.shape)

# inputs = test_set
# inputs = inputs.reshape(-1,1)
# inputs  = sc.transform(inputs)

# # Preparing X_test and predicting the prices
# # X_test = inputs[]
# # for i in range(60,200):
# #     X_test.append(inputs[i-60:i,0])
# X_test = np.array(inputs)
# X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
# predicted_stock_price = regressor.predict(X_test)
# predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# def plot_predictions1(test,predicted):
#     plt.plot(test, color='red',label='Real Stock Price')
#     plt.plot(predicted, color='blue',label='Predicted Stock Price')
#     plt.title('Stock Price Prediction')
#     plt.xlabel('Time')
#     plt.ylabel('Stock Price')
#     plt.legend()
#     plt.show()

# plot_predictions1(test_set,predicted_stock_price)

# def return_rmse(test,predicted):
#     rmse = math.sqrt(mean_squared_error(test, predicted))
#     print("The root mean squared error is {}.".format(rmse))

# print("RMSE loss: ",return_rmse(test_set,predicted_stock_price))

# import pickle

# data={"multiCompanymodel" : regressor}
# with open ('multi_company_model.pkl','wb') as file:
#   data=pickle.dump(data,file)

# import pickle
# def load_model():
#   with open('multi_company_model.pkl','rb') as file:
#     data=pickle.load(file)
#     return data

# ticker='BAC'
# interval = '1d'
# period1 = int(time.mktime(datetime.datetime(2023, 1, 1, 23, 59).timetuple())) # year,month,date, hour, min
# period2 = int(time.mktime(datetime.datetime(2023, 2, 9, 23, 59).timetuple()))


# query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

# df = pd.read_csv(query_string)
# df.insert(loc=1,
#           column='Company',
#           value=ticker)

# frames = [df]
  
# result_df = pd.concat(frames)
# result_df.to_csv('dataset.csv')
# # print(result_df)

# dataset=pd.read_csv('dataset.csv',  index_col='Date', parse_dates=['Date'])
# dataset.pop(dataset.columns[0])
# print(dataset)
# # test_set = df.iloc[:,1:2].values
# test_set = dataset['2023':].iloc[:,1:2].values
# print(test_set)

# sc = MinMaxScaler(feature_range=(0,1))
# test_set_scaled = sc.fit_transform(test_set)

# inputs = test_set
# inputs = inputs.reshape(-1,1)
# inputs  = sc.transform(inputs)

# # Preparing X_test and predicting the prices
# # X_test = inputs[]
# # for i in range(60,200):
# #     X_test.append(inputs[i-60:i,0])
# X_test = np.array(inputs)
# X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
# predicted_stock_price = regressor.predict(X_test)
# predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# plot_predictions1(test_set,predicted_stock_price)
 
regressor.save('saved_model.h5')