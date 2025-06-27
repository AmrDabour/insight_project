from app.config import get_settings
import google.generativeai as genai
from PIL import Image

settings = get_settings()
genai.configure(api_key=settings.google_ai_api_key)


class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def analyze_currency_image(self, image: Image.Image):
        """
        تحليل صورة العملة باستخدام Gemini API
        """
        try:
            # النص التوجيهي المختصر
            prompt = """
            حلل العملات واطلع النتيجة بلهجة خليجية سعودية:
            
            - لو عملة واحدة أو ورقة واحدة: عندك [القيمة]
            - لو أكثر من واحدة: عندك [المبلغ الإجمالي]، وفيه [تفاصيل الأوراق]
            
            أمثلة:
            - عندك 50 ريال
            - عندك 120 ريال، ورقة 50 ريال و 3 ورقات 20 ريال
            
            استخدم اللهجة الخليجية السعودية فقط.
            اجعل الرد خالي من اي ترحيب
            """

            response = self.model.generate_content([prompt, image])
            return response.text

        except Exception as e:
            return f"خطأ: {str(e)}"
