# byot_loader
A demo tool to dynamically load toekns from another systems into a Skyflow Vault.
It reads a CSV file and creates a vault from the CSV file structure.
Data and tokens are loaded into this.

This intends to show the power of the Skyflow API first approach and platform for customers wanting to accelerate an implementation/migration ny using existing systems tokens within Skyflow

Before running the tool, you need to perform pre-setup tasks
You need to have a Skyflow Try environment account (login)

Login to your Skyflow Studio (assuminng you are a vault owner or administrator)

Create an Account level "**Service Account**"
The service account MUST have the following Assignments & Roles:
 - Assignment:  Account-Level     Role:  "Account Admin"
 - Assignment:  Workspace-level   Role:  "Vault Creator" and  "Workspace Admin"
 - SAVE the settings and generate a **credentials.json** file.  (You will be requested for this file when the script runs!)

In the "byot_loader" repo, there is a file:   **byot_params.json**
Edit this file and change **ALL** the parameter values to the ones associated with your Skyflow Account and environment

Your CSV file needs to contain the name-value pairs for: clear text data and the token to be migrated.
So this can be in the format:  text, token  or,   text1, token 1, text2, token2,text3, token3, etc
Note:
Text column can have any name, the corresponding token column must be of the format: <token_column>_token in the CSV file.

All done!  You are ready to run the loader.
The laoder will take any "Strcutured Data" CSV file you provide.  A few samples are provided in the distribution and have been used to validate correct operation.
If you want to generate your own test data, you can use any tool of you choice or an online utility like e.g. Mockaroo:  https://www.mockaroo.com/

Now run the loader:   byot.py   and follow the prompts.
> python3 byot.py
