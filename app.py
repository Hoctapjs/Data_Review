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
POS_ADJ = ["gorgeous", "soft", "natural", "thick", "beautiful", "amazing",
           "flawless", "stunning", "perfect", "lush", "silky", "full"]
TITLE_TEMPLATES = {
    "Positive": [
        "Perfect color match for me", "Best extensions I've ever tried, no joke",
        "Okay these exceeded my expectations", "So so happy with these",
        "Worth every penny tbh", "Just get them, seriously", "Don't hesitate, just try them",
        "Obsessed \U0001F60D", "These are {adj1} !!!", "{adj1} and so {adj2}",
        "{adj1} quality for the price", "Honestly {adj1}",
        "Blends in and looks {adj1}", "{adj1}, {adj2}, and so natural",
        "Cannot get over how {adj1} these are",
    ],
    "Neutral": [
        "Decent but not perfect", "Okay for the price I guess", "Mixed feelings about these",
        "Good but a few annoying issues", "Average overall", "It's fine, nothing special",
        "Pretty but a bit {flaw}", "Nice color but kinda {flaw}",
        "Does the job, but {flaw}", "{adj1} enough, with some downsides",
    ],
}
NEU_MILD_ADJ = ["Decent", "Okay", "Fine", "Acceptable", "Average"]
NEU_FLAW = ["thin", "shiny", "shed-prone", "pricey", "stiff"]

# --- BODY: mỗi sắc thái có nhiều nhóm câu, mỗi câu đứng độc lập -------------
BODY_BANK = {
    "Positive": {
        "opener": [
            "Okay I'm obsessed with these, not gonna lie.",
            "So I've been on a bit of a hair journey and these were such a win.",
            "Honestly wasn't expecting much for the price but wow.",
            "I bought these for my sister's wedding and ended up keeping them for everyday lol.",
            "Been eyeing these for weeks and finally caved... no regrets!",
            "First time trying clip-ins and I'm kicking myself for not doing it sooner.",
            "Ordered the 22 inch in a darker brown and I'm in love.",
            "My natural hair has been thinning lately so I took a chance on these.",
            "Ngl I almost didn't order because of the price, so glad I did.",
            "Used to drop $300+ on extensions, these are honestly just as good.",
            "Bought these for prom and ended up wearing them every weekend since.",
            "I've tried so many brands and these are the ones I keep coming back to.",
            "Got these for a trip and they were a total game changer.",
            "My hairdresser actually asked where I got these, that says it all.",
            "Second time ordering from this shop and they never disappoint.",
            "Was super skeptical reading mixed reviews but mine came out perfect.",
        ],
        "quality": [
            "The hair is SO soft, like it genuinely feels like my own.",
            "Quality is unreal for what I paid, I keep telling everyone.",
            "They're thick from top to bottom, not that thin scraggly weft situation.",
            "Real human hair so I can curl it, straighten it, whatever, and it just holds up.",
            "I've washed them a few times now and they still look brand new tbh.",
            "Texture matches mine almost exactly, which never happens for me.",
            "No weird plastic shine, they look like actual hair which is rare.",
            "They don't tangle at all, even after a windy day out.",
            "Honestly thicker than I expected from the photos, in a good way.",
            "Dyed them a shade darker and they took the color beautifully.",
            "Three months in and they've held up way better than my last set.",
            "The wefts are full all the way to the ends, no thinning out.",
        ],
        "color": [
            "The color match was spot on, my stylist couldn't even tell.",
            "They blend in so well that no one has a clue I'm wearing them.",
            "Color is exactly like the photos, which honestly surprised me.",
            "I was nervous about the shade but it disappeared right into my hair.",
            "Got so many compliments and nobody believes it's not all mine.",
            "Picked the neutral brown and it matched on the first try, shocking.",
            "Blends seamlessly even though my hair has a bit of an ombre going on.",
            "The roots are a touch darker which actually helps it look natural.",
            "My mom couldn't tell where my hair ended and the extensions started.",
        ],
        "usage": [
            "Clipped them in straight out of the box, didn't even style them, and they looked amazing.",
            "The clips actually hold, they don't slide around all day like cheaper ones.",
            "Took me like 5 minutes to put in once I got the hang of it.",
            "They hold a curl forever, even after sleeping on them.",
            "Came packaged really nicely with a couple extra clips too, nice touch.",
            "Love that I can just take them out before bed, so low maintenance.",
            "Wore them dancing all night and not one clip budged.",
            "So easy to wash and dry compared to the sew-ins I used to have.",
            "Heat styling them is no problem, curls last me two whole days.",
            "Came with a little gift and a thank you note, such a sweet touch.",
        ],
        "extra": [
            "Wore them for 12 hours straight and forgot they were even in.",
            "My only regret is not ordering them sooner.",
            "I sleep in them sometimes and they're totally fine the next morning.",
            "Even my husband noticed and he never notices anything lol.",
            "I keep finding excuses to wear them, even just running errands.",
            "Customer service answered my sizing question within an hour too.",
            "Shipping was way faster than I expected, came in two days.",
            "Bought a second set in a lighter shade for summer already.",
            "They survived a beach trip with salt water and everything.",
            "Honestly looks better than the $400 ones my friend has.",
            "I've gotten stopped twice asking what my 'natural' hair routine is.",
            "Took photos for a friend who didn't believe they were clip-ins.",
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
            "These have my whole heart, ordering again soon.",
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
            "Holds a curl okay but drops faster than my natural hair.",
        ],
        "color": [
            "Color's close but not an exact match, slightly off from the pics.",
            "Looks fine once it's styled, but straight out the bag it's a bit much.",
            "The shade is nice but doesn't read super natural to me.",
            "Had to tone it down a little to get it to blend properly.",
            "Came out darker than the website photo, just a heads up.",
            "Blends okay from far away but up close you can sort of tell.",
        ],
        "usage": [
            "Clipping them in is easy enough, no complaints there.",
            "The clips are kinda bulky though, you can feel them a bit.",
            "Takes some fiddling to get them to blend right.",
            "Needed a bit of work before they looked believable.",
            "The clips dig in a little if I wear them all day.",
            "Packaging was pretty basic, nothing extra included.",
            "Shipping took longer than I expected too.",
            "Had to trim them a bit to get a natural shape.",
        ],
        "extra": [
            "I'll probably keep them for occasional use rather than daily.",
            "Might work better on someone with thicker hair than mine.",
            "Returned my first set and the second was a bit better.",
            "They're fine for photos but I can tell up close in person.",
            "Wish they'd included a few extra clips honestly.",
            "Texture isn't bad but it's not the wow I see in other reviews.",
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
        "Super thick and great quality.", "Best hair extensions I've ever tried. Thanks \U0001F60D",
        "Perfect \U0001F60D", "Love them, exactly as described.", "Soft, full, and gorgeous.",
        "Matched my color perfectly, so happy.", "Obsessed. Buying more.",
        "Exactly what I wanted, would buy again.", "10/10 would recommend.",
        "Gorgeous hair, blends like a dream.", "Better than I hoped, honestly.",
        "These are everything, so soft!", "Couldn't be happier with them.",
        "Amazing quality for the price.", "Look completely natural, love it.",
        "Fast shipping and beautiful hair.", "My new favorite, hands down.",
        "Thick, soft, perfect match. Done.", "Worth it, just buy them.",
        "So pretty and easy to use \U0001F60D", "Five stars, no notes.",
    ],
    "Neutral": [
        "They're okay, nothing special.", "Decent for the price I suppose.",
        "Bit shiny but otherwise fine.", "Alright, expected a little more.",
        "Does the job, not amazing though.", "Fine, but kinda thin.",
        "Color was slightly off for me.", "Good enough, not great.",
        "Average, would've liked more hair.", "Okay quality, a touch shiny.",
        "Middle of the road honestly.", "They're fine, nothing to write home about.",
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


MIDDLE_CATS = ["quality", "color", "usage", "extra"]


def build_body(sentiment):
    # ~10% là review ngắn một câu (giống phân bố thật)
    if random.random() < 0.10:
        return random.choice(SHORT_BODIES[sentiment])

    bank = BODY_BANK[sentiment]
    # luôn có opener + closer, chọn ngẫu nhiên 2-4 câu giữa (giữ đúng thứ tự)
    chosen = set(random.sample(MIDDLE_CATS, random.randint(2, 4)))
    order = [c for c in MIDDLE_CATS if c in chosen]

    parts = [random.choice(bank["opener"])]
    parts += [random.choice(bank[c]) for c in order]
    parts.append(random.choice(bank["closer"]))
    return " ".join(parts)

REVIEWER_NAMES = [
    "Amazon Customer", "RyB", "Andres Alomia", "Bella", "Julien", "Nicole", "Sara",
    "Zoey Lebrun", "Rachel Moriel", "Emily R.", "Jessica M.", "Hannah", "Olivia Grace",
    "Sophie T.", "Megan", "Chloe", "Ashley", "Grace W.", "Lauren", "Mia",
]


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
            "reviewer_name": random.choice(REVIEWER_NAMES),
            "reviewer_email": "" if not them_email
            else f"{random.choice(REVIEWER_NAMES).split()[0].lower()}{random.randint(1, 999)}@example.com",
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
