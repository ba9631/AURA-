# AURA-Adaptive User-guided Rendering Architecture For Robust Interior Design 
---
## 🚀 Features

- Upload an image of your room (preferably empty)
- Choose your preferred:
  - Interior style (e.g., Modern, Vintage, Bohemian, Minimalist)
  - Budget range (Low / Medium / High)
  - Room type (Living Room, Bedroom, Kitchen, Office)
  - Furniture elements (Text input)
  - Color palette (Neutral, Warm, Cool, Pastel, Monochrome)
  - Lighting (Natural / Artificial)
- Generate multiple design outputs using **Stable Diffusion ControlNet**
- Get an estimated cost based on budget and room type
---
  ## 🧠 How It Works

1. **Depth Estimation**: A depth map is generated from the input image using Hugging Face's `depth-estimation` pipeline.
2. **Prompt Generation**: A descriptive prompt is created based on user inputs.
3. **Image Generation**: The prompt and depth map are passed to a pre-trained `StableDiffusionControlNetPipeline`.
4. **Cost Estimation**: A simple logic estimates cost using budget and room type.
5. **UI/UX**: Built with Gradio for easy interaction.

---
