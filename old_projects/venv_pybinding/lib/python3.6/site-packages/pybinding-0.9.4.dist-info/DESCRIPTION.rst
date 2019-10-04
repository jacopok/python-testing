Documentation: http://pybinding.site/

v0.9.4 | 2017-07-13

* Fixed issues with multi-orbital models: matrix onsite terms were not set correctly if all the
  elements on the main diagonal were zero ([#5](https://github.com/dean0x7d/pybinding/issues/5)),
  hopping terms were being applied asymmetrically for large multi-orbital systems
  ([#6](https://github.com/dean0x7d/pybinding/issues/6)). Thanks to
  [@oroszl (László Oroszlány)](https://github.com/oroszl) for reporting the issues.

* Fixed KPM Hamiltonian scaling for models with all zeros on the main diagonal but asymmetric
  spectrum bounds (non-zero KPM scaling factor `b`).

* Fixed compilation on certain Linux distributions
  ([#4](https://github.com/dean0x7d/pybinding/issues/4)). Thanks to
  [@nu11us (Will Eggleston)](https://github.com/nu11us) for reporting the issue.

* Fixed compilation with Visual Studio 2017.

* Improved support for plotting slices of multi-layer systems. See "Plotting Guide" > "Model
  structure" > "Slicing layers" in the documentation.



