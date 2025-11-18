# NBA-predictions
Albion and Alex DS340W project on Predicting the next NBA stars

GOAL: Find out the next best players in the NBA (18-23 years old) and can still be in college. Take data from the last 5 years of NBA players and how they might of been in college and predict the next stars of the league.

We are using NBA.com/stats and basketball-reference/stats to find statistics for NBA players in the last 5 years and College basketball players for the last 5 years. We are also using NBA and NCAA data from 2000-2019 for our training set attempting to predict on players from 2020-2025 for the Test set. 

We are first using a cluster based classification system to mark all players in the NBA from 2000-2019 into different cluster tiers ranging from 1-5, 1 being superstars and 5 being limited becnh players. 

We are then using Supervised Learning Techniques like Logistic Regression, Random Forest, and XGBoost to predict on the young NBA and college players and attempt to fit them into the current clusters we have. 

Parent Paper: https://scholar.smu.edu/cgi/viewcontent.cgi?article=1033&context=datasciencereview


