Various simple experiments with The RDKit

drawmol takes SMILES from stdin and produces images (DRAWMOL_IMGTYPE defaults to
svg) in a specified output directory.

testdraw.py experiments with legends using rdkit drawing primitives

timings times various RDKit operations to compare with file I/O (I was trying
to decide what was worth caching for a web service)
mmtimer.py is a utility, might be handy elsewhere

On an Intel(R) Core(TM) i7-7500U CPU @ 2.70GHz, with NVME SSD (Dell XPS13),

0.000513 ms/readline ( 0.000513 ms/readline tot, 999850 in 0.513 secs) 26257984
0.000515 ms/readline ( 0.000515 ms/readline tot, 999850 in 0.515 secs) 26257984
0.000706 ms/sha256 ( 0.00664 ms/sha256 tot, 100023 in 0.664 secs) 6401472
0.00127 ms/GetNumAtoms ( 0.111 ms/GetNumAtoms tot, 9500 in 1.06 secs) 116540
0.00154 ms/GetNumBonds ( 0.112 ms/GetNumBonds tot, 9500 in 1.06 secs) 121468
0.00594 ms/readline ( 0.00594 ms/readline tot, 100023 in 0.594 secs) 2626394
0.0565 ms/filewrite ( 0.0624 ms/filewrite tot, 16500 in 1.03 secs) 0
0.0668 ms/MolToSmiles ( 0.177 ms/MolToSmiles tot, 6000 in 1.06 secs) 125365
0.104 ms/MolFromSmiles ( 0.11 ms/MolFromSmiles tot, 9500 in 1.05 secs) 241419
0.17 ms/MolToMolBlock ( 0.28 ms/MolToMolBlock tot, 4000 in 1.12 secs) 4391013
2.53 ms/MolToImageSVG ( 2.64 ms/MolToImageSVG tot, 500 in 1.32 secs) 3349583
5.08 ms/MolToMolBlockEmbed ( 5.19 ms/MolToMolBlockEmbed tot, 500 in 2.6 secs) 521241
5.15 ms/fsync ( 5.22 ms/fsync tot, 500 in 2.61 secs) 0
6.45 ms/MolToImagePNG ( 6.56 ms/MolToImagePNG tot, 500 in 3.28 secs) 2827093


0.000524 ms/readline ( 0.000524 ms/readline tot, 999850 in 0.524 secs) 26257984
0.000538 ms/readline ( 0.000538 ms/readline tot, 999850 in 0.538 secs) 26257984
0.0023 ms/sha256 ( 0.008 ms/sha256 tot, 100711 in 0.805 secs) 6445504
0.00569 ms/readline-rand10 ( 0.00569 ms/readline-rand10 tot, 100711 in 0.573 secs) 2645671
0.0425 ms/GetNumAtoms ( 0.182 ms/GetNumAtoms tot, 11500 in 2.1 secs) 141148
0.0561 ms/GetNumBonds ( 0.196 ms/GetNumBonds tot, 10500 in 2.06 secs) 133072
0.0577 ms/filewrite ( 0.0634 ms/filewrite tot, 32000 in 2.03 secs) 0
0.123 ms/MolToSmiles ( 0.263 ms/MolToSmiles tot, 8000 in 2.11 secs) 167061
0.134 ms/MolFromSmiles ( 0.14 ms/MolFromSmiles tot, 14500 in 2.03 secs) 372299
0.213 ms/MolToMolBlock ( 0.353 ms/MolToMolBlock tot, 6000 in 2.12 secs) 6594947
2.98 ms/MolToImageSVG ( 3.12 ms/MolToImageSVG tot, 1000 in 3.12 secs) 6878672
7.2 ms/MolToMolBlockEmbed ( 7.34 ms/MolToMolBlockEmbed tot, 500 in 3.67 secs) 529211
7.3 ms/MolToImagePNG ( 7.44 ms/MolToImagePNG tot, 500 in 3.72 secs) 2833502
7.81 ms/fsync ( 7.87 ms/fsync tot, 500 in 3.94 secs) 0
