"""Run with Python 3 from any directory. Values are in MPa, metres and kelvin."""
import csv
from math import log, pi, sqrt
from pathlib import Path

with Path(__file__).with_name("Yield-data.csv").open() as stream:
    rows = list(csv.DictReader(stream))
baseline = float(rows[0]["yield_strength_MPa"])
w = [float(row["MgO_wt_percent"]) / 100 for row in rows[1:]]
y = [float(row["yield_strength_MPa"]) for row in rows[1:]]
v = [(x / 3580) / (x / 3580 + (1 - x) / 2810) for x in w]

def evaluate(d=600e-9, dt=700, eta=0.5, mismatch=14e-6, interaction=0.20, rss=False):
    prior = []
    b, shear = 0.286e-9, 26900
    for x in v:
        spacing = d * ((pi / (6*x))**(1/3) - 1)
        density = 12*x*mismatch*dt / (b*d*(1-x))
        taylor = 3.06*interaction*shear*b*sqrt(density)
        orowan = 0.13*shear*b/spacing*log(d/(2*b))
        increment = sqrt(taylor**2 + orowan**2) if rss else taylor + orowan
        prior.append(baseline + increment + eta*x*baseline)
    def fit(indices):
        return min(0, sum(v[i]**2*(y[i]-prior[i]) for i in indices) /
                      sum(v[i]**4 for i in indices))
    folds = [fit([j for j in range(3) if j != i]) for i in range(3)]
    predictions = [p + beta*x*x for p, beta, x in zip(prior, folds, v)]
    errors = [a-b for a,b in zip(y,predictions)]
    sse = sum(e*e for e in errors)
    return (fit(range(3)), folds, predictions, sum(map(abs,errors))/3,
            sqrt(sse/3), 1-sse/sum((a-sum(y)/3)**2 for a in y))

if __name__ == "__main__":
    for options in [{}, {"d":480e-9},{"d":720e-9},{"dt":560},{"dt":730},
                    {"eta":0.25},{"eta":0.75},{"interaction":0.16},{"interaction":0.24},{"rss":True}]:
        print(options, evaluate(**options))
