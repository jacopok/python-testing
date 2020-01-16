

tmax = 300
# params = (0, tmax, np.array([[[1, 1], [-1, -1]], [[-.5, 0], [0.5, 0]]]))
params_so = (0, tmax, np.array([[1., 1.], [-1., -1.]]), np.array([[-.5, 0], [0.5, 0]]))
h0 = .01
plt.close()
# ts, e_xs = euler(second_order, *params, h=h0)
# ts, m_xs = midpoint(second_order, *params, h=2*h0)
# ts, f_xs = fourth_order(second_order, *params, h=4*h0)
Gp = partial(G_prime_mass, Gmasses=[1.,1.])
ts, l_xs = leapfrog_KDK(G, *params_so, h=h0)
ts, lD_xs=leapfrog_DKD(G, *params_so, h=h0)
h_ts, h_xs = hermite(G, Gp, *params_so, h=h0)

solutions = {"Leapfrog KDK": l_xs, "Leapfrog DKD": lD_xs, "Hermite": h_xs}
color = iter(rainbow(np.linspace(0,1,len(solutions))))

for n in solutions:
    c = next(color)
    for i in range(solutions[n].shape[3]):
        l=None
        if (i == 0):
            l = n
        plt.plot(*np.rollaxis(solutions[n][:,0,i,:], -1), label=l, c=c, alpha=.3)

# for i in range(2):
#     # plt.plot(e_xs[:,0,i,0], e_xs[:,0,i,1], label="Euler")
#     # plt.plot(m_xs[:,0,i,0], m_xs[:,0,i,1], label="Midpoint")
#     # plt.plot(f_xs[:, 0, i, 0], f_xs[:, 0, i, 1], label="RK")
#     plt.plot(*np.rollaxis(l_xs[:, 0, i, :], -1), label=)
#     plt.plot(*np.rollaxis(lD_xs[:, 0, i, :]), label=)
#     plt.plot(*np.rollaxis(h_xs[:,0,i,:]), label=)
plt.legend()
plt.show()

# tmax = 100
# ratio = 1e-2
# params = (0, tmax, np.array([[0, 0], [1, 0]]), np.array([[0, -ratio], [0, 1]]))
# masses = [1, ratio]
# h0 = .01
# plt.close()
# my_G = partial(G_mass, Gmasses=masses)
# ts, xs = leapfrog_KDK(my_G, *params, h=h0)
# plt.plot(xs[:, 0, 0, 0], xs[:, 0, 0, 1], label="M")
# plt.plot(xs[:, 0, 1, 0], xs[:, 0, 1, 1], label="m")
# plt.legend()
# plt.show()