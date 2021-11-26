from pycbc.types.timeseries import TimeSeries
from pycbc.types.frequencyseries import FrequencySeries
from pycbc.filter import match
import numpy
import matplotlib.pyplot as plt

data = numpy.sin(numpy.arange(0, 100, 100 / (4096.0 * 64)))
# data += numpy.random.normal(scale=.01, size=data.shape)

# plt.plot(data)
# plt.show()

filtD = TimeSeries(data, dtype=numpy.float64, delta_t=1.0 / 4096)

frequency_series_filt = filtD.to_frequencyseries()

dt_fraction = .5

filtD_offset_subsample = (
    frequency_series_filt *
    numpy.exp(2j * numpy.pi * frequency_series_filt.sample_frequencies *
              frequency_series_filt.delta_t * dt_fraction))

o, _ = match(filtD, filtD_offset_subsample, subsample_interpolation=True)
print(1-o)

# assert numpy.isclose(1, o, rtol=0, atol=1e-8)
