<!-- SYNTHETIC DEMONSTRATION MANUSCRIPT.
     Every number below is invented to exercise Kalam's drafting and review skills.
     None of it is a scientific result. Do not cite it, and do not carry any value
     from it into a real manuscript. -->

# Repeated hot-dry extremes leave a persistent carbon debt in modelled tropical forests

A. Demo^1^, B. Example^2^

^1^Department of Earth System Science, Example University, Exampleton, Country
^2^Institute for Carbon Cycle Research, Example University, Exampleton, Country

Correspondence: a.demo@example.edu

## Abstract

Recovery from a hot-dry extreme is usually judged from how quickly a forest's carbon
fluxes return to normal, but the quantity that matters for the
carbon budget is the stock. We test whether flux recovery implies stock recovery
with paired 20-year simulations of a terrestrial carbon-cycle model at four
tropical forest sites. The two runs in each pair differ only in whether the anomalies of
identified hot-dry months are retained or replaced by non-extreme values from the same
calendar month. Monthly net biome production returns to its baseline range within 6–18
months after 80% of events. Ecosystem carbon at year 20 is nonetheless lower in 73% of
800 site-parameter simulations, with a pooled median deficit of 1.9 Mg C ha^−1^ (95%
interval −0.6 to 5.4). The deficit is mainly productivity that never occurred
rather than additional respiration. Recovery diagnosed from fluxes can
therefore overstate the recovery of carbon stocks.

## Introduction

Tropical forests hold a large share of terrestrial carbon and account for much of the
interannual variability in the global land sink [@Author2019Sink]. Compound hot and dry
conditions, which suppress photosynthesis and raise respiration at the same time, are
projected to become more frequent across the humid tropics [@Author2021Extremes]. How
much carbon such events cost over decades depends not only on how deep each anomaly is
but on whether the forest makes the carbon back before the next one arrives.

That question is normally answered with a recovery time: the interval over which net
carbon exchange returns to its pre-event range [@Author2020Recovery]. The metric is
attractive because eddy-covariance and satellite records resolve fluxes far better than
stocks. It is also indirect. A flux that has returned to normal has stopped losing
carbon, which is not the same as having replaced the carbon already lost or foregone.
Replacing it requires a subsequent period of above-normal uptake, and nothing in a
return-to-baseline diagnostic reports whether that happened. Observational tests are
scarce because the counterfactual — the same forest under the same climate without the
extreme months — cannot be measured.

Here we construct that counterfactual in a model. We ask whether repeated hot-dry
extremes leave a forest with measurably less carbon after 20 years than the same
background climate without them, and whether the answer can be read off the recovery of
the fluxes. We find that it cannot: fluxes recover within months while a stock deficit
persists for two decades.

## Results

### A paired design that isolates the extreme months

We simulated 20 years of carbon cycling at four tropical forest sites spanning wet to
seasonally dry conditions, using a parsimonious carbon-allocation and turnover model
[@Author2018Dalec] with 200 forest-constrained parameter sets per site (800
site-parameter simulations in total). Each parameter set was run twice from the same
equilibrated initial carbon pools. The repeated-extremes run used the observed seasonal
cycle, the long-term climate trends, and the identified hot-dry anomalies. The
no-extremes counterfactual was identical except that during identified extreme months
the temperature, precipitation and vapour-pressure-deficit anomalies were replaced by
non-extreme values drawn from the same calendar month (Fig. 1a). Extreme months were
those jointly above the 90th-percentile temperature and vapour-pressure-deficit
thresholds and below the 10th-percentile precipitation threshold. Combustion was
disabled in both runs, so no part of the difference is fire.

The paired structure means the two runs differ only in the extreme months themselves.
We define the carbon debt as *D*~20~ = *C*~no-extremes~(20 yr) −
*C*~repeated-extremes~(20 yr), so a positive *D*~20~ means the forest that experienced
the extremes finished the simulation with less ecosystem carbon (Fig. 1b).

### Fluxes recover within months

Monthly net biome production returned to its site's baseline interquartile range within
6–18 months after 80% of individual extreme events (Fig. 1c). On the recovery-time
diagnostic alone, these forests had absorbed each event and moved on well before the
next one.

### The stock deficit does not

The stock tells a different story. Median *D*~20~ was 4.2, 2.7, 1.1 and 0.3 Mg C ha^−1^
at the four sites, ordered from wettest to driest, and 73% of the 800 site-parameter
simulations ended with a positive *D*~20~ (Fig. 2a). Pooling all simulations gives a
median debt of 1.9 Mg C ha^−1^ with a 95% interval of −0.6 to 5.4 Mg C ha^−1^. The
interval crosses zero: this ensemble does not exclude the possibility of full stock
recovery in an individual forest, and we treat the sign of the pooled median, not its
magnitude, as the result.

The ordering across sites runs opposite to intuition, with the largest debts at the
wettest site. The wet site has the most carbon to lose during an anomaly and the
smallest fraction of its productivity already limited by seasonal water stress, so the
same percentile-defined extreme removes more absolute carbon there.

A placebo test rules out the splicing procedure itself as the cause. Replacing the same
number of randomly selected non-extreme months produced a median year-20 difference of
0.05 Mg C ha^−1^ (95% interval −0.7 to 0.8), an order of magnitude below the extreme
case and centred on zero (Fig. 2b). The debt tracks which months were replaced, not how
many.

### The debt is mostly productivity that never happened

A factorial decomposition of the pooled median debt attributes 68% to lower cumulative
net primary production, 27% to additional ecosystem respiration and 5% to interactions
with pool turnover (Fig. 2c). The deficit is therefore dominated by uptake that did not
occur during and shortly after each anomaly, rather than by carbon actively respired
away. This matters for detection: foregone productivity leaves no anomalous efflux to
observe once the flux has returned to baseline, which is precisely why a
return-to-baseline diagnostic misses it.

The result is stable against the choices that define it. Varying the extreme-definition
percentile gave pooled median debts of 1.6, 1.9 and 2.1 Mg C ha^−1^ for the 85th, 90th
and 95th percentiles; changing numerical-optimizer seeds moved the pooled median by less
than 0.04 Mg C ha^−1^, and aggregating the climate forcing monthly rather than daily by
0.06 Mg C ha^−1^ (Supplementary Fig. S1). Narrowing the parameter bounds reduced the
fraction of simulations with a positive debt from 73% to 69%.

## Discussion

Returning carbon fluxes to their normal range does not by itself replace carbon lost or
foregone during previous extremes. Doing so would require a compensating period of
above-normal net uptake, and in these simulations that period does not arrive: the
forest resumes its baseline behaviour from a lower stock and stays there. The two
recovery questions — has the flux normalised, and has the stock been replaced — have
different answers on different timescales, and a study that reports only the first is
silent on the second.

Several limits bound this conclusion. It rests on one model structure at four sites, and
the pooled uncertainty spans zero, so the experiment supports a model-based possibility
of persistent carbon debt rather than a global estimate of its size. The process
attribution is likewise internal to the model and does not establish which mechanism
dominates in real forests. We have not tested 20-year stock differences observationally,
and the counterfactual that makes the experiment possible is also what makes it
unobservable. Whether the debt continues to accumulate under a higher event frequency,
or saturates as the pools equilibrate at a lower level, is not resolved by a 20-year
simulation.

The practical implication is narrower than the mechanism but more immediate. Assessments
that infer ecosystem recovery from the time required for fluxes to return to normal may
overstate the recovery of carbon stocks, and the residual is invisible to the diagnostic
being used. Where stocks are the quantity of interest — carbon accounting, sink
attribution, the durability of forest-based removals — flux recovery time should be
reported alongside a stock comparison rather than in place of one [@Author2022Legacy].

## Data Availability

The synthetic forcing and output used in this demonstration are generated by
`figures/make_demo_figures.py` in this manuscript directory. No observational dataset
underlies this text.

## Code Availability

`figures/make_demo_figures.py` reproduces every figure from the values recorded in its
`RESULTS` dictionary.

## Acknowledgements

<!-- Any standing funding/institutional acknowledgement sentence from resources/User/USER.md goes
     here, once, if this file carries the Acknowledgements; methods.md carries a slot for it too.
     Do not print it in both files. -->

## Author Contributions

A.D. designed the experiment, ran the simulations and wrote the manuscript. B.E.
contributed the process decomposition and revised the manuscript.

## Competing Interests

The authors declare no competing interests.

## Figures

**Figure 1 | Paired experimental design and the two recovery timescales.**
**a**, Months at one site identified as jointly hot and dry, whose anomalies the
counterfactual replaces. **b**, Ecosystem carbon over 20 years in the paired runs for
the wet site's median parameter set; the arrow marks the year-20 carbon debt *D*~20~.
**c**, Composite net biome production anomaly relative to the event month; the shaded
band is the site's baseline interquartile range.
`figures/main/figure1_design_and_trajectories.pdf`

**Figure 2 | Carbon debt, placebo test and process attribution.**
**a**, Distribution of *D*~20~ across 200 parameter sets at each site, wettest to
driest, with the reported site medians marked. Violin widths are illustrative of the
ensemble spread. **b**, Pooled median *D*~20~ and its 95% interval against the
neutral-splice placebo. **c**, Share of the pooled median debt attributed to each
process by the factorial decomposition.
`figures/main/figure2_carbon_debt.pdf`
