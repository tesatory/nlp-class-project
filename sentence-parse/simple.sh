./bitpar -v grammar lexicon penn23.words.txt penn23.out.txt
perl post-process.pl penn23.out.txt penn23.finalout.txt 
./evalb -p sample.prm penn23.trees.txt penn23.finalout.txt 