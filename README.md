# VPN Master برای اندروید 🛡️

کلاینت کامل و واقعی VPN برای اندروید — ساخته‌شده روی هستهٔ **sing-box**
(همان هسته‌ای که NekoBox / SFA / v2rayNG با آن کار می‌کنند). نه وب‌ویو، نه شبیه‌سازی:
اتصال از طریق `VpnService` سیستمی و رابط `TUN` انجام می‌شود.

| | |
|---|---|
| نام برنامه | **VPN Master** |
| شناسهٔ پکیج | `com.vpnmaster.app` (کنار SFA اصلی هم نصب می‌شود) |
| نسخه | `1.0.0` |
| حداقل اندروید | 7.0 (API 24) — واریانت `otherLegacy` برای اندروید 5 به بالا |
| هسته | sing-box (libbox) — همهٔ پروتکل‌ها |
| رابط کاربری | فارسی (و ۲۰+ زبان دیگر) |
| مجوز | GPL-3.0 (متن در `LICENSE`) |

## چه چیزهایی دارد؟

- **همهٔ پروتکل‌ها**: Shadowsocks, VMess, VLESS (+Reality), Trojan, Hysteria2, TUIC,
  WireGuard, SSH, AnyTLS, ShadowTLS, HTTP/SOCKS, Tor, NaiveProxy …
- **ورود کانفیگ از هر جایی**: لینک `vless://`، `vmess://`، `ss://`، `trojan://`،
  `hysteria2://`، `tuic://`، سابسکریپشن (URL)، فایل JSON، اسکن QR
- **حالت TUN** (تمام ترافیک گوشی) + حالت **Proxy** (فقط اپ‌های انتخابی)
- **پروکسی per-app**: انتخاب اینکه کدام برنامه‌ها از VPN رد شوند
- **مسیر‌دهی (Routing)**: قواعد دامنه/IP، بلاک تبلیغات، split-tunnel
- **DNS سفارشی**، IP‌ست، تست سرعت و latency، انتخاب خودکار سرور (urltest)
- کاشی (Quick Settings Tile)، شروع خودکار در بوت، ضبط لاگ برای عیب‌یابی

## چطور APK بسازم؟

این مخزن **سورس کامل + کامپایل خودکار ابری** است. کامپایل اپ اندروید به
Android SDK، NDK و رم زیاد نیاز دارد؛ به همین دلیل یک Workflow آماده گذاشته شده
که گیت‌هاب در چند کلیک برایت APK امضاشده می‌سازد (رایگان؛ اولین اجرا ۳۰ تا ۶۰ دقیقه،
چون هستهٔ Go با NDK از صفر کامپایل می‌شود؛ اجراهای بعدی با cache سریع‌تر است).

### روش ۱ — گیت‌هاب (پیشنهادی، بدون نصب هیچ‌چیزی)

1. فایل ZIP این پروژه را از حالت فشرده خارج کن.
2. در [github.com/new](https://github.com/new) یک مخزن **Private** یا Public بساز
   (مثلاً `vpn-master`). هیچ گزینه‌ای را تیک نزن.
3. در صفحهٔ مخزن: **Add file → Upload files** → همهٔ فایل‌ها و پوشه‌ها را
   با کشیدن و رها کردن آپلود کن → **Commit changes**.
   > پوشهٔ `.github` هم باید آپلود شود (اگر پنهان است، در ویندوز
   > View → Show → Hidden items را روشن کن).
   >
   > راه جایگزین (Git):
   > ```bash
   > git init && git add -A
   > git commit -m "VPN Master"
   > git branch -M main
   > git remote add origin https://github.com/USERNAME/vpn-master.git
   > git push -u origin main
   > ```
4. برو به تب **Actions** → اگر پیام تأیید دیدی **I understand my workflows, go ahead** را بزن.
5. از ستون چپ **Build VPN Master APK** → دکمهٔ **Run workflow** → **Run workflow**.
6. صبر کن تا علامت ✅ سبز ظاهر شود (اولین اجرا ~۳۰ تا ۶۰ دقیقه، چون هسته از صفر کامپایل می‌شود).
   اگر توی این مرحله خطای API بین هسته و اپ دیدی، دوباره Run workflow بزن و ورودی
   `sing_box_ref` را از `testing` به `stable` عوض کن.
7. همان صفحه پایین: بخش **Artifacts** → **VPNMaster-APK** را دانلود کن.
   داخلش چند APK هست:
   - `VPNMaster-1.0.0-arm64-v8a.apk` ← **برای ۹۵٪ گوشی‌ها این را نصب کن**
   - `VPNMaster-1.0.0-armeabi-v7a.apk` ← گوشی‌های قدیمی ۳۲ بیتی
   - `VPNMaster-1.0.0-universal.apk` ← اگر مطمئن نیستی (حجم بیشتر)
   - `x86`, `x86_64` ← شبیه‌ساز

**نکتهٔ امنیتی:** اگر Secret تعریف نکنی، گیت‌هاب یک کلید امضای موقت می‌سازد؛
برای اینکه آپدیت‌های بعدی روی همان اپ نصب شوند، یک‌بار کلید بساز و در Secrets بگذار:

```bash
keytool -genkeypair -keystore release.keystore -storetype PKCS12 -alias vpnmaster \
  -storepass YOURPASS -keyalg RSA -keysize 4096 -validity 10950 -dname "CN=VPN Master"
base64 -w0 release.keystore     # ویندوز: certutil -encode release.keystore out.txt
```
سپس در مخزن: **Settings → Secrets and variables → Actions → New repository secret**:
`KEYSTORE_BASE64`، `KEYSTORE_PASS`، `ALIAS_NAME`، `ALIAS_PASS`.
اگر کلید را عوض نکنی، اندروید اجازهٔ آپدیت روی نسخهٔ قبلی را نمی‌دهد و باید اپ را حذف/نصب کنی.

### روش ۲ — Android Studio روی کامپیوتر خودت

پیش‌نیاز: JDK 17، Go، Android SDK با NDK `28.0.13004108`، آزاد ~۲۰ گیگابایت فضای دیسک.

```bash
# ۱) هسته
git clone --depth 1 https://github.com/SagerNet/sing-box
cd sing-box && make lib_install && make lib_android
#    خروجی: libbox.aar و libbox-legacy.aar
mkdir -p ../vpn-master/app/libs
cp libbox.aar libbox-legacy.aar ../vpn-master/app/libs/

# ۲) کلید امضا (همیشه همین کلید را نگه دار)
cd ../vpn-master
keytool -genkeypair -keystore app/release.keystore -storetype PKCS12 -alias vpnmaster \
  -storepass YOURPASS -keyalg RSA -keysize 4096 -validity 10950 -dname "CN=VPN Master"

# ۳) رمزها
cat > local.properties <<EOF
KEYSTORE_PASS=YOURPASS
ALIAS_NAME=vpnmaster
ALIAS_PASS=YOURPASS
EOF

# ۴) ساخت
./gradlew :app:assembleOtherRelease
# خروجی: app/build/outputs/apk/other/release/
```
یا ساده‌تر: پوشه را در Android Studio باز کن (Open → پوشهٔ پروژه) و
Build → Generate Signed App Bundle / APK.

### روش ۳ — خط فرمان روی لینوکس/مک

همان گام‌های روش ۲؛ فقط `ANDROID_HOME` و `ANDROID_NDK_HOME` را ست کن.

## بعد از نصب: چطور وصل شوم؟

اپ خودش سرور ندارد و ندارد که داشته باشد؛ روی هر سروری که داری کار می‌کند:

- **از اپ ویندوز VPN Master**: در تب «گوشی اندروید» آدرس سابسکریپشن
  (`http://192.168.x.x:2081/sub`) یا QR را بگیر → در اپ اندروید:
  **پروفایل‌ها ← + ← Import from URL / Scan QR**
- **لینک دستی**: هر لینکی که از سرویس‌دهنده‌ات داری را پیست کن؛ خودش تشخیص می‌دهد.
- **فایل کانفیگ**: `config.json` (sing-box) را از فایل اضافه کن.
- سپس روی دکمهٔ اتصال بزن؛ اولین بار اندروید اجازهٔ VPN می‌خواهد → **OK**.

راهنمای کامل ساخت سرور هم در پوشهٔ اپ ویندوز (`server/install-server.sh`) هست.

## چه چیزی نسبت به اپ اصلی (SFA) عوض شده؟

- نام نمایشی: `VPN Master` (همهٔ رشته‌های رابط کاربری)
- `applicationId`: `com.vpnmaster.app` (به‌جای `io.nekohasekai.sfa`) → نصب مستقل و کنار اپ اصلی
- آیکون تازه (سپر + تیک، سبز/تیره) در ۵ اندازه + آیکون تطبیقی (adaptive) و مونوکروم
- رنگ پس‌زمینهٔ آیکون `#0D1119`، نام فایل خروجی `VPNMaster-1.0.0`
- نسخه `1.0.0` و `VERSION_CODE=1`
- Workflow ساخت APK در `.github/workflows/build-apk.yml`
- بقیهٔ کد هسته و رابط کاربری دست‌نخورده مانده (پایدار و تست‌شده)

> تغییر پکیج با کلید «namespace» انجام شده است؛ کلاس‌های Kotlin سر جای خودشان
> هستند (`io.nekohasekai.sfa`) تا هیچ رفرنس کد/منیفست نشکند — این دقیقاً همان
> روش استاندارد اندروید است (`applicationId` ≠ `namespace`).

## عیب‌یابی

| خطا | راه‌حل |
|---|---|
| `android SDK not found` | `ANDROID_HOME` ست نیست؛ در Actions خودش ست می‌شود |
| `java version should be openjdk 17` | برای ساخت libbox با JDK 17 اجرا کن (در Workflow گام ۲) |
| `Could not find libs/libbox.aar` | گام ساخت هسته اجرا نشده؛ فایل را در `app/libs/` بگذار |
| خطای API بین libbox و اپ | ورودی `sing_box_ref` را از `testing` به `stable` یا تگ `v1.14.4` تغییر بده |
| `App not installed` هنگام آپدیت | امضا عوض شده؛ اپ قبلی را حذف کن یا از همان کلید استفاده کن |
| ساختار R8/`Missing class` | `app/proguard-rules.pro` را ببین؛ نسخهٔ هسته را با اپ هم‌تراز کن |

## ساختار پروژه

```
.github/workflows/build-apk.yml   ← ساخت ابری APK (کلیک و تمام)
app/                              ← سورس اپ اندروید (Kotlin/Compose)
  src/main/res/values-fa/          ← ترجمهٔ فارسی
  src/main/res/mipmap-*/           ← آیکون‌ها
tools/render-icons.py             ← بازتولید آیکون‌ها
version.properties                ← شمارهٔ نسخه
LICENSE                           ← GPL-3.0
```

## اعتبار و مجوز

این پروژه بر پایهٔ [SagerNet/sing-box-for-android](https://github.com/SagerNet/sing-box-for-android)
(GPL-3.0، © nekohasekai) و هستهٔ [sing-box](https://github.com/SagerNet/sing-box) ساخته شده است.
طبق مجوز GPLv3 سورس در اختیار توست. این نسخه **مخزن رسمی نیست** و هیچ وابستگی
یا تأییدی از سوی نویسندگان اصلی ندارد؛ نام «VPN Master» هم عمداً با آن‌ها متفاوت است.
استفاده از این نرم‌افزار باید مطابق قوانین محل زندگی‌ات باشد.
