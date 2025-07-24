
import gradio as gr
import torch
from PIL import Image
from transformers import pipeline
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

# Load models
depth_estimator = pipeline("depth-estimation")
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-depth", torch_dtype=torch.float16)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16,
)
try:
    pipe.enable_xformers_memory_efficient_attention()
except:
    pass

pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# Prompt Generator
def generate_prompt(style, budget, room_type, furniture, color_theme, lighting):
    budget_desc = {
        "low": "affordable furniture and basic decor",
        "medium": "stylish furniture with cozy elements",
        "high": "luxurious furniture with elegant decor"
    }
    return f"A {style} {room_type} with {furniture}, {budget_desc[budget]}, a {color_theme} color palette, and {lighting} lighting"

# Design Function
def generate_custom_design(input_image, style, budget, room_type, furniture, color_theme, lighting):
    input_image = input_image.resize((512, 512))
    depth = depth_estimator(input_image)["depth"].resize((512, 512))

    prompt = generate_prompt(style, budget, room_type, furniture, color_theme, lighting)

    # Generate design images
    results = pipe(prompt, image=depth, num_inference_steps=30, guidance_scale=7.5, num_images_per_prompt=3)

    # Estimate cost based on budget and room type
    cost = estimate_cost(budget, room_type)

    return results.images, cost

# Cost Estimation Function
def estimate_cost(budget, room_type):
    base_cost = {
        "living room": 1000,
        "bedroom": 800,
        "kitchen": 1200,
        "office": 900
    }

    budget_multiplier = {
        "low": 1.0,
        "medium": 1.5,
        "high": 2.0
    }

    # Calculate estimated cost
    estimated_cost = base_cost[room_type] * budget_multiplier[budget]
    return f"${estimated_cost:.2f}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🛋 Customizable AI Interior Designer")
    gr.Markdown("Upload an image of an empty room and fully customize your interior style!")

    with gr.Row():
        input_image = gr.Image(type="pil", label="Upload Room Image")

        with gr.Column():
            style = gr.Dropdown(["modern", "vintage", "bohemian", "minimalist"], label="Style", value="modern")
            budget = gr.Dropdown(["low", "medium", "high"], label="Budget", value="medium")
            room_type = gr.Dropdown(["living room", "bedroom", "kitchen", "office"], label="Room Type", value="living room")
            furniture = gr.Textbox(label="Furniture (e.g., sofa, table, plants)")
            color_theme = gr.Dropdown(["neutral", "warm", "cool", "pastel", "monochrome"], label="Color Theme", value="neutral")
            lighting = gr.Dropdown(["natural", "warm artificial", "cool artificial"], label="Lighting", value="natural")
            generate_btn = gr.Button("Generate Design")

    output_images = gr.Gallery(label="Customized Designs")
    estimated_cost_output = gr.Textbox(label="Estimated Cost", interactive=False)

    generate_btn.click(
        fn=generate_custom_design,
        inputs=[input_image, style, budget, room_type, furniture, color_theme, lighting],
        outputs=[output_images, estimated_cost_output]
    )

demo.launch(debug=True)
