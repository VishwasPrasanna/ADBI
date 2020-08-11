# Load the libraries 
# To install pcalg library you may first need to execute the following commands:
# source("https://bioconductor.org/biocLite.R")
# biocLite("graph")
# biocLite("RBGL")


# Above code did not work for me so I had to use the below code to install and load libraries needed 
# install.packages("BiocManager")
# BiocManager::install("graph")
# BiocManager::install("RBGL")
# BiocManager::install("Rgraphviz")
# install.packages("vars")
# library(vars)
# install.packages("pcalg")
# library(pcalg)

# Read the input data 
input <- read.csv('data.csv')


# Build a VAR model 
# Select the lag order using the Schwarz Information Criterion with a maximum lag of 10
VARselect(input, lag.max=10)
var_model<- VAR(input, p=1)
# see ?VARSelect to find the optimal number of lags and use it as input to VAR()

# Extract the residuals from the VAR model 
var_residuals <- residuals(var_model)
# see ?residuals

# Check for stationarity using the Augmented Dickey-Fuller test 
summary_stats <- function(d){ summary(ur.df(d, type="none")) }
apply(var_residuals, 2,summary_stats)  
# Based on Augmented Dickey-Fuller test, p-value for residuals of variables 
# is significatly less than 0.05 providing evidence
# to reject the null hypothesis meaning the residuals follow stationary pattern
# see ?ur.df

# Check whether the variables follow a Gaussian distribution  
summary_stats2 <- function(d) { ks <- ks.test(d, "pnorm") }
apply(var_residuals, 2, summary_stats2)
#Based on one-sample kolmogorov-Smirnov test, p-value for residuals of variables
# is significatly less than 0.05 providing evidence to reject the null hypothesis, meaning the variables follow gaussian distribution.
# see ?ks.test

# Write the residuals to a csv file to build causal graphs using Tetrad software


# OR Run the PC and LiNGAM algorithm in R as follows,
# see ?pc and ?LINGAM 

# PC Algorithm
# alpha value is set to 0.1 
sufficient_stats <- list(C=cor(var_residuals), n=nrow(var_residuals))
pc_model <- pc(sufficient_stats, indepTest=gaussCItest, alpha=0.1, labels=colnames(var_residuals), skel.method="stable", verbose=TRUE)
plot(pc_model, main="Output for PC Algorithm")

# LiNGAM Algorithm
# LINGAM was deprecated so used lingam() 
# default prune value of lingam() function is set to 1
# lingam_model <- LINGAM(var_residuals, verbose=TRUE)
lingam_model <- lingam(var_residuals, verbose=TRUE)
show(lingam_model)
