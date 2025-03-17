import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ttest_ind
from runGamesPosition import runGA as runGA_position
from runGamesSituation import runGA as runGA_situation

# Note: Only smallClassic and mediumClassic were used
levels = ["testClassic","smallClassic","mediumClassic","trickyClassic","originalClassic"]

def visualiseProcess(timescale_value=5, level="mediumClassic"):
    averages1, bests1 = runGA_position(timescale=timescale_value,gridLayout=level)
    averages2, bests2 = runGA_situation(timescale=timescale_value,gridLayout=level)
    
    generations = range(1, timescale_value + 1)
    plt.figure(figsize=(10, 6))
    plt.plot(generations, averages1, label='Position Averages')
    plt.plot(generations, bests1, label='Position Bests')
    plt.plot(generations, averages2, label='Situation Averages', linestyle='dashed')
    plt.plot(generations, bests2, label='Situation Bests', linestyle='dashed')

    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Evolutionary Progress')
    plt.legend()
    plt.show()
    save = input("Save?")
    plt.savefig(level + 'Visualisation.png')

def runExperiments(numberOfRuns=2, timescale_value=2, level="mediumClassic"):
    results = pd.DataFrame(columns=["Position Agent", "Situation Agent"])
    for i in range(numberOfRuns):
        _, bests = runGA_position(timescale=timescale_value,gridLayout=level)
        results.loc[i,"Position Agent"] = bests[-1]
        _, bests = runGA_situation(timescale=timescale_value,gridLayout=level)
        results.loc[i,"Situation Agent"] = bests[-1]
    results.to_excel(level + "Data.xlsx")
    return results

def analyseResults(level="mediumClassic"):
    results = pd.read_excel(level + "Data.xlsx", index_col=0)
    ttest_result = ttest_ind(results["Position Agent"],results["Situation Agent"])
    results.boxplot(grid=False)
    plt.ylabel('Fitness')
    plt.title("Statistic: " + str(ttest_result.statistic) + \
              "\nP-value: " + str(ttest_result.pvalue))
    plt.savefig(level + 'Boxplot.png')
    plt.show()

#visualiseProcess(timescale_value=100, level=levels[3])
#print(runExperiments(numberOfRuns=10, timescale_value=10, level=levels[2]))
analyseResults(level=levels[2])





