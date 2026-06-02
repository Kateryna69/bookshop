import os
import django
import random
import requests
from django.utils.text import slugify
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookshop.settings')
django.setup()

from shop.models import Category, Product


categories = {
    'thriller': Category.objects.get_or_create(name='Трилери', slug='trylery', defaults={'icon': '🔪'})[0],
    'fantasy': Category.objects.get_or_create(name='Фантастика', slug='fantastyka', defaults={'icon': '🚀'})[0],
    'psychology': Category.objects.get_or_create(name='Психологія', slug='psykholohiia', defaults={'icon': '🧠'})[0],
    'selfdev': Category.objects.get_or_create(name='Саморозвиток', slug='samorozvytok', defaults={'icon': '💡'})[0],
    'romance': Category.objects.get_or_create(name='Романтика', slug='romantyka', defaults={'icon': '💕'})[0],
    'fiction': Category.objects.get_or_create(name='Художня', slug='khudozhnia', defaults={'icon': '📖'})[0],
    'detective': Category.objects.get_or_create(name='Детективи', slug='detektyvy', defaults={'icon': '🔍'})[0],
    'horror': Category.objects.get_or_create(name='Жахи', slug='zhakhy', defaults={'icon': '👻'})[0],
}


books_list = [

    ('Harvest Tess Gerritsen', 'Жнива', 'Тесс Герітсон', 'thriller',
     'Медичний трилер про незаконну торгівлю органами. Лікар-хірург стикається з темною стороною медицини.'),
    ('The Surgeon Tess Gerritsen', 'Хірург', 'Тесс Герітсон', 'thriller',
     'Серійний вбивця полює на жінок у Бостоні. Детектив Джейн Різолі бере слід маніяка.'),
    ('The Apprentice Tess Gerritsen', 'Учень', 'Тесс Герітсон', 'thriller',
     'Продовження серії про Різолі та Айлс. Хірург повертається і починає нову гру.'),
    ('The Sinner Tess Gerritsen', 'Грішниця', 'Тесс Герітсон', 'thriller',
     'У монастирі знайдено тіло черниці. Детектив Різолі розслідує загадкове вбивство.'),
    ('Body Double Tess Gerritsen', 'Двійник', 'Тесс Герітсон', 'thriller',
     'Судмедексперт Мора Айлс знаходить власне тіло. Хто ця жінка і чому вона схожа на неї?'),
    ('Vanish Tess Gerritsen', 'Зникнення', 'Тесс Герітсон', 'thriller',
     'У моргу прокидається жінка яку вважали мертвою. Різолі та Айлс у небезпеці.'),

    
    ('Darkness Calls Gillian Flynn', 'Вас цікавить пітьма', 'Кейт Куінн', 'thriller',
     'Секретна мережа жінок-шпигунів у часи Другої світової війни. Напружений історичний трилер.'),

    
    ('Cafe on the Edge of the World John Strelecky', 'Кафе на краю світу', 'Джон Стрелекі', 'selfdev',
     'Філософська притча про сенс життя. Мандрівник зупиняється у загадковому кафе і знаходить відповіді.'),
    ('The Big Five for Life John Strelecky', "П'ять головних мрій життя", 'Джон Стрелекі', 'selfdev',
     'Продовження бестселера про пошук сенсу. Як знайти своє призначення і жити повним життям.'),

    
    ('The Midnight Library Matt Haig', 'Опівнічна бібліотека', 'Метт Хейґ', 'fiction',
     'Між життям і смертю існує бібліотека з книгами всіх можливих життів. Яке життя обрати?'),
    ('Eleanor Oliphant is Completely Fine', 'Елінор Олівант у повному порядку', 'Ґейл Ганімен', 'fiction',
     'Дивакувата самотня жінка і її шлях до порятунку через несподівану дружбу.'),
    ('The Thursday Murder Club Richard Osman', 'Клуб вбивств по четвергах', 'Річард Осман', 'detective',
     'Чотири пенсіонери у будинку відпочинку розслідують реальні злочини. Дотепний детектив.'),
    ('The Seven Husbands of Evelyn Hugo', 'Сім чоловіків Евелін Г’юго', 'Тейлор Дженкінс Рід', 'romance',
     'Легендарна голлівудська зірка нарешті розкриває таємниці свого бурхливого життя.'),
    ('It Ends with Us Colleen Hoover', 'Все закінчується з нами', 'Коллін Гувер', 'romance',
    'Пронизлива історія кохання про силу та сміливість залишити токсичні стосунки.'),
    ('Verity Colleen Hoover', 'Веріті', 'Коллін Гувер', 'thriller',
     'Письменниця знаходить рукопис із зізнанням у злочині. Межа між правдою і вигадкою стирається.'),
    ('November 9 Colleen Hoover', '9 листопада', 'Коллін Гувер', 'romance',
     'Двоє незнайомців зустрічаються щороку лише 9 листопада. Роман про долю і вибір.'),

   
    ('The Body Keeps the Score Bessel van der Kolk', 'Тіло веде рахунок', 'Бессел ван дер Колк', 'psychology',
     'Революційна книга про травму та її вплив на тіло і психіку. Шляхи до зцілення.'),
    ('Maybe You Should Talk to Someone Lori Gottlieb', 'Може, вам варто поговорити з кимось', 'Лорі Готліб', 'psychology',
     'Психотерапевт сама звертається до психотерапевта. Захоплива книга про людську природу.'),
    ('The Subtle Art of Not Giving Mark Manson', 'Тонке мистецтво забивати', 'Марк Менсон', 'selfdev',
     'Нестандартний підхід до гарного життя. Чесна книга про те що насправді важливо.'),
    ('Atomic Habits James Clear', 'Атомні звички', 'Джеймс Клір', 'selfdev',
     'Науково доведений спосіб формувати корисні звички і позбуватися шкідливих.'),
    ('Think Like a Monk Jay Shetty', 'Думай як монах', 'Джей Шетті', 'selfdev',
     'Колишній чернець розповідає як застосувати мудрість монастиря у сучасному житті.'),
    ('How to Be a Good Citizen', 'Як стати відповідальним громадянином', 'Філіп Зімбардо', 'selfdev',
     'Практичний посібник про громадянську відповідальність та роль кожного у суспільстві.'),
    ('Adult Children of Emotionally Immature Parents', 'Дорослі діти емоційно незрілих батьків', 'Ліндсі Гібсон', 'psychology',
     'Як вижити після дитинства з емоційно недоступними батьками і знайти себе.'),

    ('The Hitchhiker Guide to the Galaxy Douglas Adams', 'Автостопом по галактиці', 'Дуглас Адамс', 'fantasy',
     'Культова фантастична комедія. Земля знищена для будівництва траси і один землянин вирушає у космос.'),
    ('Ready Player One Ernest Cline', 'Перший гравець приготуйся', 'Ернест Клайн', 'fantasy',
     'У 2045 році люди живуть у віртуальній реальності ОАЗИС. Починається епічне полювання за скарбом.'),
    ('The Martian Andy Weir', 'Марсіанин', 'Енді Вейр', 'fantasy',
     'Астронавт залишений на Марсі сам і має вижити за допомогою науки та гумору.'),
    ('Project Hail Mary Andy Weir', 'Проект Аве Марія', 'Енді Вейр', 'fantasy',
     'Самотній астронавт прокидається у космосі без пам’яті. Йому треба врятувати Землю.'),
    ('The Name of the Wind Patrick Rothfuss', 'Ім’я вітру', 'Патрік Ротфусс', 'fantasy',
     'Легендарний маг розповідає справжню історію свого життя. Епічне фентезі.'),

    
    ('IT Stephen King', 'Воно', 'Стівен Кінг', 'horror',
     'У місті Дері зникають діти. Група друзів стикається із злом що живе у каналізації.'),
    ('The Shining Stephen King', 'Сяйво', 'Стівен Кінг', 'horror',
     'Сімя залишається на зиму у готелі. Ізоляція і надприродні сили зводять батька з розуму.'),
    ('Misery Stephen King', "Мізері", 'Стівен Кінг', 'horror',
     'Письменник потрапляє до рук своєї найбожевільнішої шанувальниці. Класичний психологічний трилер.'),

   
    ('Gone Girl Gillian Flynn', 'Зникла', 'Ґіліан Флінн', 'detective',
     'У день річниці весілля зникає дружина. Чоловік — головний підозрюваний. Хто бреше?'),
    ('Sharp Objects Gillian Flynn', 'Гострі предмети', 'Ґіліан Флінн', 'detective',
     'Журналістка повертається до рідного міста розслідувати вбивства дівчаток.'),
    ('The Girl with the Dragon Tattoo Stieg Larsson', 'Дівчина з татуюванням дракона', 'Стіґ Ларссон', 'detective',
     'Журналіст і хакерка розслідують зникнення що сталося 40 років тому. Скандинавський нуар.'),
    ('Big Little Lies Liane Moriarty', 'Великі маленькі брехні', 'Ліан Моріарті', 'detective',
     'На шкільному заході хтось гине. Три жінки знають більше ніж говорять.'),
    ('The Woman in the Window AJ Finn', 'Жінка у вікні', 'А. Дж. Фінн', 'detective',
     'Агорафоб спостерігає за сусідами і стає свідком злочину. Але чи можна їй вірити?'),

    
    ('The Notebook Nicholas Sparks', 'Щоденник пам’яті', 'Ніколас Спаркс', 'romance',
     'Незабутня історія кохання що долає десятиліття розлуки та хвороби.'),
    ('Me Before You Jojo Moyes', 'До зустрічі з тобою', 'Джоджо Мойєс', 'romance',
     'Дівчина доглядає за паралізованим чоловіком. Вони змінюють одне одного назавжди.'),
    ('The Fault in Our Stars John Green', 'Винні зірки', 'Джон Грін', 'romance',
     'Двоє підлітків з онкологією закохуються. Пронизлива і смішна одночасно книга про життя.'),
    ('Normal People Sally Rooney', 'Звичайні люди', 'Саллі Руні', 'fiction',
     'Двоє молодих ірландців пов’язані складними стосунками від школи до університету.'),
    ('Conversations with Friends Sally Rooney', 'Розмови з друзями', 'Саллі Руні', 'fiction',
     'Студентка-поетеса заплутується у стосунках з одруженим чоловіком. Сучасна ірландська проза.'),
]


def make_slug(name):
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'є': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'i', 'і': 'i', 'й': 'y',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh',
        'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
        'ю': 'yu', 'я': 'ya', 'ё': 'yo', 'ъ': '', 'ї': 'yi',
    }
    name_lower = name.lower()
    transliterated = ''
    for char in name_lower:
        transliterated += translit_map.get(char, char)
    base_slug = slugify(transliterated)
    if not base_slug:
        base_slug = f'book-{random.randint(1000, 9999)}'
    slug = base_slug
    counter = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    return slug


def import_book(search_query, ua_name, author, category_key, description):
    if Product.objects.filter(name=ua_name).exists():
        print(f'⚠️  Вже існує: {ua_name}')
        return

    url = f'https://openlibrary.org/search.json?q={search_query}&limit=1'
    cover_id = None

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('docs'):
            book = data['docs'][0]
            cover_id = book.get('cover_i')
    except Exception as e:
        print(f'⚠️  Не вдалось знайти обкладинку для: {ua_name} ({e})')

    price = random.randint(180, 520)
    old_price = price + random.randint(40, 120) if random.choice([True, False]) else None
    stock = random.randint(5, 40)
    rating = round(random.uniform(4.2, 5.0), 1)
    rating_count = random.randint(20, 800)
    is_featured = random.choice([True, False, False, False])

    try:
        product = Product.objects.create(
            category=categories[category_key],
            name=ua_name,
            slug=make_slug(ua_name),
            author=author,
            price=price,
            old_price=old_price,
            stock=stock,
            rating=rating,
            rating_count=rating_count,
            is_featured=is_featured,
            description=description,
        )

        
        if cover_id:
            try:
                img_url = f'https://covers.openlibrary.org/b/id/{cover_id}-M.jpg'
                img_response = requests.get(img_url, timeout=10)
                if img_response.status_code == 200:
                    product.cover.save(
                        f'{product.slug}.jpg',
                        ContentFile(img_response.content),
                        save=True
                    )
                    print(f'✅ {ua_name} — {author} (з обкладинкою 🖼)')
                else:
                    print(f'✅ {ua_name} — {author} (без обкладинки)')
            except Exception:
                print(f'✅ {ua_name} — {author} (обкладинку не вдалось завантажити)')
        else:
            print(f'✅ {ua_name} — {author} (без обкладинки)')

    except Exception as e:
        print(f'❌ Помилка для {ua_name}: {e}')


print('📚 Починаємо імпорт українських перекладів...\n')
for item in books_list:
    import_book(*item)

print(f'\n🎉 Готово! Додано книг: {len(books_list)}')