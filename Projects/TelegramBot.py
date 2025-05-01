import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler


BOT_TOKEN = '7769716517:AAHidJOLJQQYF5f3n6rZH6SUUsVrVenulh0'

# Configurações básicas de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Simulação de fontes de dados
def get_latest_news():
    return [
        "📰 FURIA vence a Team Liquid por 2-0!",
        "📢 Rumores indicam nova contratação para o time!",
        "🔥 Pro League começa semana que vem. FURIA na estreia!"
    ]

def get_upcoming_matches():
    return [
        "🗓️ FURIA vs G2 - 30/04 às 17:00",
        "🗓️ FURIA vs Vitality - 02/05 às 20:00"
    ]

def get_player_stats():
    return {
        "KSCERATO": "Rating 1.18, KD +120",
        "yuurih": "Rating 1.15, KD +95",
        "FalleN": "Rating 1.10, KD +60",
    }

# Comandos
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🔥 Bem-vindo ao Chat Oficial dos Fãs da FURIA CS:GO! 🔥\n"
        "Use os comandos para se atualizar:\n\n"
        "/news - Últimas notícias\n"
        "/matches - Próximos jogos\n"
        "/stats - Estatísticas dos jogadores\n"
        "/vote - Vote no MVP!"
    )

async def news(update: Update, context: CallbackContext):
    noticias = get_latest_news()
    response = "\n\n".join(noticias)
    await update.message.reply_text(f"📰 Últimas Notícias:\n\n{response}")

async def matches(update: Update, context: CallbackContext):
    jogos = get_upcoming_matches()
    response = "\n\n".join(jogos)
    await update.message.reply_text(f"📅 Próximos Jogos:\n\n{response}")

async def stats(update: Update, context: CallbackContext):
    stats = get_player_stats()
    response = "\n\n".join(f"{player}: {info}" for player, info in stats.items())
    await update.message.reply_text(f"📊 Estatísticas dos Jogadores:\n\n{response}")

async def vote(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("KSCERATO", callback_data='vote_KSCERATO')],
        [InlineKeyboardButton("yuurih", callback_data='vote_yuurih')],
        [InlineKeyboardButton("FalleN", callback_data='vote_FalleN')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('🏆 Quem foi o MVP do último jogo?', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    escolha = query.data.replace('vote_', '')
    await query.edit_message_text(text=f"✅ Obrigado por votar no {escolha}!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Registrando os comandos
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('news', news))
    app.add_handler(CommandHandler('matches', matches))
    app.add_handler(CommandHandler('stats', stats))
    app.add_handler(CommandHandler('vote', vote))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot rodando...")
    app.run_polling()

if __name__ == '__main__':
    main()