# academic-transcript-sc

### HOW TO RUN

Move to project directory
<br /> create `.env` file `touch .env`
<br /> copy value from `.env.sample file`

#### Deploy SC to Ganache <br />
&emsp; stat ganache 
&emsp; copy account address and private key to `.env` file <br />
&emsp; requirement : py-solc-x  version : 1.1.1 <br />
&emsp; Comand : `python3 contract/deploy.py` <br />
&emsp; Copy contract address to `.env` file

#### (Optional) create virtual env
&emsp; install virtualenv package `pip install virtualenv` <br />
&emsp; create virtual env : `virtualenv venv` <br />
&emsp; activate virtual environtment <br />
&emsp; linux : `source venv/bin/activate` <br />
&emsp; windows cmd  : `cd venv/scripts` -> `activate` <br />
&emsp; install required package : `pip install -r requirements.txt` <br />
&emsp; run flask `flask run`





   
