# -*- coding: utf-8 -*-
"""
Web app sinh dữ liệu review sản phẩm (tiếng Anh) - Bản nâng cấp siêu đa dạng cho Straight V-Part Wig.
"""
import random
from datetime import date, timedelta
from io import BytesIO

import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------------
# NGÂN HÀNG MẢNH GHÉP (tiếng Anh) - chuyên biệt cho Straight V-Part Wig
# ----------------------------------------------------------------------------
RATING = {"Positive": [5, 5, 5, 5, 4], "Neutral": [3, 3, 3]}

TITLE_TEMPLATES = {
    "Positive": [
        "Looks exactly like my real hair flat ironed",
        "Exactly what I was looking for in a V-part!",
        "Love that I don't need ANY leave-out",
        "The best glueless wig I've ever purchased",
        "Beautiful straight texture and no lace to cut",
        "The blend at the roots is absolutely amazing",
        "My go-to for a quick protective style",
        "One of my favorite glueless wigs ever",
        "Great quality and feels so real",
        "Super happy with this V-part wig purchase!",
        "Zero leave-out and still looks so natural",
        "Perfect for a sleek, bone-straight look",
        "Lightweight and doesn't pull on my edges",
        "Easy to install and stays put all day",
        "Exceeded my expectations for a no-leave-out wig",
        "Looks even better in person than the pics",
        "Sleek, shiny, and super easy to manage",
        "Love this V-part, so beginner friendly!",
        "Perfect instant length without messing with glue",
        "Would definitely buy again in a heartbeat",
        "The hair feels incredibly soft and silky",
        "So easy to put on and go",
        "Looks very realistic, the V-shape is perfect",
        "Comfortable to wear for 8+ hours",
        "Beautiful right out of the packaging",
        "A total game changer for quick glueless styles",
        "Got so many compliments!",
        "Saves me so much time in the morning",
        "Perfect color match for my natural roots",
        "Obsessed with this straight V-part!"
    ],
    "Neutral": [
        "Nice V-part wig but the color match was a bit off",
        "Good quality, just the wrong shade for my hair",
        "Cap is a bit big for smaller heads",
        "Wanted to love it but the V-opening was tricky to hide",
        "Quality was decent, but you have to style the roots to lay flat",
        "Close match but the clips can be uncomfortable",
        "Nice overall but didn't blend perfectly with my natural hairline",
        "The V-part opening is a bit too narrow for my liking",
        "Good hair, difficult color match",
        "Looks nice but it's a bit heavy on the clips",
        "A little too shiny out of the box, needed dry shampoo",
        "Okay for the price but tangles easily at the nape",
        "It's decent but the tracks near the V are a bit bulky",
        "Thinner than expected at the very ends",
        "It's okay, just takes some practice to secure the clips right without tension"
    ],
}

BODY_BANK = {
    "Positive": {
        "opener": [
            "I've been looking for a quick glueless V-part wig for a while and decided to risk it on this one.",
            "My natural edges are currently recovering from lace glue, so I needed a safe protective style.",
            "I needed something quick and sleek for work mornings when I don't have time to melt lace.",
            "I was tired of spending an hour trying to blend a U-part with my leave-out.",
            "I've tried a few different wigs before and wanted to see how this straight V-part compared.",
            "I purchased this right before a vacation because I wanted a completely glueless option.",
            "I wanted a style that gives me instant length without leaving any of my real hair out.",
            "After seeing a few 'no leave-out' tutorials online, I decided to give this V-part a try.",
            "I normally wear full lace wigs, but I wanted something way faster that lets my scalp breathe.",
            "I've been searching for a realistic, dead-straight V-part and finally hit the jackpot with this.",
            "I wanted a style that looked super polished and high-fashion without requiring adhesive.",
            "This was my very first time trying a V-part wig.",
            "I wanted something lightweight that wouldn't give me a tension headache from the clips.",
            "I ordered this because I wanted that sleek look without damaging my natural hair with flat irons.",
            "I needed a simple, throw-on-and-go hairpiece."
        ],
        "quality": [
            "The hair feels like healthy, salon-grade hair and flows beautifully.",
            "It moves and shakes just like real hair, no awkward stiffness at the tracks.",
            "The texture is super smooth, exactly like freshly flat-ironed hair.",
            "It doesn't have that cheap, blinding plastic shine.",
            "The strands are incredibly soft while still maintaining a realistic thickness.",
            "I was honestly impressed by how natural the fibers looked even up close.",
            "The ends look blunt and healthy instead of looking stringy or split.",
            "The hair handles low-heat styling perfectly fine.",
            "I ran a straightener through it on low heat and it got even sleeker.",
            "After comb-out and a bit of serum, it stayed incredibly soft and manageable.",
            "The sleek texture held up beautifully even after a long night out.",
            "The density feels completely natural—not too thin, but not ridiculously heavy either.",
            "The wig has a beautiful swing to it when I walk.",
            "It doesn't feel overly coated or greasy like some wigs I've ordered online.",
            "The quality feels premium, honestly mimicking much more expensive human hair brands."
        ],
        "color": [
            "The shade was an absolute perfect match to my natural roots.",
            "I was so nervous about the color blending at the part, but it looks flawless.",
            "The color looks incredibly natural in person.",
            "Because of the narrow V-shape, the color difference (if any) is totally hidden.",
            "The product photos on the listing gave a very accurate representation of the actual tone.",
            "The color looks even better and more vibrant when you step into natural sunlight.",
            "I had zero trouble matching this to my natural 1B hair color.",
            "The tone is realistic and has the right dark undertones without looking flat.",
            "The color match was spot on, which is usually rare for me when buying hair online.",
            "Once I styled the root area, the color blend looked totally seamless."
        ],
        "fit_usage": [
            "It literally takes me less than 2 minutes to clip it in and walk out the door.",
            "I love that I can wear this with absolutely ZERO leave-out.",
            "The clips grip tightly onto my braids without slipping down.",
            "The built-in combs and narrow V-shape feel incredibly secure.",
            "I didn't need to sew it down, use glue, or leave any hair out.",
            "It's so much more comfortable and breathable than wearing a lace front.",
            "The V-part section sits super flat against my head and doesn't look bulky.",
            "I wore it through a whole shift and didn't get a single headache from the clips.",
            "The cap inside is very breathable and lightweight.",
            "Installation is completely foolproof and beginner-friendly.",
            "I had my hair braided straight back, clipped this in, and was done in 5 minutes flat."
        ]
    },
    "Neutral": {
        "opener": [
            "So... I have slightly mixed feelings about this V-part wig.",
            "It's okay I guess, just wasn't exactly what I pictured in my head.",
            "I really wanted to love this wig but I'm kind of on the fence.",
            "Not terrible, but not mind-blowing either—somewhere right in the middle.",
            "Decent enough wig for a quick style, but it has a few drawbacks.",
            "I'm torn on this one; there are definitely pros and cons.",
            "It's an alright hairpiece, it just didn't wow me like the reviews said.",
            "Okay, so it's a bit of a hit and miss for me personally."
        ],
        "quality": [
            "The hair is soft, but it's SO shiny that it looks a little artificial in direct sunlight.",
            "The quality is just okay; the hair gets thin pretty quickly toward the ends.",
            "It sheds a bit more than I'd like when I run a wide-tooth comb through it.",
            "The tracks near the V-part feel a bit stiff at the roots.",
            "It's about what you'd expect for the price tag—nothing premium.",
            "It felt super silky at first but got a little dry and tangled at the nape after two wears.",
            "It has decent thickness at the crown, but the bottom half looks a bit skimpy.",
            "The hair texture is smooth, but it tangles easily underneath."
        ],
        "color": [
            "The shade ended up being a hair darker than what was shown in the pictures.",
            "The color tone looked a bit different in person compared to my screen.",
            "The quality of the piece is fine, but color matching is hard online.",
            "Even with no leave-out, you could see a slight contrast at my hairline.",
            "The shade was close, but it just had a slightly warmer undertone than my own hair.",
            "The color match wasn't quite seamless enough for me.",
            "The difference in color between my edges and the wig is noticeable in daylight."
        ],
        "fit_usage": [
            "Clipping it in is easy enough, but the cap feels a bit large for my head.",
            "The V-part opening is a bit stiff and takes some work to lay flat.",
            "It takes some serious fiddling with a hot comb to get the tracks to hide properly.",
            "If you have a smaller head, the cap might bunch up in the back.",
            "The clips near the part dig into my scalp a little bit after a few hours.",
            "Had to use my own stronger clips because the ones attached felt flimsy."
        ]
    },
}

LIFE_EVENTS = [
    "I bought this V-part for my birthday dinner and it photographed beautifully.",
    "I got this for a formal event and honestly it made me feel so sleek without a salon visit.",
    "After having a baby my edges thinned out, so this glueless option is a lifesaver.",
    "I've been dealing with heat damage, so I wanted an easy style with zero leave-out.",
    "I ordered this for a weekend trip and ended up wearing it every day because it's so easy.",
    "My natural hair is just past my shoulders, so I needed this for that dramatic long look.",
    "I needed something quick for a family photoshoot and this worked flawlessly.",
    "I bought this for a night out and the sleek straight hair looked stunning.",
    "I wanted long, straight hair without dealing with lace glue or sew-ins.",
    "I've always had fine hair, so I needed this extra fullness without stressing my roots."
]

HAIR_SITUATIONS = [
    "My hair is naturally pretty fine and short.",
    "I have shoulder-length hair and wanted a sleek long look.",
    "I've always struggled with melting lace fronts, so V-parts are my new obsession.",
    "I refuse to use glue on my edges anymore, so this was perfect.",
    "I have medium-thick hair but wanted that extra dramatic length down to my waist.",
    "I wanted a polished look without damaging my natural hair with flat irons.",
    "I've been trying to grow my hair out and just need a zero-manipulation protective style.",
    "I hate leaving my real hair out because of humidity, so the V-part is ideal."
]

PRODUCT_DETAILS = [
    "I ordered the 22-inch straight version.",
    "I went with the 24-inch extra long set.",
    "I chose the length that falls right around my mid-back.",
    "The length I picked matched my expectations perfectly.",
    "I was worried the cap would be too big, but the adjustable straps really helped.",
    "The narrow V-shape opening at the top was designed perfectly.",
    "I got the 18-inch because I wanted a more natural, everyday length."
]

MINOR_CONS = [
    "The color looked a tiny bit darker in my bathroom but looked fine under normal light.",
    "It took me a couple of tries to get the front clips placed right so it wouldn't bulge.",
    "It's a little bit heavy if you clip it onto very fine braids.",
    "The tracks at the V-opening felt a bit stiff at first but they softened up.",
    "I wish the clips were just a tiny bit smaller.",
    "The ends were a little thinner than the top, but a quick trim fixed it.",
    "I had to use a wax stick and hot comb to get the top to lay completely flat.",
    "I had to bobby pin the sides down to make sure it felt extra secure."
]

RESULTS = [
    "Nobody at the party could tell I was wearing a wig.",
    "The blend at the roots was seamless and looked like it was growing from my scalp.",
    "I got so many compliments on how sleek my hair looked.",
    "My friends were completely shocked when I told them it was a glueless V-part.",
    "Even my stylist noticed how flat and natural the install looked.",
    "It looked incredibly chic and high-end in all my pictures.",
    "The instant length and volume made such a massive difference.",
    "It lays incredibly flat at the roots once you press it with a hot comb."
]

RECOMMENDATIONS = [
    "I'd definitely buy from this brand again.",
    "Really happy with how this glueless wig turned out.",
    "Would absolutely recommend it if you want a break from lace.",
    "Worth every single penny in my opinion.",
    "I'll probably order another one in a curly texture just to have options.",
    "So glad I decided to give the no-leave-out method a try.",
    "I'd highly recommend this to anyone wanting a break from heat and adhesives.",
    "Definitely one of my best quick beauty purchases this year."
]

SHORT_BODIES = {
    "Positive": [
        "Very happy with this V-part wig, super sleek and glueless!",
        "The hair feels soft, straight, and I didn't even need leave-out.",
        "Looks exactly like the photos, love the instant length.",
        "Great quality straight wig and very easy to clip in.",
        "Stays secure all day long without hurting my scalp or edges.",
        "The way it lays flat at the roots is absolutely amazing.",
        "Easy to install, flat iron, and maintain. 5 stars!",
        "Beautiful silky straight texture. Exceeded my expectations.",
        "Would definitely buy another one again soon.",
        "Looks very realistic, no fake shine and no glue needed.",
        "The wig moves naturally and gives great volume.",
        "Perfect everyday wig for when I'm in a rush.",
        "Exactly what I was looking for to get that bone-straight look.",
        "Super comfortable, breathable cap, and beginner friendly.",
        "One of my favorite protective styles so far!"
    ],
    "Neutral": [
        "Nice quality wig, but the V-part was a little stiff at first.",
        "The shade was slightly off but the texture of the hair felt nice.",
        "Good wig overall, just takes some hot combing to lay flat.",
        "The hair quality was fine, but the cap size was too big.",
        "The wig was nice but the tracks at the top were a bit bulky.",
        "Would probably try a different brand next time.",
        "Not a bad hairpiece, just requires some styling effort at the roots.",
        "The color match didn't work out for me but it's decently made.",
        "Everything was fine with the clips except the cap was loose.",
        "Hair was quite smooth, but tangled easily at the back of the neck."
    ],
}

def build_title(sentiment):
    return random.choice(TITLE_TEMPLATES[sentiment])

def build_body(sentiment):
    if random.random() < 0.12:
        return random.choice(SHORT_BODIES[sentiment])

    parts = []
    
    # 80% kể sự kiện
    if random.random() < 0.8:
        parts.append(random.choice(LIFE_EVENTS))

    # Tình trạng tóc (luôn có)
    parts.append(random.choice(HAIR_SITUATIONS))

    # 70% chi tiết sản phẩm
    if random.random() < 0.7:
        parts.append(random.choice(PRODUCT_DETAILS))

    # Chất lượng (luôn có)
    parts.append(random.choice(BODY_BANK[sentiment]["quality"]))
    
    # 80% nói về màu sắc / độ hòa trộn
    if random.random() < 0.8:
        parts.append(random.choice(BODY_BANK[sentiment]["color"]))

    # 60% nói về cách sử dụng / form dáng
    if random.random() < 0.6:
        parts.append(random.choice(BODY_BANK[sentiment]["fit_usage"]))

    # Khuyết điểm nhỏ
    if sentiment == "Positive":
        if random.random() < 0.35:
            parts.append(random.choice(MINOR_CONS))
    else:
        parts.append(random.choice(MINOR_CONS))

    # Kết quả & Đề xuất (luôn có)
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
        return first                                         
    elif r < 0.67:
        return f"{first} {random.choice(_LAST_INITIALS)}."   
    else:
        return f"{first} {random.choice(_LAST_NAMES)}"       

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
# GIAO DIỆN STREAMLIT
# ----------------------------------------------------------------------------
def df_to_excel_bytes(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="reviews")
    return buffer.getvalue()

st.set_page_config(page_title="V-Part Wig Review Generator", page_icon="📝", layout="wide")
st.title("📝 Bộ sinh dữ liệu review - Straight V-Part Wig")
st.caption("Sinh review chuyên biệt cho tóc giả V-part (tập trung vào tính năng glueless, no leave-out).")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    so_dong = st.number_input("Số dòng cần sinh", min_value=1, max_value=1_000_000,
                              value=500, step=100)

    st.subheader("Sắc thái")
    dung_positive = st.checkbox("Positive (4-5★)", value=True)
    dung_neutral = st.checkbox("Neutral (3★)", value=True)

    ts_positive = st.slider("Trọng số Positive", 0, 100, 75, disabled=not dung_positive)
    ts_neutral = st.slider("Trọng số Neutral", 0, 100, 25, disabled=not dung_neutral)

    them_email = st.checkbox("Sinh email giả (reviewer_email)", value=False)

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

    st.subheader("Xem trước dữ liệu")
    st.dataframe(df.head(100), use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    json_str = df.to_json(orient="records", force_ascii=False, indent=2)
    xlsx = df_to_excel_bytes(df)

    d1, d2, d3 = st.columns(3)
    d1.download_button("⬇️ Tải CSV", data=csv, file_name="vpart_reviews.csv",
                       mime="text/csv", type="primary", use_container_width=True)
    d2.download_button("⬇️ Tải JSON", data=json_str.encode("utf-8"),
                       file_name="vpart_reviews.json", mime="application/json",
                       use_container_width=True)
    d3.download_button("⬇️ Tải Excel", data=xlsx, file_name="vpart_reviews.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True)
else:
    st.info("👈 Cấu hình ở thanh bên rồi bấm **Sinh dữ liệu** để bắt đầu.")
