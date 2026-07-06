# -*- coding: utf-8 -*-
"""
Web app sinh dữ liệu review sản phẩm (tiếng Anh) - Bản nâng cấp cho Straight Ponytail Extensions.
"""
import random
from datetime import date, timedelta
from io import BytesIO

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# NGÂN HÀNG MẢNH GHÉP (tiếng Anh) - chuyên biệt cho Straight Ponytail
# ----------------------------------------------------------------------------
RATING = {"Positive": [5, 5, 5, 5, 4], "Neutral": [3, 3, 3]}

POS_ADJ = [
    "natural", "realistic", "comfortable", "silky", "lightweight", "smooth",
    "sleek", "seamless", "easy-to-use", "flattering", "secure", "thick"
]

TITLE_TEMPLATES = {
    "Positive": [
        "Looks exactly like my real hair pony",
        "Exactly what I was looking for!",
        "Love how sleek and long it is",
        "Very secure and comfortable to wear",
        "Beautiful straight ponytail",
        "The blend is absolutely amazing",
        "My go-to for a quick bad hair day fix",
        "One of my favorite hair pieces ever",
        "Great quality and feels so real",
        "Super happy with this purchase!",
        "The hair swings so naturally",
        "Perfect for a sleek high pony look",
        "Lightweight and doesn't pull my head down",
        "Easy to install and stays put all day",
        "Exceeded my expectations for the price",
        "Looks even better in person than the pics",
        "Sleek, shiny, and super easy to manage",
        "Love this ponytail extension!",
        "Perfect instant length and volume",
        "Would definitely buy again in a heartbeat",
        "The fiber/hair feels incredibly soft",
        "So easy to blend with my natural hair",
        "Looks very realistic, not fake shiny",
        "Comfortable to wear for 8+ hours",
        "Beautiful right out of the packaging",
        "A total game changer for quick hairstyles",
        "Got so many compliments!",
        "Saves me so much time in the morning",
        "Perfect color match",
        "Obsessed with this pony!"
    ],
    "Neutral": [
        "Nice ponytail but the color match was off",
        "Good quality, just the wrong shade for me",
        "Color looked different under natural light",
        "Wanted to love it but the shade didn't fit",
        "Quality was decent, color matching is tricky",
        "Close match but you can tell it's fake hair",
        "Nice overall but didn't blend perfectly with my ends",
        "The tone just didn't work for my hair",
        "Good hair extension, difficult color match",
        "Looks nice but it's a bit too heavy",
        "A little too shiny out of the box",
        "Okay for the price but tangles easily",
        "It's decent but the wrap-around part is bulky",
        "Thinner than expected at the ends",
        "It's okay, just takes some practice to secure"
    ],
}

NEU_MILD_ADJ = ["Decent", "Okay", "Fine", "Acceptable", "Average"]
NEU_FLAW = ["thin at the ends", "a bit synthetic shiny", "shed-prone", "heavy", "stiff"]

BODY_BANK = {
    "Positive": {
        "opener": [
            "I've been looking for a quick ponytail extension for a while and decided to risk it on this one.",
            "My natural hair is pretty short and thin, so putting it into a decent pony is almost impossible.",
            "I needed something quick and sleek for work mornings when I don't have time to blow dry my hair.",
            "I was tired of spending an hour trying to flatten and style my own stubborn hair into a high pony.",
            "I've tried a few different clip-in ponytails before and wanted to see how this one compared.",
            "I purchased this right before an event and ended up loving it way more than I expected.",
            "I wanted a protective style that gives me instant Ariana Grande vibes without the salon price.",
            "After seeing a few tutorials online, I decided to give this wrap-around pony a try.",
            "I normally wear full clip-in sets, but I wanted something way faster for everyday use.",
            "I've been searching for a realistic, dead-straight ponytail and finally hit the jackpot with this.",
            "I wanted a style that looked super polished and high-fashion without requiring 30 minutes of effort.",
            "This was my very first time trying a drawstring/wrap ponytail extension.",
            "I wanted something lightweight that wouldn't give me a headache after wearing it all day.",
            "I ordered this because I wanted that sleek baddie look without committing to permanent tape-ins.",
            "I needed a simple hairpiece that would blend effortlessly with my natural sleeked-back hair."
        ],
        "quality": [
            "The hair feels like healthy, salon-grade hair and flows beautifully.",
            "It moves and shakes just like real hair, no awkward stiffness at all.",
            "The texture is super smooth, exactly like freshly flat-ironed hair.",
            "It doesn't have that cheap, blinding plastic shine that most synthetic pieces have.",
            "The strands are incredibly soft while still maintaining a realistic thickness.",
            "I was honestly impressed by how natural the fibers looked even up close under bright lights.",
            "The ends look blunt and healthy instead of looking stringy or split.",
            "The hair handles low-heat styling perfectly fine to match my texture.",
            "I ran a straightener through it on low heat and it got even sleeker.",
            "After comb-out and a bit of leave-in spray, it stayed incredibly soft and manageable.",
            "The sleek texture held up beautifully even after a long night of dancing.",
            "The density feels completely natural—not too thin, but not ridiculously heavy either.",
            "The ponytail has a beautiful swing to it when I walk.",
            "It doesn't feel overly coated or greasy like some extensions I've ordered online.",
            "The quality feels premium, honestly mimicking much more expensive brands."
        ],
        "color": [
            "The shade was an absolute perfect match to my current hair tone.",
            "I was so nervous about trying to match my hair online, but it blended seamlessly.",
            "The color looks incredibly multi-dimensional and natural in person.",
            "It blended so well with my natural hair that you can't see the transition at all.",
            "The product photos on the listing gave a very accurate representation of the actual tone.",
            "The color looks even better and more vibrant when you step into natural sunlight.",
            "I had zero trouble blending the piece with my own bun underneath.",
            "The tone is realistic and has the right undertones without looking flat.",
            "The color match was spot on, which is usually rare for me when buying hair online.",
            "Once I wrapped the base section around, the color blend looked totally flawless."
        ],
        "fit_usage": [
            "It literally takes me less than two minutes to secure it and walk out the door.",
            "Getting ready for school or work in the morning is a breeze now.",
            "I love that the clip grips tightly onto my hair elastic without slipping down.",
            "The built-in comb and velcro strap feel incredibly secure without pulling on my scalp.",
            "I didn't need to use a million bobby pins to keep it from falling off.",
            "It's so much more comfortable and less sweaty than wearing a full traditional wig.",
            "The base sits flush against my natural bun and doesn't look bulky from the side.",
            "I wore it through a whole 10-hour shift and didn't get a single tension headache.",
            "The net attachment inside is very breathable and lightweight.",
            "Installation is completely foolproof and beginner-friendly.",
            "I had it clipped in, wrapped, and pinned in under sixty seconds flat."
        ],
        "results": [
            "The end result is an instant confidence booster.",
            "It gives me that perfect, sleek Instagram look immediately.",
            "It adds the exact amount of dramatic length and volume I wanted.",
            "The overall look is super clean, professional, and classy."
        ],
        "extra": [
            "Literally everyone at my office thought it was my real hair grown out.",
            "My own hair stylist saw me wearing it and was shocked at how well it blended.",
            "I've already worn it to multiple dinners and weekend outings.",
            "This has officially become my signature look for lazy hair days.",
            "I received at least five compliments within the first hour of wearing it out.",
            "People just assume I got a professional blowout or premium salon extensions.",
            "It photographs beautifully on camera without catching any fake glare.",
            "Nobody could tell where my actual hair ended and the ponytail extension started.",
            "I love how it stays sleek and tangle-free even when it's windy outside.",
            "I've worn it for long, hot days and it stayed perfectly secure the whole time."
        ],
        "value": [
            "For this price point, the quality is honestly unbeatable.",
            "I've spent double the money on high-end beauty supply extensions that weren't this nice.",
            "The value definitely exceeded what I expected for an affordable hair piece.",
            "It looks and feels like a luxury luxury extension piece.",
            "I think this is an absolute steal given how often I'm going to wear it.",
            "Considering how great the fiber looks, the price is incredibly reasonable.",
            "The construction of the wrap mechanism makes it well worth the investment.",
            "I feel like I got way more value than what I actually paid for."
        ],
        "shipping": [
            "The packaging was neat and it came with extra bobby pins, which was a nice touch.",
            "Shipping was fast and the hair arrived perfectly straight with no weird kinks.",
            "It arrived beautifully boxed so the hair wasn't squished or messy.",
            "The package arrived a day earlier than estimated, super happy with that.",
            "It was packed carefully to prevent any tangling during transit."
        ],
        "support": [
            "Customer service helped me pick the right option based on my root photos.",
            "The seller was extremely helpful and responsive when I messaged them.",
            "Great communication from the shop, they really care about customer satisfaction."
        ],
        "closer": [
            "Overall, I am absolutely in love with this ponytail.",
            "I will definitely be purchasing another one as a backup.",
            "Highly recommend this to anyone looking for an instant, effortless glow-up.",
            "This is hands down one of my best online hair purchases.",
            "I'm so incredibly glad I decided to click buy on this.",
            "It's worth every single penny.",
            "I see myself ordering a longer length from them very soon.",
            "Super satisfied and will be telling all my friends about it."
        ],
    },
    "Neutral": {
        "opener": [
            "So... I have slightly mixed feelings about this ponytail extension.",
            "It's okay I guess, just wasn't exactly what I pictured in my head.",
            "I really wanted to love this pony but I'm kind of on the fence.",
            "Not terrible, but not mind-blowing either—somewhere right in the middle.",
            "Decent enough extension for a quick style, but it has a few drawbacks.",
            "I'm torn on this one; there are definitely pros and cons.",
            "It's an alright hairpiece, it just didn't wow me like the reviews said.",
            "Okay, so it's a bit of a hit and miss for me personally."
        ],
        "quality": [
            "The hair is soft, but it's SO shiny that it looks a little artificial in direct sunlight.",
            "The quality is just okay; the hair gets thin pretty quickly toward the ends.",
            "It sheds a bit more than I'd like when I run a wide-tooth comb through it.",
            "The fiber feels a bit stiff and doesn't have that fluid swing of real hair.",
            "It's about what you'd expect for the price tag—nothing premium.",
            "It felt super silky at first but got a little dry and tangled after two wears.",
            "It has decent thickness at the base, but the bottom half looks a bit skimpy.",
            "The hair texture is smooth, but it tangles easily around the back of my neck."
        ],
        "color": [
            "The shade ended up being a hair darker than what was shown in the pictures.",
            "The color tone looked a bit different in person compared to my screen.",
            "The quality of the piece is fine, but the color matching is just hard online.",
            "I had a bit of an issue getting the hair color to blend perfectly with my natural hair.",
            "The shade was close, but you can see a slight contrast where my real hair ends.",
            "The color wasn't bad, it just had a slightly warmer undertone than my own hair.",
            "The color match wasn't quite seamless enough for me to wear it completely down.",
            "The difference in color between my bun and the extension is noticeable in daylight."
        ],
        "fit_usage": [
            "Clipping the comb into my hair tie is easy enough, but the piece feels heavy.",
            "The wrap-around strand is a bit bulky and takes a lot of pins to secure tightly.",
            "It takes some serious fiddling and hairspray to get it to stay up without sliding.",
            "If you have fine hair like me, the weight of the pony pulls your hair down after an hour.",
            "The comb attachment digs into my scalp a little bit if I wrap it too tight.",
            "Had to use my own stronger bobby pins because the wrap strip kept unravelling."
        ],
        "results": [
            "The final look is alright, just a bit more high-maintenance than I expected.",
            "Adds length but makes my head look a little disproportionate because of the heavy base.",
            "Looks decent from the front, but from the back, you can tell it's an attachment."
        ],
        "extra": [
            "I'll probably keep it for costume parties or photos, but not for everyday wear.",
            "This would definitely work better on someone with a thick, strong natural ponytail.",
            "It's fine for social media photos, but up close in person, it looks a bit synthetic.",
            "Wish the wrap section was made with a bit more hair to cover the velcro better."
        ],
        "value": [
            "For the cheap price, it's fair. Just don't expect luxury salon quality.",
            "It's not a total rip-off, but it's definitely an budget-tier item.",
            "Average value—I've bought similar hairpieces at local beauty stores for less."
        ],
        "shipping": [
            "Shipping took a bit longer than expected and the tip of the pony was slightly bent.",
            "Packaging was super basic, just a plastic bag, so the hair was a bit frizzy upon arrival."
        ],
        "support": [
            "Reached out to the seller about a exchange and the reply was a bit slow."
        ],
        "closer": [
            "It's fine for an occasional night out, just not a daily staple for me.",
            "For what it costs, I can't complain too much, it gets the job done.",
            "Wouldn't say I'm obsessed, but it's usable if you know how to style it.",
            "I'll probably shop around for a higher-quality lightweight brand next time.",
            "Three stars feels fair—decent product but has its flaws.",
            "Middle of the road. Neither amazing nor terrible."
        ],
    },
}

SHORT_BODIES = {
    "Positive": [
        "Very happy with this ponytail extension, super sleek!",
        "The hair feels soft, straight, and blends beautifully.",
        "Looks exactly like the photos, love the instant length.",
        "Great quality straight pony and very easy to put on.",
        "Stays secure all day long without hurting my head.",
        "The blend with my natural hair is absolutely amazing.",
        "Easy to install, comb out, and maintain. 5 stars!",
        "Beautiful silky straight texture. Exceeded my expectations.",
        "Would definitely buy another one again soon.",
        "Looks very realistic, no fake doll shine at all.",
        "The ponytail moves naturally and gives great volume.",
        "Perfect everyday pony for when I'm in a rush.",
        "Exactly what I was looking for to get that sleek high pony look.",
        "Super comfortable, lightweight, and natural looking.",
        "One of my favorite quick hair pieces so far!"
    ],
    "Neutral": [
        "Nice quality extension, just couldn't get a perfect color match.",
        "The shade was slightly off but the texture of the hair felt nice.",
        "Good ponytail overall, the color just didn't blend perfectly with my hair.",
        "The hair quality was fine, but the shade matching was difficult.",
        "The ponytail was nice but the color looked different in person than online.",
        "Would probably try a different shade or brand next time.",
        "Not a bad hairpiece, just the wrong undertone for my natural hair.",
        "The color match didn't work out for me but the return process was easy.",
        "Everything was fine with the clip and wrap except the shade variance.",
        "Hair was quite smooth, but the color wasn't quite right for my roots."
    ],
}


def build_title(sentiment):
    tpl = random.choice(TITLE_TEMPLATES[sentiment])
    adj_pool = POS_ADJ if sentiment == "Positive" else NEU_MILD_ADJ
    title = tpl.format(
        adj1=random.choice(adj_pool),
        adj2=random.choice(adj_pool),
        flaw=random.choice(NEU_FLAW),
    ) if "{" in tpl else tpl
    return title[:1].upper() + title[1:]


# ----------------------------------------------------------------------------
# STORY-BASED BANKS - Câu chuyện hậu trường đã đổi sang ngữ cảnh Ponytail
# ----------------------------------------------------------------------------
LIFE_EVENTS = [
    "I bought this ponytail piece for my birthday dinner and it photographed beautifully.",
    "I got this for a formal event and honestly it made me feel so sleek and confident.",
    "After having a baby my hair thinned out, so this ponytail helps me feel put-together again.",
    "I've been dealing with hair breakage, so I wanted an easy high-pony style to protect my ends.",
    "I ordered this for a weekend trip and ended up wearing it to every single dinner.",
    "My natural hair is just past my shoulders, so I needed this for that dramatic long look.",
    "I needed something quick for a family photoshoot and this worked flawlessly.",
    "I bought this for engagement photos and the sleek straight hair looked stunning on camera.",
    "I wanted a long, high ponytail without paying hundreds for salon bondings.",
    "I've always had fine hair that looks sad in a hair tie, so I needed this extra fullness."
]

HAIR_SITUATIONS = [
    "My hair is naturally pretty fine and short.",
    "I have shoulder-length hair and wanted a sleek long look.",
    "I've always struggled with getting a high ponytail to look thick.",
    "My natural hair is blunt cut, so blending can sometimes be tricky.",
    "I have medium-thick hair but wanted that extra dramatic length down to my back.",
    "My own ponytail always looks like a tiny stub, so I needed help.",
    "I wanted a polished look without damaging my natural hair with constant heat.",
    "I've been trying to grow my hair out but it's stuck at that awkward length."
]

PRODUCT_DETAILS = [
    "I ordered the 22-inch straight version.",
    "I went with the 26-inch extra long set.",
    "I chose the length that falls right around my mid-back.",
    "The length I picked matched my expectations perfectly.",
    "I have fine hair and was worried the wrap-around band would look too bulky.",
]

MINOR_CONS = [
    "The color looked a tiny bit darker in my bathroom but blended fine under normal light.",
    "It took me a couple of tries to get the clip placement tight enough so it wouldn't slide.",
    "It's a little bit heavy if you position it directly on the very top of your head.",
    "The wrap strand felt stiff at first but it softened up with some manipulation.",
    "I wish the velcro part was just a tiny bit smaller.",
    "The ends were a little thinner than the top, but a quick trim fixed it.",
    "The first time wrapping the extra hair around the base took some practice.",
    "I had to bobby pin it down tightly to make sure it felt secure on my small head."
]

RESULTS = [
    "Nobody at the party could tell I was wearing an extension piece.",
    "The blend at the base was seamless and looked completely natural.",
    "I got so many compliments on how sleek my hair looked.",
    "My friends were completely shocked when I told them it was a clip-on.",
    "Even my boyfriend noticed how good the sleek high pony looked.",
    "It looked incredibly chic and high-end in all my pictures.",
    "The instant length and volume made such a massive difference.",
    "It gave me that perfect bounce and sway when walking."
]

RECOMMENDATIONS = [
    "I'd definitely buy from this brand again.",
    "Really happy with how this turned out.",
    "Would absolutely recommend it if you love slicked-back styles.",
    "Worth every single penny in my opinion.",
    "I'll probably order another one in a different length just to have options.",
    "So glad I decided to ignore the negative reviews and try it.",
    "I'd highly recommend this to anyone with fine hair wanting a thick pony.",
    "Definitely one of my better quick beauty purchases this year."
]


def build_body(sentiment):
    if random.random() < 0.12:
        return random.choice(SHORT_BODIES[sentiment])

    parts = []
    if random.random() < 0.8:
        parts.append(random.choice(LIFE_EVENTS))

    parts.append(random.choice(HAIR_SITUATIONS))

    if random.random() < 0.7:
        parts.append(random.choice(PRODUCT_DETAILS))

    parts.append(random.choice(BODY_BANK[sentiment]["quality"]))
    
    if random.random() < 0.8:
        parts.append(random.choice(BODY_BANK[sentiment]["color"]))

    if random.random() < 0.6:
        parts.append(random.choice(BODY_BANK[sentiment]["fit_usage"]))

    if sentiment == "Positive":
        if random.random() < 0.35:
            parts.append(random.choice(MINOR_CONS))
    else:
        parts.append(random.choice(MINOR_CONS))

    parts.append(random.choice(RESULTS))
    parts.append(random.choice(RECOMMENDATIONS))

    return " ".join(parts)

_FIRST_NAMES = [
    "Emily", "Jessica", "Ashley", "Lauren", "Megan", "Rachel", "Nicole", "Amanda",
    "Sarah", "Jennifer", "Olivia", "Sophia", "Emma", "Chloe", "Grace", "Bella",
    "Candice", "Shyan", "Marcia", "Nikki", "Makayla", "Noelle", "Mandi", "Zoey",
    "Hannah", "Tiffany", "Brooke", "Kayla", "Madison", "Brittany", "Samantha",
    "Taylor", "Danielle", "Heather", "Amber", "Chelsea", "Courtney", "Haley",
    "Katelyn", "Lindsay", "Melissa", "Paige", "Shelby", "Stephanie", "Whitney",
    "Alyssa", "Brianna", "Cassandra", "Destiny", "Faith", "Gabrielle", "Hope",
    "Jasmine", "Kaitlyn", "Leah", "Morgan", "Natalie", "Peyton", "Quinn",
    "Riley", "Sierra", "Trinity", "Valerie", "Vanessa", "Victoria", "Wendy",
    "Abigail", "Alexis", "Allison", "Ariel", "Aubrey", "Autumn", "Bailey",
    "Brenda", "Carla", "Carmen", "Caroline", "Claire", "Crystal", "Dana",
    "Dawn", "Denise", "Diana", "Elena", "Elise", "Ellie", "Eva", "Fiona",
    "Gina", "Hailey", "Harper", "Holly", "Isabel", "Isla", "Jade", "Jamie",
    "Janet", "Julia", "Julie", "June", "Karen", "Kate", "Katherine", "Kelsey",
    "Kim", "Kristen", "Laura", "Lily", "Lisa", "Luna", "Lydia", "Mackenzie",
    "Maria", "Marissa", "Mary", "Maya", "Mia", "Michelle", "Miranda", "Monica",
    "Nancy", "Nina", "Nora", "Pam", "Patricia", "Priya", "Rebecca", "Regina",
    "Renee", "Rosa", "Sabrina", "Sandra", "Sara", "Shannon", "Sharon", "Stacy",
    "Summer", "Susan", "Tamara", "Teresa", "Tori", "Tracy", "Trisha", "Veronica",
    "Vivian", "Wanda", "Yvonne", "Zoe",
]

_LAST_INITIALS = list("ABCDEFGHJKLMNOPQRSTUVWXYZ")

_LAST_NAMES = [
    "Anderson", "Baker", "Barnes", "Bennett", "Brooks", "Brown", "Butler", "Campbell",
    "Carter", "Clark", "Collins", "Cook", "Cooper", "Cox", "Davis", "Edwards",
    "Evans", "Fisher", "Foster", "Garcia", "Gray", "Green", "Griffin", "Hall",
    "Harris", "Harrison", "Hayes", "Henderson", "Hill", "Howard", "Hughes", "Jackson",
    "James", "Jenkins", "Johnson", "Jones", "Kelly", "King", "Lee", "Lewis",
    "Long", "Martin", "Mason", "Miller", "Mitchell", "Moore", "Morgan", "Morris",
    "Nelson", "Parker", "Patterson", "Perez", "Perry", "Peterson", "Phillips", "Price",
    "Reed", "Richardson", "Rivera", "Roberts", "Robinson", "Rodriguez", "Rogers", "Ross",
    "Russell", "Sanders", "Scott", "Simmons", "Smith", "Stewart", "Taylor", "Thomas",
    "Thompson", "Torres", "Turner", "Walker", "Ward", "Watson", "White", "Williams",
    "Wilson", "Wood", "Wright", "Young",
]


def _random_reviewer_name():
    first = random.choice(_FIRST_NAMES)
    r = random.random()
    if r < 0.34:
        return first                                          # chỉ first name
    elif r < 0.67:
        return f"{first} {random.choice(_LAST_INITIALS)}."   # first + initial
    else:
        return f"{first} {random.choice(_LAST_NAMES)}"       # first + last name


# ----------------------------------------------------------------------------
# HÀM SINH DỮ LIỆU
# ----------------------------------------------------------------------------
def sinh_du_lieu(so_dong, sac_thai_chon, trong_so, ngay_bat_dau, ngay_ket_thuc,
                 them_email, seed=None):
    if seed is not None:
        random.seed(seed)

    records = []
    so_ngay = max((ngay_ket_thuc - ngay_bat_dau).days, 0)

    for _ in range(so_dong):
        sentiment = random.choices(sac_thai_chon, weights=trong_so, k=1)[0]

        record = {
            "title": build_title(sentiment),
            "body": build_body(sentiment),
            "rating": random.choice(RATING[sentiment]),
            "review_date": (ngay_bat_dau + timedelta(days=random.randint(0, so_ngay))).isoformat(),
            "reviewer_name": _random_reviewer_name(),
            "reviewer_email": "" if not them_email
            else f"{_random_reviewer_name().split()[0].lower()}{random.randint(1, 999)}@gmail.com",
            "sentiment": sentiment,
        }
        records.append(record)

    return pd.DataFrame(records)


# ----------------------------------------------------------------------------
# GIAO DIỆN
def df_to_excel_bytes(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="reviews")
    return buffer.getvalue()


# ----------------------------------------------------------------------------
st.set_page_config(page_title="Review Data Generator", page_icon="📝", layout="wide")
st.title("📝 Bộ sinh dữ liệu review sản phẩm (English)")
st.caption("Tạo dữ liệu review tiếng Anh giả lập (hair extensions) - schema khớp JSON: "
           "title, body, rating, review_date, reviewer_name, reviewer_email.")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    so_dong = st.number_input("Số dòng cần sinh", min_value=1, max_value=1_000_000,
                              value=10_000, step=1_000)

    st.subheader("Sắc thái")
    dung_positive = st.checkbox("Positive (4-5★)", value=True)
    dung_neutral = st.checkbox("Neutral (3★)", value=True)

    st.caption("Tỉ lệ (trọng số) mỗi sắc thái:")
    ts_positive = st.slider("Trọng số Positive", 0, 100, 70, disabled=not dung_positive)
    ts_neutral = st.slider("Trọng số Neutral", 0, 100, 30, disabled=not dung_neutral)

    them_email = st.checkbox("Sinh email giả (reviewer_email)", value=False,
                             help="Bỏ chọn để để trống giống JSON mẫu.")

    c1, c2 = st.columns(2)
    ngay_bat_dau = c1.date_input("Từ ngày", value=date.today() - timedelta(days=365))
    ngay_ket_thuc = c2.date_input("Đến ngày", value=date.today())

    dung_seed = st.checkbox("Cố định seed (tái lập kết quả)", value=False)
    seed = st.number_input("Seed", value=42, disabled=not dung_seed)

    tao = st.button("🚀 Sinh dữ liệu", type="primary", use_container_width=True)

# Gom lựa chọn
sac_thai_chon, trong_so = [], []
if dung_positive:
    sac_thai_chon.append("Positive"); trong_so.append(ts_positive)
if dung_neutral:
    sac_thai_chon.append("Neutral"); trong_so.append(ts_neutral)

if tao:
    if not sac_thai_chon:
        st.error("Vui lòng chọn ít nhất một sắc thái.")
    elif sum(trong_so) == 0:
        st.error("Tổng trọng số đang bằng 0. Hãy tăng trọng số cho sắc thái đã chọn.")
    elif ngay_ket_thuc < ngay_bat_dau:
        st.error("'Đến ngày' phải lớn hơn hoặc bằng 'Từ ngày'.")
    else:
        with st.spinner(f"Đang sinh {so_dong:,} dòng..."):
            df = sinh_du_lieu(
                so_dong, sac_thai_chon, trong_so, ngay_bat_dau, ngay_ket_thuc,
                them_email, seed=int(seed) if dung_seed else None,
            )
        st.session_state["df"] = df

# Hiển thị kết quả
if "df" in st.session_state:
    df = st.session_state["df"]
    st.success(f"Đã sinh xong {len(df):,} dòng dữ liệu!")

    m1, m2, m3 = st.columns(3)
    m1.metric("Tổng số review", f"{len(df):,}")
    m2.metric("Điểm sao trung bình", f"{df['rating'].mean():.2f} ⭐")
    m3.metric("Số sắc thái", df["sentiment"].nunique())

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("Phân bố sắc thái")
        st.bar_chart(df["sentiment"].value_counts())
    with g2:
        st.subheader("Phân bố điểm sao")
        st.bar_chart(df["rating"].value_counts().sort_index())

    st.subheader("Xem trước dữ liệu")
    st.dataframe(df.head(200), use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    json_str = df.to_json(orient="records", force_ascii=False, indent=2)
    xlsx = df_to_excel_bytes(df)

    d1, d2, d3 = st.columns(3)
    d1.download_button("⬇️ Tải CSV", data=csv, file_name="reviews.csv",
                       mime="text/csv", type="primary", use_container_width=True)
    d2.download_button("⬇️ Tải JSON", data=json_str.encode("utf-8"),
                       file_name="reviews.json", mime="application/json",
                       use_container_width=True)
    d3.download_button("⬇️ Tải Excel", data=xlsx, file_name="reviews.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True)
else:
    st.info("👈 Cấu hình ở thanh bên rồi bấm **Sinh dữ liệu** để bắt đầu.")
