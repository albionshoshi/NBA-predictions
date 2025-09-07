import pandas as pd

def inchesConverter(x):
    g= x.strip().split("'")
    return (int(g[0])*12+float(g[1]))


combine = pd.read_csv("NBACombine.csv")
collegeStats = pd.read_csv("CollegeStats.csv")
nbaStats = pd.read_csv("nba_player_data.csv")

combine = combine.rename(columns={'Player': 'Name'})
nbaStats = nbaStats.rename(columns={"PLAYER":'Name'})
temp = combine.dropna()

combineCollegeMerge = pd.merge(temp, collegeStats, on='Name', how='inner')


wingspan = combineCollegeMerge["Wingspan"].apply(lambda x: inchesConverter(x))
height = combineCollegeMerge["Height Without Shoes"].apply(lambda x: inchesConverter(x))
reach = combineCollegeMerge["Standing Reach"].apply(lambda x: inchesConverter(x))
combineCollegeMerge["Wingspan"],combineCollegeMerge["Height Without Shoes"],combineCollegeMerge["Standing Reach"] = wingspan, height, reach
collegeFinal = combineCollegeMerge[["Name","Year","Height Without Shoes","Wingspan","Standing Reach","G","PTS","TRB","AST","2P%","3P%","FT%","Pos"]]

nba =nbaStats.groupby("Name").agg({"GP":'sum'})
Final = pd.merge(collegeFinal, nba, on='Name', how='inner')
Final["Suc"] = (Final["GP"] > 174).astype(int)
Final = Final.drop_duplicates()

print(Final)

Final.to_csv("cleanedStats.csv",index=False)

train = Final.sample(frac=.7, random_state=11)
leftover = Final.drop(train.index)
test = leftover.sample(frac = 2/3, random_state=11)
validation = leftover.drop(test.index)

train.to_csv("TrainSet.csv",index=False)
test.to_csv("TestSet.csv",index=False)
validation.to_csv("ValidationSet.csv",index=False)