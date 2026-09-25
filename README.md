# Keyboard Heatmap Visualizer

Simulated annealing over keyboard layouts to minimize finger travel for a given piece of text, animated live with matplotlib: a heatmap of key-press frequency plus a live-updating plot of key travel distance per iteration.

## Running

```bash
python "Keyboard Optimization with Simulated Annealing.py"
```

Requires `numpy` and `matplotlib`. Edit `input_str`, `initial_temp`, `cooling_rate`, and `num_iterations` at the top of the script to change the text being optimized for or the annealing schedule.

## How it works

Each finger has a fixed home key and a set of keys it's responsible for; pressing a key costs a round-trip distance from that finger's home position. Starting from a random layout, each iteration swaps two keys to get a neighbouring layout and scores it by total finger travel needed to type `input_str`. A neighbour is accepted if it's better, or with a probability that shrinks as `temp` cools (standard simulated annealing, so early on it can still accept worse layouts to escape local minima). The animation shows the running heatmap of key-press frequency for the best layout found so far, alongside a live plot of distance per iteration.
