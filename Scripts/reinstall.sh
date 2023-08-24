echo " "
echo "          Removendo o ambiente virtual"
conda deactivate;conda remove --name bot --all
echo " "
echo "          Criando o ambiente virtual bot"
echo " "
conda create -n bot
conda activate bot
source update.sh
