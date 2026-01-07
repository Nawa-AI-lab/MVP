# الخطوة 1: ابدأ من صورة Ollama الرسمية
FROM ollama/ollama

# الخطوة 2: قم بتثبيت Python ومكتبة Ollama
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install ollama

# الخطوة 3: انسخ ملف تطبيق الوكيل الخاص بنا إلى داخل الحاوية
# هذه المرة، الملف موجود بالتأكيد
COPY app.py /app.py

# الخطوة 4: قم بتحميل النموذج الصغير أثناء عملية البناء
RUN ollama pull tinylama

# الخطوة 5: الأمر النهائي الذي سيتم تشغيله
CMD ["/bin/sh", "-c", "ollama serve & python3 /app.py"]
