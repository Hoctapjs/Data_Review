# -*- coding: utf-8 -*-
"""
Web app sinh dữ liệu review sản phẩm (tiếng Anh) - bản cải tiến.
Schema khớp với JSON mẫu: title, body, rating, review_date, reviewer_name, reviewer_email.
Chạy:  streamlit run app.py
"""
import random
from datetime import date, timedelta

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# NGÂN HÀNG MẢNH GHÉP (tiếng Anh) - ghép ngẫu nhiên -> hàng trăm nghìn tổ hợp
# 2 sắc thái: Positive (4-5★), Neutral (3★)
# ----------------------------------------------------------------------------
RATING = {"Positive": [5, 5, 5, 5, 4], "Neutral": [3, 3, 3]}

# --- TITLE: ghép từ template + ngân hàng tính từ ---------------------------
POS_ADJ = [
    "texture",
    "realistic",
    "blend",
    "soft",
    "pattern",
    "full",
    "seamless",
    "flawless",
    "easy",
    "lightweight",
    "comfortable",
    "beginner-friendly"
]
TITLE_TEMPLATES = {
    "Positive": [
    "Love this texture",
    "Looks very natural",
    "Beautiful wave pattern",
    "So easy to wear",
    "Exactly what I wanted",
    "Very happy with this wig",
    "The hair is so soft",
    "Great quality hair",
    "Perfect for everyday wear",
    "Easy to install",
    "Beautiful and natural looking",
    "One of my favorite wigs",
    "The waves look amazing",
    "Really impressed with the quality",
    "Love how it blends",
    "Looks just like the photos",
    "The texture is beautiful",
    "Exceeded my expectations",
    "The volume is perfect",
    "Very beginner friendly",
    "Would definitely buy again",
    "Soft and easy to manage",
    "Beautiful from the first wear",
    "The hair feels amazing",
    "Natural looking and comfortable",
    "Great everyday style",
    "The pattern stayed beautiful",
    "Perfect amount of fullness",
    "Love this hair",
    "A great purchase"
    ],
    "Neutral": [
        "Nice wig but the color wasn't right",
    "Good quality, wrong shade for me",
    "Color looked different in person",
    "Wanted to love it but the color was off",
    "Quality was good, color not so much",
    "Close match but not quite",
    "Nice overall but didn't blend perfectly",
    "The color just didn't work for me",
    "Good wig, difficult color match",
    "Looks nice but not my shade"
    ],
}
TITLE_TEMPLATES["Positive"] += [
    "Perfect color match for me",
    "Worth it",
    "Amazing!",
    "Great extensions!",
    "Perfect for my wedding day!",
    "You can't even tell I'm wearing clip ins",
    "These are GORGEOUS !!!",
    "So happy with these",
    "Exceeded my expectations",
    "Exactly what I was looking for",
]

TITLE_TEMPLATES["Neutral"] += [
    "Nice wig but the color wasn't right",
    "Good quality, wrong shade for me",
    "Color looked different in person",
    "Wanted to love it but the color was off",
    "Quality was good, color not so much",
    "Close match but not quite",
    "Nice overall but didn't blend perfectly",
    "The color just didn't work for me",
    "Good wig, difficult color match",
    "Looks nice but not my shade"
]

NEU_MILD_ADJ = ["Decent", "Okay", "Fine", "Acceptable", "Average"]
NEU_FLAW = ["thin", "shiny", "shed-prone", "pricey", "stiff"]

# --- BODY: mỗi sắc thái có nhiều nhóm câu, mỗi câu đứng độc lập -------------
BODY_BANK = {
    "Positive": {
        "opener": [
     "I've been wearing this wig for a few weeks now and wanted to share my thoughts.",
    "I was looking for a natural everyday style and decided to try this wig.",
    "After reading a lot of reviews, I finally ordered this one.",
    "I've tried several wigs over the years and this has been one of my favorites.",
    "This was my first time trying this texture and I'm glad I gave it a chance.",
    "I wanted something easy to wear without spending hours styling my hair.",
    "I've been looking for a wig that looked natural and blended well.",
    "I purchased this for everyday wear and it has worked out really well.",
    "I wasn't sure what to expect but the quality surprised me.",
    "I wanted a style that looked natural without too much effort.",
    "I bought this before an event and ended up wearing it much more often.",
    "I've been trying different wigs lately and this one stands out.",
    "I wanted a low-maintenance style and this has been a great option.",
    "I was mainly looking for something comfortable and natural looking.",
    "This is my first U Part Wig and the experience has been very positive."
],
        "quality": [
    "The hair is very soft and easy to manage.",
    "The texture feels natural and realistic.",
    "The wave pattern looks just like the photos.",
    "The hair feels lightweight while still looking full.",
    "The quality was better than I expected.",
    "The texture remained soft after washing.",
    "The waves stayed consistent throughout the wig.",
    "The hair has very natural movement.",
    "I experienced very little shedding.",
    "The wig feels well made and durable.",
    "The texture looks realistic in person.",
    "The waves fall naturally without looking overly styled.",
    "The density feels natural for everyday wear.",
    "The hair brushes easily and doesn't tangle much.",
    "The quality has held up well so far."
        ],
        "color": [
    "The color matched the product photos really well.",
    "I was pleasantly surprised by how accurate the color looked in person.",
    "The shade blended naturally with my own hair.",
    "The color was exactly what I expected from the listing.",
    "The color looked very true to the photos online.",
    "I was worried about ordering online, but the shade ended up being a great match.",
    "The color worked perfectly with my natural hair.",
    "It blended much better than I expected.",
    "The shade looked very natural once installed.",
    "The color was spot on compared to the website images.",
    "The tone matched my hair beautifully.",
    "I had no issues getting the color to blend.",
    "The shade looked even better in person.",
    "It matched my hair surprisingly well.",
    "The color looked realistic and natural."
],
        "fit_usage": [
    "Installation took less than ten minutes.",
    "It was surprisingly beginner friendly.",
    "I had it secured and styled in under fifteen minutes.",
    "Much easier than installing a lace wig.",
    "The clips felt secure without pulling my hair.",
    "I wore it all day and it stayed in place.",
    "The cap was comfortable throughout the day.",
    "I didn't need any glue at all.",
    "Getting ready in the morning became so much faster.",
    "I can put it on before work in just a few minutes.",
    "It sits flat against my head and feels secure.",
    "The construction feels very sturdy."
],
        "results": [
            "Most people probably wouldn't notice, but I can tell they're extensions.",
            "The overall look is decent once styled properly.",
            "They add volume, which is what I wanted.",
            "The end result is okay but not amazing.",
        ],
        "extra": [
    "I've received several compliments while wearing it.",
    "A few people asked where I got my hair done.",
    "Nobody realized I was wearing a wig.",
    "It has become part of my regular rotation.",
    "I've worn it multiple times already.",
    "The style still looks great after several wears.",
    "I find myself reaching for this one often.",
    "The texture photographs really well.",
    "It blends nicely with my natural hair.",
    "I've been very pleased with how it wears throughout the day.",
    "The style works well for both casual and dressy occasions.",
    "It looks natural both indoors and outdoors." 
        ],
        "value": [
            "I've spent twice as much on extensions before and honestly these look better.",
            "Considering the quality, I expected them to cost much more.",
            "Not the cheapest option out there, but I'm happy with what I received.",
            "After wearing them for a few months, I definitely feel like I got my money's worth.",
            "The quality surprised me given the price point.",
            "I was hesitant because of the price at first, but I don't regret it.",
            "They've lasted much longer than some more expensive sets I've owned.",
            "For something I wear this often, the investment feels completely justified.",
            "I've already ordered another set, which probably says enough.",
            "The results were much better than I expected for what I paid.",
            "Honestly, these ended up being a better purchase than some salon treatments I've paid for.",
            "The price felt reasonable once I saw the quality in person.",
            "I would rather buy these again than spend more on a premium brand.",
            "They still look great months later, so I feel good about the purchase.",
            "Looking back, I wish I had bought them sooner.",
        ],
        "shipping": [
            "Shipping took a little longer than expected but it was absolutely worth the wait.",
            "Arrived faster than I thought it would.",
            "The order arrived right on time and was packaged beautifully.",
            "I was nervous ordering online but everything arrived perfectly.",
            "It took about three weeks to arrive but the quality made up for it immediately.",
            "The wait felt long but once I opened the package I understood why.",
        ],
        "support": [
            "Customer service was incredibly helpful when I had questions about color matching.",
            "The support team helped me pick the perfect shade.",
            "They responded to my email much faster than expected.",
            "Customer service was kind and patient throughout the process.",
            "I needed help choosing between two colors and they guided me perfectly.",
        ],
        "closer": [
            "100% buying another set, probably in a different length.",
            "Would recommend to literally anyone, just try them.",
            "Worth every single penny and then some.",
            "So glad I took the chance on these \U0001F60D",
            "Already telling all my friends about them.",
            "Don't overthink it, just get them.",
            "Will be a repeat customer for sure.",
            "Genuinely can't recommend these enough.",
            "Easily my best beauty purchase this year.",
            "Doing a happy dance over here, 10/10.",
            "If I could give six stars I would.",
            "Saving this shop to my favorites for sure.",
            "Just go for it, you won't regret it.",
            "These have my whole heart, ordering again soon.","Really happy with this purchase.",
    "I'd definitely buy this again.",
    "Would absolutely recommend it.",
    "I'll probably order another one.",
    "So glad I decided to try it.",
    "This will definitely stay in my rotation.",
    "Exactly what I was hoping for.",
    "Very satisfied overall.",
    "One of my favorite hair purchases so far.",
    "I'd recommend it to anyone looking for a natural everyday wig."

        ],
    },
    "Neutral": {
        "opener": [
            "So... I have mixed feelings about these honestly.",
            "They're fine I guess, just not what I was picturing.",
            "Wanted to love these but I'm kind of on the fence.",
            "Not bad, not amazing, somewhere right in the middle.",
            "Decent enough for the price, with a couple of buts.",
            "Torn on these ones, there's good and bad.",
            "They're alright, just didn't wow me the way I hoped.",
            "Okay so it's a yes and a no for me.",
            "I really wanted to love these but it's complicated.",
        ],
        "quality": [
            "The hair is soft but it's SO shiny it almost looks fake in certain light.",
            "Quality's okay, though the wefts are thinner than I hoped.",
            "They shed a bit more than I'd like, found strands here and there.",
            "Feels a little different from my real hair, can't quite explain it.",
            "It's about what you'd expect for the money, nothing more.",
            "Soft at first but got a little dry after a couple washes.",
            "Decent thickness up top but it thins out toward the ends.",
            "Holds a curl okay but drops faster than my natural hair.", "The hair quality itself was actually pretty nice.",
    "The wig feels soft and well made.",
    "The density looked natural enough.",
    "The construction seemed solid overall.",
    "The hair was smooth and easy to style.",
    "I didn't have any issues with shedding.",
    "The wig felt comfortable throughout the day.",
    "The quality wasn't the problem for me.",
        ],
        "color": [
    "The shade ended up being slightly darker than I expected.",
    "The color looked a little different in person than it did online.",
    "The quality was nice but the color wasn't quite right for me.",
    "I had some trouble getting the color to blend with my hair.",
    "The shade was close, just not close enough for a seamless blend.",
    "The color wasn't bad, it just didn't work with my hair tone.",
    "I expected the color to be a little lighter.",
    "The wig looked nice overall, but the color wasn't what I anticipated.",
    "The shade was slightly off compared to the product photos.",
    "I think a different color would have worked better for me.",
    "The blend would have been much better if the color matched more closely.",
    "The color difference was more noticeable in natural light."
],
        "fit_usage": [
            "Clipping them in is easy enough, no complaints there.",
            "The clips are kinda bulky though, you can feel them a bit.",
            "Takes some fiddling to get them to blend right.",
            "Needed a bit of work before they looked believable.",
            "The clips dig in a little if I wear them all day.",
            "Had to trim them a bit to get a natural shape.",
        ],
        "results": [
            "The end result is alright, not quite what I pictured.",
            "Adds some volume but the look is just okay.",
            "Decent once styled, but I can tell up close.",
            "Does what it says, nothing wow about the result.",
        ],
        "extra": [
            "I'll probably keep them for occasional use rather than daily.",
            "Might work better on someone with thicker hair than mine.",
            "Returned my first set and the second was a bit better.",
            "They're fine for photos but I can tell up close in person.",
            "Wish they'd included a few extra clips honestly.",
            "Texture isn't bad but it's not the wow I see in other reviews.",
        ],
        "value": [
            "For the price it's about what you'd expect, no more.",
            "Not sure it's worth it, but it's not a rip-off either.",
            "Okay value, I've seen better for similar money.",
            "Fair price I guess, just don't expect premium.",
        ],
        "shipping": [
            "Shipping took longer than I expected honestly.",
            "Arrived on time, packaging was pretty basic though.",
            "Delivery was fine, nothing fast but nothing terrible.",
            "Took a couple weeks to show up, just so you know.",
        ],
        "support": [
            "Reached out with a question and the reply was okay, a bit slow.",
            "Customer service was fine, nothing that stood out.",
            "Got my answer eventually, took a little while.",
        ],
        "closer": [
            "Fine for the odd occasion, just not an everyday thing for me.",
            "For the price I can't really complain too hard.",
            "Wouldn't say I'm wowed, but they do the job.",
            "Ended up ordering a second pack to get enough coverage.",
            "They're okay, might shop around next time though.",
            "Not sure I'd repurchase, but they're not bad either.",
            "Three stars feels about right, decent but not special.",
            "Middle of the road, they're neither great nor terrible.",
            "Would consider another brand before reordering these.",
        ],
    },
}

# Một số review "một câu" cụt ngủn (giống phân bố review thật)
SHORT_BODIES = {
    "Positive": [
       "Very happy with this purchase.",
    "The texture is beautiful and natural looking.",
    "Soft hair and easy to wear.",
    "Looks just like the photos.",
    "Great quality for the price.",
    "Very easy to install.",
    "The waves are beautiful.",
    "Comfortable and natural looking.",
    "Would definitely purchase again.",
    "The hair feels soft and realistic.",
    "Exactly what I was looking for.",
    "Beautiful texture and very easy to manage.",
    "Blends really well.",
    "The quality exceeded my expectations.",
    "One of my favorite wigs so far."
],
    "Neutral": [
    "Nice quality, just not the right color for me.",
    "The shade was slightly off but the hair felt nice.",
    "Good wig overall, color just didn't blend well.",
    "Quality was great, color wasn't.",
    "The wig was nice but the shade looked different in person.",
    "Would probably try another color next time.",
    "Not a bad wig, just the wrong shade for my hair.",
    "The color match didn't work out for me.",
    "Everything was fine except the color.",
    "Hair was nice, color wasn't quite right."
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
# STORY-BASED BANKS - các mảnh ghép kể chuyện mua hàng (dùng chung 2 sắc thái)
# ----------------------------------------------------------------------------
LIFE_EVENTS = [
    "I bought these for my wedding and they photographed beautifully.",
    "I got these for prom and honestly they made me feel so much more confident.",
    "After having my second baby my hair started thinning and these helped a lot.",
    "I've been dealing with hair loss recently so I wanted something to add volume.",
    "I ordered these for a family vacation and ended up wearing them almost every day.",
    "My natural hair has gotten thinner over the last few years so I wanted some extra fullness.",
    "I needed something quick for an event and these worked perfectly.",
    "I bought these for engagement photos and they looked amazing on camera.",
    "I wanted longer hair without committing to permanent extensions.",
    "I've always had fine hair so I was looking for extra thickness.",
]

HAIR_SITUATIONS = [
    "My hair is naturally pretty thin.",
    "I have shoulder length hair and wanted more volume.",
    "I've always struggled with fine hair.",
    "My hair started shedding a lot this year.",
    "I have thick hair but wanted extra length.",
    "My ends have been looking really thin lately.",
    "I wanted fuller hair without damaging my natural hair.",
    "I've been trying to grow my hair out but it's taking forever.",
]

PRODUCT_DETAILS = [
    "I ordered the 22 inch version.",
    "I went with the 24 inch set.",
    "I chose Chocolate Brown.",
    "I picked Neutral Brown and it matched surprisingly well.",
    "I ordered Platinum Blonde.",
    "My hair is naturally dark brown.",
    "I have fine hair and was worried the clips would show.",
]

MINOR_CONS = [
    "The color looked a little darker in person but blended fine.",
    "It took me a couple tries to get the placement right.",
    "I probably should have ordered a second pack for extra volume.",
    "The clips felt bulky at first but I got used to them.",
    "I wish I had gone one shade lighter.",
    "The ends were slightly thinner than I expected.",
    "The first time putting them in took some practice.",
    "I had to trim them slightly to blend better with my haircut.",
]

RESULTS = [
    "Nobody could tell I was wearing extensions.",
    "The blend was seamless and looked completely natural.",
    "I got so many compliments on my hair.",
    "My stylist was impressed with the quality.",
    "Even my husband noticed the difference.",
    "They looked amazing in photos.",
    "The extra volume made such a difference.",
    "They gave me the long hair I've always wanted.",
]

RECOMMENDATIONS = [
    "I'd definitely buy these again.",
    "Really happy with this purchase.",
    "Would absolutely recommend them.",
    "Worth every penny in my opinion.",
    "I'll probably order another set.",
    "So glad I decided to try them.",
    "I'd recommend them to anyone wanting more volume.",
    "Definitely one of my better beauty purchases.",
]


def build_body(sentiment):
    # ~12% là review ngắn một câu (giống phân bố thật)
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

    d1, d2 = st.columns(2)
    d1.download_button("⬇️ Tải CSV", data=csv, file_name="reviews.csv",
                       mime="text/csv", type="primary", use_container_width=True)
    d2.download_button("⬇️ Tải JSON", data=json_str.encode("utf-8"),
                       file_name="reviews.json", mime="application/json",
                       use_container_width=True)
else:
    st.info("👈 Cấu hình ở thanh bên rồi bấm **Sinh dữ liệu** để bắt đầu.")
