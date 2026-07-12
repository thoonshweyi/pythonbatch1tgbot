from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from databaseconfig import dbconnect
from dotenv import load_dotenv 
import os 
from datetime import datetime, timezone
import pymongo

load_dotenv()

# pybot22bot 

CLASS, STUDENTID, ATTCODE = range(3)  

#=> Collection name 
COLLECTION_NAME = "attendances"

#=> Ask for CLASS 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Nodejs B1","Python B2", "Reactjs B3" ,"WDF 15"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard= True,resize_keyboard=True)

    await update.message.reply_text("Please choose your class : ", reply_markup=markup)
    return CLASS 


#=> TEmp Save class and ASK for studnetid 
async def getclass(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data['class'] = update.message.text
    await update.message.reply_text("Enter your Student ID (eg., WDF0001): ")
    return STUDENTID

#=> TEmp Save studnetid and ASK for attcode 
async def getstudentid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data['studentid'] = update.message.text
    await update.message.reply_text("Enter your Attendance Code (eg., 1AB): ")
    return ATTCODE


#=> Temp Save  and insert to DB 
async def getattcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['attcode'] = update.message.text
    user = update.effective_user

    user_class = context.user_data['class']
    user_studentid = context.user_data['studentid']
    user_attcode = context.user_data['attcode']

    db = dbconnect() 
    collection = db[COLLECTION_NAME]


    data = {
        "user_id": str(user.id),
        "class": user_class,
        "studentid": user_studentid, 
        "attcode": user_attcode,
        "createdAt": datetime.now(timezone.utc)
    } 

    try:  
        collection.insert_one(data)
        await update.message.reply_text("Attendance recorded successfully.")
    except Exception as e: 
        print("Error inseting attendance: ")
        await update.message.reply_text("Failed to record attendance")
    return ConversationHandler.END 

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    #=> Connect wtih mongo
    db = dbconnect()
    collection = db[COLLECTION_NAME]

    try:

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        records = list(
            collection.find({"user_id":user_id}).sort("createdAt",pymongo.ASCENDING)  #-1
        )

        print("Record", records)
        # Record [{'_id': ObjectId('6919f272a005940d389e5635'), 'user_id': '1752806715', 'class': 'Nodejs B1', 'studentid': 'WDF9315', 'attcode': '1ab', 'createdAt': datetime.datetime(2025, 11, 16, 15, 49, 6, 488000)}]



        if records:
            message = "📋 *Your Attendance Records:*\n\n"
            for record in records:
                created = record.get("createdAt")
                date_str = created.strftime("%Y-%m-%d %H:%M:%S") if created else "N/A"
                message += (
                    f"🏫 *Class:* {record.get('class')}\n"
                    f"🧑‍🎓 *Student ID:* {record.get('studentid')}\n"
                    f"🔢 *Code:* {record.get('attcode')}\n"
                    f"🕒 *Date:* {date_str}\n\n"
                )
        else:
            message = "No attendance records found!"

        # Send final text
        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("⚠️ Failed to fetch attendance records.")

    return ConversationHandler.END



#=> Cancle command "/cancel"
async def cancel(update: Update,context: ContextTypes.DEFAULT_TYPE) -> int: 
    await update.message.reply_text("Registration cancelled!")
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CLASS:[MessageHandler(filters.TEXT & ~filters.COMMAND,getclass)], 
            STUDENTID:[MessageHandler(filters.TEXT & ~filters.COMMAND,getstudentid)],       
            ATTCODE:[MessageHandler(filters.TEXT & ~filters.COMMAND,getattcode)],       
        },
        fallbacks=[CommandHandler('cancel',cancel)]
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('report',report))
    print("Bot is running..")
    app.run_polling()


if __name__ == "__main__":
    main()


