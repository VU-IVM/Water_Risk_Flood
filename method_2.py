# METHOD 2 - USING AN EMPIRICAL FUNCTION
# Fit the empirical function to obtain the IDF. Here we use a power law.

#We use the IDF values to create the variables needed to solve the equation:
#log(I) = log(k) + m log(D) + n log(D)

k=1
regression = NaN(pd.DataFrame.shape(return_periods,2)*pd.DataFrame.shape(duration,2),4)
for i=1:pd.DataFrame.shape(return_periods,2):
    for j=1:pd.DataFrame.shape(duration,2):
        regression[k,1]=log10(IDF(i,j)) #Y
        regression[k,2]= 1 #Filling X1 = 1 so that we know the regression intercept
        regression[k,3]=log10(return_periods(i)) #X2
        regression[k,4]=log10(duration(j)) #X3
        k = k+1
    end
end

#Creating the matrices
Y = regression[:,1] 
X_matrix = regression(:,[2 3 4])

#Solving the general linear model. For more information, see:
#https://en.wikipedia.org/wiki/Regression_analysis

X_matrix_transpose = transpose(X_matrix)
part_a = X_matrix_transpose*Y
part_b0 = X_matrix_transpose*X_matrix
part_b = inv(part_b0)
betas = part_b*part_a
beta_values = [10^betas(1) betas(2) -betas(3)]

#Calculate the empirical IDF based on the coefficients found.
Durations = 0.5:0.005:24
IDF_emp = NaN(size(return_periods,2),size(Durations,2))
for i=1:size(return_periods,2)
    IDF_emp(i,:)= beta_values(1)*(return_periods(i).^beta_values(2))./(Durations.^(beta_values(3)))
end

#Plot the results
figure('Name','IDF curves - Power Law')
for i=1: size(return_periods,2)
    plot(duration, IDF(i,:), '.k')
    hold on
    plot(Durations,IDF_emp(i,:), '-')
end
hold off
grid on
#Add a legend to your figure!
xlabel('Duration (hours)')
ylabel('Rainfall Intensity (mm/hr)')
xlim([0 25])