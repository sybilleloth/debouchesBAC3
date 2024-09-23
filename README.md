# Projet Streamlit "sortiebac3enFrance.py"
**Auteur:**

*Sybille DL. : sybille@hotmail.fr*

## about the app

This is an overview of opportunities for young graduates in professional/global/LMD & MEEF Masters provided by French universities

Author and editor of the present investigation : French " Ministère de l'Enseignement Supérieur et de la Recherche".
On the dataset basis provided by Ministère de l'Enseignement Supérieur et de la Recherche, those pages displayed through this streamlit app, help us understand how the French educational system is spread all over French régions ans West Indies and how they all deliver a diploma opening the doors of working world.

The analysis pages underline how wide the range of matters and majors is.

investigation hypothesis
Evaluate the accuracy of the data provided regarding the period of graduation between 2019 and 2021
Clean and keep accurate data that can be efficient to analyse
Acquire a relevant knowledge of the provided data in order to answer the initial question
Analyze and explore the data
Visualize and present the final conclusion
In a few words : does the French educational system lead to work all over France equally, are there some favorable universities and how high is the rate of students resuming their studies when they graduate with a BAC + 3 ?

this streamlit app has been developed and set up in Sept. 2024 thanks to open source tools introduced in page (MERCI)



### launch with MacOS / Linux

- in the terminal; please do execute : `bash setup.sh` (the first time only
- afterwards, execute `bash run.sh` to display the app created with Streamlit.

### Windows

Do execute the following commands in the forthcoming proper ordre :
- set-up libraries as listed in requirements.txt and initiate the database :

`pip install --update pip`
`pip install -r requirements.txt`
`python3 setup.py`
'from your directory : `cd {your_directory}`
- check the existing files with ' `ls` command 
- In order to call the Streamlit app :  **`streamlit run sortiebac3enfrance.py`**
- In order to call the logs on the app : **'python check_directory.py'**

### set up the kernel (virtual environment)

Step 1 : Clone this projet from the GitHub platform
- Open a terminal/console
- clone the project locally with "git clone". Replace the  <URL_du_projet> with your GitHub's project URL.
--- 'git clone <URL_du_projet>
access the project's directory : 
--- 'cd <nom_du_projet>'

Step 2  : Create a virtual environment 
create it with the following command  (env, venv or as you like as long as it reminds you this is an 'environment')
--- 'python -m venv env'
activate on windows : 
---'env\Scripts\activate'
activate with macOS & Linux :
---'source env/bin/activate'

Step 3 : install dependencies with requirements.txt
---'pip install -r requirements.txt'

Step 4 : it's worth checking ! 
---'pip list'

Step 5 : if you want to disactivate the environment
---'deactivate'

### Tools & others specifics 
The font is the EXO google's font : Exo set up in the app (all files included). It's employed as it is a free one, available for all kind of machines and OS Systems

The python language is V.3.12


Enjoy ! 