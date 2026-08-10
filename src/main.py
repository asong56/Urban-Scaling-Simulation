import os
import csv
import datetime
from model import CityEngine

def run_simulation(round_name, intellect, population, wealth, cost, tax_baseline, edu_baseline, years):
    edu_rates = [round(edu_baseline * factor, 3) for factor in [0.5, 0.75, 1.0, 1.25, 1.5]]
    tax_rates = [round(tax_baseline * factor, 3) for factor in [0.5, 0.75, 1.0, 1.25, 1.5]]
    
    _src_dir = os.path.dirname(os.path.abspath(__file__))
    _data_dir = os.path.join(_src_dir, "..", "data")
    os.makedirs(_data_dir, exist_ok=True)
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    filepath = os.path.join(_data_dir, f"results_{today_str}.csv")

    config = {
        "intellect": intellect,
        "population": population,
        "wealth": wealth,
        "cost": cost
    }

    print(f"--- Simulation {round_name} started. ({years} years) ---")
    
    with open(filepath, 'w', newline = '') as f:
        fieldnames = ['run_id','year','population','gini','morale','yield','edu_rate','tax_rate']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    
        for i in edu_rates:
            for j in tax_rates:
                run_id = f"Sample_{i}_{j}"
                sample = CityEngine(name=run_id, config=config)
                
                for year in range(1, years + 1):
                    response = sample.run_fiscal_year(i,j)
                    if isinstance(response, dict) and response['population'] == 0:
                        break
                    if response == 0:
                        break
                
                report = sample.get_report()
                zipped_data = zip(
                    report['history_pop'], 
                    report['history_gini'], 
                    report['history_morale'], 
                    report['history_yield']
                )
                
                for idx, (pop, gini, mor, yld) in enumerate(zipped_data):
                    writer.writerow({
                        'run_id': run_id,
                        'year': idx + 1,
                        'population': pop,
                        'gini': gini,
                        'morale': round(mor, 2),
                        'yield': yld,
                        'edu_rate': i,
                        'tax_rate': j
                    })
    
    print(f"Simulation complete. {round_name} data saved to {filepath}")
    return filepath

if __name__ == "__main__":
    round_name = input("Round Name: ")
    intellect = float(input("Initial Intellect: "))
    population = int(input("Initial Population: "))
    wealth = float(input("Initial Personal Wealth: "))
    cost = float(input("Initial Survival Cost: "))
    tax_baseline = float(input("Tax Base: "))
    edu_baseline = float(input("Educational Input Base: "))
    years = int(input("Years: "))
    run_simulation(round_name, intellect, population, wealth, cost, tax_baseline, edu_baseline, years)


