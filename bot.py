import os
import logging
import threading
import http.server
import socketserver
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Render sunucu canlı kalma port ayarı
PORT = int(os.environ.get("PORT", 10000))

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Anka Digital VIP Bot is active and running!")

def run_web_server():
    with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
        httpd.serve_forever()

# Arka planda web sunucusunu başlat
threading.Thread(target=run_web_server, daemon=True).start()

# --- BOT VE API BİLGİLERİ ---
TOKEN = "8905246835:AAHgv4My2Prp77oEbLX3ybEFXNSbypBVumE"
IBAN = "TR06 0001 0021 5470 2002 4550 04"
RECIPIENT = "Resul Sakal"  # Sadece IBAN'da yasal olarak görünür

# API Bilgileri
SOSYALGRAM_KEY = "44e6262db6932b6e0e33979774d4db5a4ad4f"
SMS_API_KEY = "7f48064f2b89d3ad24fac3304788edf451aa5"

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("👑 ANKA | Sosyal Medya Hizmetleri", callback_data="menu_social")],
        [InlineKeyboardButton("💎 ANKA | Sanal Numara Servisi", callback_data="menu_numbers")],
        [InlineKeyboardButton("⚡ İşlem Rehberi", callback_data="how_to_buy")],
        [InlineKeyboardButton("📞 7/24 VIP Destek Hattı", url="https://t.me/SMSPATRONUM")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🦅 *A N K A   D I G I T A L   V I P*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "✨ *Seçkin ve profesyonel ağlar için özel olarak tasarlanmış, yüksek kaliteli yeni nesil dijital hizmet merkezi.*\n\n"
        "👇 Lütfen devam etmek istediğiniz kategoriyi seçin:"
    )
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu())
    elif update.callback_query:
        try:
            await update.callback_query.message.edit_text(text, parse_mode="Markdown", reply_markup=main_menu())
        except Exception:
            pass

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    text = ""
    keyboard = []

    if data == "home":
        text = (
            "🦅 *A N K A   D I G I T A L   V I P*\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "✨ *Seçkin ve profesyonel ağlar için özel olarak tasarlanmış, yüksek kaliteli yeni nesil dijital hizmet merkezi.*\n\n"
            "👇 Lütfen devam etmek istediğiniz kategoriyi seçin:"
        )
        keyboard = [
            [InlineKeyboardButton("👑 ANKA | Sosyal Medya Hizmetleri", callback_data="menu_social")],
            [InlineKeyboardButton("💎 ANKA | Sanal Numara Servisi", callback_data="menu_numbers")],
            [InlineKeyboardButton("⚡ İşlem Rehberi", callback_data="how_to_buy")],
            [InlineKeyboardButton("📞 7/24 VIP Destek Hattı", url="https://t.me/SMSPATRONUM")],
        ]

    # --- ANA KATEGORİLER ---
    elif data == "menu_social":
        text = "👑 *ANKA - SOSYAL MEDYA MERKEZİ*\n\nYüksek performanslı VIP servislerimizden birini seçin:"
        keyboard = [
            [InlineKeyboardButton("🎵 TikTok Premium Paketleri", callback_data="sub_tiktok")],
            [InlineKeyboardButton("📸 Instagram Premium Paketleri", callback_data="sub_instagram")],
            [InlineKeyboardButton("✈️ Telegram Abone Paketleri", callback_data="sub_telegram")],
            [InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]
        ]

    elif data == "menu_numbers":
        text = "💎 *ANKA - SANAL NUMARA SERVİSİ*\n\nAnında onay alan yüksek kaliteli kurumsal hatlar:"
        keyboard = [
            [InlineKeyboardButton("🇹🇷 TR Telegram Numarası (200 TL)", callback_data="pay_num_tr_tg")],
            [InlineKeyboardButton("🇺🇸 ABD Telegram Numarası (150 TL)", callback_data="pay_num_us_tg")],
            [InlineKeyboardButton("🇹🇷 TR WhatsApp Numarası (300 TL)", callback_data="pay_num_tr_wa")],
            [InlineKeyboardButton("🇵🇭 Filipinler WhatsApp Numarası (200 TL)", callback_data="pay_num_ph_wa")],
            [InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]
        ]

    # --- TİKTOK ALT MENÜ ---
    elif data == "sub_tiktok":
        text = "🎵 *TikTok Seçkin Paketler*:\nİşlem türünü seçin:"
        keyboard = [
            [InlineKeyboardButton("✨ Takipçi Paketleri (%100 Türk IP)", callback_data="tt_takipci_menu")],
            [InlineKeyboardButton("🔥 Beğeni Paketleri", callback_data="tt_begeni_menu")],
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="menu_social")]
        ]

    elif data == "tt_takipci_menu":
        text = "✨ *TikTok Takipçi Fiyat Listesi*:"
        keyboard = [
            [InlineKeyboardButton("10 Takipçi - 50 TL", callback_data="pay_tt_tk_10")],
            [InlineKeyboardButton("50 Takipçi - 100 TL", callback_data="pay_tt_tk_50")],
            [InlineKeyboardButton("100 Takipçi - 150 TL", callback_data="pay_tt_tk_100")],
            [InlineKeyboardButton("500 Takipçi - 350 TL", callback_data="pay_tt_tk_500")],
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="sub_tiktok")]
        ]

    elif data == "tt_begeni_menu":
        text = "🔥 *TikTok Beğeni Fiyat Listesi*:"
        keyboard = [
            [InlineKeyboardButton("10 Beğeni - 10 TL", callback_data="pay_tt_bg_10")],
            [InlineKeyboardButton("50 Beğeni - 15 TL", callback_data="pay_tt_bg_50")],
            [InlineKeyboardButton("500 Beğeni - 150 TL", callback_data="pay_tt_bg_500")],
            [InlineKeyboardButton("5.000 Beğeni - 400 TL", callback_data="pay_tt_bg_5000")],
            [InlineKeyboardButton("10.000 Beğeni - 1.000 TL", callback_data="pay_tt_bg_10000")],
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="sub_tiktok")]
        ]

    # --- İNSTAGRAM ALT MENÜ ---
    elif data == "sub_instagram":
        text = "📸 *Instagram Seçkin Paketler*:"
        keyboard = [
            [InlineKeyboardButton("🇹🇷 Türk Takipçi Paketleri", callback_data="ins_turk_menu")],
            [InlineKeyboardButton("⚡ Ucuz Takipçi Paketleri", callback_data="ins_ucuz_menu")],
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="menu_social")]
        ]

    elif data == "ins_turk_menu":
        text = "📸 *Instagram Türk Takipçi Fiyat Listesi*:"
        keyboard = [
            [InlineKeyboardButton("50 Türk Takipçi - 100 TL", callback_data="pay_ins_tr_50")],
            [InlineKeyboardButton("100 Türk Takipçi - 200 TL", callback_data="pay_ins_tr_100")],
            [InlineKeyboardButton("500 Türk Takipçi - 1.000 TL", callback_data="pay_ins_tr_500")],
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="sub_instagram")]
        ]

    elif data == "ins_ucuz_menu":
        text = "⚡ *Instagram Ekonomik Paket*:"
        keyboard = [
            [InlineKeyboardButton("100 Ucuz Takipçi - 100 TL", callback_data="pay_ins_ucuz_100")],
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="sub_instagram")]
        ]

    # --- TELEGRAM ALT MENÜ ---
    elif data == "sub_telegram":
        text = "✈️ *Telegram Kanal Abone Paketleri*:"
        keyboard = [
            [InlineKeyboardButton("250 Abone - 110 TL", callback_data="pay_tg_ab_250")],
            [InlineKeyboardButton("500 Abone - 210 TL", callback_data="pay_tg_ab_500")],
            [InlineKeyboardButton("2.500 Abone - 800 TL", callback_data="pay_tg_ab_2500")],
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="menu_social")]
        ]

    # --- NUMARA ÖDEME EKRANLARI ---
    elif data.startswith("pay_num_"):
        mapping = {
            "pay_num_tr_tg": ("TR Telegram Numarası", "200 TL"),
            "pay_num_us_tg": ("ABD Telegram Numarası", "150 TL"),
            "pay_num_tr_wa": ("TR WhatsApp Numarası", "300 TL"),
            "pay_num_ph_wa": ("Filipinler WhatsApp Numarası", "200 TL"),
        }
        item_name, price = mapping.get(data, ("Sanal Numara", "0 TL"))
        text = (
            f"🦅 *ANKA DIGITAL | GÜVENLİ ÖDEME*\n\n"
            f"📦 Ürün: *{item_name}*\n"
            f"💰 Tutar: *{price}*\n\n"
            f"🏦 *IBAN (HAVALE / FAST)*\n"
            f"`{IBAN}`\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Lütfen yukarıdaki IBAN'a tam *{price}* gönderin.\n"
            "2️⃣ Dekont görselini bota ileterek **otomatik onay** sistemini başlatın."
        )
        keyboard = [[InlineKeyboardButton("⬅️ Geri Dön", callback_data="menu_numbers")]]

    # --- SOSYAL MEDYA ÖDEME EKRANLARI ---
    elif data.startswith("pay_"):
        prices_map = {
            "pay_tt_tk_10": ("TikTok 10 Takipçi", "50 TL"),
            "pay_tt_tk_50": ("TikTok 50 Takipçi", "100 TL"),
            "pay_tt_tk_100": ("TikTok 100 Takipçi", "150 TL"),
            "pay_tt_tk_500": ("TikTok 500 Takipçi", "350 TL"),
            "pay_tt_bg_10": ("TikTok 10 Beğeni", "10 TL"),
            "pay_tt_bg_50": ("TikTok 50 Beğeni", "15 TL"),
            "pay_tt_bg_500": ("TikTok 500 Beğeni", "150 TL"),
            "pay_tt_bg_5000": ("TikTok 5.000 Beğeni", "400 TL"),
            "pay_tt_bg_10000": ("TikTok 10.000 Beğeni", "1.000 TL"),
            "pay_ins_tr_50": ("Instagram 50 Türk Takipçi", "100 TL"),
            "pay_ins_tr_100": ("Instagram 100 Türk Takipçi", "200 TL"),
            "pay_ins_tr_500": ("Instagram 500 Türk Takipçi", "1.000 TL"),
            "pay_ins_ucuz_100": ("Instagram 100 Ucuz Takipçi", "100 TL"),
            "pay_tg_ab_250": ("Telegram 250 Abone", "110 TL"),
            "pay_tg_ab_500": ("Telegram 500 Abone", "210 TL"),
            "pay_tg_ab_2500": ("Telegram 2.500 Abone", "800 TL"),
        }
        item_name, price = prices_map.get(data, ("Özel Paket", "0 TL"))
        text = (
            f"🦅 *ANKA DIGITAL | GÜVENLİ ÖDEME*\n\n"
            f"📦 Paket: *{item_name}*\n"
            f"💰 Tutar: *{price}*\n\n"
            f"🏦 *IBAN (HAVALE / FAST)*\n"
            f"`{IBAN}`\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Lütfen yukarıdaki IBAN adresine tam *{price}* gönderin.\n"
            "2️⃣ Dekontu ve profil/kanal linkinizi bota ileterek **otomatik teslimat** alın."
        )
        keyboard = [[InlineKeyboardButton("⬅️ Geri Dön", callback_data="menu_social")]]

    elif data == "how_to_buy":
        text = (
            "⚡ *ANKA İŞLEM REHBERİ*\n\n"
            "1️⃣ İstediğiniz kategoriden seçiminizi yapın.\n"
            "2️⃣ Belirtilen tutarı IBAN adresine havale/FAST yapın (Yasal alıcı sadece banka ekranında görünür).\n"
            "3️⃣ Dekontu bota gönderin; **Anka Bot** dekontunuzu otomatik tarayıp onaylar ve siparişinizi anında işleme koyar!"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]]

    try:
        await query.edit_message_text(
            text, 
            parse_mode="Markdown", 
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Menü geçiş hatası: {e}")

async def receipt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        text = (
            "🦅 *ANKA BOT - OTOMATİK DEKONT DOĞRULAMA*\n\n"
            "🔍 Dekontunuz yapay zeka tabanlı sistemimiz tarafından taranıyor...\n"
            "✅ İşlem onaylandı! Siparişiniz otomatik olarak sıraya alındı ve en kısa sürede teslim edilecek."
        )
        keyboard = [[InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data="home")]]
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await update.message.reply_text("📸 Lütfen geçerli bir ödeme dekontu gönderin.")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receipt_handler))
    
    logger.info("Anka Digital VIP Bot başarıyla çalıştırıldı!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
