echo " " 
echo "          Atualizando o Conda"
conda update -n base -c defaults conda
echo " "
echo "          Procurando atualizacoes pro Ubuntu"
sudo apt update && sudo apt upgrade
echo " "
echo "          Atualizando o pip"
sudo python3 -m pip install --upgrade pip
echo " "
source env.sh
