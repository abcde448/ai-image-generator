# 🎨 AI Image Generator

A web application that generates stunning images from text prompts using Stable Diffusion — powered by Python and Streamlit. No design skills needed. Just type, click, and see your idea come to life.

---

## ✨ Features

- 🖊️ Enter any text prompt to generate a unique image
- ⚡ Real-time image generation with a loading spinner
- 🖼️ Generated image displayed directly in the browser UI
- 💾 Image automatically saved as `output.png`
- 🚫 No API key required (runs fully locally with Stable Diffusion)
- 🛡️ Error handling for smooth user experience

---

## 🛠️ Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Language   | Python 3.9+                          |
| UI         | Streamlit                            |
| AI Model   | Stable Diffusion v1.5 (Hugging Face) |
| Libraries  | diffusers, transformers, torch, PIL  |
| Env Mgmt   | python-dotenv                        |

---

## 📁 Project Structure

```
ai-image-generator/
├── app.py                        # Streamlit web app (main entry point)
├── stable_diffusion_generate.py  # CLI image generation script
├── generate_and_display.py       # OpenAI-based generation script
├── show_image.py                 # Display helper script
├── ai_image_generator/
│   ├── config.py                 # Central configuration
│   ├── client.py                 # API client setup
│   ├── generator.py              # Image generation logic
│   ├── saver.py                  # Image saving logic
│   └── logger.py                 # Shared logger
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
└── output.png                    # Generated image (auto-created)
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/ai-image-generator.git
cd ai-image-generator
```

**2. Install dependencies**
```bash
pip3 install streamlit diffusers transformers accelerate torch pillow python-dotenv
```

---

## 🔐 Environment Variables

If using the OpenAI-based scripts, create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Open `.env` and add your key:

```
OPENAI_API_KEY=your_api_key_here
```

> ⚠️ Never commit your real API key to GitHub. The `.env` file is gitignored by default.

The Streamlit app (`app.py`) uses Stable Diffusion locally and **does not require any API key**.

---

## 🚀 How to Run

**Streamlit Web App (recommended)**
```bash
python3 -m streamlit run app.py
```
Opens automatically at `http://localhost:8501`

**CLI Script (Stable Diffusion, no API key)**
```bash
python3 stable_diffusion_generate.py
```

**CLI Script (OpenAI API)**
```bash
python3 show_image.py
```

> 📦 First run downloads the Stable Diffusion model (~4GB). Subsequent runs use the local cache.

---

## 💡 Example Prompts

```
A cute young Bengali girl wearing a saree, with round glasses, reading a book
in a cozy room with warm lighting, highly detailed, cinematic, realistic.
```

```
A futuristic city skyline at night with neon lights reflecting on wet streets, 4K.
```

```
A peaceful mountain landscape at sunrise, oil painting style, highly detailed.
```

---

## 🔮 Future Improvements

- [ ] Add image size and quality controls in the UI
- [ ] Support multiple image generation at once
- [ ] Add style presets (anime, realistic, oil painting, etc.)
- [ ] Image history gallery to browse past generations
- [ ] Download button for generated images
- [ ] Deploy to Hugging Face Spaces or Streamlit Cloud
- [ ] Add negative prompt input field

---

## 👨‍💻 Author

**Arafat Rabbi**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Md Rabbi Hasan](https://www.linkedin.com/in/md-rabbi-hasan-3249652b1)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with ❤️ using Python, Streamlit, and Stable Diffusion.
