

LOCALES = {
    "uz": {
        # Greeting / onboarding
        "welcome": "Assalomu alaykum! Farmatsevtika botiga xush kelibsiz!",
        "hello": "Assalomu alaykum! Farmatsevtika botiga xush kelibsiz!",
        "choose_lang": "Iltimos, tilni tanlang:",
        "need_register": "Iltimos, avval ro'yxatdan o'ting.",

        # Main menu & buttons
        "menu": "Asosiy menyu:",
        "back": "⬅️ Orqaga",
        "btn_search": "🔎 Qidiruv",
        "btn_feedback": "💬 Fikr bildirish",
        "btn_lang": "🌐 Tilni o'zgartirish",
        "btn_locations": "📍 Lokatsiyalar",
        "btn_ai": "🤖 Sun'iy intellekt",

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

        # Feedback & Complaint (user flow)
        "fb_enter_title": "Fikr yoki shikoyat turini tanlang:",
        "fb_choose": "Iltimos, quyidagidan birini tanlang:",
        "fb_btn_feedback": "🟢 Fikr bildirish",
        "fb_btn_complaint": "🔴 Shikoyat qilish",

        "fb_rate_ask": "Iltimos, baholang:",
        "fb_text_ask": "Fikringizni yozib yuboring:",
        "fb_thanks": "Rahmat! Fikringiz qabul qilindi.",
        "fb_rated": "Rahmat! Bahoyingiz qabul qilindi.",

        # Complaint steps (ikkala kalit mos keladi)
        "cmp_text_ask": "Shikoyatingizni batafsil yozing:",
        "cmp_ask_text": "Shikoyatingizni batafsil yozing:",  # alias for handler
        "cmp_addons_title": "Rasm yoki lokatsiya qo‘shishingiz mumkin, so‘ng “Yuborish”ni bosing.",
        "cmp_btn_photo": "📷 Rasm yuborish",
        "cmp_btn_loc": "📍 Lokatsiyani yuborish",
        "cmp_btn_send": "✅ Shikoyatni yuborish",
        "cmp_photo_saved": "Rasm qabul qilindi.",
        "cmp_loc_saved": "Lokatsiya qabul qilindi.",
        "cmp_sent": "Shikoyatingiz yuborildi. Rahmat!",
        "cmp_more": "Qo‘shimcha ma’lumot yuborishingiz mumkin: rasm yoki lokatsiya. Tayyor bo‘lsangiz “Yuborish”ni bosing.",
        "cmp_send_photo": "Iltimos, shikoyat uchun rasm yuboring (galereyadan yoki kamera orqali).",
        "cmp_send_location": "Iltimos, lokatsiyangizni yuboring (📎 biriktirish → “Location”).",
        "cmp_photo_ok": "Rasm qabul qilindi.",
        "cmp_loc_ok": "Lokatsiya qabul qilindi.",
        "cmp_send_loc": "Iltimos, lokatsiyangizni yuboring.",
        "cmp_send_location": "Iltimos, lokatsiyangizni yuboring.",  # alias (ixtiyoriy)


        # Group message (to moderators)
        "grp_tag_feedback": "🟢 FIKR",
        "grp_tag_complaint": "🔴 SHIKOYAT",
        "grp_feedback": "Foydalanuvchi fikri",
        "grp_complaint": "Foydalanuvchi shikoyati",
        "grp_lang": "🧷 Til",
        "grp_user": "👤 Foydalanuvchi",
        "grp_username": "🔗 Username",
        "grp_contact": "📞 Kontakt",
        "grp_age": "🎂 Yoshi",
        "grp_text": "✍️ Matn",
        "grp_rating": "⭐ Baho",
        "grp_location": "📍 Lokatsiya mavjud",
        "grp_photo": "🖼 Rasm biriktirilgan",

        # Locations (user)
        "loc_menu_title": "Lokatsiyalar bo‘limi:",
        "loc_btn_nearest": "📍 Eng yaqin lokatsiya",
        "loc_btn_all": "📍 Hamma lokatsiyalar",
        "ask_share_loc": "Iltimos, hozirgi joylashuvingizni yuboring.",
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

        # Admin – locations
        "admin_loc_add": "➕ Lokatsiya qo‘shish",
        "admin_loc_title": "Filial nomini yuboring (masalan: Chilonzor apteka).",
        "admin_loc_address": "Manzilni yozing (masalan: Chilonzor, Toshkent).",
        "admin_loc_link": "Ixtiyoriy: xarita havolasini yuboring yoki \"o‘tkazib yuborish\" deb yozing.",
        "admin_loc_ask_point": "📍 Endi lokatsiyani yuboring (\"Turgan joyni yuborish\" tugmasidan foydalaning).",
        "admin_loc_saved": "✅ Lokatsiya saqlandi.",

        # Admin – drug CRUD prompts
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
        
        #aksiya va habar yuborish 
        "adm_broadcast_menu": "✉️ Yuborish bo‘limi:",
        "adm_btn_send_promo": "🎉 Aksiya yuborish",
        "adm_btn_send_msg": "🪪 Habar yuborish",

        # Oqim savollari
        "adm_bc_want_photo": "Rasm qo‘shmoqchimisiz?",
        "adm_bc_yes": "Ha, rasm qo‘shaman",
        "adm_bc_no": "Yo‘q, rasm yo‘q",
        "adm_bc_send_photo": "Iltimos, rasm yuboring (yoki ⬅️ Orqaga).",
        "adm_bc_photo_ok": "Rasm qabul qilindi.",
        "adm_bc_ask_text": "Matnni yuboring:",
        "adm_bc_preview_title": "🔎 Oldindan ko‘rish",
        "adm_bc_edit": "✏️ Tahrirlash",
        "adm_bc_edit_text": "✏️ Matnni tahrirlash",
        "adm_bc_edit_photo": "🖼 Rasmini almashtirish",
        "adm_bc_send": "📢 Hamma foydalanuvchiga yuborish",
        "adm_bc_cancel": "❌ Bekor qilish",
        "adm_bc_sending": "Yuborilmoqda… Bu biroz vaqt olishi mumkin.",
        "adm_bc_done": "✅ Yuborildi.",
        "adm_bc_cancelled": "Bekor qilindi.",


        # Admin – pharmacy CRUD prompts
        "adm_ph_title": "Apteka nomi (filial nomi):",
        "adm_ph_lat": "Latitude (masalan 41.285):",
        "adm_ph_lon": "Longitude:",
        "adm_ph_addr": "Manzil:",
        "adm_ph_link": "Xarita havolasi (yo‘q bo‘lsa '-' yozing):",
        "adm_ph_saved": "✅ Apteka qo‘shildi: {title} (id={id})",
        "adm_btn_users_export": "📊 Foydalanuvchilar ma’lumoti (Excel)",
        "adm_export_prep": "⏳ Hisobot tayyorlanmoqda…",
        "adm_export_done": "✅ Hisobot tayyor. Quyidagi faylni yuklab oling.",
        "adm_export_empty": "Hali foydalanuvchilar topilmadi.",


        # AI
        "ai_welcome": "🤖 Sun'iy intellekt rejimi. Istalgan savolingizni yozing.\nChiqish: “⬅️ Orqaga” yoki /ai_stop",
        "ai_intro": "🤖 Sun'iy intellekt rejimi. Istalgan savolingizni yozing.\nChiqish: “⬅️ Orqaga” yoki /ai_stop",
        "ai_no_key": "Kechirasiz, AI hozircha sozlanmagan.",
        "ai_empty": "Iltimos, savolingizni yozing.",
        "ai_thinking": "Yozayapman…",
        "ai_fail": "Kechirasiz, hozir javob bera olmadim.",
        "ai_no_image": "Hali rasmga javob berish yoq. Matn yuboring.",
        "ai_stopped": "Suhbat yakunlandi.",
        "ai_ended": "Suhbat yakunlandi.",
        "ai_rate_limited": "Hozircha ko‘p so‘rov yuborildi yoki kvota tugagan. Birozdan so‘ng yana urinib ko‘ring.",
        "ai_system_prompt": "Siz foydali va qisqa javob beradigan yordamchisiz. Javobni foydalanuvchi tilida bering.",
    },

    "en": {
        # Greeting / onboarding
        "welcome": "Welcome to the Pharmaceutics bot!",
        "hello": "Welcome to the Pharmaceutics bot!",
        "choose_lang": "Please choose a language:",
        "need_register": "Please register first.",

        # Main menu & buttons
        "menu": "Main menu:",
        "back": "⬅️ Back",
        "btn_search": "🔎 Search",
        "btn_feedback": "💬 Feedback",
        "btn_lang": "🌐 Change language",
        "btn_locations": "📍 Locations",
        "btn_ai": "🤖 AI Assistant",

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

        # Feedback & Complaint
        "fb_enter_title": "Choose feedback type:",
        "fb_choose": "Please choose one:",
        "fb_btn_feedback": "🟢 Send feedback",
        "fb_btn_complaint": "🔴 File a complaint",

        "fb_rate_ask": "Please rate:",
        "fb_text_ask": "Please write your feedback:",
        "fb_thanks": "Thanks! Your feedback has been received.",
        "fb_rated": "Thanks! Your rating is saved.",

        # Complaint steps (both keys provided)
        "cmp_text_ask": "Please describe your complaint in detail:",
        "cmp_ask_text": "Please describe your complaint in detail:",  # alias
        "cmp_addons_title": "You may attach a photo or location, then press “Send”.",
        "cmp_btn_photo": "📷 Send a photo",
        "cmp_btn_loc": "📍 Send location",
        "cmp_btn_send": "✅ Submit complaint",
        "cmp_photo_saved": "Photo saved.",
        "cmp_loc_saved": "Location saved.",
        "cmp_sent": "Your complaint has been sent. Thank you!",
        "cmp_more": "You can add more info: a photo or your location. When ready, press “Send”.",
        "cmp_send_photo": "Please send a photo for your complaint (from gallery or camera).",
        "cmp_send_location": "Please share your location (📎 attach → “Location”).",
        "cmp_photo_ok": "Photo received.",
        "cmp_loc_ok": "Location received.",
        "cmp_send_loc": "Please send your location.",
        "cmp_send_location": "Please send your location.",  # alias (optional)



        # Group message (to moderators)
        "grp_tag_feedback": "🟢 FEEDBACK",
        "grp_tag_complaint": "🔴 COMPLAINT",
        "grp_feedback": "User feedback",
        "grp_complaint": "User complaint",
        "grp_lang": "🧷 Language",
        "grp_user": "👤 User",
        "grp_username": "🔗 Username",
        "grp_contact": "📞 Contact",
        "grp_age": "🎂 Age",
        "grp_text": "✍️ Text",
        "grp_rating": "⭐ Rating",
        "grp_location": "📍 Location attached",
        "grp_photo": "🖼 Photo attached",

        # Locations
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
        "adm_btn_users_export": "📊 Users report (Excel)",
        "adm_export_prep": "⏳ Preparing the report…",
        "adm_export_done": "✅ Report is ready. Download the file below.",
        "adm_export_empty": "No users yet.",

        # aksiya va habar yuborish 
        "adm_broadcast_menu": "✉️ Broadcast menu:",
        "adm_btn_send_promo": "🎉 Send promotion",
        "adm_btn_send_msg": "🪪 Send message",

        "adm_bc_want_photo": "Do you want to attach an image?",
        "adm_bc_yes": "Yes, add image",
        "adm_bc_no": "No image",
        "adm_bc_send_photo": "Please send the image (or ⬅️ Back).",
        "adm_bc_photo_ok": "Image saved.",
        "adm_bc_ask_text": "Send the text:",
        "adm_bc_preview_title": "🔎 Preview",
        "adm_bc_edit": "✏️ Edit",
        "adm_bc_edit_text": "✏️ Edit text",
        "adm_bc_edit_photo": "🖼 Change image",
        "adm_bc_send": "📢 Send to all users",
        "adm_bc_cancel": "❌ Cancel",
        "adm_bc_sending": "Sending… This may take a moment.",
        "adm_bc_done": "✅ Sent.",
        "adm_bc_cancelled": "Cancelled.",    

        # AI
        "ai_welcome": "🤖 AI mode. Ask me anything.\nExit: “⬅️ Back” or /ai_stop",
        "ai_intro": "🤖 AI mode. Ask me anything.\nExit: “⬅️ Back” or /ai_stop",
        "ai_no_key": "Sorry, AI is not configured yet.",
        "ai_empty": "Please type your question.",
        "ai_thinking": "Thinking…",
        "ai_fail": "Sorry, I couldn't answer now.",
        "ai_no_image": "Image inputs are not supported yet. Please send text.",
        "ai_stopped": "Chat ended.",
        "ai_ended": "Chat ended.",
        "ai_rate_limited": "Too many requests or quota exceeded. Please try again shortly.",
        "ai_system_prompt": "You are a helpful, concise assistant. Answer in the user's language.",
    },

    "ru": {
        # Greeting / onboarding
        "welcome": "Добро пожаловать в фарма-бота!",
        "hello": "Добро пожаловать в фарма-бота!",
        "choose_lang": "Пожалуйста, выберите язык:",
        "need_register": "Пожалуйста, сначала зарегистрируйтесь.",

        # Main menu & buttons
        "menu": "Главное меню:",
        "back": "⬅️ Назад",
        "btn_search": "🔎 Поиск",
        "btn_feedback": "💬 Отзыв",
        "btn_lang": "🌐 Сменить язык",
        "btn_locations": "📍 Локации",
        "btn_ai": "🤖 ИИ-помощник",

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

        # Feedback & Complaint
        "fb_enter_title": "Выберите тип: отзыв или жалоба:",
        "fb_choose": "Пожалуйста, выберите действие:",
        "fb_btn_feedback": "🟢 Оставить отзыв",
        "fb_btn_complaint": "🔴 Подать жалобу",

        "fb_rate_ask": "Пожалуйста, оцените:",
        "fb_text_ask": "Напишите ваш отзыв:",
        "fb_thanks": "Спасибо! Ваш отзыв получен.",
        "fb_rated": "Спасибо! Ваша оценка сохранена.",

        # Complaint steps (ikkala kalit)
        "cmp_text_ask": "Опишите вашу жалобу подробно:",
        "cmp_ask_text": "Опишите вашу жалобу подробно:",  # alias
        "cmp_addons_title": "Можно приложить фото или локацию, затем нажмите «Отправить».",
        "cmp_btn_photo": "📷 Отправить фото",
        "cmp_btn_loc": "📍 Отправить локацию",
        "cmp_btn_send": "✅ Отправить жалобу",
        "cmp_photo_saved": "Фото сохранено.",
        "cmp_loc_saved": "Локация сохранена.",
        "cmp_sent": "Ваша жалоба отправлена. Спасибо!",
        "cmp_more": "Можно добавить доп. информацию: фото или локацию. Готово — нажмите «Отправить».",
        "cmp_send_photo": "Пожалуйста, отправьте фото для вашей жалобы (из галереи или с камеры).",
        "cmp_send_location": "Пожалуйста, отправьте вашу локацию (📎 вложение → «Location»/«Местоположение»).",
        "cmp_photo_ok": "Фото получено.",
        "cmp_loc_ok": "Локация получена.",
        "cmp_send_loc": "Пожалуйста, отправьте вашу локацию.",
        "cmp_send_location": "Пожалуйста, отправьте вашу локацию.",  # alias (необязательно)



        # Group message (to moderators)
        "grp_tag_feedback": "🟢 ОТЗЫВ",
        "grp_tag_complaint": "🔴 ЖАЛОБА",
        "grp_feedback": "Отзыв пользователя",
        "grp_complaint": "Жалоба пользователя",
        "grp_lang": "🧷 Язык",
        "grp_user": "👤 Пользователь",
        "grp_username": "🔗 Username",
        "grp_contact": "📞 Контакт",
        "grp_age": "🎂 Возраст",
        "grp_text": "✍️ Текст",
        "grp_rating": "⭐ Оценка",
        "grp_location": "📍 Приложена локация",
        "grp_photo": "🖼 Приложено фото",

        # Locations
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


        #admin aksia qoyish va habar yuborish
        "adm_broadcast_menu": "✉️ Раздел рассылки:",
        "adm_btn_send_promo": "🎉 Отправить акцию",
        "adm_btn_send_msg": "🪪 Отправить сообщение",

        "adm_bc_want_photo": "Хотите прикрепить изображение?",
        "adm_bc_yes": "Да, добавить изображение",
        "adm_bc_no": "Нет изображения",
        "adm_bc_send_photo": "Пожалуйста, пришлите изображение (или ⬅️ Назад).",
        "adm_bc_photo_ok": "Изображение сохранено.",
        "adm_bc_ask_text": "Отправьте текст:",
        "adm_bc_preview_title": "🔎 Предпросмотр",
        "adm_bc_edit": "✏️ Редактировать",
        "adm_bc_edit_text": "✏️ Редактировать текст",
        "adm_bc_edit_photo": "🖼 Заменить изображение",
        "adm_bc_send": "📢 Отправить всем пользователям",
        "adm_bc_cancel": "❌ Отменить",
        "adm_bc_sending": "Отправляем… Это может занять немного времени.",
        "adm_bc_done": "✅ Отправлено.",
        "adm_bc_cancelled": "Отменено.",
        "adm_btn_users_export": "📊 Отчёт по пользователям (Excel)",
        "adm_export_prep": "⏳ Готовим отчёт…",
        "adm_export_done": "✅ Отчёт готов. Скачайте файл ниже.",
        "adm_export_empty": "Пользователей пока нет.",

        # AI
        "ai_welcome": "🤖 Режим ИИ. Задайте любой вопрос.\nВыход: «⬅️ Назад» или /ai_stop",
        "ai_intro": "🤖 Режим ИИ. Задайте любой вопрос.\nВыход: «⬅️ Назад» или /ai_stop",
        "ai_no_key": "Извините, ИИ пока не настроен.",
        "ai_empty": "Пожалуйста, напишите свой вопрос.",
        "ai_thinking": "Печатаю…",
        "ai_fail": "Извините, сейчас не могу ответить.",
        "ai_no_image": "Изображения пока не поддерживаются. Отправьте текст.",
        "ai_stopped": "Диалог завершён.",
        "ai_ended": "Диалог завершён.",
        "ai_rate_limited": "Слишком много запросов или исчерпана квота. Попробуйте позже.",
        "ai_system_prompt": "Вы полезный и лаконичный ассистент. Отвечайте на языке пользователя.",
    },
}
