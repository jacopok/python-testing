#%%
import numpy as np
import matplotlib.pyplot as plt

delta_t = .1
times = np.arange(0, 100, step=delta_t)
N = len(times)

f0 = .1
real_signal = (
    np.cos(2*np.pi*times*f0)
    + np.random.default_rng().normal(scale=.1, size=N)
    )

dft_numpy = np.fft.rfft(real_signal)
frequencies_numpy = np.fft.rfftfreq(n=N, d=delta_t)

indices_td = np.arange(N)
indices_fd = np.arange(N // 2 + 1)
spinner = np.exp(-1j * 2 * np.pi * np.outer(indices_td, indices_fd) / N )
dft_byhand = np.sum(real_signal[:, np.newaxis] * spinner, axis=0)

frequencies_byhand = indices_fd / N / delta_t

# %%

plt.loglog(frequencies_byhand, abs(dft_byhand), ls='--', alpha=.5)
plt.loglog(frequencies_numpy, abs(dft_numpy), ls=':', alpha=.4)

# %%
print(max(abs(frequencies_numpy - frequencies_byhand)))
print(max(abs(dft_numpy - dft_byhand)))

# %%

signal_recovered = np.fft.irfft(dft_byhand, N)

delta_f = 1 / N / delta_t
times_recovered = np.fft.fftfreq(n=N, d=delta_f) % (delta_t * N)

plt.plot(times, real_signal)
plt.plot(times_recovered, signal_recovered)

print(np.allclose(times, times_recovered))
print(np.allclose(real_signal, signal_recovered))

# %%

plt.plot(times, real_signal / signal_recovered - 1)

# %%

full_dft_byhand = np.empty(N, dtype=np.complex128)
full_dft_byhand[:N // 2+1] = dft_byhand
full_dft_byhand[N // 2+1:] = np.conj(dft_byhand[1:-1][::-1])

spinner_inv = np.exp(2j * np.pi * np.outer(np.arange(N), np.arange(N)) / N)

recovered_byhand = np.sum(full_dft_byhand[np.newaxis, :] * spinner_inv, axis=1) / N 

plt.plot(times_recovered, abs(recovered_byhand - real_signal), label='byhand')
plt.plot(times_recovered, abs(signal_recovered - real_signal), label='numpy')
plt.legend()

# %%

fft = np.fft.fft(real_signal)
rfft = np.fft.rfft(real_signal)

# recovered2 = np.sum(full_fft[np.newaxis,:] * spinner_inv, axis=1) / N
# plt.plot((full_fft[:N//2+1] - dft_numpy).imag)
# plt.plot((full_fft[:N//2+1] - dft_numpy).real)


# plt.plot(abs(fft[:N // 2 + 1] - rfft)) # OK
plt.plot(abs(fft[N//2+1:] - np.conj(rfft[1:-1][::-1])))

# %%

frequencies_numpy
# %%
1/(2* delta_t)
# %%

total_time = delta_t * N

sum_time = np.sum(abs(real_signal)** 2)

sum_freq = np.sum(abs(dft_numpy[0])**2 + 2 * (abs(dft_numpy[1:]) ** 2)) / N

ratio = sum_freq / sum_time

# %%

# %%
