# path: locales.py

LOCALES = {
    "uz": {

        # Greeting / onboarding
        "welcome": "Assalomu alaykum! Farmatsevtika botiga xush kelibsiz!",
        "hello":   "Assalomu alaykum! Farmatsevtika botiga xush kelibsiz!",
        "choose_lang": "Iltimos, tilni tanlang:",
        "need_register": "Iltimos, avval ro'yxatdan o'ting.",

        # Main menu & buttons
        "menu": "Asosiy menyu:",
        "back": "⬅️ Orqaga",
        "btn_search": "🔎 Qidiruv",
        "btn_feedback": "💬 Fikr bildirish",
        "btn_lang": "🌐 Tilni o'zgartirish",
        "btn_locations": "📍 Lokatsiyalar",

        # Register flow
        "reg_name": "Ism va familiyangizni yuboring (masalan: Ali Aliyev).",
        "reg_contact": "Telefon raqamingizni kontakt ko'rinishida yuboring yoki yozing.",
        "reg_age": "Yoshingizni kiriting (masalan: 23).",
        "reg_done": "Tabriklaymiz! Ro'yxatdan o'tdingiz.",

        # Search flow
        "search_ask": "Dori nomini yozing yoki rasm yuboring.",
        "search_none": "Kechirasiz, dori topilmadi. Boshqa nom kiriting yoki rasm yuboring.",
        "drug_info": "🧪 Dori haqida ma'lumot",
        "uses": "Qo'llanilishi",
        "side": "Yon ta'siri",
        "dose": "Dozalar",
        "price": "Narx oralig'i",
        "call": "Call center",
        "nearest": "Eng yaqin apteka",
        "send_location": "📍 Eng yaqin apteka uchun lokatsiya yuboring.",
        "alternatives": "💡 Muqobil dorilar",
        "dose_calc": "🧮 Doza kalkulyatori",
        "more_search": "➕ Yana qidirish",

        # Feedback flow
        "feedback_ask": "Fikringizni yozing:",
        "feedback_got": "Rahmat! Fikringiz qabul qilindi.",
        "complaint_ask": "Shikoyatingizni yozing (ixtiyoriy rasm/lokatsiya jo'nating).",
        "complaint_ok": "Xabaringiz yuborildi.",

        # Locations (user)
        "loc_menu_title": "Lokatsiyalar bo‘limi:",
        "loc_btn_nearest": "📍 Eng yaqin lokatsiya",
        "loc_btn_all": "📍 Hamma lokatsiyalar",
        "ask_share_loc": "Iltimos, yurayotgan joyingizni yuboring.",
        "ask_share_button": "📍 Turgan joyni yuborish",
        "no_locations": "Hozircha lokatsiyalar bazada yo‘q.",
        "loc_list_title": "Filiallar ro‘yxati:",
        "choose_or_nearest": "Quyidagi tugmalardan birini tanlang yoki eng yaqinini ko‘ring.",
        "nearest_prefix": "Eng yaqin lokatsiya:",
        "loc_sent_caption": "📍 {title}\n{address}",

        # Admin – common
        "admin": "🛠 Admin panel",
        "admin_only": "Bu bo‘lim faqat adminlar uchun.",
        "skip": "o‘tkazib yuborish",

        # Admin – locations (custom Locations bo‘limi)
        "admin_loc_add": "➕ Lokatsiya qo‘shish",
        "admin_loc_title": "Filial nomini yuboring (masalan: Chilonzor apteka).",
        "admin_loc_address": "Manzilni yozing (masalan: Chilonzor, Toshkent).",
        "admin_loc_link": "Ixtiyoriy: xarita havolasini yuboring yoki \"o‘tkazib yuborish\" deb yozing.",
        "admin_loc_ask_point": "📍 Endi lokatsiyani yuboring (\"Turgan joyni yuborish\" tugmasidan foydalaning).",
        "admin_loc_saved": "✅ Lokatsiya saqlandi.",

        # Admin – drug CRUD (promptlar)
        "adm_drug_name": "Dori nomi:",
        "adm_drug_uses": "Qo‘llanilishi:",
        "adm_drug_side": "Yon ta'siri:",
        "adm_drug_dose": "Dozasi:",
        "adm_drug_price_min": "Minimal narx (masalan 10000 yoki 10.5):",
        "adm_drug_price_max": "Maksimal narx:",
        "adm_drug_call": "Call-center (yo‘q bo‘lsa '-' yozing):",
        "adm_drug_alts": "Muqobillar (',' bilan, yo‘q bo‘lsa '-' yozing):",
        "adm_saved": "✅ Saqlandi.",
        "adm_deleted": "🗑 O‘chirildi.",
        "adm_wrong_number": "❗️ Noto‘g‘ri format. Raqam kiriting.",

        # Admin – pharmacy CRUD (promptlar)
        "adm_ph_title": "Apteka nomi (filial nomi):",
        "adm_ph_lat": "Latitude (masalan 41.285):",
        "adm_ph_lon": "Longitude:",
        "adm_ph_addr": "Manzil:",
        "adm_ph_link": "Xarita havolasi (yo‘q bo‘lsa '-' yozing):",
        "adm_ph_saved": "✅ Apteka qo‘shildi: {title} (id={id})",

        ## AI
        "btn_ai": "🤖 Sun'iy intellekt",
        "ai_intro": "🤖 Sun'iy intellekt rejimi.\nIstalgan savolingizni yozing. Yakunlash uchun pastdagi “⬅️ Orqaga” tugmasini bosing.",
        "ai_thinking": "Yozayapman…",
        "ai_ended": "Suhbat yakunlandi.",

    },

    "en": {
        # Greeting / onboarding
        "welcome": "Welcome to the Pharmaceutics bot!",
        "hello":   "Welcome to the Pharmaceutics bot!",
        "choose_lang": "Please choose a language:",
        "need_register": "Please register first.",

        # Main menu & buttons
        "menu": "Main menu:",
        "back": "⬅️ Back",
        "btn_search": "🔎 Search",
        "btn_feedback": "💬 Feedback",
        "btn_lang": "🌐 Change language",
        "btn_locations": "📍 Locations",

        # Register flow
        "reg_name": "Send your full name (e.g., John Doe).",
        "reg_contact": "Share your phone as a contact or type it.",
        "reg_age": "Enter your age (e.g., 23).",
        "reg_done": "You're registered!",

        # Search flow
        "search_ask": "Type a drug name or send a photo.",
        "search_none": "Sorry, nothing found. Try another name or photo.",
        "drug_info": "🧪 Drug information",
        "uses": "Uses",
        "side": "Side effects",
        "dose": "Dosage",
        "price": "Price range",
        "call": "Call center",
        "nearest": "Nearest pharmacy",
        "send_location": "📍 Send your location to find nearby pharmacies.",
        "alternatives": "💡 Alternatives",
        "dose_calc": "🧮 Dose calculator",
        "more_search": "➕ Search more",

        # Feedback flow
        "feedback_ask": "Write your feedback:",
        "feedback_got": "Thanks! Received.",
        "complaint_ask": "Write your complaint (you may add photo/location).",
        "complaint_ok": "Your report is sent.",

        # Locations (user)
        "loc_menu_title": "Locations menu:",
        "loc_btn_nearest": "📍 Nearest location",
        "loc_btn_all": "📍 All locations",
        "ask_share_loc": "Please share your current location.",
        "ask_share_button": "📍 Send current location",
        "no_locations": "No locations in the database yet.",
        "loc_list_title": "Branch list:",
        "choose_or_nearest": "Choose one below or view the nearest.",
        "nearest_prefix": "Nearest location:",
        "loc_sent_caption": "📍 {title}\n{address}",

        # Admin – common
        "admin": "🛠 Admin panel",
        "admin_only": "This section is for admins only.",
        "skip": "skip",

        # Admin – locations
        "admin_loc_add": "➕ Add location",
        "admin_loc_title": "Send the branch title (e.g., Chilonzor pharmacy).",
        "admin_loc_address": "Send the address.",
        "admin_loc_link": "Optional: send map URL or type \"skip\".",
        "admin_loc_ask_point": "📍 Now send the location (use the \"Send current location\" button).",
        "admin_loc_saved": "✅ Location saved.",

        # Admin – drug CRUD
        "adm_drug_name": "Drug name:",
        "adm_drug_uses": "Uses:",
        "adm_drug_side": "Side effects:",
        "adm_drug_dose": "Dosage:",
        "adm_drug_price_min": "Min price (e.g., 10000 or 10.5):",
        "adm_drug_price_max": "Max price:",
        "adm_drug_call": "Call-center (type '-' if none):",
        "adm_drug_alts": "Alternatives (comma-separated, '-' if none):",
        "adm_saved": "✅ Saved.",
        "adm_deleted": "🗑 Deleted.",
        "adm_wrong_number": "❗️ Invalid format. Please enter a number.",

        # Admin – pharmacy CRUD
        "adm_ph_title": "Pharmacy (branch) title:",
        "adm_ph_lat": "Latitude (e.g., 41.285):",
        "adm_ph_lon": "Longitude:",
        "adm_ph_addr": "Address:",
        "adm_ph_link": "Map URL (type '-' if none):",
        "adm_ph_saved": "✅ Pharmacy added: {title} (id={id})",

        ##ai
        "btn_ai": "🤖 AI Assistant",
        "ai_intro": "🤖 AI mode.\nAsk me anything. Tap “⬅️ Back” to finish.",
        "ai_thinking": "Thinking…",
        "ai_ended": "Chat ended.",

    },

    "ru": {
        # Greeting / onboarding
        "welcome": "Добро пожаловать в фарма-бота!",
        "hello":   "Добро пожаловать в фарма-бота!",
        "choose_lang": "Пожалуйста, выберите язык:",
        "need_register": "Пожалуйста, сначала зарегистрируйтесь.",

        # Main menu & buttons
        "menu": "Главное меню:",
        "back": "⬅️ Назад",
        "btn_search": "🔎 Поиск",
        "btn_feedback": "💬 Отзыв",
        "btn_lang": "🌐 Сменить язык",
        "btn_locations": "📍 Локации",

        # Register flow
        "reg_name": "Отправьте ФИО (например: Иван Иванов).",
        "reg_contact": "Отправьте телефон контактом или введите его.",
        "reg_age": "Введите ваш возраст (например: 23).",
        "reg_done": "Вы зарегистрированы!",

        # Search flow
        "search_ask": "Введите название лекарства или отправьте фото.",
        "search_none": "К сожалению, ничего не найдено. Попробуйте другое название/фото.",
        "drug_info": "🧪 Информация о препарате",
        "uses": "Показания",
        "side": "Побочные эффекты",
        "dose": "Дозировки",
        "price": "Диапазон цен",
        "call": "Колл-центр",
        "nearest": "Ближайшая аптека",
        "send_location": "📍 Отправьте локацию для поиска ближайших аптек.",
        "alternatives": "💡 Аналоги",
        "dose_calc": "🧮 Калькулятор доз",
        "more_search": "➕ Ещё поиск",

        # Feedback flow
        "feedback_ask": "Напишите отзыв:",
        "feedback_got": "Спасибо! Получено.",
        "complaint_ask": "Опишите жалобу (можно приложить фото/локацию).",
        "complaint_ok": "Отправлено.",

        # Locations (user)
        "loc_menu_title": "Меню локаций:",
        "loc_btn_nearest": "📍 Ближайшая локация",
        "loc_btn_all": "📍 Все локации",
        "ask_share_loc": "Пожалуйста, отправьте вашу текущую геолокацию.",
        "ask_share_button": "📍 Отправить текущую локацию",
        "no_locations": "Локации в базе пока отсутствуют.",
        "loc_list_title": "Список филиалов:",
        "choose_or_nearest": "Выберите один из вариантов ниже или посмотрите ближайший.",
        "nearest_prefix": "Ближайшая локация:",
        "loc_sent_caption": "📍 {title}\n{address}",

        # Admin – common
        "admin": "🛠 Админ-панель",
        "admin_only": "Этот раздел только для администраторов.",
        "skip": "пропустить",

        # Admin – locations
        "admin_loc_add": "➕ Добавить локацию",
        "admin_loc_title": "Отправьте название филиала (например: Чиланзар аптека).",
        "admin_loc_address": "Отправьте адрес.",
        "admin_loc_link": "Необязательно: пришлите ссылку на карту или напишите «пропустить».",
        "admin_loc_ask_point": "📍 Теперь отправьте геолокацию (кнопка «Отправить текущую локацию»).",
        "admin_loc_saved": "✅ Локация сохранена.",

        # Admin – drug CRUD
        "adm_drug_name": "Название препарата:",
        "adm_drug_uses": "Показания:",
        "adm_drug_side": "Побочные эффекты:",
        "adm_drug_dose": "Дозировка:",
        "adm_drug_price_min": "Мин. цена (напр., 10000 или 10.5):",
        "adm_drug_price_max": "Макс. цена:",
        "adm_drug_call": "Колл-центр (если нет — «-»):",
        "adm_drug_alts": "Аналоги (через запятую, «-» если нет):",
        "adm_saved": "✅ Сохранено.",
        "adm_deleted": "🗑 Удалено.",
        "adm_wrong_number": "❗️ Неверный формат. Введите число.",

        # Admin – pharmacy CRUD
        "adm_ph_title": "Название аптеки (филиала):",
        "adm_ph_lat": "Широта (например, 41.285):",
        "adm_ph_lon": "Долгота:",
        "adm_ph_addr": "Адрес:",
        "adm_ph_link": "Ссылка на карту (если нет — «-»):",
        "adm_ph_saved": "✅ Аптека добавлена: {title} (id={id})",

        #ai
        "btn_ai": "🤖 ИИ-помощник",
        "ai_intro": "🤖 Режим ИИ.\nЗадайте любой вопрос. Нажмите «⬅️ Назад» чтобы выйти.",
        "ai_thinking": "Печатаю…",
        "ai_ended": "Диалог завершён.",

    },
}
