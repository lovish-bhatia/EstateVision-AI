# Realty Assistant — AI Property Video Generator

A Streamlit prototype that turns property details and 4–8 uploaded property photos into a promotional MP4 video.

## Features
- Premium real-estate studio interface
- Property details form
- Template-based promotional script generation using only supplied facts
- Upload 4–8 JPG/PNG/WEBP property photos
- HD 16:9 MP4 with title, photo-caption scenes and enquiry ending
- In-browser preview and MP4 download
- Helpful validation for missing details/photos

## Requirements
- Python 3.10 or 3.11 recommended
- VS Code
- Internet connection for initial package installation

## Setup (Windows / VS Code)
1. Extract the ZIP folder.
2. Open the extracted `realty_assistant_project` folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

   ```bash
   py -m venv .venv
   ```

5. Activate it:

   ```bash
   .venv\Scripts\activate
   ```

6. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. Run the website:

   ```bash
   streamlit run app.py
   ```

8. Browser opens at `http://localhost:8501`.

## How to test
- Enter a property name, location, type, price and features.
- Click **Generate property script**.
- Upload at least 4 real property photos (JPG/PNG/WEBP).
- Click **Generate MP4 video**.
- Preview the video and download `realty_property_promo.mp4`.

## Sample property data
- Name: The Grand Residences
- Location: Sector 78, Mohali
- Type: Apartment
- Configuration: 3 BHK
- Price: ₹85 Lakh onwards
- Area: 1,450 sq. ft.
- Features: Spacious living room, modular kitchen, 3 bedrooms, balcony, covered parking
- CTA: Call now to schedule your site visit

## AI / model / API note
This prototype uses transparent, template-based script generation rather than an external generative-AI API. It uses only facts entered by the user and does not invent amenities, distances, approvals or property claims. This keeps the prototype usable without API keys and makes the generated copy easy to verify.

## Libraries used
- Streamlit — web interface
- Pillow — image processing and text overlays
- MoviePy — MP4 video composition
- NumPy — frame conversion
- ImageIO-FFmpeg — video encoding support

## Limitations
- No live property database or listing verification.
- No AI voice-over or background music in this prototype.
- Video uses a fixed template and hard cuts between scenes.
- User must provide rights-cleared property images.
- This is an assignment prototype, not a production listing platform.

## Demo checklist
- Show the form and enter sample property details.
- Generate the promotional script.
- Upload 4–8 property photos.
- Generate and preview the MP4.
- Download the MP4 and show the README / source code.
