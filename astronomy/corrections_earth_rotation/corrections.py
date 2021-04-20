import pandas as pd

data = pd.read_csv('eopc04.62-now', delim_whitespace=True)

#               EARTH ORIENTATION PARAMETER (EOP) PRODUCT CENTER CENTER (PARIS OBSERVATORY)
#                      INTERNATIONAL EARTH ROTATION AND REFERENCE SYSTEMS SERVICE
#                                    EOP (IERS) 14 C04 TIME SERIES                 
#               Description: https://hpiers.obspm.fr/eoppc/eop/eopc04/C04.guide.pdf
#                            contact: christian.bizouard@obspm.fr
#
#  
#             FORMAT(3(I4),I7,2(F11.6),2(F12.7),2(F11.6),2(F11.6),2(F11.7),2(F12.6))
##################################################################################

