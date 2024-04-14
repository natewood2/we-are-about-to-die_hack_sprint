import matplotlib.pyplot as plt

years = [2016, 2017, 2018, 2019, 2020, 2021, 2022]
emissions = [129, 128, 123, 115, 118, 113, 125]

plt.figure(figsize=(10, 5))
plt.plot(years, emissions, marker='o', linestyle='-', color='blue')
plt.title('ExxonMobil CO2 Emissions from 2016 to 2022')
plt.xlabel('Year')
plt.ylabel('Emissions (Million Metric Tons)')
plt.grid(True)
plt.xticks(years)
plt.show()