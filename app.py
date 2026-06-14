# -*- coding: utf-8 -*-
"""
Web app sinh dữ liệu review sản phẩm (tiếng Anh) - bản cải tiến.
Schema khớp với JSON mẫu: title, body, rating, review_date, reviewer_name, reviewer_email.
Chạy:  streamlit run app.py
"""
import random
from datetime import date, timedelta
from io import BytesIO

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# NGÂN HÀNG MẢNH GHÉP (tiếng Anh) - ghép ngẫu nhiên -> hàng trăm nghìn tổ hợp
# 2 sắc thái: Positive (4-5★), Neutral (3★)
# ----------------------------------------------------------------------------
RATING = {"Positive": [5, 5, 5, 5, 4], "Neutral": [3, 3, 3]}

# --- TITLE: ghép từ template + ngân hàng tính từ ---------------------------
POS_ADJ = [
    "natural",
    "realistic",
    "comfortable",
    "soft",
    "lightweight",
    "smooth",
    "beautiful",
    "seamless",
    "easy",
    "flattering",
    "versatile",
    "well-made"
]
TITLE_TEMPLATES = {
    "Positive": [
    "Looks just like my real hair",
    "Exactly what I was looking for",
    "Love how natural it looks",
    "Very comfortable to wear",
    "Beautiful straight hair",
    "The blend is amazing",
    "Easy to wear every day",
    "One of my favorite wigs",
    "Great quality and natural looking",
    "Very happy with this purchase",
    "The hair moves so naturally",
    "Perfect for everyday wear",
    "Lightweight and comfortable",
    "Easy to install and style",
    "Exceeded my expectations",
    "Looks even better in person",
    "Natural looking and easy to manage",
    "Love this wig",
    "A great protective style",
    "Would definitely buy again",
    "The hair feels amazing",
    "So easy to blend",
    "Looks very realistic",
    "Comfortable all day",
    "Beautiful from the first wear"
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
   "I've been wearing wigs for a few years now and decided to try this one after seeing the reviews.",
    "My natural hair has gotten a little thinner over the years, so I wanted something that looked natural without damaging my hair further.",
    "I needed something quick for work every morning and this seemed like a good option.",
    "I was tired of spending so much time styling my own hair every day.",
    "I've tried several U Part Wigs before and wanted to see how this one compared.",
    "I purchased this before a family event and ended up loving it more than expected.",
    "I wanted a protective style that still looked like my own hair.",
    "After watching a few videos online, I decided to give this wig a try.",
    "I normally wear lace wigs, but I wanted something easier for everyday use.",
    "I've been searching for a realistic straight wig for a while and finally decided to order this one.",
    "I was looking for a style that looked polished without requiring much effort.",
    "This was my first time trying a U Part Wig.",
    "I wanted something lightweight that I could wear comfortably throughout the day.",
    "I ordered this because I wanted extra length without committing to extensions.",
    "I needed something simple that would blend naturally with my own hair."
],
        "quality": [
    "The hair feels like real healthy hair and blends naturally with my own.",
    "You can definitely tell it's human hair from the way it moves and feels.",
    "The texture feels very similar to my natural straightened hair.",
    "There isn't that synthetic shine that some wigs have.",
    "The hair feels soft while still looking realistic.",
    "I was impressed by how natural the strands looked up close.",
    "The ends look healthy and full instead of thin.",
    "The hair responds well to heat styling.",
    "I curled it once and the style held surprisingly well.",
    "After washing it, the hair remained soft and manageable.",
    "The texture still looked beautiful after several wears.",
    "The density feels natural and not overly heavy.",
    "The strands move naturally when I walk.",
    "It doesn't feel overly processed like some human hair wigs I've tried.",
    "The quality reminds me of much more expensive wigs."
        ],
        "color": [
    "The color looked very close to the product photos.",
    "I was nervous about ordering online, but the shade matched what I expected.",
    "The color looked natural in person.",
    "The shade blended well with my own hair.",
    "The listing photos were a pretty accurate representation.",
    "The color looked even better in natural lighting.",
    "I had no trouble blending the shade with my hair.",
    "The tone looked realistic and not overly flat.",
    "The color was exactly what I hoped it would be.",
    "The shade looked very natural once installed."
],
        "fit_usage": [
    "It only took me a few minutes to install.",
    "Getting ready in the morning is much faster now.",
    "I like that I can take it off at night whenever I want.",
    "The clips feel secure without pulling on my hair.",
    "I didn't need any glue or complicated styling.",
    "It's much easier than wearing a lace wig every day.",
    "The wig sits flat against my head and feels secure.",
    "I wore it all day without any discomfort.",
    "The cap feels lightweight and breathable.",
    "It has become my go-to protective style.",
    "Installation was very beginner friendly.",
    "I had it blended and ready in less than ten minutes."
],
        "results": [
            "Most people probably wouldn't notice, but I can tell they're extensions.",
            "The overall look is decent once styled properly.",
            "They add volume, which is what I wanted.",
            "The end result is okay but not amazing.",
        ],
        "extra": [
    "Several people assumed it was my real hair.",
    "My hairstylist was impressed with how natural it looked.",
    "I've already worn it to work multiple times.",
    "This has become my favorite everyday hairstyle.",
    "I received compliments the first day I wore it.",
    "A coworker asked if I had done something different with my hair.",
    "The blend looked even better after I trimmed my leave out.",
    "I find myself reaching for this wig more than any other one I own.",
    "It photographs really well without looking overly shiny.",
    "Nobody could tell where my hair ended and the wig began.",
    "I appreciate how natural it looks in daylight.",
    "I've worn it for long days and it stayed comfortable."
        ],
        "value": [
            "For the price, I honestly think the quality is very good.",
    "I've paid more for wigs that weren't nearly as nice as this one.",
    "The quality exceeded what I expected at this price point.",
    "It feels like a much more expensive wig.",
    "I think this was a great value for the money.",
    "Considering the quality of the hair, the price felt very reasonable.",
    "I've purchased higher-priced wigs before and this one compares surprisingly well.",
    "The construction and hair quality make it feel worth the investment.",
    "I feel like I got exactly what I paid for, if not more.",
    "For everyday wear, this is a great option without spending a fortune."
        ],
        "shipping": [
           "My order arrived sooner than expected.",
    "Shipping was faster than I anticipated.",
    "The wig arrived well packaged and in good condition.",
    "Everything was packed neatly and securely.",
    "I was happy with how quickly my order was processed.",
    "The packaging kept everything looking great during shipping.",
    "My package arrived right on schedule.",
    "The wig was ready to wear straight out of the package.",
    "Delivery was smooth and hassle free.",
    "I appreciated the careful packaging."
        ],
        "support": [
            "Customer service was very helpful when I had a question before ordering.",
    "The support team responded quickly to my inquiry.",
    "I appreciated how helpful customer service was.",
    "Communication throughout the process was excellent.",
    "The seller was very responsive and professional.",
    "I received a quick response when I needed assistance.",
    "The company made the entire experience easy.",
    "Customer support answered my questions clearly.",
    "It was nice knowing help was available if needed.",
    "The service matched the quality of the product."
        ],
        "closer": [
  "Overall I'm very happy with my purchase.",
    "I'd definitely purchase this again.",
    "I would recommend it to anyone looking for a natural everyday style.",
    "This has been one of my better wig purchases.",
    "I'm glad I decided to give it a try.",
    "It was worth the investment for me.",
    "I can see myself ordering another one in the future.",
    "It has exceeded my expectations so far.",
    "Very satisfied with the quality overall.",
    "I'd happily recommend it to friends and family."
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
    "The hair feels soft and natural.",
    "Looks just like the photos.",
    "Great quality and easy to wear.",
    "Very comfortable all day.",
    "The blend is amazing.",
    "Easy to install and maintain.",
    "Beautiful straight texture.",
    "Would definitely buy again.",
    "Looks very realistic.",
    "The hair moves naturally.",
    "Great everyday wig.",
    "Exactly what I was looking for.",
    "Comfortable and natural looking.",
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
