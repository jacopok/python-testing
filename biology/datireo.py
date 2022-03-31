from strain_hardening_mod import StressSweep, plot_sweeps, Sample, FrequencySweep

samples = [Sample(chitosan_concentration=0.8, rdg=72, stress_sweep=
    StressSweep(tau=[
        0.103628,
        0.154098,
        0.22921,
        0.340896,
        0.507067,
        0.754255,
        1.121608,
        1.667544,
        2.480463,
        3.688784,
        5.487986,
        8.164467,
        12.137643,
        18.038471,
        26.797951,
        39.747044,
        59.007874,
        87.439301,
        129.707199,
        192.34285,
        284.949066,
        423.016724,
        574.512939
    ], g_prime=[
        42.910912,
        43.172272,
        43.104431,
        43.175701,
        43.09277,
        42.985321,
        43.237415,
        43.734844,
        43.616528,
        43.796329,
        43.47028,
        43.18935,
        43.77039,
        44.777027,
        46.356522,
        50.574478,
        53.848454,
        61.900314,
        69.2267,
        79.99543,
        100.358513,
        108.584686,
        0.130763],
                gamma=[
            0.002414,
            0.003569,
            0.005317,
            0.007894,
            0.011764,
            0.017543,
            0.025936,
            0.038122,
            0.05686,
            0.084211,
            0.126226,
            0.189008,
            0.277261,
            0.402772,
            0.577995,
            0.785816,
            1.095635,
            1.412421,
            1.872041,
            2.401083,
            2.826035,
            3.771224,
            172.642548
        ]
    ), frequency_sweep= 
    FrequencySweep(frequency=[
        100,
        90,
        80,
        70,
        60,
        46.419998,
        31.620001,
        21.540001,
        14.68,
        10,
        6.81,
        4.64,
        3.16,
        2.5,
        1.468,
        1,
        0.68,
        0.46,
        0.31,
        0.21,
        0.1,
        0.08,
        0.06,
        0.03,
        0.01], g_prime=[
        3943.09375,
        3041.370605,
        898.418945,
        7393.207031,
        1873.668457,
        405.867432,
        33.638062,
        28.043762,
        21.791656,
        62.978874,
        41.461411,
        34.520874,
        30.741972,
        36.06041,
        36.095829,
        36.109989,
        36.306286,
        36.013695,
        35.787094,
        35.600136,
        35.606949,
        35.9338,
        36.251537,
        36.733913,
        37.567974], g_second=[
        999.855652,
        1717.990845,
        1124.113403,
        7257.486328,
        807.844177,
        589.208862,
        166.265182,
        13.86916,
        4.366801,
        53.197578,
        5.822842,
        2.931954,
        2.300973,
        1.62264,
        1.263456,
        0.984497,
        0.713738,
        0.643857,
        0.559917,
        0.516861,
        0.512691,
        0.520687,
        0.558688,
        0.691369,
        1.281984] ) ), 
                Sample(chitosan_concentration=1.0, rdg=90, stress_sweep=
    StressSweep(tau=[
        0.101444,
        0.15087,
        0.224349,
        0.333605,
        0.496155,
        0.738308,
        1.098516,
        1.634184,
        2.43052,
        3.614626,
        5.375626,
        7.993818,
        11.885744,
        17.668753,
        26.265284,
        39.017296,
        58.001015,
        86.179192,
        128.008896,
        190.107574,
        282.377686,
        419.530548,
        623.328979,
        927.600952,
        444.64505
    ], g_prime=[
        105.574593,
        106.189911,
        107.763535,
        109.651077,
        110.173088,
        106.519066,
        103.922203,
        102.625114,
        102.865204,
        103.668686,
        104.456123,
        105.938896,
        108.402641,
        112.732483,
        117.494392,
        129.953629,
        136.268784,
        150.116913,
        172.685364,
        208.313934,
        255.622192,
        314.410706,
        402.573486,
        349.52182,
        0.177562
        ],
    gamma=[
        0.000961,
        0.001421,
        0.002081,
        0.003042,
        0.004502,
        0.00693,
        0.010568,
        0.01592,
        0.023622,
        0.034858,
        0.05145,
        0.075439,
        0.10962,
        0.156699,
        0.223498,
        0.30018,
        0.425547,
        0.573911,
        0.740782,
        0.911426,
        1.103104,
        1.331801,
        1.542884,
        2.633762,
        989.801697
        ]), frequency_sweep=
    FrequencySweep(frequency=[
        100,
        90,
        80,
        70,
        60,
        46.419998,
        31.620001,
        21.540001,
        14.68,
        10,
        6.81,
        4.64,
        3.16,
        2.5,
        1.468,
        1,
        0.68,
        0.46,
        0.31,
        0.21,
        0.1,
        0.08,
        0.06,
        0.03,
        0.01], g_prime=[
        1174.750977,
        3181.974609,
        4900.437988,
        2354.400879,
        1257.145752,
        293.519775,
        109.167603,
        63.317383,
        126.15509,
        131.138824,
        80.017143,
        122.982224,
        127.734909,
        127.701042,
        124.870842,
        122.267761,
        119.725403,
        119.229683,
        118.625748,
        116.382469,
        110.11644,
        107.770996,
        103.437538,
        101.661842,
        97.08049], g_second=[
        1177.276855,
        3664.532959,
        2988.591553,
        2481.398193,
        309.845184,
        61.240425,
        57.961582,
        207.003067,
        4.447275,
        12.566051,
        12.759765,
        4.671105,
        4.261343,
        3.264773,
        2.827128,
        2.703748,
        2.708164,
        2.305827,
        2.010285,
        2.098864,
        2.10513,
        1.886386,
        1.924049,
        1.970472,
        2.797244] ) ), 
            Sample(chitosan_concentration=1.3, rdg=117, stress_sweep= 
              StressSweep(tau=[
        0.10103,
        0.150269,
        0.223492,
        0.332357,
        0.494234,
        0.735172,
        1.093625,
        1.626842,
        2.419837,
        3.598939,
        5.352771,
        7.960898,
        11.839373,
        17.608263,
        26.185354,
        38.933498,
        57.880398,
        86.042068,
        127.845085,
        189.946686,
        282.241577,
        419.456299,
        623.274109,
        926.29834,
        1376.981812,
        1795.725586
    ], g_prime=[
        147.238403,
        147.119843,
        147.829453,
        150.141663,
        153.167206,
        151.64888,
        149.402985,
        147.293686,
        146.397629,
        147.241806,
        147.554443,
        148.568527,
        150.167847,
        151.069153,
        153.608658,
        159.14798,
        167.47728,
        178.10939,
        202.253952,
        236.147095,
        278.63797,
        326.647034,
        413.420563,
        527.345154,
        651.371521,
        0.284449,
        ],
        gamma=[
            0.000686,
            0.001021,
            0.001511,
            0.002212,
            0.003225,
            0.004845,
            0.007315,
            0.011038,
            0.016518,
            0.024427,
            0.036254,
            0.053551,
            0.078793,
            0.116489,
            0.170371,
            0.244501,
            0.345413,
            0.482813,
            0.63172,
            0.8038,
            1.01201,
            1.282114,
            1.504434,
            1.752037,
            2.106986,
            552.594116] ), frequency_sweep= 
        FrequencySweep(frequency=[
            100,
            90,
            80,
            70,
            60,
            46.419998,
            31.620001,
            21.540001,
            14.68,
            10,
            6.81,
            4.64,
            3.16,
            2.5,
            1.468,
            1,
            0.68,
            0.46,
            0.31,
            0.21,
            0.1,
            0.08,
            0.06,
            0.03,
            0.01], 
                g_prime=[
            374.010742,
            1004.59082,
            2503.736328,
            603.475098,
            401.435547,
            131.210205,
            246.768555,
            115.801758,
            155.62561,
            167.603714,
            175.919189,
            182.970016,
            173.306503,
            172.9487,
            170.385284,
            168.214325,
            164.675217,
            162.89447,
            159.950912,
            158.02478,
            151.139572,
            145.978363,
            142.572784,
            138.602631,
            136.457413],
                g_second=[
            3419.010986,
            2483.078613,
            1724.254395,
            37.201584,
            479.260254,
            219.86853,
            23.335403,
            172.759094,
            20.987322,
            9.225343,
            9.480248,
            10.592808,
            7.946284,
            7.176764,
            5.825496,
            5.531624,
            4.630491,
            4.937768,
            4.678379,
            3.573081,
            3.45309,
            5.240385,
            2.71481,
            4.794035,
            4.069367] 
                ) 
            ) 
        ]

if __name__ == '__main__':

    for sample in samples:
        print(sample.frequency_sweep.shear_modulus())
  
