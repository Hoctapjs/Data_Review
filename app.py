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
        "fit_usage": [
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
        "results": [
            "Most people probably wouldn't notice, but I can tell they're extensions.",
            "The overall look is decent once styled properly.",
            "They add volume, which is what I wanted.",
            "The end result is okay but not amazing.",
        ],
        "extra": [
            "I've struggled with thinning hair for years, so this meant a lot to me.",
            "It helped me feel more like myself again.",
            "I felt confident walking into an event without worrying about my hair.",
            "For the first time in a long while, I actually enjoyed styling my hair.",
            "It made a noticeable difference in how I felt about my appearance.",
            "I wasn't expecting such a boost in confidence.",
            "Getting compliments again felt really nice.",
            "I finally stopped stressing about my hair every morning.",
            "It helped me feel polished and put together.",
            "I wish I had found this sooner.",
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


BODY_SECTIONS = [
    ("shipping",  0.25),   # 20-30%
    ("support",   0.20),   # 15-25%
    ("quality",   0.90),   # 90%
    ("color",     0.60),   # 50-70%
    ("fit_usage", 0.70),   # 60-80%
    ("results",   0.80),   # 70-90%
    ("extra",     0.25),   # 20-30%
    ("value",     0.35),   # 30-40%
]


def build_body(sentiment):
    # ~10% là review ngắn một câu (giống phân bố thật)
    if random.random() < 0.10:
        return random.choice(SHORT_BODIES[sentiment])

    bank = BODY_BANK[sentiment]
    parts = [random.choice(bank["opener"])]
    for key, prob in BODY_SECTIONS:
        if random.random() < prob:
            parts.append(random.choice(bank[key]))
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
