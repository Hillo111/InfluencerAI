# InfluencerAI

## Project description

The goal of this project is to create a virtual personality, interacting with the world through Instagram. This "person" (as I will refer to it) is able to both react to existing content on Instagram, as well as create complete posts of its own. 
This "person" is able to emulate whatever personality you want, allowing you to reach vast audiences
#
## Installation
This instruction set is made for Windows.
1. Download the stable difussion webui (by AUTOMATIC1111), following the guide [here](https://github.com/AUTOMATIC1111/stable-diffusion-webui#installation-and-running)
2. Edit the `webui-user.bat` file in the repo and add the `--api` flag to the `COMMANDLINE_ARGS` parameter.
3. Download the [RealisticVision2.0 model](https://civitai.com/api/download/models/29460) and place it in the `/models/Stable-diffusion/` folder of the stable diffusion webui repo.
4. Download the associated [VAE decoder](https://civitai.com/api/download/models/29460?type=VAE) and place it in `/models/VAE/`
5. Download this repo into a folder of your choice with

`git clone https://github.com/Hillo111/InfluencerAI.git`

6. Navigate to the repo and download requirements
```
cd degeneracy
pip install -r requirements.txt
```
#
## Configuration
1. Open up `config.py`
2. [Get an OpenAI API key](https://platform.openai.com/account/api-keys) and set it to the `OPEN_AI_API_KEY` variable

3. Go to [Instagram](https://instagram.com) and create an account. I suggest using an email from a temporary email site. Alternatively, you could use an existing account, but I highly advise against it, as its likely that at some point Instagram will suspend the acount. 
4.  Set the `ACCOUNT_EMAIL` and `ACCOUNT_PASSWORD` variables

You can always set these again whenever the account gets suspended.

5. The program locally saves all images and their prompts. Set `IMAGES_FOLDER` to the folder where you want these saved. **This must be set to a valid folder, or posting will not work**.
6. Next, customize the `CHARACTER` however you want. Keep in mind that
    - The location name must be a real place
    - All parameters in string form are sent as is to ChatGPT and the SD model - i.e. you can set it to whatever you want, as long as it makes logical sense
    - Values with a decimal are 0.0 - 1.0
#
## Usage
1. Run `webui-user.bat`. Wait until you see `Running on local URL: http://127.0.0.1:7860`.
2. In a new command prompt window, navigate to this repo and run `python main.py`

Now, you should see the scheduler create two events. Upon reaching the time specified, an Instagram window will be opened and the "person" will either make a post or react to some posts. **Do not close the command prompt** or it will not work. 

3. Alternatively, if you want to see the posting or reacting immediatley, you can instead run `test_post.py` or `test_responses.py` instead.

![post](/demo_images/demo1.png)