# masterthesisprograms

Programs used for target analysis for the 14N(p,g)15O reaction studied in my master thesis (related to the LUNA experiment to be performed in 2022-2023 at Gran Sasso National Laboratories).
1) Simulation to calculate the yield profile (integral of the cross section over the effective stoppping power between two energy values) starting from the target composition: number of layers,
thickness in atoms/cm^2, percentages of nitrogen and tantalum in each layer. The cross section is calculated apart from a normalization constant (to be fitted). NAMEFILE: 'integrale_yieldsim_v3.py'.
2) Program to add beam straggling effects by convolution of the yield values with a gaussian function. NAMEFILE: 'convoluzione2.py'.
3) Program to analyze '.root' files containing energy spectra for gamma rays acquired by a Ge detector. Gets the charge and timestamps form related histograms saved in the '.root' file
   and calculates the areas under the peaks of interest in the energy spectra (also subtracting the background). Calculates the yield (area under a peak divided by the charge) for aech
   beam energy and for each gamma ray transition studied for the 15O nucleus. NAMEFILE 'open_tree_multifilev4.C'.
4) Program to calculate the yield and the expected counting rate starting from the S-factor (to calculate the cross section) and the stopping powers of the target elements. For every proton energy
   the cross section divided by the effective stopping power is integrated over the energy lost by the beam in the target to obtain the yield. Then the rate is calculated as R=yield x I/e x      efficiency, assuming a beam current I=100 muA (e is the electric charge) and target thickness of 10^18 atoms/cm^2, the efficiency is of the Ge detector.   
