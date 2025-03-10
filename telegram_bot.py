import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

DESTINO = "/mnt/nextcloud/ander_arriola1/files/multimedia/musica"
NEXTCLOUD_SCAN_CMD = ["docker", "exec", "-u", "www-data", "nextcloud", "php", "occ", "files:scan", "--path=ander_arriola1/files/multimedia/musica"]

# Función para responder al comando /start
async def start(update: Update, context):
    mensaje = (
        "🎵 *Bienvenido al Bot de Música* 🎵\n\n"
        "Puedes usar los siguientes comandos:\n"
        "  - `/download <enlace>` - Descarga la músia.\n"
        "  - `/playlist <enlace>` - Crea una playlist.\n"
        "  - `/complete <enlace>` - Descarga la música y crea una playlist.\n\n"
        "¡Disfruta tu música! 🎶"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

# Función para descargar música y moverla (sin Subsonic)
async def download(update: Update, context):
    await handle_download(update, context, run_subsonic=False)

# Función para descargar música, moverla y ejecutar Subsonic
async def complete(update: Update, context):
    await handle_download(update, context, run_subsonic=True)

# Función para crear una playlist
async def playlist(update: Update, contexto):
    enlace = contexto.args[0]
    await update.message.reply_text("🚀 Ejecutando Subsonic Helper...")
    subprocess.run(["python3", "subsonic/subsonic_helper.py", enlace], check=True)
    await update.message.reply_text("Playlist creada!")

# Función general para manejar la descarga
async def handle_download(update: Update, context, run_subsonic):
    if len(context.args) == 0:
        await update.message.reply_text("Debes proporcionar un enlace. Ejemplo:\n/download https://open.spotify.com/track/...")
        return

    enlace = context.args[0]
    await update.message.reply_text(f"🎵 Descargando: {enlace}...")

    try:
        subprocess.run(["python3", "-m", "spotdl", enlace], check=True)
        subprocess.run(["sudo", "rsync", "-av", "--remove-source-files", "musica/", DESTINO], check=True)
        subprocess.run(["sudo", "find", "musica", "-type", "d", "-empty", "-delete"], check=True)

        await update.message.reply_text("🔄 Actualizando archivos en Nextcloud...")
        subprocess.run(NEXTCLOUD_SCAN_CMD, check=True)

        if run_subsonic:
            await playlist(update, contexto)

        await update.message.reply_text("✅ Todo listo. ¡Música actualizada en Nextcloud! 🎶")

    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))
    app.add_handler(CommandHandler("complete", complete))
    app.add_handler(CommandHandler("playlist", playlist))

    print("Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()

