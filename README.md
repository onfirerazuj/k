#### First Time Setup ####

pkg update -y && pkg upgrade -y

pkg install -y git python python-pip nano

pip install requests SignerPy phonenumbers rich flask

termux-setup-storage

cd /storage/emulated/0/

pkg install git

git clone https://github.com/DevKhaledHossam/t.git

cd t
cp t $HOME/
cd $HOME
chmod +x t

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


#################################
#### التشغيل بعدين ####
#################################

cd $HOME
rm -f n.txt
nano n.txt
./t


#################################
#### تحديث الأداة ####
#################################

cd $HOME

# حذف الملف القديم
rm -f t

# حذف المجلد القديم
rm -rf /storage/emulated/0/t

# تحميل آخر إصدار
cd /storage/emulated/0/
git clone https://github.com/DevKhaledHossam/t.git

# نقل الملف الجديد
cd t
cp t $HOME/

# إعطاء صلاحية تشغيل
cd $HOME
chmod +x t

# تشغيل
./t
