from main import *
check_sd_server()
set_options(
    {
        "sd_model_checkpoint": 'realisticVisionV20_v20NoVAE.safetensors',
        'sd_vae': 'vae-ft-mse-840000-ema-pruned.safetensors'
    }
)
make_post(CHARACTER)