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

#### without virtual env
&emsp; install required package : `pip install -r requirements.txt` <br />
&emsp; run flask `flask run`

## TO DO
- ✅b̶u̶i̶l̶d̶ ̶p̶a̶g̶e̶ ̶i̶n̶s̶e̶r̶t̶ ̶d̶a̶t̶a̶,̶ ̶g̶e̶t̶ ̶d̶a̶t̶a̶,̶ ̶v̶e̶r̶i̶f̶y̶i̶n̶g̶ ̶d̶a̶t̶a̶
- ✅i̶m̶p̶l̶e̶m̶e̶n̶t̶ ̶w̶e̶b̶s̶i̶t̶e̶ ̶u̶s̶i̶n̶g̶ ̶f̶l̶a̶s̶k̶
- ⏳change input form to can store student identity and score list
- ⏳connect from HTML to API
- ⏳test page
