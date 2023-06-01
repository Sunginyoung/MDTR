## Multi-dimensional Transcriptomic Ruler
* Multi-dimenisonal transcriptomic ruler (MDTR) provides measurements of the degree of dysregulation in gene expression data at the transcriptome level for five hepatotoxicity mechanisms.

  _Five hepatotoxicity mechanisms_
  * Oxidative stress
  * Immunological response
  * Altered lipid metabolism
  * Mitochondrial dysfunction
  * Bile acids accumulation
* The measured values are visualized through radar chart.
* MDTR is also accessible on the website: http://biohealth.snu.ac.kr/software/MDTR

## Intallation
`MDTR.py` is implemented in with [Python](https://www.python.org/) libraries. 
The following are the requirements for `MDTR.py`

### Requirements
* Python        (over 3.7)
* Pandas        (over 1.3.5)
* NumPy         (over 1.21.5)
* SciPy         (over 1.7.3)
* scikit-learn  (over 1.0.2)
* Matplotlib    (over 3.5.3)

## Usage
`MDTR.py` supports command-line invocation as below:
```
usage: python MDTR.py [-h] [--r R] expr outdir

positional arguments:
  expr        File path of gene expression data.
              Tab-delimited file format (.txt) is recommended for input data.
              It is also recommended to use Z-normalized files.
  outdir      Directory to save a result file

optional arguments:
  -h, --help  show this help message and exit
  --r R       (1/0) Whether to save the radar chart for the measured results (default=0)
```
**Expression data** should follow the format below:

    Gene  Sample1 Sample2    # Header
    G1  Exp11  Exp12
    G2  Exp21 Exp22
    G3  Exp31 Exp32
    ...
    
* The data is recommended in tab-delimited file format, where rows represent genes and columns represent expression values.
* The first row should correspond to the sample ID, and the first column should contain the gene symbol.
* Please perform z-normalization of the expression values.

## Example
First, clone the repository or download compressed source code files.
```
$ git clone https://github.com/Sunginyoung/net_stratification.git
$ cd MDTR
```
You can see the valid parameters for net_stratificaion by help option:
```
$ python ./MDTR.py --help
```
You can run MDTR with toy expression data.
1. If you want a radar chart visualization:
```
$ python ./MDTR.py \
                                ./example/input/Toy_Expression.txt  \
                                ./example/output  \
                                --r 1
```
2. If you do not want radar chart visualization:
```
$ python ./MDTR.py \
                                ./example/input/Toy_Expression.txt  \
                                ./example/output  \
                                --r 0
```


## Contact
If you have any questions or concerns, please send an email to [inyoung.sung@snu.ac.kr](inyoung.sung@snu.ac.kr).
