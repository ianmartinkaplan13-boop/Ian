import streamlit as st
import os
import time
import subprocess

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Cap Cut IA",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Cap Cut IA")
st.write("Creá videos con texto, imágenes, audio y voz.")

# --------------------------------------------------
# CARPETA PARA LOS VIDEOS
# --------------------------------------------------

CARPETA_VIDEOS = "videos"

if not os.path.exists(CARPETA_VIDEOS):
    os.makedirs(CARPETA_VIDEOS)

# --------------------------------------------------
# HISTORIAL DEL CHAT
# --------------------------------------------------

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant",
            "content": (
                "¡Hola! 👋 Soy Cap Cut IA. "
                "Podés escribirme qué video querés crear "
                "o usar el micrófono 🎤."
            )
        }
    ]

# Mostrar mensajes anteriores

for msg in st.session_state.mensajes:

    with st.chat_message(msg["role"]):

        if msg.get("video"):
            st.video(msg["video"])

            with open(msg["video"], "rb") as archivo:
                st.download_button(
                    "📥 Descargar video MP4",
                    data=archivo,
                    file_name="cap_cut_ia_video.mp4",
                    mime="video/mp4"
                )

        elif msg.get("imagen"):
            st.image(msg["imagen"], use_container_width=True)

        else:
            st.write(msg["content"])


# --------------------------------------------------
# MICRÓFONO
# --------------------------------------------------

st.subheader("🎤 Hablar con Cap Cut IA")

audio_grabado = st.audio_input(
    "Presioná para grabar tu pedido"
)

if audio_grabado:

    archivo_audio = "pedido_usuario.wav"

    with open(archivo_audio, "wb") as f:
        f.write(audio_grabado.getbuffer())

    st.audio(archivo_audio)

    st.success(
        "🎤 Audio recibido. Ahora podemos conectarlo "
        "con el sistema de IA para interpretar tu pedido."
    )


# --------------------------------------------------
# CHAT
# --------------------------------------------------

prompt = st.chat_input(
    "Escribí qué video querés crear..."
)


if prompt:

    # Mostrar mensaje del usuario

    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.mensajes.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # --------------------------------------------------
    # RESPUESTA
    # --------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🎬 Cap Cut IA está preparando tu video..."):

            time.sleep(2)

            # --------------------------------------------------
            # IMPORTANTE
            # --------------------------------------------------
            # Acá se conecta el verdadero generador de video IA.
            #
            # Tu código anterior NO hacía esto.
            #
            # Esta función solamente demuestra dónde irá
            # el generador real.
            # --------------------------------------------------

            video_generado = None

            # --------------------------------------------------
            # SI TODAVÍA NO TENEMOS GENERADOR IA
            # --------------------------------------------------

            if video_generado is None:

                st.info(
                    "⚠️ El chat funciona correctamente, "
                    "pero todavía falta conectar el modelo "
                    "que genera el video."
                )

                respuesta = (
                    "Entendí tu pedido: "
                    + prompt
                    + "\n\n"
                    "🎬 Para generar el MP4 real hay que conectar "
                    "el motor de generación de video IA."
                )

                st.write(respuesta)

                st.session_state.mensajes.append(
                    {
                        "role": "assistant",
                        "content": respuesta
                    }
                )

            # --------------------------------------------------
            # CUANDO EL GENERADOR DEVUELVA UN MP4
            # --------------------------------------------------

            else:

                st.success(
                    "✅ ¡Video generado por Cap Cut IA!"
                )

                # REPRODUCTOR DENTRO DEL CHAT

                st.video(
                    video_generado,
                    format="video/mp4"
                )

                # BOTÓN DE DESCARGA REAL

                with open(video_generado, "rb") as archivo:

                    st.download_button(
                        "📥 Descargar Video MP4",
                        data=archivo,
                        file_name="cap_cut_ia.mp4",
                        mime="video/mp4"
                    )

                st.session_state.mensajes.append(
                    {
                        "role": "assistant",
                        "content": "🎬 ¡Video generado!",
                        "video": video_generado
                    }
                )


# --------------------------------------------------
# INFORMACIÓN
# --------------------------------------------------

st.divider()

st.caption(
    "🎬 Cap Cut IA — Creado por Ian Kaplan"
)