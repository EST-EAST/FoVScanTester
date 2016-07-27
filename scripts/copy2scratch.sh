#rsync -av $home/fovscantest/ /media/sf_banco/fovscantest/
rsync -av --exclude='.git/' --exclude='.idea/' ~/fovscantest/ /media/sf_banco/fovscantest/
