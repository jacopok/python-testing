%run bayesian_hyp_testing.py 
x = simulate_detections(10000, .1, .1, .01, .01) 
y = generate_detections_classical(.01, .1, 100_000) 
plt.hist(x.N_12, label='sim', alpha=.5, density=True) 
plt.hist(y.N_12, label='gen', alpha=.5, density=True) 
plt.legend() 
plt.show()                                                                                 
