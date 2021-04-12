import logging
from filemanagement import *
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

editingIDs = []
positions = []
stringsToRemember = []

from key import token

catBot = telegram.Bot(token)

def echo(update, context):
    id = update.message.chat_id
    print("Cообщение: '{}' от {}, время: {}".format(update.message.text, id, update.message.date))

    isEditing = id in editingIDs
    position = 0
    strings = []

    
    if isEditing:
        index = editingIDs.index(id)
        position = positions[index]
        strings = stringsToRemember[index]

    def keyboardGen():
        buttons = [["Добавить мем 😎"]]
        isAdmin = "{}\n".format(id) in getAdminList()

        if isAdmin:
            buttons.append(["Прекратить отслеживание 🥵"])
        else:
            buttons.append(["Отслеживать добавленные мемы 📨"])

        keyboard = ReplyKeyboardMarkup(buttons)
        if isEditing:
            keyboard = ReplyKeyboardMarkup([["Отмена"]])
        return keyboard      

    if (isEditing == False and update.message.photo):
        update.message.reply_text("Если вы хотите добавить картинку, нажмите на кнопку 'Добавить мем 😎'", reply_markup = keyboardGen())
        return

    if (update.message.text == "/start"):
        message = "Добро пожаловать! 😇\nЭтот бот создан для поиска мемов среди мемов про котов (по ржать). Мемы в него добавляют сами пользователи, вы тоже можете это сделать. 🤓\nДля того чтобы найти мем - напиши ключевое слово, чтобы добавить картинку - нажми на кнопку 'Добавить мем 😎'"
        update.message.reply_text(message, reply_markup = keyboardGen())
    elif (update.message.text == "Добавить мем 😎"):
        editingIDs.append(id)
        positions.append(1)
        position = 1
        stringsToRemember.append([])
        isEditing = True
        update.message.reply_text("Отправьте, пожалуйста картинку, которую вы хотите добавить", reply_markup = keyboardGen())
    elif (update.message.text == "Отмена"):
        if isEditing:
            index = editingIDs.index(id)
            del positions[index]
            del stringsToRemember[index]
            del editingIDs[index]
            isEditing = False
        update.message.reply_text("Отменено 😳", reply_markup = keyboardGen())
    elif (update.message.text == "Отслеживать добавленные мемы 📨"):
        isAdmin = "{}\n".format(id) in getAdminList()
        if isAdmin == False:
            addAdmin(id)
            update.message.reply_text("Теперь когда в базу данных будет добавлен новый мем, вам придет уведомление. На самом деле, я это добавил для себя, чтобы хоть как-то модерировать поток картинок, но если вам интересно - тоже смотрите 😉", reply_markup = keyboardGen())
    elif (update.message.text == "Прекратить отслеживание 🥵"):
        isAdmin = "{}\n".format(id) in getAdminList()
        if (isAdmin):
            deleteAdmin(id)
        update.message.reply_text("Хорошо, теперь вам больше не будут приходить уведомления о новых картинках в базе", reply_markup = keyboardGen())
    
    elif (position == 1):
        if (update.message.photo):
            fileID = update.message.photo[-1].file_id
            strings.append(fileID)
            message = "Фотография принята. Теперь напишите теги, по котормы можно будет найти фотографию (например, 'курс денег упал, деньги, перспектива') 🤓"
            update.message.reply_text(message, reply_markup = keyboardGen())
            position = 2
        else:
            update.message.reply_text("Я просил вас отправить фотографию, а не текст 🙄\nОтправьте, пожалуйста, фотографию")

    elif (position == 2):
        input = update.message.text
        input = input.replace(";",",")
        input = input.replace(".", " ")
        addStringLine(id, update.message.text, strings[0])
        admins = getAdminList()
        for i in range(0, len(admins)):
            textMessage = "{}: добавлена новая картинка по тегам: {}".format(id,update.message.text)
            catBot.send_message(chat_id = int(admins[i]), text = textMessage)
            catBot.send_photo(chat_id = int(admins[i]), photo = strings[0])
        
        isEditing = False
        del positions[index]
        del stringsToRemember[index]
        del editingIDs[index]
        update.message.reply_text("Сохранено 😌", reply_markup = keyboardGen())


    else:
        photos = getPhotoIDs(update.message.text)
        if (len(photos) == 0):
            update.message.reply_text("В базе бота ничего не найдено. Вы потом можете добавить найденную картинку в базу бота, нажав на кнопку 'Добавить мем 😎'", reply_markup = keyboardGen())
            return
        if (len(photos) == 1):
            textMessage = "Найдена одна картинка:"
            update.message.reply_text(textMessage, reply_markup = keyboardGen())
            update.message.reply_photo(photos[0])
            return

        textMessage = "Найденные картинки:"
        update.message.reply_text(textMessage, reply_markup = keyboardGen())
        mediagroup = []
        for i in range(0, len(photos)):
            mediagroup.append(photos[i])
            if (len(mediagroup) == 10):
                update.message.reply_media_group([InputMediaPhoto(ph) for ph in mediagroup])
                mediagroup = []
        if (len(mediagroup) == 1):
            update.message.reply_photo(mediagroup[0])
        elif (len(mediagroup) > 1):
            update.message.reply_media_group([InputMediaPhoto(ph) for ph in mediagroup]) 
    
    if (isEditing):
        index = editingIDs.index(id)
        positions[index] = position
        stringsToRemember[index] = strings

def error (update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("Произошла ошибка, сообщите об этом разработчику (контакт есть в информации о боте)")

def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text | Filters.photo, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

main()