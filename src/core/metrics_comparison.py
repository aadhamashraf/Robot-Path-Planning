# src/core/metrics_comparison.py
import os
import matplotlib.pyplot as plt
plt.style.use('dark_background')


def showDifferences_ExecutionTime(compareAlgos):
    algos = list(compareAlgos.keys())
    times = [compareAlgos[algo][0] for algo in algos]
    steps = [compareAlgos[algo][1]/100 for algo in algos]

    time_sorted_indices = sorted(
        range(len(times)), key=lambda i: times[i], reverse=True)
    sorted_algos_by_time = [algos[i] for i in time_sorted_indices]
    sorted_times = [times[i] for i in time_sorted_indices]

    step_sorted_indices = sorted(
        range(len(steps)), key=lambda i: steps[i], reverse=True)
    sorted_algos_by_steps = [algos[i] for i in step_sorted_indices]
    sorted_steps = [steps[i] for i in step_sorted_indices]

    fig, axs = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)

    axs[0].barh(sorted_algos_by_time, sorted_times, color='skyblue')
    axs[0].set_title('Execution Time Comparison')
    axs[0].set_xlabel('Time (seconds)')
    axs[0].invert_yaxis()

    axs[1].barh(sorted_algos_by_steps, sorted_steps, color='salmon')
    axs[1].set_title('Steps Comparison')
    axs[1].set_xlabel('Number of Steps / 100')
    axs[1].invert_yaxis()

    plt.show()
