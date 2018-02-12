# python-data-science

### Install git
$ sudo apt-get install git

### Create a public key to connect automatically to Github (optional)
$ ssh -vT git@github.com
$ ls -al ~/.ssh
$ ssh-keygen -t rsa -b 4096 -C “githusername@github.com”  # Press enter 3 times until getting the key randomart
$ pbcopy < ~/.ssh/id_rsa.pub

### Go to our profile in Github (optional)
settings -> ssh keys -> add key -> past -> add key
Paste the public key (ctrl + v)

### Check if now we have a public key (optional)
$ ssh -vT git@github.com

### Fork our course repo
- Click on "fork" in the right upper corner
- Select your user
- Go to your profile of Github and go into your new ReDI_DataScience repo
- Go to your Github account and find the just forked repo
- Clone the repo in your computer
$ git clone https://github.com/your_github_name/python-data-science.git



