import streamlit as st
from PIL import (
    Image,
    ImageOps,
    ImageFilter,
    ImageEnhance
)

import segno
import io
import base64

st.set_page_config(
    page_title="Advanced Image Studio + Universal QR Engine",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Advanced Image Studio & 🔮 Universal QR Engine")

# -------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------

mode = st.sidebar.radio(
    "Workspace",
    [
        "🎨 Advanced Image Studio",
        "🔮 Universal QR Engine"
    ]
)

st.sidebar.markdown("---")

dark_color = st.sidebar.color_picker(
    "QR Line Color",
    "#000000"
)

light_color = st.sidebar.color_picker(
    "QR Background",
    "#FFFFFF"
)

# =======================================================
# IMAGE STUDIO
# =======================================================

if mode == "🎨 Advanced Image Studio":

    st.header("🎨 Advanced Image Studio")

    uploaded = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded:

        try:

            original = Image.open(uploaded).convert("RGB")

            st.markdown("## Filter Controls")

            filter_choice = st.selectbox(
                "Choose Filter",
                [
                    "Original",
                    "Black & White",
                    "Sepia Tone",
                    "Gaussian Blur",
                    "Contour Sketch",
                    "Vibrant Saturation",
                    "Retro Negative",
                    "Emboss Art"
                ]
            )

            st.markdown("---")
            st.markdown("## Crop")

            left = st.number_input(
                "Left",
                0,
                original.width,
                0
            )

            top = st.number_input(
                "Top",
                0,
                original.height,
                0
            )

            right = st.number_input(
                "Right",
                left + 1,
                original.width,
                original.width
            )

            bottom = st.number_input(
                "Bottom",
                top + 1,
                original.height,
                original.height
            )

            working = original.crop(
                (
                    left,
                    top,
                    right,
                    bottom
                )
            )

            st.markdown("---")
            st.markdown("## Resize")

            new_width = st.slider(
                "Width",
                50,
                2000,
                working.width
            )

            new_height = st.slider(
                "Height",
                50,
                2000,
                working.height
            )

            working = working.resize(
                (
                    new_width,
                    new_height
                )
            )

            st.markdown("---")
            st.markdown("## Compression")

            quality = st.slider(
                "JPEG Quality",
                1,
                100,
                90
            )

            try:

                if filter_choice == "Original":
                    edited = working

                elif filter_choice == "Black & White":
                    edited = ImageOps.grayscale(working).convert("RGB")

                elif filter_choice == "Sepia Tone":

                    gray = ImageOps.grayscale(working)

                    edited = ImageOps.colorize(
                        gray,
                        "#704214",
                        "#FFF5D6"
                    )

                elif filter_choice == "Gaussian Blur":
                    edited = working.filter(
                        ImageFilter.GaussianBlur(radius=3)
                    )

                elif filter_choice == "Contour Sketch":
                    edited = working.filter(
                        ImageFilter.CONTOUR
                    )

                elif filter_choice == "Vibrant Saturation":

                    enhancer = ImageEnhance.Color(working)

                    edited = enhancer.enhance(2.5)

                elif filter_choice == "Retro Negative":

                    edited = ImageOps.invert(working)

                elif filter_choice == "Emboss Art":

                    edited = working.filter(
                        ImageFilter.EMBOSS
                    )

            except Exception as e:

                st.warning(f"Filter processing failed:\n\n{e}")

                edited = working

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### Original")

                st.image(original)

            with col2:

                st.markdown("### Processed")

                st.image(edited)

            output = io.BytesIO()

            edited.save(
                output,
                format="JPEG",
                quality=quality
            )

            optimized = output.getvalue()

            original_size = len(uploaded.getvalue()) / 1024
            optimized_size = len(optimized) / 1024

            st.markdown("### Compression Metrics")

            st.write(f"Original Size: **{original_size:.2f} KB**")
            st.write(f"Optimized Size: **{optimized_size:.2f} KB**")

            reduction = original_size - optimized_size

            st.write(f"Difference: **{reduction:.2f} KB**")

            st.download_button(
                "⬇ Download Processed Image",
                optimized,
                "processed.jpg",
                "image/jpeg"
            )

        except Exception as e:

            st.error(
                f"Image pipeline failed:\n\n{e}"
            )

# =======================================================
# QR ENGINE
# =======================================================

else:

    st.header("🔮 Universal QR Engine")

    qr_mode = st.radio(
        "Select Pipeline",
        [
            "Text to QR",
            "Link to QR",
            "Image to QR"
        ]
    )

    payload = None

    if qr_mode == "Text to QR":

        payload = st.text_area(
            "Enter Text"
        )

    elif qr_mode == "Link to QR":

        payload = st.text_input(
            "Enter URL"
        )

    else:

        image_upload = st.file_uploader(
            "Upload Image",
            type=[
                "png",
                "jpg",
                "jpeg"
            ]
        )

        if image_upload:

            try:

                raw = image_upload.read()

                encoded = base64.b64encode(raw).decode()

                mime = "image/png"

                if image_upload.type:
                    mime = image_upload.type

                payload = (
                    f"data:{mime};base64,"
                    + encoded
                )

                st.success(
                    "Image successfully converted to Base64 URI."
                )

                st.text_area(
                    "Encoded Payload",
                    payload,
                    height=180
                )

            except Exception as e:

                st.warning(
                    f"Base64 encoding failed:\n\n{e}"
                )

    if payload:

        try:

            qr = segno.make(
                payload,
                error="H"
            )

            buffer = io.BytesIO()

            qr.save(
                buffer,
                kind="png",
                scale=8,
                dark=dark_color,
                light=light_color
            )

            qr_bytes = buffer.getvalue()

            st.image(qr_bytes)

            st.download_button(
                "⬇ Download QR",
                qr_bytes,
                "qr_code.png",
                "image/png"
            )

        except Exception as e:

            st.warning(
                f"QR generation failed:\n\n{e}"
            )
