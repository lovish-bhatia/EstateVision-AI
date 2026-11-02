
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips
from io import BytesIO
import tempfile, os, re, textwrap as tw

st.set_page_config(page_title="EstateVision AI | Property Studio", page_icon="🏡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#f7f8fb 0%,#eef2f8 100%);}
.block-container {padding-top:1.4rem; max-width:1250px;}
.hero {background:linear-gradient(115deg,#101c35,#203b62); padding:30px 34px; border-radius:22px; color:white; margin-bottom:22px; box-shadow:0 14px 35px #15284722;}
.hero h1 {font-family:'Playfair Display',serif; font-size:38px; margin:0 0 8px 0; color:white;}
.hero p {color:#dce6f4; font-size:15px; margin:0;}
.eyebrow {color:#e9a45b; text-transform:uppercase; letter-spacing:2px; font-weight:700; font-size:11px;}
.metric {background:white;border:1px solid #e7eaf0;border-radius:16px;padding:16px 18px;}
.metric small {color:#778196;font-weight:600;}
.metric h3 {margin:4px 0 0 0;color:#172744;}
.section {font-size:21px;font-weight:700;color:#172744;margin:10px 0 4px 0;}
.hint {color:#718096;font-size:13px;}
div.stButton>button, div.stDownloadButton>button {background:#e28b42;color:white;border:0;border-radius:10px;padding:0.65rem 1.2rem;font-weight:700;}
div.stButton>button:hover, div.stDownloadButton>button:hover {background:#c9742d;color:white;border:0;}
[data-testid="stSidebar"] {background:#111e36;}
[data-testid="stSidebar"] * {color:#f3f6fb;}
</style>
""", unsafe_allow_html=True)

if "video_bytes" not in st.session_state:
    st.session_state.video_bytes = None
if "script_text" not in st.session_state:
    st.session_state.script_text = ""

st.sidebar.markdown("## 🏡 ESTATEVISION AI")
st.sidebar.caption("PROPERTY VIDEO STUDIO")
page = st.sidebar.radio("WORKSPACE", ["Create Property Video", "How It Works"])
st.sidebar.markdown("---")
st.sidebar.caption("AI-powered content creation\n\nBuilt with Python • Streamlit • MoviePy")

st.markdown("""
<div class="hero">
  <div class="eyebrow">REAL ESTATE • CONTENT STUDIO</div>
  <h1>Turn Property Photos Into<br>Beautiful Listing Videos.</h1>
  <p>Create polished property promos in minutes — add details, upload photos, generate your story and export an MP4.</p>
</div>
""", unsafe_allow_html=True)

if page == "How It Works":
    st.markdown("## A simple workflow")
    cols = st.columns(3)
    for c, n, title, desc in zip(cols, ["01","02","03"], ["Add details","Upload photos","Generate & share"], ["Enter verified property information.","Add 4–8 real property images.","Create a video preview and download MP4."]):
        with c:
            st.markdown(f"""<div class="metric"><small>STEP {n}</small><h3>{title}</h3><p>{desc}</p></div>""", unsafe_allow_html=True)
    st.info("The generator uses template-based copywriting. It does not invent amenities, distances, approvals or other property claims.")
    st.markdown("### Output")
    st.write("A landscape 16:9 MP4 with an opening title, property photo scenes, feature captions and a final enquiry slide.")
else:
    a,b,c = st.columns(3)
    with a: st.markdown('<div class="metric"><small>FORMAT</small><h3>16:9 HD</h3></div>', unsafe_allow_html=True)
    with b: st.markdown('<div class="metric"><small>PHOTO INPUT</small><h3>4–8 images</h3></div>', unsafe_allow_html=True)
    with c: st.markdown('<div class="metric"><small>EXPORT</small><h3>MP4 video</h3></div>', unsafe_allow_html=True)

    st.markdown('<div class="section">01 · Property information</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Enter accurate details. The video will only use the information provided below.</div>', unsafe_allow_html=True)
    with st.form("property_form"):
        c1,c2 = st.columns(2)
        with c1:
            property_name = st.text_input("Property / Project name", "The Grand Residences")
            location = st.text_input("Location", "Sector 78, Mohali")
            property_type = st.selectbox("Property type", ["Apartment","Villa","Independent House","Penthouse","Studio","Commercial"])
            bhk = st.selectbox("Configuration", ["1 BHK","2 BHK","3 BHK","4 BHK","5 BHK","Not specified"])
        with c2:
            price = st.text_input("Price", "₹85 Lakh onwards")
            area = st.text_input("Area (optional)", "1,450 sq. ft.")
            features = st.text_area("Key features (comma separated)", "Spacious living room, modular kitchen, 3 bedrooms, balcony, covered parking")
            cta = st.text_input("Contact / Call-to-action", "Call now to schedule your site visit")
        submitted = st.form_submit_button("✨ Generate property script", use_container_width=True)
    if submitted:
        facts = [property_name.strip(), location.strip(), property_type, price.strip()]
        if not all(facts):
            st.error("Please fill Property name, Location, Property type and Price.")
        else:
            feature_list = [x.strip() for x in features.split(",") if x.strip()]
            intro = f"Discover {property_name}, a {property_type.lower()} located in {location}."
            details = f"Available at {price}."
            if bhk != "Not specified": details += f" This property offers a {bhk} configuration."
            if area.strip(): details += f" The listed area is {area.strip()}."
            feature_line = ("Key highlights include " + ", ".join(feature_list[:6]) + ".") if feature_list else "Explore the property and its spaces."
            closing = cta.strip() or "Contact us today for more information."
            st.session_state.script_text = " ".join([intro, details, feature_line, closing])
    if st.session_state.script_text:
        st.success("Property script generated.")
        st.text_area("Generated promotional script", st.session_state.script_text, height=110)

    st.markdown('<div class="section">02 · Upload property photos</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Upload 4–8 clear photos of the actual property: exterior, living room, kitchen, bedroom, balcony or amenities.</div>', unsafe_allow_html=True)
    uploads = st.file_uploader("Choose property images", type=["jpg","jpeg","png","webp"], accept_multiple_files=True)
    if uploads:
        st.write(f"**{len(uploads)} image(s) selected**")
        if len(uploads) > 8:
            st.warning("Only the first 8 images will be used.")
        preview_cols = st.columns(min(len(uploads),4))
        for i, f in enumerate(uploads[:8]):
            with preview_cols[i % len(preview_cols)]:
                st.image(f, caption=f.name, use_container_width=True)

    st.markdown('<div class="section">03 · Create your property video</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">The video includes a title scene, photo scenes with captions and a final enquiry prompt.</div>', unsafe_allow_html=True)

    def get_font(size, bold=False):
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
        for p in candidates:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
        return ImageFont.load_default()

    def draw_wrapped(draw, text, xy, font, fill, max_chars=34, spacing=12):
        lines = tw.wrap(text, width=max_chars)
        y = xy[1]
        for line in lines:
            draw.text((xy[0],y), line, font=font, fill=fill)
            y += font.size + spacing
        return y

    def make_slide(img, title, subtitle, is_cover=False):
        W,H = 1280,720
        canvas = Image.new("RGB",(W,H),(16,28,51))
        if img is not None:
            photo = ImageOps.fit(img.convert("RGB"),(W,H),method=Image.Resampling.LANCZOS)
            # Dark translucent overlay for readable typography
            overlay = Image.new("RGBA",(W,H),(0,0,0,0))
            od = ImageDraw.Draw(overlay)
            od.rectangle((0,450,W,H), fill=(8,17,33,190))
            if is_cover: od.rectangle((0,0,W,H), fill=(8,17,33,95))
            canvas = Image.alpha_composite(photo.convert("RGBA"),overlay).convert("RGB")
        d = ImageDraw.Draw(canvas)
        d.rounded_rectangle((55,48,310,94), radius=18, fill=(226,139,66))
        d.text((78,61),"ESTATEVISION AI",font=get_font(19,True),fill="white")
        if is_cover:
            draw_wrapped(d,title,(65,250),get_font(54,True),"white",max_chars=27,spacing=14)
            draw_wrapped(d,subtitle,(68,430),get_font(27),"#F5C28E",max_chars=55,spacing=8)
        else:
            draw_wrapped(d,title,(65,535),get_font(36,True),"white",max_chars=36,spacing=8)
            draw_wrapped(d,subtitle,(68,630),get_font(22),"#F5C28E",max_chars=65,spacing=5)
        return np.array(canvas)

    if st.button("🎬 Generate MP4 video", type="primary", use_container_width=True):
        if not st.session_state.script_text:
            st.error("First fill property details and click 'Generate property script'.")
        elif not uploads or len(uploads) < 4:
            st.error("Please upload at least 4 property images as required by the assignment.")
        else:
            try:
                with st.spinner("Creating your HD property video... Please wait."):
                    feature_list = [x.strip() for x in features.split(",") if x.strip()]
                    title = property_name.strip()
                    subtitle = f"{location}  •  {price}"
                    pil_images = []
                    for f in uploads[:8]:
                        f.seek(0)
                        pil_images.append(Image.open(BytesIO(f.read())).convert("RGB"))
                    scenes = []
                    scenes.append(make_slide(pil_images[0], title, subtitle, True))
                    for i, im in enumerate(pil_images):
                        cap = feature_list[i % len(feature_list)] if feature_list else f"Explore this {property_type.lower()}"
                        scenes.append(make_slide(im, cap, f"{bhk}  |  {location}"))
                    scenes.append(make_slide(pil_images[-1], "Interested in this property?", cta.strip() or "Contact us today for more information."))
                    clips = [ImageClip(frame).set_duration(3.2) for frame in scenes]
                    final = concatenate_videoclips(clips, method="compose")
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                        outpath = tmp.name
                    final.write_videofile(outpath, fps=24, codec="libx264", audio=False, preset="ultrafast", logger=None)
                    final.close()
                    with open(outpath,"rb") as vf:
                        st.session_state.video_bytes = vf.read()
                    os.remove(outpath)
                st.success("Your property video is ready!")
            except Exception as e:
                st.error(f"Video could not be generated: {e}")
                st.info("Try JPG/PNG images and ensure MoviePy and FFmpeg are installed. Restart the app after installing requirements.")

    if st.session_state.video_bytes:
        st.markdown("### 04 · Preview & download")
        st.video(st.session_state.video_bytes)
        st.download_button("⬇️ Download property video (MP4)", data=st.session_state.video_bytes,
                           file_name="realty_property_promo.mp4", mime="video/mp4", use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#8792a5;font-size:12px'>REALTY ASSISTANT · AI PROPERTY VIDEO STUDIO · Prototype for demonstration</div>", unsafe_allow_html=True)
