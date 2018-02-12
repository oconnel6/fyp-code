# Final Year Project Programming Stuff
## Push to github
`git add .`   
`git commit -m "Some message"`    
`git push origin master`    

## Pull from github  
`git pull`

## Run python file
`python script.py`  
Or, for python 3: `python3 script.py`

## Install Python package on MacNeill
`pip install --user <package name>`
- Note: couldn't get pip to work for python3 on MacNeill so using python2

## Running script automatically
- Used a cron job 
- `crontab -e` to edit the cron jobs for my account
- `_ _ _ _ _ python myscript.py`
  - The first 5 numbers specify how often to run the cron job
  - Minute, hour, day, month, day of week
  - So for every day: 0 12 * * *
  
