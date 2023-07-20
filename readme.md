# [Placeholder Title]

The goal of this project is to create a virtual personality, interacting with the world through Instagram. This "person" (as I will refer to it) is able to both react to existing content on Instagram, as well as create complete posts of its own. 
#
## Installation
1. Download AUTOMATIC1111's stable difussion webui, following the guide [here](https://something.com)
2. Edit the `webui-user.bat` file in the `sd-webui` repo and add the `--api` flag to the `COMMANDLINE_ARGS` parameter.
3. Download this repo into a folder of your choice with

`git clone https://github.com/something`

4. Navigate to the repo and download requierements
```
cd something
pip install -r requierments.txt
```
5. [Get an OpenAI API key](https://openapi.com) and set it with 
```
setx OPEN_API_KEY <your key>
```

6. Go to [Instagram](https://instagram.com) and create an account. I suggest using an email from a temporary email site. Alternatively, you could use an existing account, but I highly advise against it, as its likely that at some point Instagram will suspend the acount. 
7.  Set your account email and password with
```
setx ACCOUNT_EMAIL <the account email>
setx ACCOUNT_PASSWORD <the acccount password>
```
You can always set these again whenever the account gets suspended.
#
## Configuration
1. Open up `config.py`
2. The program locally saves all images and their prompts. Set `IMAGES_FOLDER` to the folder where you want these saved. If you want to disable this, set the parameter to empty
3. 
