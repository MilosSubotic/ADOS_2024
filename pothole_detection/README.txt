napomena: pre pokretanja svake skripte prilagoditi putanje 

- u raw_data folder staviti sve slike pre menjanja rezolucije
- pokrenuti 0_rename.py da se nazivi slika postave na 1.jpg, 2.jpg itd.
- pokrenuti 1_compress_imgs.sh skriptu 
- pokrenuti 2_gen_labels.py i oznaciti sve slike - za prelazak na sl. sliku pritisnuti q
- pokrenuti 3_reorganize.py
- 80% slika/labela je smesteno u train, 10% u valid, 10% u test
- 4_train.py - model yolov8s 
- 5_detect_test.py - rezultati u runs/detect/predict (best) i predict2 (last)

source env/bin/activate

