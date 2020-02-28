 #!/bin/zsh
 imgpath=$(ls -1t ~/Downloads/img*.jpg | head -1)
 python main.py ${imgpath}