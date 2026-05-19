#### First Time Setup ####

pkg update -y && pkg upgrade -y

pkg install -y git python python-pip nano

pip install requests SignerPy phonenumbers rich flask

termux-setup-storage

cd /storage/emulated/0/

# تحميل المشروع
pkg install git

git clone https://github.com/DevKhaledHossam/t.git

# الدخول للمجلد
cd t

# نسخ الملف التنفيذي للهوم
cp t $HOME/

# الرجوع للهوم
cd $HOME

# إعطاء صلاحية تشغيل
chmod +x t

# إنشاء ملف الأرقام
nano n.txt

# الصق الأرقام بهذا الشكل:
# +201234567890
# +201111111111

# للحفظ:
# CTRL + X
# ثم Y
# ثم ENTER

# تشغيل الأداة
./t
