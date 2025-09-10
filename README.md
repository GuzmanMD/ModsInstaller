# ModsInstaller  
______________________________________________________________________________________  

This application is used to install mods for each game (there are three pre-defined games)
without having to do anything. You open the .exe, select the game, wait, and voila, the mods
are installed without having to do anything.

_______________________________________________________________________________________
  
  
  
IMPORTANT
If your games are from M4CKD0GE REPACKS (with online from online-fix.me) and you install mods, if you want online access, you must copy certain files back to the game's root folder:
./game (M4CKD0GE REPACKS)/ 
    
    
    
This archives are in:  
mods_{juego}/archivos_{juego}  
  
____________________________________  
If you clone the repository and want to change a game you've to change the api names, line 10-14:  

GITHUB_USER = "GuzmanMD" < change  
GITHUB_REPO = "ModsInstaller" < change  
 
  
Also change line 132, where the names of the games are and the folder the app will look for to download the mods.zip and decompress it.
  juegos = [("Lethal Company", "mods_lethal"), ("REPO", "mods_repo"), ("Phasmo", "mods_phasmo")]


