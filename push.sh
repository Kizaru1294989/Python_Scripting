echo "Enter your message"
read message
echo "Processing"
git add .
git commit -m"${message}"
git status
echo "Pushing data to repo"
git push

echo "
███████ ██    ██  ██████  ██████ ███████ ███████ ███████ 
██      ██    ██ ██      ██      ██      ██      ██      
███████ ██    ██ ██      ██      █████   ███████ ███████ 
     ██ ██    ██ ██      ██      ██           ██      ██ 
███████  ██████   ██████  ██████ ███████ ███████ ███████                                                   
"
echo "data send succesffuly to the github repo"