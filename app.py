import gradio as gr
import numpy as np
from PIL import Image
import cv2

def apply_effect(input_image, effect, strength):
    if input_image is None:
        return None

    img = input_image.astype(np.uint8)
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    result = img.copy()

    try:
        if effect == "🌊 Ocean Blue Filter":
            result = img.copy().astype(np.float32)
            result[:,:,0] = np.clip(result[:,:,0]*0.7, 0, 255)
            result[:,:,1] = np.clip(result[:,:,1]*0.9, 0, 255)
            result[:,:,2] = np.clip(result[:,:,2]*1.3, 0, 255)
            result = result.astype(np.uint8)

        elif effect == "🌅 Sunset Filter":
            result = img.copy().astype(np.float32)
            result[:,:,0] = np.clip(result[:,:,0]*1.4, 0, 255)
            result[:,:,1] = np.clip(result[:,:,1]*0.9, 0, 255)
            result[:,:,2] = np.clip(result[:,:,2]*0.6, 0, 255)
            result = result.astype(np.uint8)

        elif effect == "🌿 Forest Green Filter":
            result = img.copy().astype(np.float32)
            result[:,:,0] = np.clip(result[:,:,0]*0.7, 0, 255)
            result[:,:,1] = np.clip(result[:,:,1]*1.3, 0, 255)
            result[:,:,2] = np.clip(result[:,:,2]*0.7, 0, 255)
            result = result.astype(np.uint8)

        elif effect == "🖤 Black & White":
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            result = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        elif effect == "✨ Glitter Effect":
            noise = np.random.randint(
                0, int(strength*25),
                img.shape, dtype=np.uint8)
            result = cv2.add(img, noise)

        elif effect == "🔥 Emboss":
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            kernel = np.array([
                [-2,-1, 0],
                [-1, 1, 1],
                [ 0, 1, 2]])
            emboss = cv2.filter2D(gray, -1, kernel) + 128
            result = cv2.cvtColor(
                emboss.astype(np.uint8),
                cv2.COLOR_GRAY2RGB)

        elif effect == "🌈 Invert Colors":
            result = 255 - img

        elif effect == "💜 Purple Haze":
            result = img.copy().astype(np.float32)
            result[:,:,0] = np.clip(result[:,:,0]*1.2, 0, 255)
            result[:,:,1] = np.clip(result[:,:,1]*0.7, 0, 255)
            result[:,:,2] = np.clip(result[:,:,2]*1.3, 0, 255)
            result = result.astype(np.uint8)

        # Apply strength as brightness
        result = cv2.convertScaleAbs(
            result, alpha=1.0,
            beta=(strength-5)*10)

        return Image.fromarray(result.astype(np.uint8))

    except Exception as e:
        print(f"Error: {e}")
        return Image.fromarray(img)

# ── App with GREEN theme ──
with gr.Blocks(
    title="Color Filter Studio",
    css="""
    .gradio-container {
        background: linear-gradient(
            135deg, #0f2027, #203a43, #2c5364) !important;
    }
    .gr-button-primary {
        background: #00b09b !important;
        border-color: #00b09b !important;
    }
    h1 { color: #00b09b !important; }
    """
) as demo:

    gr.Markdown("""
    # 🎨 Color Filter Studio
    ### Apply beautiful color filters to your photos instantly!
    """)

    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(
                label="📸 Upload Photo",
                type="numpy"
            )
            effect = gr.Radio(
                choices=[
                    "🌊 Ocean Blue Filter",
                    "🌅 Sunset Filter",
                    "🌿 Forest Green Filter",
                    "🖤 Black & White",
                    "✨ Glitter Effect",
                    "🔥 Emboss",
                    "🌈 Invert Colors",
                    "💜 Purple Haze",
                ],
                value="🌊 Ocean Blue Filter",
                label="🎭 Choose Filter"
            )
            strength = gr.Slider(
                minimum=1,
                maximum=10,
                value=5,
                step=1,
                label="⚡ Strength"
            )
            apply_btn = gr.Button(
                "✨ Apply Filter",
                variant="primary",
                size="lg"
            )

        with gr.Column(scale=1):
            output_image = gr.Image(
                label="🖼️ Result",
                type="pil"
            )
            gr.Markdown("""
            ### 🎨 Filter Guide:
            - 🌊 **Ocean Blue** — Cool blue tones
            - 🌅 **Sunset** — Warm orange tones
            - 🌿 **Forest Green** — Natural green tones
            - 🖤 **Black & White** — Classic grayscale
            - ✨ **Glitter** — Sparkle noise effect
            - 🔥 **Emboss** — 3D raised effect
            - 🌈 **Invert** — Negative colors
            - 💜 **Purple Haze** — Dreamy purple
            """)

    apply_btn.click(
        fn=apply_effect,
        inputs=[input_image, effect, strength],
        outputs=output_image
    )

demo.launch()
